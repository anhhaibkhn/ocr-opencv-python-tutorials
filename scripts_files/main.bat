@echo OFF
ECHO Executing conda commands
rem How to run a Python script in a given conda environment from a batch file.

rem It doesn't require:
rem - conda to be in the PATH
rem - cmd.exe to be initialized with conda init

ECHO Define here the path to your conda installation
rem start "miniforge3" "C:\Users\YOUR_USER_NAME\trial_projects\miniforge.lnk"
set CONDAPATH=C:\ProgramData\miniforge3

ECHO Define here the name of the environment
set ENVNAME=my_conda_env

rem The following command activates the base environment.
rem C:\ProgramData\Miniconda3\Scripts\activate.bat C:\ProgramData\Miniconda3
rem if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)

ECHO Activate the conda environment
rem Using call is required here, see: https://stackoverflow.com/questions/24678144/conda-environments-and-bat-files
call %CONDAPATH%\Scripts\activate.bat %ENVNAME%
cd trial_projects

rem Run a python script in that environment
rem python script.py

rem Deactivate the environment
rem call conda deactivate

rem If conda is directly available from the command line then the following code works.
rem call activate someenv
rem python script.py
rem conda deactivate

rem One could also use the conda run command
rem conda run -n someenv python script.py