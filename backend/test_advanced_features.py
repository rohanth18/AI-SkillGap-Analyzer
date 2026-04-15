"""
Test Script for Advanced Features API Endpoints
Tests all new endpoints to ensure they're working correctly
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

# You'll need to update these with actual values from your system
TEST_TOKEN = "your_jwt_token_here"  # Get this from login
TEST_ANALYSIS_ID = 1  # Use an actual analysis ID from your database

headers = {
    "Authorization": f"Bearer {TEST_TOKEN}",
    "Content-Type": "application/json"
}

def test_role_recommendations():
    """Test ML-powered role recommendations"""
    print("\n" + "="*60)
    print("Testing: Role Recommendations")
    print("="*60)
    
    payload = {
        "skills": ["Python", "Machine Learning", "TensorFlow", "Data Analysis", "SQL"],
        "analysis_id": TEST_ANALYSIS_ID
    }
    
    response = requests.post(f"{BASE_URL}/recommend-roles", 
                            json=payload, 
                            headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        print(f"Recommended Roles: {json.dumps(data, indent=2)}")
    else:
        print(f"❌ Error: {response.text}")

def test_learning_roadmap():
    """Test learning roadmap generation"""
    print("\n" + "="*60)
    print("Testing: Learning Roadmap Generation")
    print("="*60)
    
    payload = {
        "missing_skills": ["Docker", "Kubernetes", "AWS"],
        "job_role": "DevOps Engineer",
        "analysis_id": TEST_ANALYSIS_ID
    }
    
    response = requests.post(f"{BASE_URL}/generate-roadmap", 
                            json=payload, 
                            headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        print(f"Total Weeks: {data.get('total_weeks')}")
        print(f"Skills Covered: {data.get('skills_covered')}")
        print(f"First 3 weeks:")
        for week in data.get('roadmap', [])[:3]:
            print(f"  Week {week['week']}: {week['title']} - {week['skill']}")
    else:
        print(f"❌ Error: {response.text}")

def test_project_recommendations():
    """Test project recommendations"""
    print("\n" + "="*60)
    print("Testing: Project Recommendations")
    print("="*60)
    
    payload = {
        "missing_skills": ["Docker", "Python", "Machine Learning"],
        "analysis_id": TEST_ANALYSIS_ID
    }
    
    response = requests.post(f"{BASE_URL}/recommend-projects", 
                            json=payload, 
                            headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        projects = data.get('project_recommendations', [])
        print(f"Total Projects: {len(projects)}")
        for proj in projects[:5]:
            print(f"  - {proj['skill']}: {proj['project']}")
    else:
        print(f"❌ Error: {response.text}")

def test_resume_rewriter():
    """Test resume text rewriting"""
    print("\n" + "="*60)
    print("Testing: Resume Rewriter")
    print("="*60)
    
    payload = {
        "text": "Worked on Python projects and managed data.",
        "context": "experience"
    }
    
    response = requests.post(f"{BASE_URL}/rewrite-section", 
                            json=payload, 
                            headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        print(f"Original: {data.get('original')}")
        print(f"Rewritten: {data.get('rewritten')}")
        print(f"Improvements: {', '.join(data.get('improvements', []))}")
        print(f"Score Improvement: +{data.get('score_improvement')}%")
    else:
        print(f"❌ Error: {response.text}")

def test_complete_analysis():
    """Test getting complete analysis with all features"""
    print("\n" + "="*60)
    print("Testing: Complete Analysis (All Features)")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/analysis/{TEST_ANALYSIS_ID}/complete", 
                           headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        print(f"Job Role: {data.get('job_role')}")
        print(f"Confidence Score: {data.get('confidence_score')}%")
        
        if 'recommended_roles' in data:
            print(f"Has Role Recommendations: ✓")
        if 'roadmap' in data:
            print(f"Has Learning Roadmap: ✓")
        if 'project_recommendations' in data:
            print(f"Has Project Recommendations: ✓")
    else:
        print(f"❌ Error: {response.text}")

def test_admin_heatmap():
    """Test admin heatmap endpoint"""
    print("\n" + "="*60)
    print("Testing: Admin Heatmap")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/admin/insights/heatmap", 
                           headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        heatmap = data.get('heatmap_data', [])
        print(f"Top Missing Skills:")
        for item in heatmap[:10]:
            print(f"  - {item['skill']}: {item['count']} users")
    else:
        print(f"❌ Error: {response.text}")

def test_admin_trends():
    """Test admin trends endpoint"""
    print("\n" + "="*60)
    print("Testing: Admin Trends")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/admin/insights/trends", 
                           headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        trends = data.get('trend_data', [])
        print(f"Skill Gap Trends by Domain:")
        for trend in trends:
            print(f"  - {trend['domain']}: {trend['gap_count']} gaps")
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    print("\n" + "🚀"*30)
    print("ADVANCED FEATURES API TEST SUITE")
    print("🚀"*30)
    
    print("\n⚠️  SETUP REQUIRED:")
    print("1. Login to get JWT token")
    print("2. Update TEST_TOKEN variable in this script")
    print("3. Update TEST_ANALYSIS_ID with a valid analysis ID")
    print("\nPress Enter to continue or Ctrl+C to exit...")
    input()
    
    # Run all tests
    try:
        test_role_recommendations()
        test_learning_roadmap()
        test_project_recommendations()
        test_resume_rewriter()
        test_complete_analysis()
        test_admin_heatmap()
        test_admin_trends()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend server")
        print("Make sure the server is running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
