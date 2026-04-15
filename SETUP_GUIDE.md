# 🚀 Project Setup Guide

Follow these instructions to set up and run the AI SkillGap Analyzer project on a new computer.

---

## 📋 **Prerequisites**

Ensure you have the following installed on your system:
1.  **Node.js & npm** (v18 or higher) - [Download](https://nodejs.org/)
2.  **Python** (v3.10 or higher) - [Download](https://python.org/)
3.  **Git** (optional but recommended) - [Download](https://git-scm.com/)

---

## 📂 **1. Backend Setup (Flask API)**

Open a terminal (Command Prompt or PowerShell) and navigate to the project root folder.

### **Step 1: Navigate to backend directory**
```bash
cd project_v2/backend
```

### **Step 2: Create a virtual environment**
```bash
# Windows
python -m venv venv_new

# Mac/Linux
python3 -m venv venv_new
```

### **Step 3: Activate the virtual environment**
```bash
# Windows
.\venv_new\Scripts\activate

# Mac/Linux
source venv_new/bin/activate
```
*(You should see `(venv_new)` appear at the start of your terminal line)*

### **Step 4: Install dependencies**
```bash
pip install -r requirements.txt
```
*(If `requirements.txt` is missing, install manually: `pip install flask flask-cors flask-sqlalchemy flask-migrate flask-jwt-extended spacy fuzzywuzzy python-Levenshtein PyPDF2`)*

### **Step 5: Download spaCy language model**
```bash
python -m spacy download en_core_web_sm
```

### **Step 6: Initialize Database**
Run the application once to create the database file `instance/skillgap.db`.
```bash
python app.py
```
*(You can stop it with `Ctrl+C` after verified starting)*

### **Step 7: Seed Database (Optional)**
Populate the database with initial job roles and an admin user.
```bash
python seed_db.py
```

### **Step 8: Run the Backend Server**
```bash
python app.py
```
*The backend will start at `http://127.0.0.1:5000`*

---

## 💻 **2. Frontend Setup (React + Vite)**

Open a **new** terminal window (keep the backend running in the first one).

### **Step 1: Navigate to frontend directory**
```bash
cd project_v2/frontend
```

### **Step 2: Install dependencies**
```bash
npm install
```

### **Step 3: Run the Frontend**
```bash
npm run dev
```
*The frontend will start at `http://localhost:5173`*

---

## 🔗 **3. Access the Application**

1.  Open your browser (Chrome/Edge/Firefox).
2.  Go to: **`http://localhost:5173`**

---

## 🛡️ **Admin Credentials (Default)**

If you ran `seed_db.py`, the default admin user is:
- **Email:** `admin@skillgap.com`
- **Password:** `Admin@123`

---

## 🛠️ **Troubleshooting**

-   **"Python not found"**: Ensure Python is added to your system PATH during installation.
-   **"pip not recognized"**: Ensure you activated the virtual environment (`Step 3`).
-   **"npm not recognized"**: Ensure Node.js is installed and PATH is updated (restart terminal after install).
-   **Database Errors**: Delete the `instance` folder in `backend` and re-run `python app.py` and `python seed_db.py`.
-   **Port in use**: If port 5000 or 5173 is taken, close other apps or change the port in `app.py` or `vite.config.js`.

---

## 📝 **Summary of Commands**

**Backend (Terminal 1):**
```bash
cd project_v2/backend
.\venv_new\Scripts\activate
python app.py
```

**Frontend (Terminal 2):**
```bash
cd project_v2/frontend
npm run dev
```
