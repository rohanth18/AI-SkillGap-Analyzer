# AI SkillGap Analyzer - Advanced Features Implementation Guide

## 🎯 Overview
This document outlines the implementation of 8 advanced AI-powered features for the SkillGap Analyzer system.

## ✅ Completed Components

### 1. Database Schema Updates
**File**: `backend/app.py`
**New Models Added**:
- `RoleRecommendation` - Stores ML-based job role recommendations
- `LearningRoadmap` - Stores personalized learning plans
- `ProjectRecommendation` - Stores project suggestions
- `ResumeRewrite` - Stores resume improvement history
- `ReportDownload` - Tracks PDF report generations

### 2. ML Model Training Script
**File**: `backend/train_ml_model.py`
**Features**:
- RandomForest classifier with TF-IDF vectorization
- Trains on `it_jobs_roles.csv` data
- Predicts top 3 job roles with confidence scores
- Saves model to `models/role_recommender.pkl`

**Usage**:
```bash
python train_ml_model.py
```

### 3. Learning Roadmap Generator
**File**: `backend/roadmap_generator.py`
**Features**:
- Week-by-week learning plans for 20+ skills
- Includes topics, resources, and practice tasks
- Customizable roadmaps based on job role
- Supports Docker, Kubernetes, Python, ML, AWS, and more

### 4. Project Recommendation Engine
**File**: `backend/project_recommender.py`
**Features**:
- 100+ project ideas mapped to skills
- Covers DevOps, Programming, Data Science, Web Dev
- Difficulty-based recommendations
- Hands-on practical projects

### 5. Resume Rewriting Engine
**File**: `backend/resume_rewriter.py`
**Features**:
- Replaces weak verbs with strong action verbs
- Adds professional keywords
- Suggests quantifiable metrics
- Improves sentence structure
- Calculates improvement score

## 🚧 Remaining Implementation Tasks

### PART 1: Backend API Endpoints

Add these endpoints to `backend/app.py`:

```python
# 1. Role Recommendation Endpoint
@app.route('/api/recommend-roles', methods=['POST'])
@jwt_required()
def recommend_roles():
    from train_ml_model import predict_roles
    data = request.json
    user_skills = data.get('skills', [])
    
    recommendations = predict_roles(user_skills, top_n=3)
    
    # Save to database
    analysis_id = data.get('analysis_id')
    user_id = get_jwt_identity()
    
    role_rec = RoleRecommendation(
        analysis_id=analysis_id,
        user_id=user_id,
        recommended_roles_json=json.dumps(recommendations)
    )
    db.session.add(role_rec)
    db.session.commit()
    
    return jsonify({"recommended_roles": recommendations})

# 2. Generate Roadmap Endpoint
@app.route('/api/generate-roadmap', methods='POST'])
@jwt_required()
def generate_roadmap():
    from roadmap_generator import generate_roadmap
    data = request.json
    missing_skills = data.get('missing_skills', [])
    job_role = data.get('job_role', '')
    
    roadmap = generate_roadmap(missing_skills, job_role)
    
    # Save to database
    analysis_id = data.get('analysis_id')
    user_id = get_jwt_identity()
    
    roadmap_entry = LearningRoadmap(
        analysis_id=analysis_id,
        user_id=user_id,
        job_role=job_role,
        roadmap_json=json.dumps(roadmap)
    )
    db.session.add(roadmap_entry)
    db.session.commit()
    
    return jsonify(roadmap)

# 3. Recommend Projects Endpoint
@app.route('/api/recommend-projects', methods=['POST'])
@jwt_required()
def recommend_projects():
    from project_recommender import get_project_recommendations
    data = request.json
    missing_skills = data.get('missing_skills', [])
    
    projects = get_project_recommendations(missing_skills)
    
    # Save to database
    analysis_id = data.get('analysis_id')
    user_id = get_jwt_identity()
    
    project_rec = ProjectRecommendation(
        analysis_id=analysis_id,
        user_id=user_id,
        projects_json=json.dumps(projects)
    )
    db.session.add(project_rec)
    db.session.commit()
    
    return jsonify({"project_recommendations": projects})

# 4. Resume Rewrite Endpoint
@app.route('/api/rewrite-section', methods=['POST'])
@jwt_required()
def rewrite_section():
    from resume_rewriter import rewrite_resume_section
    data = request.json
    original_text = data.get('text', '')
    context = data.get('context', 'experience')
    
    result = rewrite_resume_section(original_text, context)
    
    # Save to database
    user_id = get_jwt_identity()
    rewrite_entry = ResumeRewrite(
        user_id=user_id,
        original_text=original_text,
        rewritten_text=result['rewritten']
    )
    db.session.add(rewrite_entry)
    db.session.commit()
    
    return jsonify(result)

# 5. Admin Insights - Heatmap
@app.route('/api/admin/insights/heatmap', methods=['GET'])
@jwt_required()
def admin_heatmap():
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
    
    # Sort by frequency
    sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    
    return jsonify({
        "heatmap_data": [{"skill": s[0], "count": s[1]} for s in sorted_skills]
    })

# 6. Admin Insights - Trends
@app.route('/api/admin/insights/trends', methods=['GET'])
@jwt_required()
def admin_trends():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({'error': 'Admin only'}), 403
    
    # Categorize skills by domain
    domains = {
        "Cloud": ["aws", "azure", "gcp", "docker", "kubernetes"],
        "AI/ML": ["machine learning", "deep learning", "tensorflow", "pytorch"],
        "DevOps": ["jenkins", "ansible", "terraform", "ci/cd"],
        "Full Stack": ["react", "angular", "node.js", "django", "flask"],
        "Data Engineering": ["sql", "mongodb", "spark", "airflow"]
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
    
    return jsonify({
        "trend_data": [{"domain": d, "gap_count": c} for d, c in domain_gaps.items()]
    })
```

