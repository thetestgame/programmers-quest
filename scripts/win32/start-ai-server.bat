@echo off
title PQ - AI

rem Define some constants for our AI server:
set MAX_CHANNELS=999999
set STATE_SERVER_CHANNEL=4002
set ASTRON_IP=127.0.0.1:7100
set EVENTLOGGER_IP=127.0.0.1:7198
set DISTRICT_NAME=Hacker Valley
set BASE_CHANNEL=1000000

echo ===============================
echo Starting Programmer's Quest AI server...
echo Shard name: %DISTRICT_NAME%
echo Base channel: %BASE_CHANNEL%
echo Max channels: %MAX_CHANNELS%
echo State Server: %STATE_SERVER_CHANNEL%
echo Astron IP: %ASTRON_IP%
echo Event Logger IP: %EVENTLOGGER_IP%
echo ===============================

cd ../../
:main
	python -m quest.ai
    
	pause
	goto main
