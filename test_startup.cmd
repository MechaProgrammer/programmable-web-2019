@ECHO OFF
SETLOCAL EnableDelayedExpansion

:: add proxies here

:: Set main folder and package name variables

SET mainFolder=Sequencer
SET packageName=sequencer_package
SET gitUrl=https://github.com/Ruutimies/programmable-web-2019.git
SET gitBranch=name_branch


:: Check if mainfolder exists
:: If it does not exists, creates a new folder and virtualenvironment set in packageName
:: If it exists, pulls new version from git and upgrades it with pip upgrade

IF EXIST %mainFolder%/nul (
start cmd /k "cd %mainFolder% && %packageName%\Scripts\activate && pip install --upgrade git+%gitUrl%@%gitBranch%"
) ELSE (
start cmd /k "mkdir %mainFolder% && cd %mainFolder% && python -m venv %packageName% && %packageName%\Scripts\activate && pip install git+%gitUrl%@%gitBranch%"
)



:: start cmd /k "mkdir Branchdir && cd Branchdir && python -m venv branch_venv && branch_venv\Scripts\activate && pip install git+https://github.com/Ruutimies/programmable-web-2019.git@doc_generator"