### PART 2: PDF Report Generation

Create `backend/pdf_generator.py`:

```python
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import matplotlib.pyplot as plt
import io
import os

def generate_pdf_report(analysis_data, user_name, output_path):
    """Generate comprehensive PDF report"""
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    story.append(Paragraph(f"Skill Gap Analysis Report", title_style))
    story.append(Paragraph(f"Candidate: {user_name}", styles['Heading2']))
    story.append(Paragraph(f"Job Role: {analysis_data['job_role']}", styles['Heading2']))
    story.append(Spacer(1, 0.3*inch))
    
    # Confidence Score
    score_text = f"<b>Confidence Score: {analysis_data['confidence_score']}%</b>"
    story.append(Paragraph(score_text, styles['Heading3']))
    story.append(Spacer(1, 0.2*inch))
    
    # Extracted Skills
    story.append(Paragraph("<b>Extracted Skills:</b>", styles['Heading3']))
    skills_text = ", ".join(analysis_data.get('extracted_skills', {}).keys())
    story.append(Paragraph(skills_text or "None", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Missing Skills
    story.append(Paragraph("<b>Missing Skills:</b>", styles['Heading3']))
    missing_text = ", ".join(analysis_data.get('missing_skills', []))
    story.append(Paragraph(missing_text or "None", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Recommended Roles
    if 'recommended_roles' in analysis_data:
        story.append(Paragraph("<b>Recommended Job Roles:</b>", styles['Heading3']))
        for role in analysis_data['recommended_roles']:
            story.append(Paragraph(f"• {role['role']} ({role['confidence']}% match)", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
    
    # Learning Roadmap Summary
    if 'roadmap' in analysis_data:
        story.append(Paragraph("<b>Learning Roadmap:</b>", styles['Heading3']))
        roadmap = analysis_data['roadmap']
        story.append(Paragraph(f"Total Duration: {roadmap['total_weeks']} weeks", styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        for week in roadmap['roadmap'][:5]:  # First 5 weeks
            week_text = f"Week {week['week']}: {week['title']} - {week['skill']}"
            story.append(Paragraph(week_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    return output_path
```

Add endpoint in `app.py`:
```python
@app.route('/api/export-report/<int:analysis_id>', methods=['GET'])
@jwt_required()
def export_report(analysis_id):
    from pdf_generator import generate_pdf_report
    
    user_id = get_jwt_identity()
    analysis = Analysis.query.get_or_404(analysis_id)
    
    if str(analysis.user_id) != str(user_id):
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    
    # Prepare data
    analysis_data = analysis.to_dict()
    
    # Add recommendations if available
    role_rec = RoleRecommendation.query.filter_by(analysis_id=analysis_id).first()
    if role_rec:
        analysis_data['recommended_roles'] = json.loads(role_rec.recommended_roles_json)
    
    roadmap = LearningRoadmap.query.filter_by(analysis_id=analysis_id).first()
    if roadmap:
        analysis_data['roadmap'] = json.loads(roadmap.roadmap_json)
    
    # Generate PDF
    reports_dir = 'reports'
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    filename = f"report_{user_id}_{analysis_id}.pdf"
    output_path = os.path.join(reports_dir, filename)
    
    generate_pdf_report(analysis_data, user.name, output_path)
    
    # Save download log
    report_log = ReportDownload(
        analysis_id=analysis_id,
        user_id=user_id,
        report_path=output_path
    )
    db.session.add(report_log)
    db.session.commit()
    
    return send_from_directory(reports_dir, filename, as_attachment=True)
```

### PART 3: Frontend Components

Create these React components in `frontend/src/pages/`:

1. **RoleRecommendations.jsx** - Display ML-recommended roles
2. **LearningRoadmap.jsx** - Show week-by-week learning plan
3. **ProjectRecommendations.jsx** - Display project suggestions
4. **ResumeRewriter.jsx** - Before/after resume text comparison
5. **AdminInsights.jsx** - Heatmaps and trend charts

### PART 4: Integration Steps

1. **Train the ML Model**:
```bash
cd backend
python train_ml_model.py
```

2. **Update Analysis Flow**:
Modify the `/api/analyze` endpoint to automatically:
- Generate role recommendations
- Create learning roadmap
- Suggest projects

3. **Add Frontend Routes** in `App.jsx`:
```javascript
<Route path="/role-recommendations/:id" element={<RoleRecommendations />} />
<Route path="/learning-roadmap/:id" element={<LearningRoadmap />} />
<Route path="/projects/:id" element={<ProjectRecommendations />} />
<Route path="/resume-rewriter" element={<ResumeRewriter />} />
<Route path="/admin/insights" element={<AdminInsights />} />
```

## 📊 Expected Outcomes

After full implementation:
- ✅ ML-powered job role recommendations
- ✅ Personalized learning roadmaps
- ✅ Project-based learning suggestions
- ✅ AI resume improvement
- ✅ Professional PDF reports
- ✅ Admin analytics dashboard
- ✅ Skill gap heatmaps
- ✅ Industry trend analysis

## 🎓 Next Steps

1. Install new dependencies: `pip install -r requirements.txt`
2. Train ML model: `python train_ml_model.py`
3. Add API endpoints to `app.py`
4. Create frontend components
5. Test end-to-end workflow
6. Generate sample PDF reports

## 📝 Notes

- The ML model requires at least 20 job roles in the CSV for good accuracy
- PDF generation requires system fonts (install if missing)
- Roadmap templates can be customized in `roadmap_generator.py`
- Project recommendations can be expanded in `project_recommender.py`
