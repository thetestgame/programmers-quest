PRC Documentation For Programmer's Quest
========================================

This document outlines the specifics of the Programmer's Quest MMO module's Panda3d Runtime Configuration files. 

## File Types

## Personal PRC file

Developers can create a personal prc file for setting values specific to their environment without risk of accidentally pushing back to source control/public builds. To setup a personal prc file create a new file in the root of the repository called ``personal.prc``. This fille will automatically be ignored by git and loaded by the development version of theProgrammer's Quest MMO Client/Server.

## All PRC Options

This section outlines all available PRC options specific to the Programmer's Quest source base. This does not outline the options available to the Panda3D game engine its self. Those options can be found <a href="https://docs.panda3d.org/1.10/python/programming/configuration/list-of-all-config-variables">here</a>

|      Option Name         | Description |
|--------------------------|-------------|
|     flow-fade-time       |             |
|   flow-initial-stage     |             |
|     time-runnables       |             |
|  want-threaded-tilemap   |             |
| want-threaded-world-cull |             |