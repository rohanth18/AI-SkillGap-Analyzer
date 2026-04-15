# Architecture Diagram Generation Prompts

**AI-Based Skill Gap Analyzer and Personalized Learning Recommendation System**

Use these prompts with AI image generation tools (DALL-E, Midjourney, etc.) or as instructions for creating professional diagrams.

---

## 1. System Perspective Design

**Prompt:**
```
Create a clean, professional system architecture diagram with a white background showing:

LEFT SIDE: A rectangular box labeled "Admin / Job Seeker" with a bidirectional arrow connecting to a smaller box below it labeled "Manage profiles/Resume analysis/Skill gap reports/Learning roadmaps/ATS optimization"

CENTER: Two rectangular boxes stacked vertically:
- Top box: "Registration & Authentication Module"
- Bottom box: "Manage data of Admin and Job Seeker"

RIGHT SIDE: A cylindrical database icon labeled "AI SkillGap Analyzer Database"

Connections:
- Bidirectional arrows between the left user box and both center modules
- Bidirectional arrows between both center modules and the database cylinder

Style: Simple black and white line diagram, professional technical documentation style, clear labels in Arial or similar sans-serif font, minimal colors (black lines, white background)
```

---

## 2. Level 0 DFD (Context Diagram)

**Prompt:**
```
Create a Data Flow Diagram (DFD) Level 0 context diagram with white background:

CENTER: A large circle labeled "AI SkillGap Analyzer" (the main system)

EXTERNAL ENTITIES (rectangles around the circle):
- Left side: "Job Seeker" rectangle
- Right side: "Admin" rectangle

DATA FLOWS (arrows with labels):
From Job Seeker to System:
- Arrow labeled "Uploads resume, Manual skills input, GitHub profile"

From System to Job Seeker:
- Arrow labeled "Skill gap analysis, Job recommendations, Learning roadmap, ATS score"

From Admin to System:
- Arrow labeled "Manage users, Update job roles, Monitor system"

From System to Admin:
- Arrow labeled "Analytics reports, Skill gap heatmaps, Audit logs"

Style: Classic DFD notation, black and white, clean lines, professional technical diagram, labels in small readable font
```

---

## 3. Level 1 DFD - Admin Module

**Prompt:**
```
Create a Level 1 Data Flow Diagram for Admin module with white background:

LEFT: Rectangle labeled "Admin"

PROCESSES (circles/ovals):
- Top: Oval labeled "Admin Login"
- Middle: Oval labeled "Manage Job Roles"
- Bottom: Oval labeled "View Analytics"

DATA STORES (open-ended rectangles):
- "User Database"
- "Roles Database"
- "Analysis Database"

FLOWS:
1. Admin → "Admin Login" process (arrow labeled "Login credentials")
2. "Admin Login" → "User Database" store (arrow labeled "Verified")
3. "User Database" → Admin (dashed arrow labeled "Success")
4. Admin → "Manage Job Roles" process (arrow labeled "Add/Edit roles")
5. "Manage Job Roles" ↔ "Roles Database" (bidirectional arrow labeled "Update")
6. Admin → "View Analytics" process (arrow labeled "Request insights")
7. "Analysis Database" → "View Analytics" (arrow labeled "Skill gap trends")
8. "View Analytics" → Admin (arrow labeled "Heatmaps & charts")

Style: Standard DFD Level 1 notation, black and white, clean professional diagram
```

---

## 4. Level 1 DFD - Job Seeker Module

**Prompt:**
```
Create a detailed Level 1 Data Flow Diagram for Job Seeker module with white background:

LEFT: Rectangle labeled "Job Seeker"

PROCESSES (ovals, arranged vertically):
1. "Registration and Login"
2. "Resume Upload and Parsing"
3. "AI Skill Extraction"
4. "Gap Analysis and Matching"
5. "Generate Recommendations"

DATA STORES (rectangles on right side):
1. "User Database"
2. "Resume Repository"
3. "Analysis Results"
4. "Job Roles Database"
5. "Learning Resources"

FLOWS:
- Job Seeker → "Registration and Login" ↔ "User Database"
- Job Seeker → "Resume Upload and Parsing" → "Resume Repository"
- "Resume Upload and Parsing" → "AI Skill Extraction"
- "AI Skill Extraction" → "Analysis Results"
- "Job Roles Database" → "Gap Analysis and Matching"
- "AI Skill Extraction" → "Gap Analysis and Matching"
- "Gap Analysis and Matching" → "Generate Recommendations"
- "Learning Resources" → "Generate Recommendations"
- "Generate Recommendations" → Job Seeker (labeled "Roadmap, Projects, YouTube resources")

Style: Professional DFD Level 1, vertical flow layout, black and white, clear process-to-store connections
```

---

## 5. Use Case Diagram - Admin

