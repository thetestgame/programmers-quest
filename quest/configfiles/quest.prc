{##########################################################################}
{# quest.prc                                                              #}
{#                                                                        #}
{# This file defines the template to auto-generate quest.prc at           #}
{# application build time.                                                #}
{##########################################################################}
{############# Generated automatically by Quest build system ##############}
{############################ DO NOT EDIT #################################}

{# Define our Notify log levels to control log/console spam               #}
notify-level-pnmimage error
notify-level-prc error

{# Define Window/Graphics options for the application                    #}
gl-display gl
gl-display dx9
gl-display dx8

win-size 800 600
fullscreen #f
sync-video #f

{# Define Audio Library options for the application                       #}
audio-music-active #t
low-memory-stream-audio #t
audio-library-name p3fmod_audio
audio-output-rate 44100
