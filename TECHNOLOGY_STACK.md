# 🛠️ AI SkillGap Analyzer - Technology Stack

## 📋 Complete Tools & Technologies Used

---

## 🎨 **FRONTEND**

### Core Framework
- **React 18.2.0** - Modern JavaScript library for building user interfaces
- **React Router DOM 6.x** - Client-side routing and navigation
- **Vite 4.x** - Next-generation frontend build tool (faster than Webpack)

### UI & Styling
- **Vanilla CSS** - Custom styling with CSS variables
- **Glassmorphism Design** - Modern frosted glass effect
- **CSS Grid & Flexbox** - Responsive layouts
- **Google Fonts (Outfit)** - Professional typography

### Data Visualization
- **Chart.js 4.x** - JavaScript charting library
- **react-chartjs-2** - React wrapper for Chart.js
  - Bar Charts (Skill gap heatmap)
  - Doughnut Charts (Domain trends)
  - Radar Charts (Skill comparison)
  - Line Charts (Progress tracking)

### HTTP Client
- **Axios 1.x** - Promise-based HTTP client
  - Request/Response interceptors
  - JWT token management
  - Error handling

### State Management
- **React Hooks** (useState, useEffect, useContext)
- **LocalStorage** - Client-side data persistence

---

## ⚙️ **BACKEND**

### Core Framework
- **Flask 2.3.2** - Lightweight Python web framework
- **Flask-CORS** - Cross-Origin Resource Sharing support
- **Flask-SQLAlchemy 3.0.5** - ORM for database operations
- **Flask-Migrate 4.0.4** - Database migrations
- **Flask-JWT-Extended 4.5.2** - JWT authentication

### Web Server
- **Waitress 3.0.2** - Production-grade WSGI server for Windows
- **Werkzeug 2.3.6** - WSGI utility library

### Database
- **SQLite** - Lightweight relational database
  - 10 tables (Users, Resumes, Analyses, Roles, etc.)
  - JSON fields for flexible data storage
  - Foreign key relationships

### Machine Learning & NLP
- **scikit-learn 1.3.0** - Machine learning library
  - RandomForestClassifier - Job role prediction
  - TfidfVectorizer - Text feature extraction
  - train_test_split - Model validation
  
- **spaCy 3.7.2** - Industrial-strength NLP
  - en_core_web_sm - English language model
  - Named Entity Recognition (NER)
  - Part-of-speech tagging
  
- **joblib 1.3.2** - Model serialization and persistence

### Text Processing
- **fuzzywuzzy 0.18.0** - Fuzzy string matching
- **python-Levenshtein 0.21.1** - Fast string similarity
- **PyPDF2 3.0.1** - PDF text extraction

### Data Processing
- **NumPy 1.24.3** - Numerical computing
- **Pandas 2.0.3** - Data manipulation (limited use due to disk space)

### PDF Generation
- **ReportLab 4.0.4** - PDF creation library
- **WeasyPrint 59.0** - HTML to PDF converter
- **Pillow 10.0.0** - Image processing

### Visualization (Backend)
- **Matplotlib 3.7.2** - Plotting library for charts

### External APIs
- **GitHub API** - Extract skills from user repositories
- **YouTube API (via requests)** - Generate learning resource links

### Utilities
- **requests 2.31.0** - HTTP library for API calls
- **python-dotenv 1.0.0** - Environment variable management

---

## 🗄️ **DATABASE SCHEMA**

### Tables (10 Total)

1. **users** - User accounts and authentication
2. **resumes** - Uploaded resume files and extracted text
3. **analyses** - Skill gap analysis results
4. **roles** - Job role definitions
5. **role_skills** - Skills required for each role
6. **audit_logs** - System activity tracking
7. **role_recommendations** - ML-generated role suggestions
8. **learning_roadmaps** - Personalized learning plans
9. **project_recommendations** - Project suggestions
10. **resume_rewrites** - Resume improvement history
11. **report_downloads** - PDF report generation logs

---

## 🤖 **ARTIFICIAL INTELLIGENCE & ML**

### Machine Learning Models

1. **Job Role Recommender**
   - Algorithm: RandomForest Classifier
   - Features: TF-IDF vectorized skills
   - Training Data: 51 IT job roles
   - Output: Top 3 role predictions with confidence scores

2. **Skill Extraction**
   - SpaCy NLP pipeline
   - Fuzzy string matching (75% threshold)
   - Manual skill input
   - GitHub repository analysis

3. **Resume Rewriter**
   - Rule-based AI system
   - Action verb replacement
   - Professional keyword insertion
   - Quantification suggestions
   - Improvement scoring algorithm

4. **Learning Roadmap Generator**
   - Template-based AI
   - 20+ skill-specific roadmaps
   - Week-by-week breakdown
   - Resource recommendation engine

5. **Project Recommender**
   - Skill-to-project mapping
   - 100+ project templates
   - Difficulty classification

---

## 🔐 **SECURITY & AUTHENTICATION**

- **JWT (JSON Web Tokens)** - Stateless authentication
- **bcrypt (via Werkzeug)** - Password hashing
- **CORS** - Cross-origin security
- **Protected Routes** - Role-based access control
- **Token Expiration** - 24-hour access tokens

---

## 📊 **DATA FLOW ARCHITECTURE**

```
User Upload Resume (PDF)
    ↓
PyPDF2 extracts text
    ↓
SpaCy NLP processes text
    ↓
Skills extracted (fuzzy matching)
    ↓
Stored in SQLite database
    ↓
ML model predicts job roles
    ↓
Roadmap & projects generated
    ↓
Results displayed in React UI
    ↓
Charts rendered with Chart.js
```

---

## 🌐 **API ARCHITECTURE**

