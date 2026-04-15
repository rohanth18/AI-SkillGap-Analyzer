"""
AI-Based Learning Roadmap Generator
Generates personalized week-by-week learning plans based on missing skills
"""

import json

# Skill learning templates with weekly breakdown
SKILL_ROADMAPS = {
    # Cloud & DevOps
    "docker": {
        "weeks": 2,
        "plan": [
            {
                "week": 1,
                "title": "Docker Fundamentals",
                "topics": ["Install Docker", "Understand images & containers", "Basic Docker commands", "Dockerfile basics"],
                "resources": ["Docker Official Docs", "Docker for Beginners - YouTube"],
                "practice": "Create a simple Python app container"
            },
            {
                "week": 2,
                "title": "Docker Advanced",
                "topics": ["Docker Compose", "Volumes & Networks", "Multi-stage builds"],
                "resources": ["Docker Compose Tutorial", "Best Practices Guide"],
                "practice": "Build a multi-container application with Docker Compose"
            }
        ]
    },
    "kubernetes": {
        "weeks": 3,
        "plan": [
            {
                "week": 1,
                "title": "Kubernetes Basics",
                "topics": ["Pods, Deployments, Services", "kubectl commands", "Minikube setup"],
                "resources": ["Kubernetes Official Tutorial", "K8s for Beginners"],
                "practice": "Deploy a simple app on Minikube"
            },
            {
                "week": 2,
                "title": "Kubernetes Intermediate",
                "topics": ["ConfigMaps & Secrets", "Persistent Volumes", "Ingress"],
                "resources": ["Kubernetes Patterns Book", "Advanced K8s Course"],
                "practice": "Deploy a stateful application"
            },
            {
                "week": 3,
                "title": "CI/CD with Kubernetes",
                "topics": ["Helm charts", "GitOps", "Automated deployments"],
                "resources": ["Helm Documentation", "ArgoCD Tutorial"],
                "practice": "Set up CI/CD pipeline with GitHub Actions"
            }
        ]
    },
    "aws": {
        "weeks": 4,
        "plan": [
            {
                "week": 1,
                "title": "AWS Fundamentals",
                "topics": ["EC2", "S3", "IAM", "VPC basics"],
                "resources": ["AWS Free Tier", "AWS Certified Cloud Practitioner"],
                "practice": "Launch an EC2 instance and host a website"
            },
            {
                "week": 2,
                "title": "AWS Compute & Storage",
                "topics": ["Lambda", "ECS", "RDS", "DynamoDB"],
                "resources": ["Serverless Framework", "AWS Database Services"],
                "practice": "Build a serverless API with Lambda"
            },
            {
                "week": 3,
                "title": "AWS Networking & Security",
                "topics": ["Load Balancers", "CloudFront", "Security Groups", "KMS"],
                "resources": ["AWS Security Best Practices", "VPC Deep Dive"],
                "practice": "Set up a secure multi-tier architecture"
            },
            {
                "week": 4,
                "title": "AWS DevOps",
                "topics": ["CodePipeline", "CloudFormation", "Monitoring with CloudWatch"],
                "resources": ["Infrastructure as Code", "AWS DevOps Pro"],
                "practice": "Deploy a full application with CI/CD"
            }
        ]
    },
    
    # Programming Languages
    "python": {
        "weeks": 4,
        "plan": [
            {
                "week": 1,
                "title": "Python Basics",
                "topics": ["Syntax", "Data types", "Control flow", "Functions"],
                "resources": ["Python.org Tutorial", "Automate the Boring Stuff"],
                "practice": "Build a calculator and file organizer"
            },
            {
                "week": 2,
                "title": "Python OOP & Data Structures",
                "topics": ["Classes & Objects", "Lists, Dicts, Sets", "File I/O"],
                "resources": ["Real Python OOP", "Python Data Structures"],
                "practice": "Create a student management system"
            },
            {
                "week": 3,
                "title": "Python Libraries",
                "topics": ["NumPy", "Pandas", "Matplotlib", "Requests"],
                "resources": ["Pandas Documentation", "Data Analysis with Python"],
                "practice": "Analyze a dataset and create visualizations"
            },
            {
                "week": 4,
                "title": "Python Projects",
                "topics": ["Web scraping", "APIs", "Testing", "Best practices"],
                "resources": ["BeautifulSoup Tutorial", "pytest Documentation"],
                "practice": "Build a web scraper and REST API"
            }
        ]
    },
    "javascript": {
        "weeks": 3,
        "plan": [
            {
                "week": 1,
                "title": "JavaScript Fundamentals",
                "topics": ["Variables", "Functions", "Arrays", "Objects", "DOM manipulation"],
                "resources": ["MDN Web Docs", "JavaScript.info"],
                "practice": "Build interactive web pages"
            },
            {
                "week": 2,
                "title": "Modern JavaScript",
                "topics": ["ES6+", "Async/Await", "Promises", "Modules"],
                "resources": ["ES6 Features", "Async JavaScript"],
                "practice": "Create a weather app using APIs"
            },
            {
                "week": 3,
                "title": "JavaScript Frameworks",
                "topics": ["React basics", "Component lifecycle", "State management"],
                "resources": ["React Official Docs", "React for Beginners"],
                "practice": "Build a todo app with React"
            }
        ]
    },
    
    # Data & ML
    "machine learning": {
        "weeks": 6,
        "plan": [
            {
                "week": 1,
                "title": "ML Fundamentals",
                "topics": ["Supervised vs Unsupervised", "Linear Regression", "Classification"],
                "resources": ["Andrew Ng's ML Course", "Scikit-learn Docs"],
                "practice": "Build a house price predictor"
            },
            {
                "week": 2,
                "title": "Data Preprocessing",
                "topics": ["Feature scaling", "Encoding", "Handling missing data"],
                "resources": ["Data Preprocessing Guide", "Pandas Tutorial"],
                "practice": "Clean and prepare a real dataset"
            },
            {
                "week": 3,
                "title": "Classification Algorithms",
                "topics": ["Decision Trees", "Random Forest", "SVM", "KNN"],
                "resources": ["Scikit-learn Algorithms", "ML Mastery"],
                "practice": "Build a spam classifier"
            },
            {
                "week": 4,
                "title": "Deep Learning Basics",
                "topics": ["Neural Networks", "TensorFlow/Keras", "CNN basics"],
                "resources": ["Deep Learning Specialization", "TensorFlow Tutorial"],
                "practice": "Build an image classifier"
            },
            {
                "week": 5,
                "title": "Model Evaluation",
                "topics": ["Cross-validation", "Metrics", "Hyperparameter tuning"],
                "resources": ["Model Evaluation Guide", "GridSearchCV"],
                "practice": "Optimize your previous models"
            },
            {
                "week": 6,
                "title": "ML Project",
                "topics": ["End-to-end pipeline", "Deployment", "MLOps basics"],
                "resources": ["ML Project Checklist", "Flask ML Deployment"],
                "practice": "Deploy an ML model as a web service"
            }
        ]
    },
    "sql": {
        "weeks": 2,
        "plan": [
            {
                "week": 1,
                "title": "SQL Basics",
                "topics": ["SELECT", "WHERE", "JOIN", "GROUP BY", "Aggregate functions"],
                "resources": ["W3Schools SQL", "SQLZoo"],
                "practice": "Query sample databases"
            },
            {
                "week": 2,
                "title": "Advanced SQL",
                "topics": ["Subqueries", "Indexes", "Transactions", "Stored Procedures"],
                "resources": ["Advanced SQL Tutorial", "Database Design"],
                "practice": "Design and implement a student management database"
            }
        ]
    },
    
    # Default template for unknown skills
    "default": {
        "weeks": 2,
        "plan": [
            {
                "week": 1,
                "title": "Fundamentals",
                "topics": ["Core concepts", "Basic syntax/usage", "Common patterns"],
                "resources": ["Official documentation", "YouTube tutorials", "Online courses"],
                "practice": "Complete beginner tutorials and exercises"
            },
            {
                "week": 2,
                "title": "Practical Application",
                "topics": ["Real-world use cases", "Best practices", "Common tools"],
                "resources": ["Advanced tutorials", "Project-based learning"],
                "practice": "Build a small project using this skill"
            }
        ]
    }
}

