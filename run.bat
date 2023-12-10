@echo off
CLS
ECHO.

:init
setlocal DisableDelayedExpansion
set "batchPath=%~0"
for %%k in (%0) do set batchName=%%~nk
set "vbsGetPrivileges=%temp%\OEgetPriv_%batchName%.vbs"
setlocal EnableDelayedExpansion

:checkPrivileges
NET FILE 1>NUL 2>NUL
if '%errorlevel%' == '0' ( goto gotPrivileges ) else ( goto getPrivileges )

:getPrivileges
if '%1'=='ELEV' (echo ELEV & shift /1 & goto gotPrivileges)

ECHO Set UAC = CreateObject^("Shell.Application"^) > "%vbsGetPrivileges%"
ECHO args = "ELEV " >> "%vbsGetPrivileges%"
ECHO For Each strArg in WScript.Arguments >> "%vbsGetPrivileges%"
ECHO args = args ^& strArg ^& " " >> "%vbsGetPrivileges%"
ECHO Next >> "%vbsGetPrivileges%"
ECHO UAC.ShellExecute "!batchPath!", args, "", "runas", 1 >> "%vbsGetPrivileges%"
"%SystemRoot%\System32\WScript.exe" "%vbsGetPrivileges%" %*
exit /B

:gotPrivileges
setlocal & pushd .
cd /d %~dp0
if '%1'=='ELEV' (del "%vbsGetPrivileges%" 1>nul 2>nul & shift /1)

title Setup
set PATH=%PATH%;%~dp0

if not exist bot-env (
    echo 'bot-env' folder not found. Installing...
    python -m venv bot-env
    call .\bot-env\Scripts\activate.bat
    pip install curl_cffi
    pip install fake_useragent
    pip install httpx
    pip install asyncio
    pip install python-dotenv
    pip install pyYAML
    pip install requests
    pip install flask
    pip install bardapi

    pip install -U discord.py-self
    echo Installed.
) else (
    call .\bot-env\Scripts\activate.bat
)

echo Starting bot...
python main.py
pause
cmd /k