### RESTful API Endpoints (20+)

**Authentication:**
- POST `/api/register`
- POST `/api/login`
- POST `/api/admin/login`

**User Features:**
- GET `/api/user/analyses`
- POST `/api/upload`
- POST `/api/analyze`
- GET `/api/analysis/<id>`
- GET `/api/analysis/<id>/complete`

**Advanced Features:**
- POST `/api/recommend-roles`
- POST `/api/generate-roadmap`
- POST `/api/recommend-projects`
- POST `/api/rewrite-section`

**Admin Features:**
- GET `/api/admin/stats`
- GET `/api/admin/users`
- GET `/api/admin/insights/heatmap`
- GET `/api/admin/insights/trends`
- POST `/api/admin/roles`
- PUT `/api/admin/roles/<id>`
- DELETE `/api/admin/roles/<id>`

**Data Management:**
- GET `/api/roles`
- POST `/api/seed`

---

## 🔧 **DEVELOPMENT TOOLS**

### Version Control
- **Git** - Source code management

### Package Managers
- **npm** - Frontend package management
- **pip** - Python package management
- **venv** - Python virtual environment

### Code Editor
- **VS Code** (recommended)
- **Extensions**: ESLint, Prettier, Python

### Testing Tools
- **Postman/Thunder Client** - API testing
- **Browser DevTools** - Frontend debugging
- **Python unittest** - Backend testing

---

## 📦 **BUILD & DEPLOYMENT**

### Frontend Build
- **Vite** - Development server & production build
- **ES Modules** - Modern JavaScript modules
- **Hot Module Replacement (HMR)** - Fast refresh

### Backend Deployment
- **Waitress** - Production WSGI server
- **Flask Debug Mode** - Development only

### Environment
- **Windows** - Primary development OS
- **Python 3.8+** - Required version
- **Node.js 16+** - Required version

---

## 📚 **EXTERNAL LIBRARIES & DEPENDENCIES**

### Frontend (package.json)
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.x",
  "axios": "^1.x",
  "chart.js": "^4.x",
  "react-chartjs-2": "^5.x"
}
```

### Backend (requirements.txt)
```
Flask==2.3.2
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
Flask-Migrate==4.0.4
Flask-JWT-Extended==4.5.2
Werkzeug==2.3.6
spacy==3.7.2
fuzzywuzzy==0.18.0
python-Levenshtein==0.21.1
requests==2.31.0
PyPDF2==3.0.1
scikit-learn==1.3.0
joblib==1.3.2
numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.2
reportlab==4.0.4
weasyprint==59.0
Pillow==10.0.0
python-dotenv==1.0.0
```

---

## 🎯 **KEY ALGORITHMS**

### 1. Confidence Score Calculation
```python
Weights:
- SpaCy exact match: 1.0
- Manual entered: 0.95
- GitHub extracted: 0.9
- Synonym match: 0.85
- Fuzzy detected: 0.75

Score = (Matched Skills / Total Required Skills) × 100
```

### 2. Fuzzy Matching
```python
Threshold: 75%
Algorithm: Levenshtein distance
Use case: Skill name variations
```

### 3. TF-IDF Vectorization
```python
Max features: 500
N-gram range: (1, 2)
Min document frequency: 1
```

---

## 🌟 **DESIGN PATTERNS**

- **MVC Architecture** - Model-View-Controller separation
- **RESTful API** - Resource-based endpoints
- **Component-Based UI** - Reusable React components
- **Repository Pattern** - Database abstraction
- **Singleton Pattern** - Database connection
- **Factory Pattern** - Model creation

---

## 📈 **PERFORMANCE OPTIMIZATIONS**

- **Lazy Loading** - Components loaded on demand
- **Memoization** - React.memo for expensive renders
- **Database Indexing** - Fast query performance
- **Caching** - LocalStorage for user data
- **Code Splitting** - Vite automatic chunking
- **Compression** - Gzip for production builds

---

## 🔍 **MONITORING & ANALYTICS**

- **Audit Logs** - User action tracking
- **Error Logging** - Console and server logs
- **Usage Statistics** - Admin dashboard metrics
- **Performance Metrics** - Response times

---

## 🚀 **DEPLOYMENT STACK**

### Recommended Production Setup:
- **Frontend**: Netlify, Vercel, or AWS S3 + CloudFront
- **Backend**: Heroku, AWS EC2, or DigitalOcean
- **Database**: PostgreSQL (upgrade from SQLite)
- **File Storage**: AWS S3 for resume uploads
- **CDN**: CloudFlare for static assets

---

## 📊 **PROJECT STATISTICS**

- **Total Lines of Code**: ~15,000+
- **Backend Python**: ~3,500 lines
- **Frontend React**: ~2,500 lines
- **ML/AI Logic**: ~1,200 lines
- **Database Models**: ~500 lines
- **API Endpoints**: 20+
- **React Components**: 15+
- **Database Tables**: 11

---

## 🎓 **LEARNING RESOURCES**

### Documentation Used:
- React Docs: https://react.dev
- Flask Docs: https://flask.palletsprojects.com
- spaCy Docs: https://spacy.io
- scikit-learn Docs: https://scikit-learn.org
- Chart.js Docs: https://www.chartjs.org

---

## 💡 **INNOVATION HIGHLIGHTS**

1. **ML-Powered Recommendations** - First-of-its-kind job role predictor
2. **AI Resume Rewriter** - Intelligent text improvement
3. **Personalized Roadmaps** - Custom learning paths
4. **Skill Gap Visualization** - Interactive charts
5. **Admin Analytics** - Deep insights dashboard

---

**Technology Stack Version**: 2.0
**Last Updated**: December 11, 2025
**Status**: Production Ready ✅
