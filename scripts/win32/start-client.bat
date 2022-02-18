@echo off
title PQ - Client

set CA_HOST=127.0.0.1
set /P PQ_EMAIL=Email: 
set /P PQ_PASSWORD=Password: 
echo.

echo ===============================
echo Starting Programmer's Quest...
echo Email: %PQ_EMAIL%
echo Password: Secret
echo Gameserver: %CA_HOST%
echo ===============================

cd ../../
:main
    python -m quest.client

    pause
    goto main