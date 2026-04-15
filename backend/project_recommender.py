"""
Project Recommendation Engine
Recommends hands-on projects based on missing skills
"""

# Project recommendations mapped to skills
PROJECT_RECOMMENDATIONS = {
    # Cloud & DevOps
    "docker": [
        "Containerize a Flask/Django web application",
        "Create a multi-container app with Docker Compose (frontend + backend + database)",
        "Build a Docker image optimization pipeline"
    ],
    "kubernetes": [
        "Deploy a Node.js app using Kubernetes + Minikube",
        "Set up a microservices architecture on K8s",
        "Implement auto-scaling and load balancing with K8s"
    ],
    "aws": [
        "Build a serverless REST API using AWS Lambda and API Gateway",
        "Deploy a scalable web app using EC2, RDS, and S3",
        "Create an automated backup system using AWS services"
    ],
    "azure": [
        "Deploy a web app to Azure App Service",
        "Build a data pipeline using Azure Data Factory",
        "Implement Azure Functions for serverless computing"
    ],
    "terraform": [
        "Provision AWS infrastructure using Terraform",
        "Create reusable Terraform modules",
        "Implement multi-environment deployment with Terraform"
    ],
    "jenkins": [
        "Set up a CI/CD pipeline with Jenkins",
        "Automate testing and deployment using Jenkins pipelines",
        "Integrate Jenkins with Docker and Kubernetes"
    ],
    "ansible": [
        "Automate server configuration with Ansible playbooks",
        "Deploy applications across multiple servers using Ansible",
        "Create Ansible roles for common tasks"
    ],
    
    # Programming Languages
    "python": [
        "Build a web scraper to collect data from websites",
        "Create a REST API using Flask/FastAPI",
        "Develop a data analysis dashboard with Pandas and Plotly"
    ],
    "javascript": [
        "Build a real-time chat application with Socket.io",
        "Create a weather app using external APIs",
        "Develop a task management app with React"
    ],
    "java": [
        "Build a Spring Boot REST API",
        "Create a library management system using Java",
        "Develop a multi-threaded file processing application"
    ],
    "c++": [
        "Implement data structures (linked lists, trees, graphs)",
        "Build a simple game using C++ and SDL",
        "Create a file compression utility"
    ],
    "go": [
        "Build a concurrent web server in Go",
        "Create a CLI tool for system administration",
        "Develop a microservice with gRPC"
    ],
    "rust": [
        "Build a command-line tool in Rust",
        "Create a web server using Actix-web",
        "Implement a concurrent file processor"
    ],
    
    # Web Development
    "react": [
        "Build a social media dashboard with React",
        "Create an e-commerce product catalog",
        "Develop a real-time collaborative whiteboard"
    ],
    "angular": [
        "Build a task management application",
        "Create a blog platform with Angular",
        "Develop an admin dashboard with charts"
    ],
    "vue": [
        "Build a recipe finder app with Vue.js",
        "Create a kanban board application",
        "Develop a music player interface"
    ],
    "node.js": [
        "Build a RESTful API with Express.js",
        "Create a real-time notification system",
        "Develop a file upload service with Node.js"
    ],
    "django": [
        "Build a blog platform with Django",
        "Create a user authentication system",
        "Develop an e-commerce website"
    ],
    "flask": [
        "Build a URL shortener service",
        "Create a blog API with Flask-RESTful",
        "Develop a file sharing platform"
    ],
    
    # Databases
    "sql": [
        "Design a student result management system",
        "Build a library database with complex queries",
        "Create an inventory management system"
    ],
    "mongodb": [
        "Build a blog backend with MongoDB",
        "Create a user profile management system",
        "Develop a product catalog with search functionality"
    ],
    "postgresql": [
        "Design a multi-tenant SaaS database",
        "Build a data warehouse for analytics",
        "Create a geospatial application with PostGIS"
    ],
    "redis": [
        "Implement caching for a web application",
        "Build a real-time leaderboard system",
        "Create a session management system"
    ],
    
    # Data Science & ML
    "machine learning": [
        "Train a spam email classifier using scikit-learn",
        "Build a house price prediction model",
        "Create a recommendation system"
    ],
    "deep learning": [
        "Build an image classifier using CNN",
        "Create a sentiment analysis model with LSTM",
        "Develop a chatbot using transformers"
    ],
    "tensorflow": [
        "Build a handwritten digit recognizer",
        "Create an object detection system",
        "Develop a time series forecasting model"
    ],
    "pytorch": [
        "Implement a neural network from scratch",
        "Build a GAN for image generation",
        "Create a transfer learning model"
    ],
    "data analysis": [
        "Analyze sales data and create insights dashboard",
        "Perform exploratory data analysis on a dataset",
        "Build automated reporting system with Python"
    ],
    "pandas": [
        "Clean and analyze a messy dataset",
        "Create data transformation pipelines",
        "Build a data quality monitoring system"
    ],
    "numpy": [
        "Implement matrix operations from scratch",
        "Build a scientific computing library",
        "Create numerical simulation programs"
    ],
    
    # Mobile Development
    "react native": [
        "Build a todo app for iOS and Android",
        "Create a weather app with geolocation",
        "Develop a social media feed"
    ],
    "flutter": [
        "Build a expense tracker app",
        "Create a news reader application",
        "Develop a fitness tracking app"
    ],
    "android": [
        "Build a note-taking app",
        "Create a camera application with filters",
        "Develop a location-based reminder app"
    ],
    
    # Testing & Quality
    "selenium": [
        "Automate web application testing",
        "Build a web scraping bot",
        "Create end-to-end test suite"
    ],
    "pytest": [
        "Write comprehensive unit tests for a Python project",
        "Implement integration testing",
        "Create a test automation framework"
    ],
    "junit": [
        "Write unit tests for a Java application",
        "Implement test-driven development",
        "Create a testing framework"
    ],
    
    # Security
    "cybersecurity": [
        "Build a password strength checker",
        "Create a network scanner tool",
        "Develop a vulnerability assessment script"
    ],
    "penetration testing": [
        "Set up a vulnerable web app and exploit it",
        "Create automated security testing scripts",
        "Build a security audit tool"
    ],
    
    # Other
    "git": [
        "Contribute to an open-source project",
        "Create a Git workflow automation script",
        "Build a Git hooks system for code quality"
    ],
    "linux": [
        "Write shell scripts for system administration",
        "Build a system monitoring dashboard",
        "Create automated backup scripts"
    ],
    "graphql": [
        "Build a GraphQL API for a blog",
        "Create a real-time subscription service",
        "Develop a GraphQL gateway"
    ]
}

