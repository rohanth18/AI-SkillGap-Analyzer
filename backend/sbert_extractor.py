"""
Advanced Skill Extraction with SBERT (Sentence-BERT)
Uses semantic similarity for highly accurate skill matching
"""

import spacy
from sentence_transformers import SentenceTransformer, util
import pickle
import os
from fuzzywuzzy import fuzz
import re
import csv

# Load spaCy model
try:
    nlp = spacy.load('en_core_web_sm')
except:
    print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")
    nlp = None

# Load SBERT model (lightweight and fast)
SBERT_MODEL = None
SKILL_EMBEDDINGS = None
KNOWN_SKILLS = []

def load_sbert_model():
    """Load SBERT model for semantic similarity"""
    global SBERT_MODEL
    if SBERT_MODEL is None:
        print("Loading SBERT model...")
        SBERT_MODEL = SentenceTransformer('all-MiniLM-L6-v2')  # Fast, 80MB model
    return SBERT_MODEL

def load_or_create_skill_embeddings(skills_list):
    """Load precomputed embeddings or create new ones"""
    global SKILL_EMBEDDINGS, KNOWN_SKILLS
    
    embeddings_path = 'models/skill_embeddings.pkl'
    
    # Try to load existing embeddings
    if os.path.exists(embeddings_path):
        try:
            with open(embeddings_path, 'rb') as f:
                data = pickle.load(f)
                SKILL_EMBEDDINGS = data['embeddings']
                KNOWN_SKILLS = data['skills']
                print(f"Loaded {len(KNOWN_SKILLS)} skill embeddings from cache")
                return SKILL_EMBEDDINGS, KNOWN_SKILLS
        except Exception as e:
            print(f"Error loading embeddings: {e}")
    
    # Create new embeddings
    print("Creating skill embeddings...")
    model = load_sbert_model()
    KNOWN_SKILLS = skills_list
    SKILL_EMBEDDINGS = model.encode(KNOWN_SKILLS, convert_to_tensor=True)
    
    # Save for future use
    os.makedirs('models', exist_ok=True)
    with open(embeddings_path, 'wb') as f:
        pickle.dump({
            'embeddings': SKILL_EMBEDDINGS,
            'skills': KNOWN_SKILLS
        }, f)
    
    print(f"Created and saved {len(KNOWN_SKILLS)} skill embeddings")
    return SKILL_EMBEDDINGS, KNOWN_SKILLS

def extract_skills_semantic(text, threshold=0.65):
    """
    Extract skills using SBERT semantic similarity
    
    Args:
        text: Resume text
        threshold: Similarity threshold (0.65 = 65% similar)
    
    Returns:
        dict: {skill: {'score': float, 'method': 'semantic'}}
    """
    if not text:
        return {}
    
    model = load_sbert_model()
    
    # Get all known skills
    from nlp_utils import load_known_skills
    all_skills = load_known_skills()
    
    # Load or create embeddings
    skill_embeddings, known_skills = load_or_create_skill_embeddings(all_skills)
    
    # Split text into sentences for better matching
    sentences = re.split(r'[.!?\n]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    # Encode resume sentences
    if not sentences:
        return {}
    
    sentence_embeddings = model.encode(sentences, convert_to_tensor=True)
    
    # Find semantic matches
    matched_skills = {}
    
    for i, skill in enumerate(known_skills):
        skill_embedding = skill_embeddings[i].unsqueeze(0)
        
        # Compute cosine similarity with all sentences
        similarities = util.cos_sim(skill_embedding, sentence_embeddings)
        max_similarity = similarities.max().item()
        
        if max_similarity >= threshold:
            matched_skills[skill] = {
                'score': round(max_similarity, 3),
                'method': 'semantic',
                'confidence': max_similarity
            }
    
    return matched_skills

def extract_skills_spacy_advanced(text):
    """
    Advanced spaCy-based extraction with PhraseMatcher
    
    Returns:
        dict: {skill: {'method': 'spacy', 'confidence': 1.0}}
    """
    if not nlp or not text:
        return {}
    
    from spacy.matcher import PhraseMatcher
    from nlp_utils import load_known_skills
    
    all_skills = load_known_skills()
    
    # Create PhraseMatcher
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill.lower()) for skill in all_skills]
    matcher.add("SKILLS", patterns)
    
    # Process text
    doc = nlp(text.lower())
    matches = matcher(doc)
    
    matched_skills = {}
    for match_id, start, end in matches:
        skill = doc[start:end].text
        # Find original case skill
        for original_skill in all_skills:
            if original_skill.lower() == skill:
                matched_skills[original_skill] = {
                    'method': 'spacy',
                    'confidence': 1.0
                }
                break
    
    return matched_skills

