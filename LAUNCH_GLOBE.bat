@echo off
echo ========================================
echo   LAUNCHING GLOBAL RISK PREDICTOR
echo ========================================
echo.
echo Starting API server...
start /B python run_api.py
echo.
echo Waiting for server to start...
timeout /t 5 /nobreak >nul
echo.
echo Opening interactive globe dashboard...
start global_risk_dashboard.html
echo.
echo ========================================
echo   DASHBOARD LAUNCHED!
echo ========================================
echo.
echo The globe is now running with live data!
echo.
echo API Server: http://localhost:8000
echo Interactive Docs: http://localhost:8000/docs
echo.
echo Press any key to stop the server...
pause >nul
taskkill /F /IM python.exe

