@echo off
echo ============================================================
echo AI SkillGap Analyzer - Upgrade Installation
echo ============================================================
echo.
echo Installing new dependencies...
echo.

REM Install sentence-transformers
echo [1/4] Installing sentence-transformers...
pip install sentence-transformers==2.2.2
if %errorlevel% neq 0 (
    echo ERROR: Failed to install sentence-transformers
    pause
    exit /b 1
)
echo SUCCESS: sentence-transformers installed
echo.

REM Install textstat
echo [2/4] Installing textstat...
pip install textstat==0.7.3
if %errorlevel% neq 0 (
    echo ERROR: Failed to install textstat
    pause
    exit /b 1
)
echo SUCCESS: textstat installed
echo.

REM Install torch
echo [3/4] Installing PyTorch...
pip install torch==2.0.1
if %errorlevel% neq 0 (
    echo ERROR: Failed to install torch
    pause
    exit /b 1
)
echo SUCCESS: PyTorch installed
echo.

REM Download spaCy model
echo [4/4] Downloading spaCy English model...
python -m spacy download en_core_web_sm
if %errorlevel% neq 0 (
    echo ERROR: Failed to download spaCy model
    pause
    exit /b 1
)
echo SUCCESS: spaCy model downloaded
echo.

echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Test the modules:
echo    python sbert_extractor.py
echo    python resume_quality_scorer.py
echo    python pdf_generator.py
echo    python enhanced_scoring.py
echo.
echo 2. Integrate into app.py
echo.
echo 3. Update database schema
echo.
echo 4. Update frontend components
echo.
echo ============================================================
pause
