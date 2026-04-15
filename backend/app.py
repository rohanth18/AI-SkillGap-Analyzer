from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
import datetime
# import pandas as pd
from nlp_utils import extract_text_from_file, extract_skills_combined, calculate_confidence_score, normalize_skill, calculate_ats_score
from recommender import get_recommendations
from github_utils import extract_skills_from_github

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skillgap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'dev-secret-key'

db = SQLAlchemy(app)
CORS(app)
migrate = Migrate(app, db)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# --- MODELS ---

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Relationships with cascade delete
    resumes = db.relationship('Resume', backref='user', cascade='all, delete-orphan')
    analyses = db.relationship('Analysis', backref='user', cascade='all, delete-orphan')
    audit_logs = db.relationship('AuditLog', backref='user', cascade='all, delete-orphan')
    role_recs = db.relationship('RoleRecommendation', backref='user', cascade='all, delete-orphan')
    roadmaps = db.relationship('LearningRoadmap', backref='user', cascade='all, delete-orphan')
    project_recs = db.relationship('ProjectRecommendation', backref='user', cascade='all, delete-orphan')
    rewrites = db.relationship('ResumeRewrite', backref='user', cascade='all, delete-orphan')
    downloads = db.relationship('ReportDownload', backref='user', cascade='all, delete-orphan')

class Resume(db.Model):
    __tablename__ = 'resumes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    filename = db.Column(db.String(256))
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Analysis(db.Model):
    __tablename__ = 'analyses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    job_role = db.Column(db.String(100))
    # JSON fields stored as text/string in SQLite
    extracted_skills_json = db.Column(db.Text) 
    manual_skills_json = db.Column(db.Text)
    github_skills_json = db.Column(db.Text)
    missing_skills_json = db.Column(db.Text)
    all_skills_json = db.Column(db.Text) # Storing full list of skills found in resume
    confidence_score = db.Column(db.Float)
    ats_score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'job_role': self.job_role,
            'extracted_skills': json.loads(self.extracted_skills_json) if self.extracted_skills_json else {},
            'manual_skills': json.loads(self.manual_skills_json) if self.manual_skills_json else [],
            'github_skills': json.loads(self.github_skills_json) if self.github_skills_json else [],
            'missing_skills': json.loads(self.missing_skills_json) if self.missing_skills_json else [],
            'all_skills': json.loads(self.all_skills_json) if self.all_skills_json else [],
            'confidence_score': self.confidence_score,
            'ats_score': self.ats_score,
            'created_at': self.created_at.isoformat()
        }

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.Text)
    skills = db.relationship('RoleSkill', backref='role', cascade='all, delete-orphan')

class RoleSkill(db.Model):
    __tablename__ = 'role_skills'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    skill = db.Column(db.String(100))

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100))
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# New models for advanced features
class RoleRecommendation(db.Model):
    __tablename__ = 'role_recommendations'
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analyses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recommended_roles_json = db.Column(db.Text)  # JSON: [{"role": "...", "confidence": 82}]
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class LearningRoadmap(db.Model):
    __tablename__ = 'learning_roadmaps'
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analyses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    job_role = db.Column(db.String(100))
    roadmap_json = db.Column(db.Text)  # JSON: week-by-week plan
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class ProjectRecommendation(db.Model):
    __tablename__ = 'project_recommendations'
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analyses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    projects_json = db.Column(db.Text)  # JSON: [{"skill": "...", "project": "..."}]
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class ResumeRewrite(db.Model):
    __tablename__ = 'resume_rewrites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    original_text = db.Column(db.Text)
    rewritten_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class ReportDownload(db.Model):
    __tablename__ = 'report_downloads'
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analyses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    report_path = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
import datetime

# ... imports ... 

app.config['JWT_SECRET_KEY'] = 'jwt-super-secret-key'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

jwt = JWTManager(app)

# ... models ...

# --- UTILS ---

def log_action(user_id, action, details):
    import json
    log = AuditLog(user_id=user_id, action=action, details=json.dumps(details))
    db.session.add(log)
    db.session.commit()
    
