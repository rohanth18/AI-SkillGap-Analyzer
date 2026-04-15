"""
Resume Quality Scorer & Red Flags Detector
Comprehensive resume analysis with grammar, readability, and structure checks
"""

import re
import textstat
from collections import Counter

# Action verbs list (strong resume verbs)
STRONG_ACTION_VERBS = {
    'achieved', 'accomplished', 'administered', 'analyzed', 'architected',
    'automated', 'built', 'collaborated', 'completed', 'configured',
    'created', 'delivered', 'demonstrated', 'designed', 'developed',
    'directed', 'engineered', 'enhanced', 'established', 'executed',
    'generated', 'implemented', 'improved', 'increased', 'initiated',
    'launched', 'led', 'managed', 'optimized', 'orchestrated',
    'organized', 'performed', 'pioneered', 'planned', 'produced',
    'programmed', 'reduced', 'redesigned', 'resolved', 'spearheaded',
    'streamlined', 'supervised', 'transformed', 'upgraded'
}

WEAK_VERBS = {
    'worked', 'did', 'made', 'helped', 'tried', 'used',
    'was', 'were', 'am', 'is', 'are', 'been', 'being',
    'responsible for', 'duties included', 'handled'
}

TECHNICAL_KEYWORDS = {
    'python', 'java', 'javascript', 'react', 'angular', 'vue',
    'node.js', 'django', 'flask', 'spring', 'docker', 'kubernetes',
    'aws', 'azure', 'gcp', 'sql', 'mongodb', 'postgresql',
    'machine learning', 'deep learning', 'tensorflow', 'pytorch',
    'git', 'ci/cd', 'agile', 'scrum', 'api', 'rest', 'graphql'
}

def detect_action_verbs(text):
    """
    Detect strong action verbs in resume
    
    Returns:
        dict: {
            'count': int,
            'verbs': list,
            'score': float (0-100)
        }
    """
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    found_verbs = []
    for verb in STRONG_ACTION_VERBS:
        if verb in words:
            found_verbs.append(verb)
    
    # Score based on density
    total_sentences = len(re.split(r'[.!?]+', text))
    verb_density = len(found_verbs) / max(total_sentences, 1)
    
    # Ideal: 1-2 action verbs per sentence
    score = min(verb_density * 50, 100)
    
    return {
        'count': len(found_verbs),
        'verbs': found_verbs[:10],  # Top 10
        'score': round(score, 1)
    }

def detect_weak_verbs(text):
    """Detect weak/passive verbs"""
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    found_weak = []
    for verb in WEAK_VERBS:
        if verb in text_lower:
            found_weak.append(verb)
    
    return {
        'count': len(found_weak),
        'verbs': found_weak,
        'penalty': min(len(found_weak) * 2, 20)  # Max 20 point penalty
    }

def calculate_readability_score(text):
    """
    Calculate readability using multiple metrics
    
    Returns:
        dict: {
            'flesch_reading_ease': float,
            'flesch_kincaid_grade': float,
            'score': float (0-100)
        }
    """
    try:
        flesch = textstat.flesch_reading_ease(text)
        grade = textstat.flesch_kincaid_grade(text)
        
        # Ideal Flesch score: 60-70 (standard)
        # Penalize too easy (<50) or too hard (>80)
        if 60 <= flesch <= 70:
            score = 100
        elif 50 <= flesch < 60 or 70 < flesch <= 80:
            score = 85
        else:
            score = 70
        
        return {
            'flesch_reading_ease': round(flesch, 1),
            'flesch_kincaid_grade': round(grade, 1),
            'score': score
        }
    except:
        return {
            'flesch_reading_ease': 0,
            'flesch_kincaid_grade': 0,
            'score': 50
        }

def detect_quantifiable_achievements(text):
    """
    Detect numbers, percentages, and measurable achievements
    
    Returns:
        dict: {
            'count': int,
            'examples': list,
            'score': float
        }
    """
    # Patterns for quantifiable achievements
    patterns = [
        r'\d+%',  # Percentages
        r'\$\d+[KMB]?',  # Money
        r'\d+\+',  # Numbers with +
        r'\d+x',  # Multipliers
        r'\d{1,3}(?:,\d{3})*',  # Large numbers
    ]
    
    achievements = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        achievements.extend(matches)
    
    # Score based on count (ideal: 3-5 per page)
    count = len(achievements)
    if count >= 5:
        score = 100
    elif count >= 3:
        score = 85
    elif count >= 1:
        score = 70
    else:
        score = 40
    
    return {
        'count': count,
        'examples': achievements[:5],
        'score': score
    }

