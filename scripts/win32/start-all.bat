rem Starts the Programmer's Quest local server environment in multiple tabs using the Windows Terminal application. 
rem If you do not have the new Windows terminal application installed this script will fall back to starting several batch windows. 
rem If you are on Windows 11 the new terminal is installed by default.

wt >nul 2>&1 && (
    wt -w 0 -d . -p "Windows PowerShell" start-astron-cluster.bat init
    wt -w 0 -d . -p "Windows PowerShell" start-uberdog-server.bat init
    wt -w 0 -d . -p "Windows PowerShell" start-ai-server.bat init
    wt -w 0 -d . -p "Windows PowerShell" start-client.bat init
) || (
    start start-astron-cluster.bat
    start start-uberdog-server.bat
    start start-ai-server.bat
    start start-client.bat
)

exit 0