# --- ROUTES ---

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    hashed_pw = generate_password_hash(data['password'])
    is_admin = data.get('is_admin', False)
    
    # Auto-make first user admin if none exist
    if User.query.count() == 0:
        is_admin = True
        
    user = User(name=data['name'], email=data['email'], password_hash=hashed_pw, is_admin=is_admin)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        # Create token with user id and claims
        additional_claims = {"is_admin": user.is_admin}
        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
        
        return jsonify({
            'message': 'Login successful',
            'token': access_token,
            'user': {'id': user.id, 'name': user.name, 'email': user.email, 'is_admin': user.is_admin}
        })
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/user/analyses', methods=['GET'])
@jwt_required()
def get_my_analyses():
    current_user_id = get_jwt_identity()
    analyses = Analysis.query.filter_by(user_id=current_user_id).order_by(Analysis.created_at.desc()).all()
    return jsonify([a.to_dict() for a in analyses])

@app.route('/api/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    result = []
    for r in roles:
        skills = [s.skill for s in r.skills]
        result.append({'id': r.id, 'name': r.name, 'description': r.description, 'skills': skills})
    return jsonify(result)

@app.route('/api/upload', methods=['POST'])
@jwt_required()
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    user_id = get_jwt_identity()
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    
    # Extract text immediately
    text = extract_text_from_file(path)
    
    resume = Resume(user_id=user_id, filename=filename, text=text)
    db.session.add(resume)
    db.session.commit()
    
    return jsonify({'message': 'File uploaded', 'resume_id': resume.id})

@app.route('/api/analyze', methods=['POST'])
@jwt_required()
def analyze_resume():
    data = request.json
    user_id = get_jwt_identity()
    resume_id = data.get('resume_id')
    role_id = data.get('role_id')
    manual_skills = data.get('manual_skills', []) # List of strings
    github_url = data.get('github_url', '')

    resume = Resume.query.get(resume_id)
    if not resume or str(resume.user_id) != str(user_id):
        return jsonify({'error': 'Resume not found or access denied'}), 404
        
    role = Role.query.get(role_id)
    if not role:
        return jsonify({'error': 'Role not found'}), 404
        
    role_skills = [s.skill for s in role.skills]
    
    # Extra Github skills
    github_skills = []
    if github_url:
        github_skills = extract_skills_from_github(github_url)

    # NLP Extraction
    extracted_data = extract_skills_combined(resume.text, github_skills, manual_skills)
    
    # Score
    score, skill_details, missing, present = calculate_confidence_score(extracted_data, role_skills)
    
    # Recommendations
    recs = get_recommendations(missing)
    
    # Calculate ATS Score
    ats_score_val = calculate_ats_score(resume.text, len(extracted_data))

    # Save Analysis
    analysis = Analysis(
        user_id=user_id,
        resume_id=resume_id,
        job_role=role.name,
        extracted_skills_json=json.dumps(skill_details),
        manual_skills_json=json.dumps(manual_skills),
        github_skills_json=json.dumps(github_skills),
        missing_skills_json=json.dumps(missing),
        all_skills_json=json.dumps(list(extracted_data.keys())), # Full extracted list
        confidence_score=score,
        ats_score=ats_score_val
    )
    db.session.add(analysis)
    db.session.commit()
    
    log_action(user_id, 'analyze', {'resume_id': resume_id, 'role': role.name, 'score': score})
    
    return jsonify({
        'analysis_id': analysis.id,
        'score': score,
        'missing': missing,
        'present': present,
        'details': skill_details,
        'recommendations': recs
    })

@app.route('/api/analysis/<int:id>', methods=['GET'])
@jwt_required()
def get_analysis_detail(id):
    analysis = Analysis.query.get_or_404(id)
    current_user_id = get_jwt_identity()
    
    # Admin can view all, user can view own
    claims = get_jwt()
    if str(analysis.user_id) != str(current_user_id) and not claims.get('is_admin'):
        return jsonify({'error': 'Access denied'}), 403
        
    missing = json.loads(analysis.missing_skills_json) if analysis.missing_skills_json else []
    recs = get_recommendations(missing)
    data = analysis.to_dict()
    data['recommendations'] = recs
    return jsonify(data)

# --- ADVANCED FEATURES ENDPOINTS ---

@app.route('/api/recommend-roles', methods=['POST'])
@jwt_required()
def recommend_roles():
    """ML-powered job role recommendations based on user skills"""
    try:
        from train_ml_model import predict_roles
        
        data = request.json
        user_skills = data.get('skills', [])
        analysis_id = data.get('analysis_id')
        user_id = get_jwt_identity()
        
        if not user_skills:
            return jsonify({'error': 'No skills provided'}), 400
        
        # Get ML predictions
        recommendations = predict_roles(user_skills, top_n=3)
        
        # Save to database
        if analysis_id:
            role_rec = RoleRecommendation(
                analysis_id=analysis_id,
                user_id=user_id,
                recommended_roles_json=json.dumps(recommendations)
            )
            db.session.add(role_rec)
            db.session.commit()
        
        return jsonify({"recommended_roles": recommendations})
    except Exception as e:
        return jsonify({'error': f'Recommendation failed: {str(e)}'}), 500

@app.route('/api/generate-roadmap', methods=['POST'])
@jwt_required()
def generate_roadmap():
    """Generate personalized learning roadmap"""
    try:
        from roadmap_generator import generate_roadmap
        
        data = request.json
        missing_skills = data.get('missing_skills', [])
        job_role = data.get('job_role', '')
        analysis_id = data.get('analysis_id')
        user_id = get_jwt_identity()
        
        if not missing_skills:
            return jsonify({'error': 'No missing skills provided'}), 400
        
        # Generate roadmap
        roadmap = generate_roadmap(missing_skills, job_role)
        
        # Save to database
        if analysis_id:
            roadmap_entry = LearningRoadmap(
                analysis_id=analysis_id,
                user_id=user_id,
                job_role=job_role,
                roadmap_json=json.dumps(roadmap)
            )
            db.session.add(roadmap_entry)
            db.session.commit()
        
        return jsonify(roadmap)
    except Exception as e:
        return jsonify({'error': f'Roadmap generation failed: {str(e)}'}), 500

@app.route('/api/recommend-projects', methods=['POST'])
@jwt_required()
def recommend_projects():
    """Get project recommendations for missing skills"""
    try:
        from project_recommender import get_project_recommendations
        
        data = request.json
        missing_skills = data.get('missing_skills', [])
        analysis_id = data.get('analysis_id')
        user_id = get_jwt_identity()
        
        if not missing_skills:
            return jsonify({'error': 'No missing skills provided'}), 400
        
        # Get project recommendations
        projects = get_project_recommendations(missing_skills)
        
        # Save to database
        if analysis_id:
            project_rec = ProjectRecommendation(
                analysis_id=analysis_id,
                user_id=user_id,
                projects_json=json.dumps(projects)
            )
            db.session.add(project_rec)
            db.session.commit()
        
        return jsonify({"project_recommendations": projects})
    except Exception as e:
        return jsonify({'error': f'Project recommendation failed: {str(e)}'}), 500

@app.route('/api/rewrite-section', methods=['POST'])
@jwt_required()
def rewrite_section():
    """AI-powered resume text rewriting"""
    try:
        from resume_rewriter import rewrite_resume_section
        
        data = request.json
        original_text = data.get('text', '')
        context = data.get('context', 'experience')
        user_id = get_jwt_identity()
        
        if not original_text or len(original_text.strip()) < 10:
            return jsonify({'error': 'Text too short to rewrite'}), 400
        
        # Rewrite the text
        result = rewrite_resume_section(original_text, context)
        
        # Save to database
        rewrite_entry = ResumeRewrite(
            user_id=user_id,
            original_text=original_text,
            rewritten_text=result['rewritten']
        )
        db.session.add(rewrite_entry)
        db.session.commit()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Rewrite failed: {str(e)}'}), 500

@app.route('/api/analysis/<int:analysis_id>/complete', methods=['GET'])
@jwt_required()
def get_complete_analysis(analysis_id):
    """Get analysis with all advanced features (recommendations, roadmap, projects)"""
    user_id = get_jwt_identity()
    analysis = Analysis.query.get_or_404(analysis_id)
    
    # Check access
    claims = get_jwt()
    if str(analysis.user_id) != str(user_id) and not claims.get('is_admin'):
        return jsonify({'error': 'Access denied'}), 403
    
    # Get base analysis data
    data = analysis.to_dict()
    
    # Ensure role recommendations use all skills from resume
    role_rec = RoleRecommendation.query.filter_by(analysis_id=analysis_id).first()
    if not role_rec:
        # Generate them now if missing using full skill set
        from train_ml_model import predict_roles
        all_skills = data.get('all_skills', [])
        if all_skills:
            recommendations = predict_roles(all_skills, top_n=3)
            role_rec = RoleRecommendation(
                analysis_id=analysis_id,
                user_id=user_id,
                recommended_roles_json=json.dumps(recommendations)
            )
            db.session.add(role_rec)
            db.session.commit()
    
    if role_rec:
        data['recommended_roles'] = json.loads(role_rec.recommended_roles_json)
    
    # Add learning roadmap if available
    roadmap = LearningRoadmap.query.filter_by(analysis_id=analysis_id).first()
    if roadmap:
        data['roadmap'] = json.loads(roadmap.roadmap_json)
    
    # Add project recommendations if available
    projects = ProjectRecommendation.query.filter_by(analysis_id=analysis_id).first()
    if projects:
        data['project_recommendations'] = json.loads(projects.projects_json)
    
    # Add YouTube recommendations for missing skills
    missing = json.loads(analysis.missing_skills_json) if analysis.missing_skills_json else []
    data['youtube_recommendations'] = get_recommendations(missing)
    
    return jsonify(data)

@app.route('/api/admin/insights/heatmap', methods=['GET'])
@jwt_required()
def admin_heatmap():
    """Get skill gap heatmap data for admin dashboard"""
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({'error': 'Admin only'}), 403
    
    # Aggregate missing skills across all analyses
    all_analyses = Analysis.query.all()
    skill_counts = {}
    
    for analysis in all_analyses:
        if analysis.missing_skills_json:
            missing = json.loads(analysis.missing_skills_json)
            for skill in missing:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
    
    # Sort by frequency and get top 20
    sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    
    return jsonify({
        "heatmap_data": [{"skill": s[0], "count": s[1]} for s in sorted_skills]
    })

@app.route('/api/admin/insights/trends', methods=['GET'])
@jwt_required()
def admin_trends():
    """Get skill gap trends by domain for admin dashboard"""
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({'error': 'Admin only'}), 403
    
    # Categorize skills by domain
    domains = {
        "Cloud": ["aws", "azure", "gcp", "docker", "kubernetes", "cloud"],
        "AI/ML": ["machine learning", "deep learning", "tensorflow", "pytorch", "ai", "ml"],
        "DevOps": ["jenkins", "ansible", "terraform", "ci/cd", "devops", "gitlab"],
        "Full Stack": ["react", "angular", "node.js", "django", "flask", "vue"],
        "Data Engineering": ["sql", "mongodb", "spark", "airflow", "data", "etl"],
        "Mobile": ["android", "ios", "react native", "flutter", "mobile"],
        "Security": ["security", "cybersecurity", "penetration", "encryption"]
    }
    
    all_analyses = Analysis.query.all()
    domain_gaps = {domain: 0 for domain in domains}
    
    for analysis in all_analyses:
        if analysis.missing_skills_json:
            missing = json.loads(analysis.missing_skills_json)
            for skill in missing:
                skill_lower = skill.lower()
                for domain, keywords in domains.items():
                    if any(kw in skill_lower for kw in keywords):
                        domain_gaps[domain] += 1
                        break  # Count each skill only once
    
    return jsonify({
        "trend_data": [{"domain": d, "gap_count": c} for d, c in domain_gaps.items()]
    })


# --- ADMIN ROUTES ---

@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    total_users = User.query.count()
    total_resumes = Resume.query.count()
    total_analyses = Analysis.query.count()
    total_roles = Role.query.count()
    avg_score = db.session.query(db.func.avg(Analysis.confidence_score)).scalar() or 0
    
    # Calculate most common missing skills
    # This might be heavy if many analyses, but okay for prototype
    all_analyses = Analysis.query.all()
    missing_counts = {}
    for a in all_analyses:
        if a.missing_skills_json:
            skills = json.loads(a.missing_skills_json)
            for s in skills:
                missing_counts[s] = missing_counts.get(s, 0) + 1
    
    # Sort and get top 5
    sorted_missing = sorted(missing_counts.items(), key=lambda item: item[1], reverse=True)[:5]
    top_missing = [{'skill': k, 'count': v} for k, v in sorted_missing]

    return jsonify({
        'total_users': total_users,
        'total_resumes': total_resumes,
        'total_analyses': total_analyses,
        'total_roles': total_roles,
        'average_score': round(avg_score, 2),
        'top_missing_skills': top_missing
    })

@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
def get_users():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({'error': 'Admin only'}), 403
        
    users = User.query.all()
    result = []
    for u in users:
        resume_count = Resume.query.filter_by(user_id=u.id).count()
        analysis_count = Analysis.query.filter_by(user_id=u.id).count()
        result.append({
            'id': u.id,
            'name': u.name,
            'email': u.email,
            'is_admin': u.is_admin,
            'resume_count': resume_count,
            'analysis_count': analysis_count
        })
    return jsonify(result)

@app.route('/api/admin/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({'error': 'Admin only'}), 403
    
    current_user_id = get_jwt_identity()
    if str(current_user_id) == str(id):
        return jsonify({'error': 'You cannot delete your own admin account'}), 400
        
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'})

@app.route('/api/admin/roles', methods=['POST'])
def add_role():
    data = request.json
    name = data['name']
    desc = data.get('description', '')
    skills = data.get('skills', []) # list of strings
    
    if Role.query.filter_by(name=name).first():
        return jsonify({'error': 'Role exists'}), 400
        
    role = Role(name=name, description=desc)
    db.session.add(role)
    db.session.commit()
    
    for s in skills:
        rs = RoleSkill(role_id=role.id, skill=normalize_skill(s))
        db.session.add(rs)
    db.session.commit()
    
    return jsonify({'message': 'Role created'})

@app.route('/api/admin/roles/<int:id>', methods=['PUT'])
def update_role(id):
    role = Role.query.get_or_404(id)
    data = request.json
    
    if 'name' in data:
        role.name = data['name']
    if 'description' in data:
        role.description = data['description']
        
    if 'skills' in data:
        # Replace all skills (simplest approach for update)
        RoleSkill.query.filter_by(role_id=id).delete()
        for s in data['skills']:
            rs = RoleSkill(role_id=role.id, skill=normalize_skill(s))
            db.session.add(rs)
            
    db.session.commit()
    return jsonify({'message': 'Role updated'})

@app.route('/api/admin/roles/<int:id>', methods=['DELETE'])
def delete_role(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    return jsonify({'message': 'Role deleted'})

@app.route('/api/seed', methods=['POST'])
def seed_database():
    # Only run if no roles?
    if Role.query.first():
        return jsonify({'message': 'Already seeded'})
        
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'it_jobs_roles.csv')
    if os.path.exists(csv_path):
        import csv
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    title = row.get('Job Title')
                    desc = row.get('Job Description')
                    skills_str = row.get('Skills')
                    
                    if not title: continue
                    
                    existing = Role.query.filter_by(name=title).first()
                    if not existing:
                        role = Role(name=title, description=desc if desc else "")
                        db.session.add(role)
                        db.session.commit()
                        
                        if skills_str:
                            s_list = skills_str.split(',')
                            for s in s_list:
                                rs = RoleSkill(role_id=role.id, skill=normalize_skill(s))
                                db.session.add(rs)
                        db.session.commit()
            return jsonify({'message': 'Database seeded from CSV'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'CSV not found'})
if __name__ == '__main__':
    with app.app_context():
        # ...
        pass
    # Force IPv4 "0.0.0.0" and disable reloader (causes issues sometimes)
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)