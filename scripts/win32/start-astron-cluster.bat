@echo off
title PQ - Astron

cd "../../astron"
:main
    astrond --loglevel info --pretty
    
    pause
    goto :main