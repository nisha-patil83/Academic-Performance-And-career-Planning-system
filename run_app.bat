@echo off
title EduPlan AI - Academic & Career Planning System
echo ========================================================
echo  Launching EduPlan AI: Academic & Career Planning System
echo ========================================================
echo.
echo Installing / Verifying dependencies...
pip install -r requirements.txt
echo.
echo ========================================================
echo  Streamlit will start on:
echo  1. Local (Laptop):  http://localhost:8501
echo  2. Mobile / Network: Check the "Network URL" displayed below!
echo     (Ensure your phone is on the same Wi-Fi/Hotspot)
echo ========================================================
echo.
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
pause