def extract_skills_fuzzy_advanced(text, threshold=75):
    """
    Advanced fuzzy matching with better normalization
    
    Returns:
        dict: {skill: {'method': 'fuzzy', 'confidence': score/100}}
    """
    if not text:
        return {}
    
    from nlp_utils import load_known_skills, normalize_skill
    
    all_skills = load_known_skills()
    text_normalized = normalize_skill(text)
    
    # Extract potential skill phrases (1-3 words)
    words = text_normalized.split()
    candidates = []
    
    for i in range(len(words)):
        for j in range(i+1, min(i+4, len(words)+1)):
            candidates.append(' '.join(words[i:j]))
    
    matched_skills = {}
    
    for skill in all_skills:
        skill_normalized = normalize_skill(skill)
        
        # Check against all candidates
        for candidate in candidates:
            score = fuzz.ratio(skill_normalized, candidate)
            
            if score >= threshold:
                if skill not in matched_skills or score > matched_skills[skill]['confidence'] * 100:
                    matched_skills[skill] = {
                        'method': 'fuzzy',
                        'confidence': score / 100,
                        'matched_text': candidate
                    }
    
    return matched_skills

def extract_skills_combined_advanced(resume_text, github_skills=None, manual_skills=None, 
                                    semantic_threshold=0.65, fuzzy_threshold=75):
    """
    ADVANCED: Combine all extraction methods with detailed evidence
    
    Returns:
        dict: {
            'extracted_skills': {
                'skill_name': {
                    'sources': ['semantic:0.78', 'github', 'manual'],
                    'confidence': 0.95,
                    'methods': ['semantic', 'github', 'manual']
                }
            },
            'total_skills': int,
            'by_method': {'semantic': 10, 'spacy': 5, ...}
        }
    """
    all_skills = {}
    method_counts = {
        'semantic': 0,
        'spacy': 0,
        'fuzzy': 0,
        'github': 0,
        'manual': 0
    }
    
    # 1. Semantic extraction (SBERT)
    print("Extracting skills with SBERT semantic matching...")
    semantic_skills = extract_skills_semantic(resume_text, threshold=semantic_threshold)
    for skill, data in semantic_skills.items():
        if skill not in all_skills:
            all_skills[skill] = {
                'sources': [],
                'confidence': 0,
                'methods': []
            }
        all_skills[skill]['sources'].append(f"semantic:{data['score']:.2f}")
        all_skills[skill]['methods'].append('semantic')
        all_skills[skill]['confidence'] = max(all_skills[skill]['confidence'], data['confidence'] * 0.9)
        method_counts['semantic'] += 1
    
    # 2. spaCy PhraseMatcher
    print("Extracting skills with spaCy PhraseMatcher...")
    spacy_skills = extract_skills_spacy_advanced(resume_text)
    for skill, data in spacy_skills.items():
        if skill not in all_skills:
            all_skills[skill] = {
                'sources': [],
                'confidence': 0,
                'methods': []
            }
        all_skills[skill]['sources'].append('spacy:exact')
        all_skills[skill]['methods'].append('spacy')
        all_skills[skill]['confidence'] = max(all_skills[skill]['confidence'], 1.0)
        method_counts['spacy'] += 1
    
    # 3. Fuzzy matching
    print("Extracting skills with fuzzy matching...")
    fuzzy_skills = extract_skills_fuzzy_advanced(resume_text, threshold=fuzzy_threshold)
    for skill, data in fuzzy_skills.items():
        if skill not in all_skills:
            all_skills[skill] = {
                'sources': [],
                'confidence': 0,
                'methods': []
            }
        all_skills[skill]['sources'].append(f"fuzzy:{data['confidence']:.2f}")
        all_skills[skill]['methods'].append('fuzzy')
        all_skills[skill]['confidence'] = max(all_skills[skill]['confidence'], data['confidence'] * 0.75)
        method_counts['fuzzy'] += 1
    
    # 4. GitHub skills
    if github_skills:
        for skill in github_skills:
            if skill not in all_skills:
                all_skills[skill] = {
                    'sources': [],
                    'confidence': 0,
                    'methods': []
                }
            all_skills[skill]['sources'].append('github')
            all_skills[skill]['methods'].append('github')
            all_skills[skill]['confidence'] = max(all_skills[skill]['confidence'], 0.9)
            method_counts['github'] += 1
    
    # 5. Manual skills
    if manual_skills:
        for skill in manual_skills:
            if skill not in all_skills:
                all_skills[skill] = {
                    'sources': [],
                    'confidence': 0,
                    'methods': []
                }
            all_skills[skill]['sources'].append('manual')
            all_skills[skill]['methods'].append('manual')
            all_skills[skill]['confidence'] = max(all_skills[skill]['confidence'], 0.95)
            method_counts['manual'] += 1
    
    return {
        'extracted_skills': all_skills,
        'total_skills': len(all_skills),
        'by_method': method_counts
    }