def get_project_recommendations(missing_skills):
    """
    Get project recommendations for missing skills
    
    Args:
        missing_skills: List of skills to learn
    
    Returns:
        list: Project recommendations with skill mapping
    """
    recommendations = []
    
    for skill in missing_skills:
        skill_lower = skill.lower()
        
        # Find matching projects
        projects = None
        for key in PROJECT_RECOMMENDATIONS:
            if key in skill_lower or skill_lower in key:
                projects = PROJECT_RECOMMENDATIONS[key]
                break
        
        if not projects:
            # Default project recommendation
            projects = [
                f"Build a beginner project using {skill}",
                f"Complete online tutorials and exercises for {skill}",
                f"Contribute to open-source projects using {skill}"
            ]
        
        # Add top 2 projects for this skill
        for project in projects[:2]:
            recommendations.append({
                "skill": skill,
                "project": project,
                "difficulty": "Beginner to Intermediate"
            })
    
    return recommendations

def get_project_by_skill(skill):
    """Get a single project recommendation for a specific skill"""
    skill_lower = skill.lower()
    
    for key in PROJECT_RECOMMENDATIONS:
        if key in skill_lower or skill_lower in key:
            return PROJECT_RECOMMENDATIONS[key][0]
    
    return f"Build a practical project using {skill}"

if __name__ == "__main__":
    # Test the project recommender
    test_skills = ["Docker", "Kubernetes", "Python", "Machine Learning", "SQL"]
    recommendations = get_project_recommendations(test_skills)
    
    print("Project Recommendations:")
    print("=" * 60)
    for rec in recommendations:
        print(f"\n{rec['skill']}:")
        print(f"  → {rec['project']}")
        print(f"  Difficulty: {rec['difficulty']}")
