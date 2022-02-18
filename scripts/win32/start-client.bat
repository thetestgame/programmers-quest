@echo off
title PQ - Client

set CA_HOST=127.0.0.1
set /P PQ_PLAYTOKEN=Username: 
echo.

echo ===============================
echo Starting Programmer's Quest...
echo Username: %PQ_PLAYTOKEN%
echo Gameserver: %CA_HOST%
echo ===============================

cd ../../
:main
    python -m quest.client

    pause
    goto main