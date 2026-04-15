@echo off
echo ===================================================
echo   CLEANING PROJECT FOR TRANSFER/BACKUP
echo ===================================================
echo.
echo This script removes system-specific folders (envs, node_modules)
echo so the project can be safely copied to another computer.
echo.
echo WARNING: This will delete 'env', 'venv', 'venv_new', and 'node_modules'.
echo You will need to re-install dependencies to run it here again.
echo.
pause

echo.
echo [1/4] Removing Backend Cache (__pycache__)...
for /d /r "backend" %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

echo.
echo [2/4] Removing Backend Virtual Environments...
if exist "backend\env" (
    echo    - Removing backend\env...
    rd /s /q "backend\env"
)
if exist "backend\venv" (
    echo    - Removing backend\venv...
    rd /s /q "backend\venv"
)
if exist "backend\venv_new" (
    echo    - Removing backend\venv_new...
    rd /s /q "backend\venv_new"
)

echo.
echo [3/4] Removing Frontend Node Modules...
if exist "frontend\node_modules" (
    echo    - Removing frontend\node_modules...
    call cmd /c "rmdir /s /q frontend\node_modules"
)

echo.
echo [4/4] Done!
echo.
echo The project is now clean. You can zip the 'project_v2' folder
echo and extract it on the new computer.
echo.
echo REMEMBER: On the new computer, you must:
echo 1. backend: python -m venv venv, activate, pip install -r requirements.txt
echo 2. backend: python -m spacy download en_core_web_sm
echo 3. frontend: npm install
echo.
pause
