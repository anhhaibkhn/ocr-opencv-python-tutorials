@echo off
TITLE miniforge
%windir%\system32\cmd.exe /K "C:\ProgramData\miniforge3\Scripts\activate.bat C:\ProgramData\miniforge3 && C:\Users\nguyenngochai\trial_projects\scripts_files\main.bat"

rem @echo off
rem start "miniforge3" "C:\Users\YOUR_USER_NAME\trial_projects\miniforge.lnk"
rem set CONDAPATH=C:\ProgramData\miniforge3\Scripts
rem set ENVNAME=my_conda_env
rem call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
