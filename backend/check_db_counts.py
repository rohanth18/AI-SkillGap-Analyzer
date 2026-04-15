from app import app, db, User, Analysis, Role, Resume

with app.app_context():
    user_count = User.query.count()
    analysis_count = Analysis.query.count()
    role_count = Role.query.count()
    resume_count = Resume.query.count()
    
    print(f"Users: {user_count}")
    print(f"Analyses: {analysis_count}")
    print(f"Roles: {role_count}")
    print(f"Resumes: {resume_count}")
