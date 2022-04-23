@echo off
title PQ - Astron

cd "../../astron"
:main
    astrond --loglevel trace --pretty
    
    pause
    goto :main