"""
Smart Resume Rewriting Engine
Improves resume text with better action verbs, grammar, and professional structure
"""

import re
import random

# Action verbs categorized by function
ACTION_VERBS = {
    "leadership": ["Led", "Directed", "Managed", "Coordinated", "Supervised", "Orchestrated", "Spearheaded"],
    "achievement": ["Achieved", "Accomplished", "Attained", "Delivered", "Exceeded", "Surpassed"],
    "creation": ["Developed", "Created", "Designed", "Built", "Engineered", "Established", "Implemented"],
    "improvement": ["Enhanced", "Optimized", "Improved", "Streamlined", "Upgraded", "Modernized", "Transformed"],
    "analysis": ["Analyzed", "Evaluated", "Assessed", "Investigated", "Researched", "Examined"],
    "collaboration": ["Collaborated", "Partnered", "Coordinated", "Facilitated", "Liaised"],
    "communication": ["Presented", "Communicated", "Articulated", "Documented", "Reported"],
    "technical": ["Programmed", "Coded", "Automated", "Integrated", "Deployed", "Configured"]
}

# Weak to strong verb mappings
VERB_IMPROVEMENTS = {
    "worked on": ["Developed", "Implemented", "Built", "Created"],
    "helped": ["Assisted", "Supported", "Facilitated", "Contributed to"],
    "did": ["Executed", "Performed", "Completed", "Accomplished"],
    "made": ["Created", "Developed", "Designed", "Established"],
    "used": ["Utilized", "Leveraged", "Employed", "Applied"],
    "was responsible for": ["Managed", "Oversaw", "Directed", "Led"],
    "handled": ["Managed", "Coordinated", "Administered", "Processed"],
    "dealt with": ["Managed", "Resolved", "Addressed", "Handled"],
    "got": ["Achieved", "Obtained", "Secured", "Acquired"],
    "tried to": ["Attempted to", "Worked to", "Strived to"]
}

# Quantification suggestions
QUANTIFICATION_PATTERNS = [
    "by {percentage}%",
    "resulting in {number}+ {metric}",
    "across {number} {units}",
    "for {number}+ {stakeholders}",
    "within {timeframe}"
]

def improve_action_verbs(text):
    """Replace weak verbs with stronger action verbs"""
    improved_text = text
    
    for weak, strong_options in VERB_IMPROVEMENTS.items():
        if weak.lower() in improved_text.lower():
            # Use regex for case-insensitive replacement
            pattern = re.compile(re.escape(weak), re.IGNORECASE)
            strong_verb = random.choice(strong_options)
            improved_text = pattern.sub(strong_verb, improved_text, count=1)
    
    return improved_text

def add_quantification_suggestions(text):
    """Suggest adding quantifiable metrics"""
    # Check if text already has numbers/percentages
    has_numbers = bool(re.search(r'\d+', text))
    
    if not has_numbers:
        suggestions = [
            " (Consider adding: improved efficiency by X%)",
            " (Tip: quantify the impact with metrics)",
            " (Add: serving X+ users/clients)"
        ]
        return text + random.choice(suggestions)
    
    return text

def improve_structure(text):
    """Improve sentence structure and grammar"""
    # Ensure it starts with an action verb
    text = text.strip()
    
    # Capitalize first letter
    if text:
        text = text[0].upper() + text[1:]
    
    # Remove redundant words
    redundant_phrases = [
        ("very very", "very"),
        ("really really", "really"),
        ("and also", "and"),
        ("in order to", "to"),
        ("due to the fact that", "because")
    ]
    
    for redundant, replacement in redundant_phrases:
        text = text.replace(redundant, replacement)
    
    # Ensure proper ending
    if text and text[-1] not in '.!?':
        text += '.'
    
    return text

def add_professional_keywords(text, domain="general"):
    """Add relevant professional keywords"""
    keywords_by_domain = {
        "technical": ["scalable", "efficient", "robust", "modular", "maintainable"],
        "data": ["data-driven", "analytical", "insights", "metrics", "optimization"],
        "management": ["strategic", "cross-functional", "stakeholder", "deliverables"],
        "general": ["professional", "collaborative", "innovative", "results-oriented"]
    }
    
    keywords = keywords_by_domain.get(domain, keywords_by_domain["general"])
    
    # Add a keyword if text is short and doesn't have professional terms
    if len(text.split()) < 15:
        keyword = random.choice(keywords)
        # Insert keyword naturally
        if "project" in text.lower():
            text = text.replace("project", f"{keyword} project", 1)
        elif "system" in text.lower():
            text = text.replace("system", f"{keyword} system", 1)
    
    return text

