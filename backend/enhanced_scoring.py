"""
Enhanced Confidence Scoring Algorithm
Advanced weighted scoring with per-skill breakdown and importance ranking
"""

def calculate_enhanced_confidence_score(extracted_skills_data, required_skills, skill_importance=None):
    """
    Calculate advanced confidence score with weighted sources
    
    Weights:
    - spaCy exact match: 1.0
    - SBERT semantic: 0.9
    - Manual skills: 0.95
    - GitHub skills: 0.9
    - Fuzzy match: 0.75
    - Synonym match: 0.85
    
    Args:
        extracted_skills_data: dict from sbert_extractor.extract_skills_combined_advanced()
        required_skills: list of required skills for the role
        skill_importance: dict {skill: importance_weight} (optional, default 1.0 for all)
    
    Returns:
        dict: {
            'confidence_score': float (0-100),
            'matched_skills': list of matched skills with details,
            'missing_skills': list of missing skills,
            'per_skill_breakdown': dict with detailed scoring,
            'match_rate': str (e.g., "8/12"),
            'weighted_score': float,
            'importance_adjusted_score': float
        }
    """
    if not required_skills:
        return {
            'confidence_score': 0,
            'matched_skills': [],
            'missing_skills': [],
            'per_skill_breakdown': {},
            'match_rate': '0/0',
            'weighted_score': 0,
            'importance_adjusted_score': 0
        }
    
    # Default importance weights (all equal)
    if skill_importance is None:
        skill_importance = {skill: 1.0 for skill in required_skills}
    
    # Method weights
    method_weights = {
        'spacy': 1.0,
        'semantic': 0.9,
        'manual': 0.95,
        'github': 0.9,
        'fuzzy': 0.75,
        'synonym': 0.85
    }
    
    extracted_skills = extracted_skills_data.get('extracted_skills', {})
    
    matched_skills = []
    missing_skills = []
    per_skill_breakdown = {}
    
    total_weight = 0
    achieved_weight = 0
    total_importance = 0
    achieved_importance = 0
    
    for req_skill in required_skills:
        req_skill_lower = req_skill.lower()
        importance = skill_importance.get(req_skill, 1.0)
        total_importance += importance
        
        found = False
        best_confidence = 0
        best_methods = []
        best_sources = []
        
        # Check if skill is in extracted skills (case-insensitive)
        for ext_skill, data in extracted_skills.items():
            if ext_skill.lower() == req_skill_lower:
                found = True
                
                # Calculate weighted confidence based on methods used
                methods = data.get('methods', [])
                confidences = []
                
                for method in methods:
                    weight = method_weights.get(method, 0.5)
                    confidences.append(weight)
                
                # Use maximum confidence from all methods
                best_confidence = max(confidences) if confidences else data.get('confidence', 0)
                best_methods = methods
                best_sources = data.get('sources', [])
                
                matched_skills.append({
                    'skill': req_skill,
                    'confidence': round(best_confidence, 3),
                    'sources': best_sources,
                    'methods': best_methods,
                    'importance': importance
                })
                
                per_skill_breakdown[req_skill] = {
                    'status': 'matched',
                    'confidence': round(best_confidence, 3),
                    'sources': best_sources,
                    'methods': best_methods,
                    'importance': importance,
                    'weighted_contribution': round(best_confidence * importance, 3)
                }
                
                achieved_weight += best_confidence
                achieved_importance += best_confidence * importance
                break
        
        if not found:
            missing_skills.append(req_skill)
            per_skill_breakdown[req_skill] = {
                'status': 'missing',
                'confidence': 0,
                'sources': [],
                'methods': [],
                'importance': importance,
                'weighted_contribution': 0
            }
        
        total_weight += 1.0
    
    # Calculate scores
    basic_score = (achieved_weight / total_weight * 100) if total_weight > 0 else 0
    importance_adjusted_score = (achieved_importance / total_importance * 100) if total_importance > 0 else 0
    
    # Final confidence score (average of basic and importance-adjusted)
    final_score = (basic_score + importance_adjusted_score) / 2
    
    # Rank missing skills by importance
    missing_skills_ranked = sorted(
        [{'skill': skill, 'importance': skill_importance.get(skill, 1.0)} 
         for skill in missing_skills],
        key=lambda x: x['importance'],
        reverse=True
    )
    
    return {
        'confidence_score': round(final_score, 2),
        'basic_score': round(basic_score, 2),
        'importance_adjusted_score': round(importance_adjusted_score, 2),
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'missing_skills_ranked': missing_skills_ranked,
        'per_skill_breakdown': per_skill_breakdown,
        'match_rate': f"{len(matched_skills)}/{len(required_skills)}",
        'match_percentage': round(len(matched_skills) / len(required_skills) * 100, 1),
        'total_required': len(required_skills),
        'total_matched': len(matched_skills),
        'total_missing': len(missing_skills),
        'average_match_confidence': round(sum(s['confidence'] for s in matched_skills) / len(matched_skills), 3) if matched_skills else 0
    }

