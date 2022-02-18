@echo off
title PQ - UberDOG

rem Define some constants for our UberDOG server:
set MAX_CHANNELS=999999
set STATE_SERVER_CHANNEL=4002
set ASTRON_IP=127.0.0.1:7100
set EVENTLOGGER_IP=127.0.0.1:7198
set BASE_CHANNEL=1000000

echo ===============================
echo Starting Programmer's Quest UD server...
echo Base channel: %BASE_CHANNEL%
echo Max channels: %MAX_CHANNELS%
echo State Server: %STATE_SERVER_CHANNEL%
echo Astron IP: %ASTRON_IP%
echo Event Logger IP: %EVENTLOGGER_IP%
echo ===============================

cd ../../
:main
	python -m quest.uberdog
    
	pause
	goto main
