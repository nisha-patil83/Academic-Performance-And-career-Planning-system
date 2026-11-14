Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " Launching EduPlan AI: Academic & Career Planning System" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan

Write-Host "`nChecking & installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "`nStarting Streamlit web dashboard..." -ForegroundColor Green
streamlit run app.py
