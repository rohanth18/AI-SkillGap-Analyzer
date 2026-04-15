import requests
import re

def extract_skills_from_github(github_url):
    """
    Extracts potential skills/technologies from a GitHub profile or repository using public API or scraping (simplified).
    Returns a list of skills found.
    """
    if not github_url:
        return []
    
    # Clean URL to get username
    username = github_url.rstrip('/').split('/')[-1]
    if not username:
        return []

    # Try to fetch public repos languages
    # Note: This uses public unauthenticated API which has rate limits.
    # ideally we would use a token if provided in env vars.
    api_url = f"https://api.github.com/users/{username}/repos"
    
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            repos = response.json()
            languages = set()
            for repo in repos:
                lang = repo.get('language')
                if lang:
                    languages.add(lang)
                
                # Also check topics if available
                topics = repo.get('topics', [])
                for topic in topics:
                    languages.add(topic)

            return list(languages)
        else:
            print(f"Failed to fetch GitHub data: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error extracting from GitHub: {str(e)}")
        return []