def detect_technical_keywords(text):
    """Detect technical keywords coverage"""
    text_lower = text.lower()
    
    found_keywords = []
    for keyword in TECHNICAL_KEYWORDS:
        if keyword in text_lower:
            found_keywords.append(keyword)
    
    # Score based on coverage
    coverage = len(found_keywords) / len(TECHNICAL_KEYWORDS) * 100
    score = min(coverage * 2, 100)  # Double the coverage for score
    
    return {
        'count': len(found_keywords),
        'keywords': found_keywords,
        'coverage': round(coverage, 1),
        'score': round(score, 1)
    }

def calculate_length_penalty(text):
    """
    Calculate penalty for resume length
    Ideal: 400-800 words
    """
    word_count = len(text.split())
    
    if 400 <= word_count <= 800:
        penalty = 0
        score = 100
    elif 300 <= word_count < 400 or 800 < word_count <= 1000:
        penalty = 10
        score = 90
    elif 200 <= word_count < 300 or 1000 < word_count <= 1200:
        penalty = 20
        score = 80
    else:
        penalty = 30
        score = 70
    
    return {
        'word_count': word_count,
        'penalty': penalty,
        'score': score,
        'status': 'optimal' if penalty == 0 else 'suboptimal'
    }

def detect_contact_info(text):
    """Detect if resume has contact information"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    
    has_email = bool(re.search(email_pattern, text))
    has_phone = bool(re.search(phone_pattern, text))
    
    return {
        'has_email': has_email,
        'has_phone': has_phone,
        'score': 100 if (has_email and has_phone) else 50 if (has_email or has_phone) else 0
    }

def detect_red_flags(text):
    """
    Detect resume red flags
    
    Returns:
        list: [
            {'flag': str, 'severity': str, 'description': str}
        ]
    """
    flags = []
    text_lower = text.lower()
    word_count = len(text.split())
    
    # 1. Missing contact info
    contact = detect_contact_info(text)
    if not contact['has_email']:
        flags.append({
            'flag': 'missing_email',
            'severity': 'high',
            'description': 'No email address found'
        })
    if not contact['has_phone']:
        flags.append({
            'flag': 'missing_phone',
            'severity': 'medium',
            'description': 'No phone number found'
        })
    
    # 2. Too short or too long
    if word_count < 200:
        flags.append({
            'flag': 'too_short',
            'severity': 'high',
            'description': f'Resume is too short ({word_count} words). Aim for 400-800 words.'
        })
    elif word_count > 1200:
        flags.append({
            'flag': 'too_long',
            'severity': 'medium',
            'description': f'Resume is too long ({word_count} words). Consider condensing.'
        })
    
    # 3. No projects section
    if 'project' not in text_lower:
        flags.append({
            'flag': 'no_projects',
            'severity': 'medium',
            'description': 'No projects section found. Consider adding relevant projects.'
        })
    
    # 4. No certifications
    cert_keywords = ['certification', 'certified', 'certificate']
    if not any(kw in text_lower for kw in cert_keywords):
        flags.append({
            'flag': 'no_certifications',
            'severity': 'low',
            'description': 'No certifications mentioned. Add relevant certifications if available.'
        })
    
    # 5. Weak verbs detected
    weak = detect_weak_verbs(text)
    if weak['count'] > 5:
        flags.append({
            'flag': 'excessive_weak_verbs',
            'severity': 'medium',
            'description': f'Found {weak["count"]} weak verbs. Use stronger action verbs.'
        })
    
    # 6. No quantifiable achievements
    achievements = detect_quantifiable_achievements(text)
    if achievements['count'] == 0:
        flags.append({
            'flag': 'no_measurable_achievements',
            'severity': 'high',
            'description': 'No quantifiable achievements found. Add metrics and numbers.'
        })
    
    # 7. Not ATS-friendly (check for tables, images references)
    if 'table' in text_lower or 'image' in text_lower:
        flags.append({
            'flag': 'not_ats_friendly',
            'severity': 'medium',
            'description': 'Resume may contain tables or images. Use plain text for ATS compatibility.'
        })
    
    # 8. Typos and grammar (basic check)
    # Count repeated words
    words = text_lower.split()
    word_freq = Counter(words)
    repeated = [word for word, count in word_freq.items() if count > 10 and len(word) > 3]
    if len(repeated) > 3:
        flags.append({
            'flag': 'possible_typos',
            'severity': 'low',
            'description': 'Possible repetitive words detected. Review for typos.'
        })
    
    return flags

def calculate_resume_quality_score(text):
    """
    MAIN FUNCTION: Calculate comprehensive resume quality score
    
    Returns:
        dict: {
            'resume_quality_score': float (0-100),
            'breakdown': {
                'grammar': float,
                'readability': float,
                'action_verbs': float,
                'technical_coverage': float,
                'quantifiable_achievements': int,
                'length_penalty': float,
                'contact_info': float
            },
            'red_flags': list,
            'recommendations': list
        }
    """
    if not text or len(text.strip()) < 50:
        return {
            'resume_quality_score': 0,
            'breakdown': {},
            'red_flags': [{'flag': 'empty_resume', 'severity': 'critical', 'description': 'Resume is empty or too short'}],
            'recommendations': ['Please upload a complete resume']
        }
    
    # Calculate all components
    action_verbs = detect_action_verbs(text)
    weak_verbs = detect_weak_verbs(text)
    readability = calculate_readability_score(text)
    achievements = detect_quantifiable_achievements(text)
    technical = detect_technical_keywords(text)
    length = calculate_length_penalty(text)
    contact = detect_contact_info(text)
    red_flags = detect_red_flags(text)
    
    # Calculate weighted score
    weights = {
        'action_verbs': 0.20,
        'readability': 0.15,
        'technical': 0.20,
        'achievements': 0.20,
        'length': 0.10,
        'contact': 0.10,
        'weak_verbs_penalty': 0.05
    }
    
    score = (
        action_verbs['score'] * weights['action_verbs'] +
        readability['score'] * weights['readability'] +
        technical['score'] * weights['technical'] +
        achievements['score'] * weights['achievements'] +
        length['score'] * weights['length'] +
        contact['score'] * weights['contact'] -
        weak_verbs['penalty'] * weights['weak_verbs_penalty']
    )
    
    # Generate recommendations
    recommendations = []
    if action_verbs['count'] < 5:
        recommendations.append('Add more strong action verbs (achieved, implemented, optimized)')
    if achievements['count'] < 3:
        recommendations.append('Include quantifiable achievements with numbers and percentages')
    if technical['count'] < 5:
        recommendations.append('Add more technical keywords relevant to your field')
    if weak_verbs['count'] > 3:
        recommendations.append('Replace weak verbs with stronger alternatives')
    if not contact['has_email']:
        recommendations.append('Add your email address')
    
    return {
        'resume_quality_score': round(max(0, min(100, score)), 2),
        'breakdown': {
            'action_verbs': action_verbs['score'],
            'readability': readability['score'],
            'technical_coverage': technical['score'],
            'quantifiable_achievements': achievements['count'],
            'achievements_score': achievements['score'],
            'length_score': length['score'],
            'contact_info': contact['score'],
            'weak_verbs_penalty': weak_verbs['penalty']
        },
        'details': {
            'action_verbs_found': action_verbs['verbs'],
            'weak_verbs_found': weak_verbs['verbs'],
            'technical_keywords': technical['keywords'],
            'achievements_examples': achievements['examples'],
            'word_count': length['word_count'],
            'readability_metrics': readability
        },
        'red_flags': red_flags,
        'recommendations': recommendations,
        'severity_counts': {
            'high': len([f for f in red_flags if f['severity'] == 'high']),
            'medium': len([f for f in red_flags if f['severity'] == 'medium']),
            'low': len([f for f in red_flags if f['severity'] == 'low'])
        }
    }

if __name__ == "__main__":
    # Test the resume quality scorer
    test_resume = """
    John Doe
    Email: john.doe@email.com | Phone: (555) 123-4567
    
    PROFESSIONAL SUMMARY
    Experienced software engineer with 5+ years developing scalable web applications.
    
    EXPERIENCE
    Senior Developer at Tech Corp (2020-Present)
    - Developed and deployed 10+ microservices using Python and Docker
    - Improved system performance by 40% through code optimization
    - Led a team of 5 developers in agile environment
    - Implemented CI/CD pipeline reducing deployment time by 60%
    
    PROJECTS
    E-commerce Platform
    - Built full-stack application using React and Node.js
    - Achieved 99.9% uptime serving 50,000+ users
    
    SKILLS
    Python, JavaScript, React, Docker, Kubernetes, AWS, SQL
    
    CERTIFICATIONS
    AWS Certified Solutions Architect
    """
    
    print("Testing Resume Quality Scorer...")
    print("=" * 60)
    
    result = calculate_resume_quality_score(test_resume)
    
    print(f"\nResume Quality Score: {result['resume_quality_score']}/100")
    print(f"\nBreakdown:")
    for key, value in result['breakdown'].items():
        print(f"  {key}: {value}")
    
    print(f"\nRed Flags ({len(result['red_flags'])}):")
    for flag in result['red_flags']:
        print(f"  [{flag['severity'].upper()}] {flag['description']}")
    
    print(f"\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  - {rec}")
