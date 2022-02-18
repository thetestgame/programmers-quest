Programmer's Quest!
===================

Programmer's Quest! The open source Python 3 MMO showcasing the power of Panda3D, Distributed Objects, and the Astron server built by a industry professional. This project is still a work in progress.

### Dependencies

* panda3d
* panda3d-blend2bam (development)
* sentry_sdk
* easygui
* gitpython (development)

## Preparing an Environment

To create a new working environment for Quest run the following commands from the directory you would like the repository to be placed.

```
git clone --recurse-submodules https://github.com/thetestgame/programmers-quest quest-src
cd quest-src
python -m pip install -r quest/docs/requirements.dev.txt
```

## Development Build

To run a development client build from source run the following command in the repository root
```
python -m quest.client
```

This will boot the game with paths defined for the source directory as well as provide useful developer hotkeys.
| Hotkey |           Description           |
|--------|---------------------------------|
|   F1   | Toggles The ShowBase OOBE mode  |
|   F2   | Reloads the applications source |

## Project Commands

The Quest MMO project has numerous commands built in to assist in the development and maintence of the application. A quick summary
of the commonly used commands is as follows.

|  Command   | Description |
|------------|-------------|
| build_apps |             |
| bdist_apps |             |
