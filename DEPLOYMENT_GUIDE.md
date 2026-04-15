# ☁️ Deployment Guide: AI SkillGap Analyzer

This guide explains how to deploy your project to the web so anyone can access it. We recommend using **Render.com** because it's free and supports both Python (Flask) and Node (React) easily.

---

## 1. Preparation

### Push to GitHub
1.  Make sure your project is pushed to a GitHub repository.
2.  Your structure should look like this in the repo:
    ```text
    /backend
      app.py
      requirements.txt
      Procfile
    /frontend
      package.json
      vite.config.js
    ```

---

## 2. Deploy Backend (Flask) on Render

1.  **Sign Up:** Go to [Render.com](https://render.com) and sign in with GitHub.
2.  **New Web Service:**
    *   Click **"New"** -> **"Web Service"**.
    *   Connect your GitHub repository.
3.  **Configure Settings:**
    *   **Name:** `skillgap-backend` (or similar)
    *   **Root Directory:** `backend` (Important!)
    *   **Environment:** `Python 3`
    *   **Build Command:** `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
    *   **Start Command:** `gunicorn app:app` (or `python app.py` if testing)
4.  **Environment Variables:**
    *   Click **"Advanced"** -> **"Add Environment Variable"**.
    *   Key: `JWT_SECRET_KEY`, Value: `your_secret_key`
    *   Key: `PYTHON_VERSION`, Value: `3.10.0` (optional)
5.  **Deploy:** Click **Create Web Service**.
    *   Render will give you a URL like: `https://skillgap-backend.onrender.com`.
    *   **Copy this URL**. You need it for the frontend.

---

## 3. Deploy Frontend (React) on Render

1.  **New Static Site:**
    *   Go to Dashboard -> **"New"** -> **"Static Site"**.
    *   Connect the **SAME** GitHub repository.
2.  **Configure Settings:**
    *   **Name:** `skillgap-frontend`
    *   **Root Directory:** `frontend`
    *   **Build Command:** `npm install && npm run build`
    *   **Publish Directory:** `dist`
3.  **Environment Variables (Important):**
    *   You need to tell the frontend where the backend is living.
    *   Add Variable: `VITE_API_BASE_URL`
    *   Value: `https://skillgap-backend.onrender.com/api` (The URL from Step 2 + `/api`).
4.  **Deploy:** Click **Create Static Site**.
    *   Render will give you a URL like: `https://skillgap-frontend.onrender.com`.
    *   **This is your live application link!**

---

## 4. Final Configuration

1.  **CORS Update (Backend):**
    *   Once your frontend is deployed, you might need to update your Backend `app.py` to allow requests from your new Frontend URL.
    *   Locate: `CORS(app)` in `app.py`.
    *   Change to: `CORS(app, resources={r"/api/*": {"origins": ["https://skillgap-frontend.onrender.com"]}})`
    *   Commit and push changes to GitHub; Render will auto-redeploy.

---

## 5. Alternative: Vercel (Frontend Only)

If you prefer Vercel for the frontend:
1.  Install Vercel CLI or use Dashboard.
2.  Import Git Repo -> Select `frontend` directory.
3.  Environment Variables: `VITE_API_BASE_URL` = `https://your-backend-url.com/api`.
4.  Deploy.

---

## 📝 Common Issues

*   **Database Reset:** On Render free tier, the SQLite database file (`skillgap.db`) might be deleted when the server restarts (ephemeral filesystem).
    *   *Solution for Production:* Switch to a **PostgreSQL** database (Render offers a free tier for this too) by changing `SQLALCHEMY_DATABASE_URI` in `app.py`.
*   **Slow Start:** Free tier services spin down after inactivity. The first request might take 50 seconds. This is normal for free plans.
