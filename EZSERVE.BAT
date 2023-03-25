@ECHO OFF
ECHO [96m---------------------------------------------------------------------------
ECHO [96mEZServe - This is the HTTP server application for EZBoards.
ECHO [96mIt will serve the contents of this folder over the network
ECHO [96m so that you may view the briefing on a web browser from other devices.
ECHO [96m---------------------------------------------------------------------------[0m

ECHO This computer's IP addresses as reported by ipconfig are:
ipconfig | findstr "IPv"

ECHO Use [96mhttp://[address]:8080/briefing.html[0m in a web browser on another device to view the briefing file there.

ECHO This server will stop if you close this window.

REM /// Now call a standalone http server to serve the file
CALL bin\onehttpd-0.8.exe .
