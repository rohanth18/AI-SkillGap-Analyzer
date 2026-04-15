def get_recommendations(missing_skills):
    """
    Generates YouTube search URLs for missing skills.
    """
    recommendations = []
    for skill in missing_skills:
        query = f"{skill} tutorial for beginners"
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        recommendations.append({
            'skill': skill,
            'link': url,
            'type': 'YouTube'
        })
    return recommendations