**Prompt:**
```
Create a UML Use Case Diagram for Admin with white background:

LEFT: Stick figure actor labeled "Admin"

RIGHT: Large rectangle (system boundary) labeled "AI SkillGap Analyzer" containing:
- Oval: "Admin Login"
- Oval: "Manage Users"
- Oval: "Manage Job Roles"
- Oval: "View Analytics Dashboard"
- Oval: "View Skill Gap Heatmaps"
- Oval: "Monitor AI Performance"

CONNECTIONS:
- Lines connecting the Admin stick figure to each use case oval

Style: Standard UML use case diagram, simple black and white, stick figure on left, system boundary box on right with use cases inside, clean professional appearance
```

---

## 6. Use Case Diagram - Job Seeker

**Prompt:**
```
Create a UML Use Case Diagram for Job Seeker with white background:

LEFT: Stick figure actor labeled "Job Seeker"

RIGHT: Large rectangle (system boundary) labeled "AI SkillGap Analyzer" containing:
- Oval: "Register & Login"
- Oval: "Upload Resume"
- Oval: "Input Manual Skills"
- Oval: "View Skill Gap Analysis"
- Oval: "Get Job Recommendations"
- Oval: "View Learning Roadmap"
- Oval: "Get Project Suggestions"
- Oval: "Optimize Resume - ATS"
- Oval: "Download Report"

CONNECTIONS:
- Lines connecting the Job Seeker stick figure to each use case oval

Style: Standard UML use case diagram, simple black and white, stick figure on left, system boundary box on right with use cases inside, clean professional appearance
```

---

## 7. Complete System Architecture Diagram

**Prompt:**
```
Create a comprehensive 3-tier system architecture diagram with white background:

TOP LAYER - "Frontend Layer":
- Box labeled "React App with Vite"
- Box labeled "Chart.js Visualization"
- Connected horizontally

MIDDLE LAYER - "Backend Layer":
- Box labeled "Flask API Server"
- Box labeled "JWT Authentication"
- Sub-section labeled "AI Core" containing:
  - "Resume Parser (spaCy)"
  - "SBERT Semantic Engine"
  - "ML Recommender (RandomForest)"

BOTTOM LAYER - "Data Layer":
- Cylinder shape labeled "SQLite Database"

EXTERNAL ENTITIES:
- Left side: "Job Seeker" icon
- Left side: "Admin" icon

CONNECTIONS:
- Users connect to Frontend
- Frontend connects to Backend via "REST API"
- Backend components interconnected
- Backend connects to Database

Style: Modern layered architecture diagram, use light blue for frontend, light green for backend, light yellow for database, black connecting lines, professional cloud architecture style
```

---

## 8. Database Schema ER Diagram

**Prompt:**
```
Create an Entity-Relationship (ER) diagram with white background showing:

MAIN ENTITIES (rectangles):
- USERS (id PK, name, email UK, password_hash, is_admin, created_at)
- RESUMES (id PK, user_id FK, filename, text_content, created_at)
- ANALYSES (id PK, user_id FK, resume_id FK, job_role, extracted_skills JSON, manual_skills JSON, github_skills JSON, missing_skills JSON, confidence_score, ats_score, created_at)
- ROLES (id PK, name UK, description)
- ROLE_SKILLS (id PK, role_id FK, skill)

ADVANCED FEATURE ENTITIES:
- ROLE_RECOMMENDATIONS (id PK, analysis_id FK, user_id FK, recommended_roles JSON, created_at)
- LEARNING_ROADMAPS (id PK, analysis_id FK, user_id FK, job_role, roadmap_json, created_at)
- PROJECT_RECOMMENDATIONS (id PK, analysis_id FK, user_id FK, projects_json, created_at)
- RESUME_REWRITES (id PK, user_id FK, original_text, rewritten_text, created_at)
- AUDIT_LOGS (id PK, user_id FK, action, details, created_at)
- REPORT_DOWNLOADS (id PK, analysis_id FK, user_id FK, report_path, created_at)

RELATIONSHIPS (crow's foot notation):
- USERS (1) to RESUMES (many)
- USERS (1) to ANALYSES (many)
- USERS (1) to AUDIT_LOGS (many)
- USERS (1) to RESUME_REWRITES (many)
- RESUMES (1) to ANALYSES (many)
- ROLES (1) to ROLE_SKILLS (many)
- ANALYSES (1) to ROLE_RECOMMENDATIONS (many)
- ANALYSES (1) to LEARNING_ROADMAPS (many)
- ANALYSES (1) to PROJECT_RECOMMENDATIONS (many)
- ANALYSES (1) to REPORT_DOWNLOADS (many)

Style: Classic ER diagram with crow's foot notation, black and white, clear entity boxes with attributes listed, relationship lines with cardinality markers (1:N)
```

---

## 9. Sequence Diagram - Job Seeker Analysis Flow