def rewrite_resume_section(original_text, context="experience"):
    """
    Main function to rewrite resume text
    
    Args:
        original_text: Original resume text
        context: Context of the text (experience, summary, skills)
    
    Returns:
        dict: Original and rewritten text with improvements
    """
    if not original_text or len(original_text.strip()) < 10:
        return {
            "original": original_text,
            "rewritten": original_text,
            "improvements": ["Text too short to rewrite effectively"],
            "score_improvement": 0
        }
    
    improvements = []
    rewritten = original_text
    
    # Step 1: Improve action verbs
    before_verbs = rewritten
    rewritten = improve_action_verbs(rewritten)
    if rewritten != before_verbs:
        improvements.append("Replaced weak verbs with stronger action verbs")
    
    # Step 2: Improve structure
    before_structure = rewritten
    rewritten = improve_structure(rewritten)
    if rewritten != before_structure:
        improvements.append("Improved sentence structure and grammar")
    
    # Step 3: Add professional keywords
    if context in ["experience", "summary"]:
        before_keywords = rewritten
        domain = detect_domain(original_text)
        rewritten = add_professional_keywords(rewritten, domain)
        if rewritten != before_keywords:
            improvements.append(f"Added professional {domain} keywords")
    
    # Step 4: Suggest quantification
    if context == "experience":
        before_quant = rewritten
        rewritten = add_quantification_suggestions(rewritten)
        if rewritten != before_quant:
            improvements.append("Added quantification suggestions")
    
    # Calculate improvement score
    score_improvement = calculate_improvement_score(original_text, rewritten)
    
    return {
        "original": original_text,
        "rewritten": rewritten,
        "improvements": improvements if improvements else ["Text is already well-written"],
        "score_improvement": score_improvement
    }

def detect_domain(text):
    """Detect the domain/field from text"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["code", "develop", "program", "software", "api", "database"]):
        return "technical"
    elif any(word in text_lower for word in ["data", "analysis", "metric", "report", "insight"]):
        return "data"
    elif any(word in text_lower for word in ["manage", "lead", "team", "coordinate", "strategy"]):
        return "management"
    else:
        return "general"

def calculate_improvement_score(original, rewritten):
    """Calculate how much the text was improved (0-100)"""
    if original == rewritten:
        return 0
    
    # Factors that contribute to improvement
    score = 0
    
    # Length increase (more detailed)
    if len(rewritten) > len(original):
        score += 20
    
    # Has numbers/metrics
    if re.search(r'\d+', rewritten) and not re.search(r'\d+', original):
        score += 30
    
    # Professional keywords
    professional_words = ["developed", "implemented", "optimized", "enhanced", "achieved", "delivered"]
    original_count = sum(1 for word in professional_words if word in original.lower())
    rewritten_count = sum(1 for word in professional_words if word in rewritten.lower())
    if rewritten_count > original_count:
        score += 25
    
    # Better structure (starts with action verb)
    if rewritten.split()[0].lower() in [v.lower() for verbs in ACTION_VERBS.values() for v in verbs]:
        score += 25
    
    return min(score, 100)

# Example templates for different resume sections
RESUME_TEMPLATES = {
    "weak_experience": [
        "Worked on Python projects and managed data.",
        "Helped with website development.",
        "Was responsible for testing.",
        "Used SQL for database queries."
    ],
    "improved_experience": [
        "Designed and implemented automated Python workflows, improving data processing efficiency by 40% while ensuring code modularity and scalability.",
        "Developed responsive web applications using React and Node.js, serving 10,000+ active users with 99.9% uptime.",
        "Executed comprehensive testing strategies including unit, integration, and end-to-end tests, reducing production bugs by 60%.",
        "Optimized complex SQL queries and database schemas, reducing query execution time by 50% and improving application performance."
    ]
}

if __name__ == "__main__":
    # Test the rewriter
    print("Resume Rewriting Engine - Test Cases")
    print("=" * 70)
    
    test_cases = [
        "Worked on Python projects and managed data.",
        "Helped with website development and testing.",
        "Was responsible for database management.",
        "Used machine learning for predictions."
    ]
    
    for i, original in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Original: {original}")
        
        result = rewrite_resume_section(original, context="experience")
        
        print(f"Rewritten: {result['rewritten']}")
        print(f"Improvements: {', '.join(result['improvements'])}")
        print(f"Score Improvement: +{result['score_improvement']}%")
        print("-" * 70)
