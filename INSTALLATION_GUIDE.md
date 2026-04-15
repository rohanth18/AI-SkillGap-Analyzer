# 🚀 Quick Installation Guide

## Current Location Issue
You're in the wrong directory! The upgrades are in `project_v2/backend/`, not in the root `backend/` folder.

---

## ✅ **CORRECT Installation Steps**

### **Step 1: Navigate to the correct directory**
```powershell
cd "project_v2\backend"
```

### **Step 2: Run the batch installation script**
```powershell
.\install_upgrades.bat
```

**OR** if you prefer manual installation:

```powershell
# Install dependencies one by one
pip install sentence-transformers==2.2.2
pip install textstat==0.7.3
pip install torch==2.0.1
python -m spacy download en_core_web_sm
```

---

## 🧪 **Step 3: Test the Modules**

After installation, test each module:

```powershell
# Still in project_v2\backend directory

# Test SBERT extraction
python sbert_extractor.py

# Test resume quality scorer
python resume_quality_scorer.py

# Test PDF generator
python pdf_generator.py

# Test enhanced scoring
python enhanced_scoring.py
```

---

## 📁 **Your Directory Structure**

```
Mca Main project just user module/
├── project_v2/                    ← YOU NEED TO BE HERE
│   ├── backend/
│   │   ├── sbert_extractor.py           ← New upgrade file
│   │   ├── resume_quality_scorer.py     ← New upgrade file
│   │   ├── pdf_generator.py             ← New upgrade file
│   │   ├── enhanced_scoring.py          ← New upgrade file
│   │   ├── install_upgrades.py          ← Installation script
│   │   ├── install_upgrades.bat         ← Batch file (NEW!)
│   │   └── requirements.txt             ← Updated
│   └── frontend/
└── skillgap_project/              ← Old project (not used)
```

---

## ⚡ **Quick Commands (Copy-Paste)**

### **From root directory:**
```powershell
cd "project_v2\backend"
.\install_upgrades.bat
```

### **Test everything:**
```powershell
python sbert_extractor.py
python resume_quality_scorer.py
python pdf_generator.py
python enhanced_scoring.py
```

---

## 🔍 **Troubleshooting**

### **If you see "Cannot find path":**
- You're in the wrong directory
- Run: `cd "project_v2\backend"`

### **If you see "No such file or directory":**
- The file is in `project_v2\backend\`, not in root `backend\`
- Check your current directory with: `pwd` or `cd`

### **If pip install fails:**
- Make sure you're in the virtual environment
- Check: You should see `(.venv)` in your prompt
- If not, run: `& ".venv\Scripts\Activate.ps1"`

---

## 📊 **Expected Installation Time**

- sentence-transformers: ~2-3 minutes (downloads ~500MB)
- textstat: ~10 seconds
- torch: ~3-5 minutes (downloads ~700MB)
- spaCy model: ~30 seconds

**Total**: ~5-10 minutes depending on internet speed

---

## ✅ **Success Indicators**

After successful installation, you should see:
```
SUCCESS: sentence-transformers installed
SUCCESS: textstat installed
SUCCESS: PyTorch installed
SUCCESS: spaCy model downloaded
```

---

## 🎯 **Next Steps After Installation**

1. ✅ Test all 4 modules (see commands above)
2. ⏳ Review integration guide in `UPGRADES_COMPLETE.md`
3. ⏳ Update `app.py` with new features
4. ⏳ Update database schema
5. ⏳ Update frontend components

---

**Need Help?** Check `UPGRADES_COMPLETE.md` for detailed documentation!