**Prompt:**
```
Create a UML Sequence Diagram with white background showing:

ACTORS/OBJECTS (vertical lifelines from left to right):
1. "Job Seeker" (stick figure)
2. "React Frontend" (box)
3. "Flask Backend" (box)
4. "AI Engine (spaCy + SBERT)" (box)
5. "ML Model (RandomForest)" (box)
6. "SQLite Database" (cylinder)

SEQUENCE OF INTERACTIONS (horizontal arrows with labels):
1. Job Seeker → Frontend: "Upload Resume (PDF)"
2. Frontend → Backend: "POST /api/upload"
3. Backend → Backend: "Extract Text (PyPDF2)" (self-call)
4. Backend → Database: "Save Resume"
5. Database → Backend: "Resume ID"
6. Backend → Frontend: "Resume ID"
7. Job Seeker → Frontend: "Select Target Role & Analyze"
8. Frontend → Backend: "POST /api/analyze"
9. Backend → Database: "Fetch Role Requirements"
10. Database → Backend: "Required Skills List"
11. Backend → AI Engine: "Extract Skills (spaCy + SBERT)"
12. AI Engine → AI Engine: "Hybrid Extraction" (self-call)
13. AI Engine → Backend: "Extracted Skills + Confidence"
14. Backend → Backend: "Calculate Skill Gap" (self-call)
15. Backend → Backend: "Calculate ATS Score" (self-call)
16. Backend → Database: "Save Analysis"
17. Backend → ML Model: "Predict Job Roles"
18. ML Model → Backend: "Top 3 Recommendations"
19. Backend → Frontend: "Analysis Results JSON"
20. Frontend → Job Seeker: "Display Skill Gap Charts"

Style: Standard UML sequence diagram, vertical dashed lifelines, horizontal arrows with labels, activation boxes on lifelines, black and white, professional appearance
```

---

## 10. Sequence Diagram - Admin Role Management

**Prompt:**
```
Create a UML Sequence Diagram with white background showing:

ACTORS/OBJECTS (vertical lifelines from left to right):
1. "Admin" (stick figure)
2. "Admin Dashboard" (box)
3. "Flask Backend" (box)
4. "SQLite Database" (cylinder)

SEQUENCE OF INTERACTIONS:
1. Admin → Dashboard: "Login as Admin"
2. Dashboard → Backend: "POST /api/login"
3. Backend → Database: "Verify Admin Credentials"
4. Database → Backend: "User Data"
5. Backend → Dashboard: "JWT Token (is_admin: true)"
6. Admin → Dashboard: "Add New Job Role"
7. Dashboard → Backend: "POST /api/admin/roles"
   Note: {name: "DevOps Engineer", skills: ["Docker", "Kubernetes"]}
8. Backend → Database: "Insert Role & Skills"
9. Database → Backend: "Success"
10. Backend → Dashboard: "Role Created"
11. Dashboard → Admin: "Show Confirmation"
12. Admin → Dashboard: "View Analytics"
13. Dashboard → Backend: "GET /api/admin/insights/heatmap"
14. Backend → Database: "Aggregate Missing Skills"
15. Database → Backend: "Skill Frequency Data"
16. Backend → Dashboard: "Heatmap JSON"
17. Dashboard → Admin: "Display Charts"

Style: Standard UML sequence diagram, clean layout, black and white
```

---

## 11. Activity Diagram - Job Seeker Workflow

**Prompt:**
```
Create a UML Activity Diagram with white background showing Job Seeker workflow:

START (filled circle) →
Decision diamond "Already Registered?"
  - No → "Register Account" → back to decision
  - Yes → "Authenticate"

From "Authenticate" → "User Dashboard"

From Dashboard → Decision diamond "Choose Action"
  - "Upload" → "Upload Resume PDF"
  - "Manual" → "Enter Skills Manually"
  - "History" → "View Past Analyses" → END

Both Upload and Manual paths → "Select Target Job Role" → "Run AI Analysis"

From "Run AI Analysis" → Decision diamond "AI Processing"
  - Error → "Show Error Message" → back to Dashboard
  - Success → "View Skill Gap Results"

From Results → "View Radar Charts" → "Get Recommendations"

From Recommendations → Decision diamond "What Next?"
  - "Roadmap" → "View Learning Roadmap"
  - "Projects" → "View Project Suggestions"
  - "ATS" → "Optimize Resume for ATS"

All three paths → "Download PDF Report" → END (filled circle with border)

Style: Standard UML activity diagram, rounded rectangles for activities, diamonds for decisions, arrows showing flow, black and white, clear swim lane layout
```

---

## 12. Activity Diagram - Admin Workflow

