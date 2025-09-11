@echo off
cls
color 0A
echo ================================================================================
echo                    PANEL FLUTTER ANALYSIS GUI
echo              NASTRAN AEROELASTICITY SUITE - FINAL VERSION
echo ================================================================================
echo.
echo Launching the GUI application...
echo.
echo Features:
echo   - Complete GUI interface with all panels
echo   - NASTRAN BDF file generation  
echo   - Multi-solver framework (Piston Theory, Doublet Lattice, NASTRAN)
echo   - File saving and loading
echo   - Full flutter analysis capabilities
echo.
echo --------------------------------------------------------------------------------
echo.

REM Try the main launcher first
".venv\Scripts\python.exe" GUI_FINAL.py
if %errorlevel% equ 0 goto :success

REM If that fails, try the backup launcher
echo.
echo Trying backup launcher...
".venv\Scripts\python.exe" GUI_LAUNCHER_FINAL.py
if %errorlevel% equ 0 goto :success

REM If that fails, try direct launch
echo.
echo Trying direct launch...
".venv\Scripts\python.exe" launch_gui.py
if %errorlevel% equ 0 goto :success

REM If all fail, show error
echo.
echo ================================================================================
echo ERROR: Could not start the GUI
echo.
echo Please try running manually:
echo   python GUI_FINAL.py
echo.
echo Or check that all dependencies are installed:
echo   pip install numpy matplotlib pandas
echo ================================================================================
pause
goto :end

:success
echo.
echo ================================================================================
echo GUI closed successfully
echo ================================================================================
echo.
pause

:end