def calculate_confidence_score_advanced(extracted_skills, required_skills):
    """
    ADVANCED: Calculate confidence score with weighted sources
    
    Weights:
    - spaCy exact match: 1.0
    - SBERT semantic: 0.9
    - Manual: 0.95
    - GitHub: 0.9
    - Fuzzy: 0.75
    
    Returns:
        dict: {
            'confidence_score': float (0-100),
            'matched_skills': list,
            'missing_skills': list,
            'per_skill_breakdown': dict
        }
    """
    if not required_skills:
        return {
            'confidence_score': 0,
            'matched_skills': [],
            'missing_skills': [],
            'per_skill_breakdown': {}
        }
    
    matched = []
    missing = []
    per_skill = {}
    total_weight = 0
    achieved_weight = 0
    
    for req_skill in required_skills:
        req_skill_lower = req_skill.lower()
        found = False
        best_confidence = 0
        
        # Check if skill is in extracted skills (case-insensitive)
        for ext_skill, data in extracted_skills.items():
            if ext_skill.lower() == req_skill_lower:
                found = True
                best_confidence = data['confidence']
                matched.append({
                    'skill': req_skill,
                    'confidence': best_confidence,
                    'sources': data['sources'],
                    'methods': data['methods']
                })
                
                per_skill[req_skill] = {
                    'status': 'matched',
                    'confidence': best_confidence,
                    'sources': data['sources']
                }
                
                achieved_weight += best_confidence
                break
        
        if not found:
            missing.append(req_skill)
            per_skill[req_skill] = {
                'status': 'missing',
                'confidence': 0,
                'sources': []
            }
        
        total_weight += 1.0
    
    # Calculate final score
    confidence_score = (achieved_weight / total_weight * 100) if total_weight > 0 else 0
    
    return {
        'confidence_score': round(confidence_score, 2),
        'matched_skills': matched,
        'missing_skills': missing,
        'per_skill_breakdown': per_skill,
        'match_rate': f"{len(matched)}/{len(required_skills)}"
    }

if __name__ == "__main__":
    # Test the advanced extraction
    test_text = """
    I am a skilled Python developer with experience in machine learning and deep learning.
    I have worked with TensorFlow, PyTorch, and scikit-learn for building ML models.
    My expertise includes natural language processing, computer vision, and data analysis.
    I am proficient in Docker and Kubernetes for containerization and orchestration.
    """
    
    print("Testing Advanced Skill Extraction...")
    print("=" * 60)
    
    result = extract_skills_combined_advanced(
        resume_text=test_text,
        manual_skills=['AWS', 'React'],
        semantic_threshold=0.65
    )
    
    print(f"\nTotal skills extracted: {result['total_skills']}")
    print(f"By method: {result['by_method']}")
    print("\nExtracted skills:")
    for skill, data in list(result['extracted_skills'].items())[:10]:
        print(f"  {skill}: {data['sources']} (confidence: {data['confidence']:.2f})")
