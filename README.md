# AI SkillGap Analyzer

An advanced Resume Analysis and Skill Gap Recommendation System.

## Features

### User
- **Register/Login/Logout**
- **Upload Resume** (PDF/Text)
- **Automatic Skill Extraction** using `spaCy` (PhraseMatcher) and `fuzzywuzzy`
- **GitHub Profile Analysis** (Extract skills from public repos)
- **Manual Skill Entry**
- **Confidence Scoring** based on weighted sources
- **Skill Gap Visualization** (Interactive Radar/Bar Charts)
- **Recommendations** (YouTube Tutorials for missing skills)
- **Dashboard** with progress tracking

### Admin
- **Admin Dashboard** with global analytics
- **Role Management** (CRUD Job roles & skills)
- **CSV Import** to seed database with IT job roles
- **User Analytics**

## Tech Stack
- **Backend**: Flask, SQLAlchemy (SQLite), spaCy, FuzzyWuzzy
- **Frontend**: React, Vite, Chart.js, Glassmorphism CSS
- **Database**: SQLite

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Node.js 16+

### 2. Backend Setup
```sh
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Initialize DB (First run)
# The app automatically creates tables on start.
# To Seed the Job Roles from CSV, login as Admin and click "Seed from CSV"
# OR use the API endpoint POST /api/seed
```

### 3. Frontend Setup
```sh
cd frontend
npm install
npm run dev
```

### 4. Running the App
1. Start Backend:
   ```sh
   cd backend
   python app.py
   ```
   Runs on http://127.0.0.1:5000

2. Start Frontend:
   ```sh
   cd frontend
   npm run dev
   ```
   Runs on http://localhost:5173

3. Access the App:
   Open http://localhost:5173 in your browser.

## Default Admin
Since there is no pre-seeded admin, the first registered user can be treated as Admin if you modify the DB or use the registration API with `is_admin: true` payload (via Postman). 
OR, for simplicity in this demo, you can modify `app.py` or manually update the database.
Alternatively, the `seed` endpoint might be accessible.

## Project Structure
- `backend/`: Flask API & AI Logic
- `frontend/`: React UI
- `backend/data/`: Datasets
