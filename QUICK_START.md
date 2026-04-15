# 🚀 Quick Start Guide - AI SkillGap Analyzer

## ⚡ Super Quick Commands (Copy & Paste)

### Windows - One Time Setup
```powershell
# Navigate to project folder
cd project_v2\backend

# Create virtual environment and install Python packages
py -m venv venv_new
venv_new\Scripts\python.exe -m pip install Flask==2.3.2 Flask-SQLAlchemy==3.0.5 Flask-CORS==4.0.0 Flask-Migrate==4.0.4 Flask-JWT-Extended==4.5.2 Werkzeug==2.3.6 spacy==3.7.2 fuzzywuzzy==0.18.0 requests==2.31.0 PyPDF2==3.0.1 scikit-learn
venv_new\Scripts\python.exe -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

# Install frontend packages
cd ..\frontend
npm install
```

### Windows - Run Project (Every Time)

**Terminal 1 - Backend:**
```powershell
cd project_v2\backend
venv_new\Scripts\python.exe app.py
```

**Terminal 2 - Frontend:**
```powershell
cd project_v2\frontend
npm run dev
```

**Then open:** http://localhost:5173

---

### Mac/Linux - One Time Setup
```bash
# Navigate to project folder
cd project_v2/backend

# Create virtual environment and install Python packages
python3 -m venv venv_new
source venv_new/bin/activate
pip install Flask==2.3.2 Flask-SQLAlchemy==3.0.5 Flask-CORS==4.0.0 Flask-Migrate==4.0.4 Flask-JWT-Extended==4.5.2 Werkzeug==2.3.6 spacy==3.7.2 fuzzywuzzy==0.18.0 requests==2.31.0 PyPDF2==3.0.1 scikit-learn
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl

# Install frontend packages
cd ../frontend
npm install
```

### Mac/Linux - Run Project (Every Time)

**Terminal 1 - Backend:**
```bash
cd project_v2/backend
source venv_new/bin/activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd project_v2/frontend
npm run dev
```

**Then open:** http://localhost:5173

---

## 📋 Prerequisites

Install these first:
- **Python 3.9+** → https://www.python.org/downloads/
- **Node.js 16+** → https://nodejs.org/

---

## ✅ Success Indicators

**Backend Running:**
- Terminal shows: `Running on http://127.0.0.1:5000`

**Frontend Running:**
- Terminal shows: `Local: http://localhost:5173/`

**Application Working:**
- Browser opens http://localhost:5173
- You see the login/register page

---

## 🛑 To Stop

Press `Ctrl+C` in both terminal windows

---

## 🎯 First Time Usage

1. Open http://localhost:5173
2. Click "Register"
3. Create account (first user = admin)
4. Login
5. Start using the app!

---

## 📁 What to Transfer to New Computer

**Transfer:**
- ✅ `project_v2/` folder (entire folder)
- ✅ This guide

**Don't Transfer:**
- ❌ `venv_new/` folder
- ❌ `node_modules/` folder
- ❌ `__pycache__/` folders

---

## 🔧 Common Issues

**"Python not found"**
→ Install Python and check "Add to PATH"

**"npm not found"**
→ Install Node.js and restart terminal

**Port already in use**
→ Close other apps using ports 5000 or 5173

---

**For detailed instructions, see:** `RUN_PROJECT_COMMANDS.txt`