def generate_skill_importance_weights(required_skills, role_type='general'):
    """
    Generate importance weights for skills based on role type
    
    Args:
        required_skills: list of skills
        role_type: str ('general', 'technical', 'leadership', 'data')
    
    Returns:
        dict: {skill: importance_weight}
    """
    # Core skills that are always important
    core_technical = ['python', 'java', 'javascript', 'sql', 'git']
    core_cloud = ['aws', 'azure', 'gcp', 'docker', 'kubernetes']
    core_data = ['machine learning', 'data analysis', 'pandas', 'numpy', 'tensorflow']
    core_leadership = ['team management', 'agile', 'scrum', 'project management']
    
    weights = {}
    
    for skill in required_skills:
        skill_lower = skill.lower()
        
        # Default weight
        weight = 1.0
        
        # Adjust based on role type
        if role_type == 'technical':
            if any(core in skill_lower for core in core_technical):
                weight = 1.5
            elif any(core in skill_lower for core in core_cloud):
                weight = 1.3
        
        elif role_type == 'data':
            if any(core in skill_lower for core in core_data):
                weight = 1.5
            elif 'python' in skill_lower or 'sql' in skill_lower:
                weight = 1.4
        
        elif role_type == 'leadership':
            if any(core in skill_lower for core in core_leadership):
                weight = 1.5
            elif any(core in skill_lower for core in core_technical):
                weight = 1.2
        
        weights[skill] = weight
    
    return weights

def get_skill_gap_insights(confidence_result):
    """
    Generate actionable insights from confidence scoring
    
    Returns:
        dict: {
            'overall_assessment': str,
            'strengths': list,
            'critical_gaps': list,
            'recommendations': list,
            'estimated_learning_time': str
        }
    """
    score = confidence_result['confidence_score']
    matched = confidence_result['matched_skills']
    missing = confidence_result['missing_skills_ranked']
    
    # Overall assessment
    if score >= 80:
        assessment = "Excellent match! You have most of the required skills."
    elif score >= 60:
        assessment = "Good match. A few skill gaps to address."
    elif score >= 40:
        assessment = "Moderate match. Significant skill development needed."
    else:
        assessment = "Limited match. Consider extensive upskilling or different role."
    
    # Identify strengths (high confidence matches)
    strengths = [
        s['skill'] for s in matched 
        if s['confidence'] >= 0.9
    ][:5]
    
    # Critical gaps (high importance missing skills)
    critical_gaps = [
        m['skill'] for m in missing 
        if m['importance'] >= 1.3
    ][:5]
    
    # Generate recommendations
    recommendations = []
    
    if len(missing) > 10:
        recommendations.append("Focus on the top 5 critical skills first")
    
    if critical_gaps:
        recommendations.append(f"Prioritize learning: {', '.join(critical_gaps[:3])}")
    
    if score < 60:
        recommendations.append("Consider taking online courses or bootcamps")
        recommendations.append("Build projects to demonstrate these skills")
    
    # Estimate learning time
    missing_count = len(missing)
    if missing_count == 0:
        learning_time = "No additional learning needed"
    elif missing_count <= 3:
        learning_time = "1-2 months of focused learning"
    elif missing_count <= 6:
        learning_time = "3-4 months of dedicated study"
    elif missing_count <= 10:
        learning_time = "6-8 months of comprehensive learning"
    else:
        learning_time = "12+ months of extensive skill development"
    
    return {
        'overall_assessment': assessment,
        'strengths': strengths,
        'critical_gaps': critical_gaps,
        'recommendations': recommendations,
        'estimated_learning_time': learning_time,
        'skill_coverage': f"{confidence_result['match_percentage']}%"
    }

if __name__ == "__main__":
    # Test the enhanced scoring
    test_extracted = {
        'extracted_skills': {
            'Python': {
                'sources': ['spacy:exact', 'semantic:0.95'],
                'confidence': 1.0,
                'methods': ['spacy', 'semantic']
            },
            'JavaScript': {
                'sources': ['fuzzy:0.82', 'github'],
                'confidence': 0.82,
                'methods': ['fuzzy', 'github']
            },
            'React': {
                'sources': ['manual'],
                'confidence': 0.95,
                'methods': ['manual']
            }
        }
    }
    
    test_required = ['Python', 'JavaScript', 'React', 'Node.js', 'Docker', 'AWS']
    
    print("Testing Enhanced Confidence Scoring...")
    print("=" * 60)
    
    # Generate importance weights
    importance = generate_skill_importance_weights(test_required, 'technical')
    
    result = calculate_enhanced_confidence_score(
        test_extracted,
        test_required,
        importance
    )
    
    print(f"\nConfidence Score: {result['confidence_score']}%")
    print(f"Match Rate: {result['match_rate']}")
    print(f"\nMatched Skills ({len(result['matched_skills'])}):")
    for skill in result['matched_skills']:
        print(f"  {skill['skill']}: {skill['confidence']:.2f} via {skill['methods']}")
    
    print(f"\nMissing Skills ({len(result['missing_skills'])}):")
    for skill_data in result['missing_skills_ranked']:
        print(f"  {skill_data['skill']} (importance: {skill_data['importance']})")
    
    # Get insights
    insights = get_skill_gap_insights(result)
    print(f"\nInsights:")
    print(f"  Assessment: {insights['overall_assessment']}")
    print(f"  Learning Time: {insights['estimated_learning_time']}")