**Prompt:**
```
Create a UML Activity Diagram with white background showing Admin workflow:

START (filled circle) → "Admin Login"

From Login → Decision diamond "Valid Credentials?"
  - No → "Access Denied" (END)
  - Yes → "Admin Dashboard"

From Dashboard → Decision diamond "Select Task"
  
Path 1 - Users:
  - "View User List" → Decision "Action"
    - "View" → "View User Details"
    - "Delete" → "Delete User" → "Save to Database"

Path 2 - Roles:
  - "Manage Job Roles" → Decision "Action"
    - "Add" → "Add New Role & Skills"
    - "Edit" → "Edit Existing Role"
    - "Delete" → "Delete Role"
  - All → "Save to Database"

Path 3 - Analytics:
  - "View System Analytics" → Decision "View Type"
    - "Heatmap" → "Skill Gap Heatmap"
    - "Trends" → "Domain Trends Chart"
    - "Stats" → "Overall Statistics"

All paths → back to "Admin Dashboard"

From Dashboard → Decision diamond "Logout?"
  - No → back to Dashboard
  - Yes → END (filled circle with border)

Style: Standard UML activity diagram, clear flow, black and white, organized layout
```

---

## 13. Technology Stack Mindmap

**Prompt:**
```
Create a mindmap diagram with white background showing the technology stack:

CENTER NODE: "AI SkillGap Analyzer"

BRANCH 1 - Frontend:
- React.js
- Vite Build Tool
- Chart.js Visualization
- Axios HTTP Client

BRANCH 2 - Backend:
- Python 3.9+
- Flask Framework
- Flask-SQLAlchemy ORM
- Flask-JWT-Extended
- Flask-CORS

BRANCH 3 - AI & ML:
- spaCy NLP
- Sentence-BERT
- Scikit-learn
- RandomForest Classifier
- TF-IDF Vectorizer
- FuzzyWuzzy

BRANCH 4 - Database:
- SQLite
- SQLAlchemy Models

BRANCH 5 - External APIs:
- YouTube Data API
- GitHub API

BRANCH 6 - Development Tools:
- Git Version Control
- VS Code
- Jupyter Notebook

Style: Professional mindmap with curved branches, black and white, clear hierarchy, organized radial layout
```

---

## 14. Deployment Architecture

**Prompt:**
```
Create a deployment architecture diagram with white background showing:

TOP LAYER - Client:
- Box labeled "Web Browser"

SECOND LAYER - Frontend Server:
- Box labeled "React App (Port: 5173)"

THIRD LAYER - Backend Server:
- Large box labeled "Flask API (Port: 5000)"
- Inside this box, a sub-section "AI Services" containing:
  - "spaCy NLP Engine"
  - "SBERT Model"
  - "RandomForest Model"

BOTTOM LAYER - Data Storage:
- Cylinder: "SQLite DB (skillgap.db)"
- Folder icon: "File Storage (uploads/)"
- Folder icon: "ML Models (models/)"

CONNECTIONS:
- Browser ↔ React App (labeled "HTTP/HTTPS")
- React App ↔ Flask API (labeled "REST API")
- Flask API ↔ All AI Services
- Flask API ↔ All Data Storage components
- RandomForest Model ↔ ML Models folder

Style: Modern deployment diagram, use different colors for each layer (light blue for client, light green for frontend, light orange for backend, light yellow for storage), clear connection lines, professional appearance
```

---

## General Styling Guidelines for All Diagrams:

- **Background**: Pure white (#FFFFFF)
- **Lines**: Black (#000000), 1-2px width
- **Text**: Arial or Helvetica, 10-12pt, black
- **Shapes**: Outlined in black, white fill
- **Arrows**: Simple black arrows with clear direction
- **Layout**: Clean, organized, adequate spacing between elements
- **Format**: High resolution (300 DPI minimum), PNG or SVG format
- **Size**: Standard A4 or Letter size for printing
- **Consistency**: Use same shapes for same elements across all diagrams

---

## Tools Recommendation:

1. **AI Image Generation**: Use these prompts with DALL-E 3, Midjourney, or Stable Diffusion
2. **Diagram Tools**: Draw.io (free), Lucidchart, Microsoft Visio, PlantUML
3. **Code-based**: Mermaid.js (already provided in PROJECT_DIAGRAMS.md)
4. **Professional**: Hire a technical illustrator with these specifications
5. **Online Mermaid**: https://mermaid.live/ for rendering Mermaid code

---

## Key Differences from Generic Job Portal:

This system is specifically designed for:
- **Two user roles only**: Job Seekers and Admins (NO Recruiters)
- **AI-powered skill extraction**: Using spaCy and SBERT for semantic analysis
- **Personalized learning**: Generating custom roadmaps and project recommendations
- **ATS optimization**: Helping users improve resume scores for applicant tracking systems
- **Gap analysis**: Identifying missing skills for target job roles
- **ML-based recommendations**: Using RandomForest to predict suitable career paths
