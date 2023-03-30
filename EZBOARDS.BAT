@ECHO OFF
ECHO [33m-------------------------------------------------------------------------------
ECHO [33mEZBoards - Instant single-click briefing to kneeboards conversion for Falcon BMS.
ECHO [33mBy "Logic". See ReadMe.txt for documentation.
ECHO [33m-------------------------------------------------------------------------------[0m

REM /// Get BASEDIR and PILOTBIN from Registry.
REM /// Note: This part will need to be updated in future versions of BMS.
SET REGPATH="HKLM\SOFTWARE\WOW6432Node\Benchmark Sims\Falcon BMS 4.37"

REM /// delims is a TAB followed by a space
FOR /F "tokens=2* delims=	 " %%A IN ('REG QUERY %REGPATH% /v baseDir') DO SET BASEDIR=%%B
ECHO BASEDIR=%BASEDIR%

FOR /F "tokens=2* delims=	 " %%A IN ('REG QUERY %REGPATH% /v PilotCallsign') DO SET PILOTBIN=%%B
ECHO PILOTBIN=%PILOTBIN%

FOR /F "tokens=2* delims=	 " %%A IN ('REG QUERY %REGPATH% /v curTheater') DO SET THEATER=%%B
ECHO THEATER=%THEATER%

REM /// Convert the REG_BINARY callsign from Registry to a string
SETLOCAL EnableDelayedExpansion
ECHO !PILOTBIN!> temp.hex
CALL certutil -decodehex temp.hex str.txt >nul
ENDLOCAL
SET /p PILOTCALLSIGN=<str.txt
( DEL temp.hex & DEL str.txt )>nul

ECHO PILOTCALLSIGN=%PILOTCALLSIGN%

REM /// Note: Does not take into account "Falcon BMS.cfg" g_sBriefingsDirectory!
SET BRIEFINGTXT="%BASEDIR%\User\Briefings\briefing.txt"
ECHO BRIEFINGTXT=%BRIEFINGTXT%

IF NOT EXIST %BRIEFINGTXT% (
  ECHO [91mCould not find briefing.txt file. Did you press PRINT?[0m
  GOTO ERROR
)

SET CALLSIGNINI="%BASEDIR%\User\Config\%PILOTCALLSIGN%.ini"
ECHO CALLSIGNINI=%CALLSIGNINI%

IF NOT EXIST %CALLSIGNINI% (
  ECHO [91mCould not find callsign DTC file. You won't get target steerpoints.[0m
  SET CALLSIGNINI=
)

taskkill /im openkneeboardapp.exe
REM /// Step 1: Generate HTML version of briefing data to briefing.html .
ECHO [33mGenerating HTML version of briefing data to briefing.html.[0m
bin\xbrief.exe %BRIEFINGTXT% %CALLSIGNINI% > briefing.html
IF %ERRORLEVEL% NEQ 0 GOTO ERROR
ECHO [32mOk.[0m

REM /// If you don't need the kneeboards but just want to have the HTML,
REM /// you may as well exit here by uncommenting the following line.
REM GOTO SUCCESS

REM /// Step 1.5: Pyboard to add more html
ECHO [33mPyboards to add more HTML.[0m
bin\pyboard.exe -f briefing.html -b %BRIEFINGTXT% -j py\airfields.json
ECHO [32mOk.[0m

REM /// Step 2: Render the HTML file to briefing.png image.
ECHO [33mRendering HTML to briefing.png image.[0m
bin\wkhtmltoimage.exe --width 2048 --height 1554 --disable-smart-width --enable-local-file-access briefing.html briefing.png
IF %ERRORLEVEL% NEQ 0 GOTO ERROR
ECHO [32mOk.[0m

REM /// Step 3: Convert the briefing.png image file to a DDS texture file briefing.DDS .
ECHO [33mConverting the briefing.png image file to a DDS texture file.[0m
bin\texconv.exe -f DXT1 -m 1 -y -h 2048 briefing.png
IF NOT EXIST briefing.DDS GOTO ERROR
ECHO [32mOk.[0m

REM /// Step 4: Copy the DDS texture file to the kneeboard texture file in the target path.
REM /// Kneeboards textures are in files 7982.dds and following.
REM /// One file holds a left+right double page for the kneeboards.
SET TARGETFILE=7982.dds

REM /// Path to theater dds files. Default to Korea KTO.
SET THEATERPATH=%BASEDIR%\Data\TerrData\Objects\KoreaObj

REM /// Looks into the Theaters.txt and tries to match %THEATER% with one on the list,
REM /// Then returns the partial path of the objects folder containing the .dss files.
FOR /F "usebackq tokens=1-2 delims=," %%G IN (Theaters.txt) DO IF %%G == "%THEATER%" SET THEATERPATH=%BASEDIR%%%H

SET TARGET="%THEATERPATH%\%TARGETFILE%"
ECHO TARGET=%TARGET%
IF NOT EXIST %TARGET% (
  ECHO [91mTarget file doesn't exist. Check theater.[0m
  GOTO ERROR
)

REM /// Make a backup if not already done.
SET BACKUPFILE=%TARGETFILE%.bak
SET BACKUPTARGET="%THEATERPATH%\%BACKUPFILE%"
IF NOT EXIST %BACKUPTARGET% (
  ECHO [33mMaking a backup copy of %TARGETFILE% to %BACKUPTARGET%.[0m
  COPY /y %TARGET% %BACKUPTARGET%
)

REM /// Do the actual copy.
ECHO [33mCopying the result to %TARGET%.[0m
COPY /y briefing.DDS %TARGET%
IF %ERRORLEVEL% NEQ 0 GOTO ERROR
ECHO [32mOk.[0m

REM /// Successful exit.
:SUCCESS
ECHO [42m[97mSUCCESS.[0m
IF "%~1"=="" PAUSE
cd "C:\Program Files\OpenKneeboard\bin"
start OpenKneeboardApp.exe
EXIT 0

REM /// Exit on error.
:ERROR
ECHO [41m[97m### ERROR ###[0m
IF "%~1"=="" PAUSE
EXIT 1
