# Project Portability Analysis

This report outlines why the project might not be running on other computers and lists the necessary steps to fix it.

## 1. Non-Portable Environmental Folders (CRITICAL)
The following directories contain system-specific files and absolute paths that **cannot** be transferred to another computer:
- `backend/env/`
- `backend/venv_new/`
- `backend/__pycache__/`
- `frontend/node_modules/`

**Why this fails:** 
Python virtual environments (`env`, `venv`) contain hardcoded paths to the Python interpreter on the *original* machine (e.g., `d:\project_v2\...`). On a new PC, these paths are invalid, causing immediate crashes. Similarly, `node_modules` may contain compiled binaries specific to the OS version.

**Solution:** 
You must **DELETE** these folders before copying the project, or simply ignoring them. On the new PC, you must recreate them (install dependencies).

## 2. Missing NLP Models
The backend uses the `en_core_web_sm` model for SpaCy.
- `pip install -r requirements.txt` installs the library, but **NOT** the model.
- If the new PC is offline or has network issues, the app will fail to start.

**Solution:**
On the new PC, after installing requirements, you must run:
```bash
python -m spacy download en_core_web_sm
```
*Alternatively, rely on the `install_upgrades.py` script if it handles this, but manual verifiction is safer.*

## 3. Database & Uploads
- `backend/instance/skillgap.db`: Contains user data. It is portable (SQLAlchemy/SQLite), but if you want a "fresh" install, you should delete this file on the new PC.
- `backend/uploads/`: Contains uploaded resumes. If you copy the DB, you MUST copy this folder too, or the DB will point to non-existent files.

## Summary Checklist for New PC
1. **Clean**: Remove `env`, `venv_new`, `node_modules` before copying.
2. **Install Python**: Ensure Python 3.10+ is installed.
3. **Install Node**: Ensure Node.js 18+ is installed.
4. **Setup Backend**:
   ```bash
   cd backend
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   python app.py
   ```
5. **Setup Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
