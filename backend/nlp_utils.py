import spacy
from spacy.matcher import PhraseMatcher
from fuzzywuzzy import fuzz, process
import PyPDF2
import csv
import re
import os

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback or try to download
    print("Spacy model not found. Attempting download could fail if no internet/permissions.")
    # We might just fail here if strict, or try valid download
    try:
        from spacy.cli import download
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    except:
        print("CRITICAL: Failed to load spacy model.")
        nlp = spacy.blank("en") # minimal fallback

def extract_text_from_file(file_path):
    """Extracts text from PDF or TXT files."""
    text = ""
    if file_path.endswith('.pdf'):
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
    elif file_path.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading TXT: {e}")
            return ""
    return text

def normalize_skill(skill):
    """Normalizes skill text (lowercase, stripped)."""
    return skill.lower().strip()

def load_known_skills():
    """
    Loads all unique skills from the CSV to build a knowledge base.
    """
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'it_jobs_roles.csv')
    if not os.path.exists(csv_path):
        return []
    
    all_skills = set()
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'Skills' in row and row['Skills']:
                    skills_list = [s.strip() for s in row['Skills'].split(',')]
                    for s in skills_list:
                        all_skills.add(normalize_skill(s))
    except Exception as e:
        print(f"Error loading CSV: {e}")
        
    return list(all_skills)

KNOWN_SKILLS = load_known_skills()

def extract_skills_spacy(text, skills_list=None):
    """
    Extracts skills using spaCy PhraseMatcher.
    """
    if skills_list is None:
        skills_list = KNOWN_SKILLS

    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(text) for text in skills_list]
    matcher.add("SKILLS", patterns)

    doc = nlp(text)
    matches = matcher(doc)
    
    extracted = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        extracted.add(normalize_skill(span.text))
    
    return list(extracted)

def extract_skills_combined(text, github_skills_list=None, manual_skills_list=None):
    """
    Combines different extraction methods.
    Returns: { 'skill': score, ... } or just a list of unique skills
    """
    spacy_skills = extract_skills_spacy(text)
    
    all_found = set(spacy_skills)
    
    # Check manual
    manual = set()
    if manual_skills_list:
        for ms in manual_skills_list:
            best_match = process.extractOne(ms, KNOWN_SKILLS, scorer=fuzz.ratio)
            if best_match and best_match[1] > 85:
                manual.add(best_match[0])
            else:
                manual.add(normalize_skill(ms))
    
    # GitHub
    gh_skills = set()
    if github_skills_list:
        for gh in github_skills_list:
             gh_skills.add(normalize_skill(gh))
             
    unique_skills = all_found.union(manual).union(gh_skills)
    
    results = {}
    for skill in unique_skills:
        sources = []
        if skill in spacy_skills:
            sources.append('spacy')
        if skill in manual:
            sources.append('manual')
        if skill in gh_skills:
            sources.append('github')
        
        results[skill] = sources
        
    return results

def calculate_confidence_score(extracted_skills_dict, role_required_skills):
    """
    extracted_skills_dict: { 'skill_name': ['spacy', 'manual', ...], ... }
    role_required_skills: list of strings
    
    Weights from user prompt:
    SpaCy exact match: 1.0
    Manual entered: 0.95
    GitHub import: 0.9
    Synonym match: 0.85
    Fuzzy detected: 0.75
    """
    req = [normalize_skill(s) for s in role_required_skills]
    if not req:
        return 0, {}, [], [] 
        
    max_score = len(req) * 1.0
    current_score = 0
    
    missing_skills = []
    present_skills = []
    skill_details = {}
    
    for r_skill in req:
        match_found = None
        match_type = 'exact' # or fuzzy
        
        if r_skill in extracted_skills_dict:
            match_found = r_skill
        else:
            choices = list(extracted_skills_dict.keys())
            if choices:
                best = process.extractOne(r_skill, choices, scorer=fuzz.token_sort_ratio)
                if best and best[1] > 80:
                    match_found = best[0]
                    match_type = 'fuzzy'
            
        if match_found:
            sources = extracted_skills_dict[match_found]
            weight = 0
            
            # Prioritize highest weight source
            if 'spacy' in sources:
                weight = 1.0
            elif 'manual' in sources:
                weight = 0.95
            elif 'github' in sources:
                weight = 0.9
            else:
                weight = 0.85 # Default/synonym
                
            # If fuzzy, apply fuzzy weight 0.75 OR the source penalty?
            # Prompt says "Fuzzy match 0.75". This implies if we matched via fuzzy,
            # regardless of source (though usually fuzzy implies 'extracted via fuzzy logic'), 
            # but here we matched the *names* via fuzzy.
            if match_type == 'fuzzy':
                weight = 0.75
            
            current_score += weight
            present_skills.append(r_skill)
            skill_details[r_skill] = {
                'match': match_found,
                'sources': sources,
                'weight': weight
            }
        else:
            missing_skills.append(r_skill)
            
    final_score = (current_score / max_score) * 100 if max_score > 0 else 0
    return round(final_score, 2), skill_details, missing_skills, present_skills

def calculate_ats_score(text, skills_found_count):
    """
    Calculates an approximate ATS friendliness score based on content.
    """
    score = 0
    text_lower = text.lower()
    
    # 1. Text Extraction Success (20 pts)
    # If we extracted text, it means it's readable.
    if len(text) > 500:
        score += 20
    elif len(text) > 100:
        score += 10
        
    # 2. Contact Info Presence (35 pts)
    # Email (20)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    if re.search(email_pattern, text):
        score += 20
    # Phone (15)
    phone_pattern = r'(\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}'
    if re.search(phone_pattern, text):
        score += 15
        
    # 3. Keyword/Skills Density (25 pts)
    if skills_found_count >= 15:
        score += 25
    elif skills_found_count >= 8:
        score += 15
    elif skills_found_count > 0:
        score += 10
        
    # 4. Structure/Headers (20 pts)
    headers = ['experience', 'education', 'skills', 'projects', 'summary', 'profile', 'certifications', 'languages']
    header_count = 0
    for h in headers:
        if h in text_lower:
            header_count += 1
    
    if header_count >= 4:
        score += 20
    elif header_count >= 2:
        score += 10
    elif header_count >= 1:
        score += 5
        
    return min(100, score)