def generate_roadmap(missing_skills, job_role):
    """
    Generate a personalized learning roadmap based on missing skills
    
    Args:
        missing_skills: List of skills the user needs to learn
        job_role: Target job role
    
    Returns:
        dict: Complete roadmap with weekly breakdown
    """
    if not missing_skills:
        return {
            "job_role": job_role,
            "total_weeks": 0,
            "message": "Congratulations! You have all required skills.",
            "roadmap": []
        }
    
    roadmap = []
    current_week = 1
    
    for skill in missing_skills[:10]:  # Limit to top 10 skills
        skill_lower = skill.lower()
        
        # Find matching template
        template = None
        for key in SKILL_ROADMAPS:
            if key in skill_lower:
                template = SKILL_ROADMAPS[key]
                break
        
        if not template:
            template = SKILL_ROADMAPS["default"]
        
        # Add skill roadmap with adjusted week numbers
        for week_plan in template["plan"]:
            roadmap_entry = {
                "week": current_week,
                "skill": skill,
                "title": week_plan["title"],
                "topics": week_plan["topics"],
                "resources": week_plan["resources"],
                "practice": week_plan["practice"]
            }
            roadmap.append(roadmap_entry)
            current_week += 1
    
    return {
        "job_role": job_role,
        "total_weeks": current_week - 1,
        "skills_covered": len(missing_skills[:10]),
        "roadmap": roadmap
    }

def generate_roadmap_summary(roadmap_data):
    """Generate a text summary of the roadmap"""
    if not roadmap_data.get("roadmap"):
        return "No learning roadmap needed - you have all required skills!"
    
    summary = f"Learning Roadmap for {roadmap_data['job_role']}\n"
    summary += f"Total Duration: {roadmap_data['total_weeks']} weeks\n"
    summary += f"Skills to Learn: {roadmap_data['skills_covered']}\n\n"
    
    for week in roadmap_data["roadmap"]:
        summary += f"Week {week['week']}: {week['title']} ({week['skill']})\n"
        summary += f"  Topics: {', '.join(week['topics'])}\n"
        summary += f"  Practice: {week['practice']}\n\n"
    
    return summary

if __name__ == "__main__":
    # Test the roadmap generator
    test_skills = ["Docker", "Kubernetes", "Python", "Machine Learning"]
    roadmap = generate_roadmap(test_skills, "DevOps Engineer")
    
    print(json.dumps(roadmap, indent=2))
    print("\n" + "="*60)
    print(generate_roadmap_summary(roadmap))
