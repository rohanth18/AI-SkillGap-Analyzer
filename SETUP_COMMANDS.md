# 🚀 Complete Setup Commands for Running Project on Another System

## Prerequisites
- **Python 3.9+** installed
- **Node.js 16+** installed
- **Git** (optional, for cloning)

---

## 📋 Step-by-Step Setup Instructions

### **Step 1: Copy the Project**

Transfer the entire `project_v2` folder to the new system, or if using Git:

```bash
# If you have it in a repository
git clone <your-repository-url>
cd project_v2
```

---

### **Step 2: Backend Setup**

#### **2.1 Navigate to Backend Directory**
```bash
cd project_v2/backend
```

#### **2.2 Create Virtual Environment**

**On Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### **2.3 Install Python Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### **2.4 Download spaCy Language Model**
```bash
python -m spacy download en_core_web_sm
```

#### **2.5 Install Additional Upgrades (Optional but Recommended)**
```bash
pip install sentence-transformers==2.2.2
pip install textstat==0.7.3
pip install torch==2.0.1
```

#### **2.6 Initialize Database**
The database will be created automatically when you first run the app.

---

### **Step 3: Frontend Setup**

#### **3.1 Open New Terminal and Navigate to Frontend**
```bash
cd project_v2/frontend
```

#### **3.2 Install Node Dependencies**
```bash
npm install
```

---

### **Step 4: Running the Application**

You need **TWO terminals** running simultaneously:

#### **Terminal 1 - Backend Server**

```bash
# Navigate to backend folder
cd project_v2/backend

# Activate virtual environment (if not already activated)
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Run the Flask server
python app.py
```

**Expected Output:**
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

#### **Terminal 2 - Frontend Development Server**

```bash
# Navigate to frontend folder
cd project_v2/frontend

# Run the Vite dev server
npm run dev
```

**Expected Output:**
```
VITE v4.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

---

### **Step 5: Access the Application**

Open your browser and go to:
```
http://localhost:5173
```

---

## 🔧 Quick Copy-Paste Commands

### **Windows (PowerShell)**

```powershell
# Backend Setup
cd project_v2\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# In a NEW terminal - Frontend Setup
cd project_v2\frontend
npm install

# Run Backend (Terminal 1)
cd project_v2\backend
.\venv\Scripts\Activate.ps1
python app.py

# Run Frontend (Terminal 2)
cd project_v2\frontend
npm run dev
```

### **Mac/Linux (Bash)**

```bash
# Backend Setup
cd project_v2/backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# In a NEW terminal - Frontend Setup
cd project_v2/frontend
npm install

# Run Backend (Terminal 1)
cd project_v2/backend
source venv/bin/activate
python app.py

# Run Frontend (Terminal 2)
cd project_v2/frontend
npm run dev
```

---

## 👤 First Time Login

### **Create Admin Account:**

1. Go to `http://localhost:5173`
2. Click **"Register"**
3. Fill in your details:
   - Name: Your Name
   - Email: admin@example.com
   - Password: your_password
4. Click **Register**

**Note:** The first registered user automatically becomes an admin!

### **Seed Database with Job Roles:**

After logging in as admin:
1. Go to Admin Dashboard
2. Click **"Seed from CSV"** button
   
OR use the API directly:
```bash
curl -X POST http://127.0.0.1:5000/api/seed
```

---

## 🐛 Troubleshooting

### **Issue: Python not found**
```bash
# Check Python installation
python --version
# or
python3 --version

# If not installed, download from: https://www.python.org/downloads/
```

### **Issue: Node/npm not found**
```bash
# Check Node installation
node --version
npm --version

# If not installed, download from: https://nodejs.org/
```

### **Issue: PowerShell script execution disabled (Windows)**
```powershell
# Run PowerShell as Administrator and execute:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or use this alternative to activate venv:
venv\Scripts\python.exe app.py
```

### **Issue: Port already in use**

**Backend (Port 5000):**
```bash
# Windows - Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

**Frontend (Port 5173):**
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5173 | xargs kill -9
```

### **Issue: Module not found errors**
```bash
# Make sure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
project_v2/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── venv/                  # Virtual environment (created)
│   ├── instance/              # Database folder (auto-created)
│   │   └── skillgap.db       # SQLite database
│   ├── uploads/               # Resume uploads folder
│   ├── data/                  # CSV data files
│   └── models/                # ML models
│
├── frontend/
│   ├── src/                   # React source code
│   ├── package.json           # Node dependencies
│   ├── node_modules/          # Node packages (created)
│   └── vite.config.js         # Vite configuration
│
└── README.md                  # Project documentation
```

---

## 🎯 URLs Reference

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | React UI |
| Backend API | http://127.0.0.1:5000 | Flask REST API |
| Admin Dashboard | http://localhost:5173/admin | Admin panel |

---

## 📝 Default Credentials

- **First user registered = Admin automatically**
- No pre-configured credentials
- Create your own account on first run

---

## ✅ Verification Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 16+ installed
- [ ] Backend dependencies installed
- [ ] spaCy model downloaded
- [ ] Frontend dependencies installed
- [ ] Backend running on port 5000
- [ ] Frontend running on port 5173
- [ ] Can access http://localhost:5173
- [ ] Can register a new user
- [ ] Database seeded with job roles

---

## 🆘 Need Help?

Check these files for more information:
- `README.md` - General project overview
- `INSTALLATION_GUIDE.md` - Detailed installation steps
- `TECHNOLOGY_STACK.md` - Tech stack details
- `ADVANCED_FEATURES_GUIDE.md` - Advanced features documentation

---

**Happy Coding! 🚀**
