#SingleInstance
#MaxHotkeysPerInterval 10000

; video parameters:
VIDEO_WIDTH := 1000
VIDEO_HEIGHT := 800
PROJECT_WIDTH := 1920
PROJECT_HEIGHT := 1080
; evaluated video parameters:
NEW_VIDEO_XPOS := Floor(PROJECT_WIDTH/2 - VIDEO_WIDTH/2)
NEW_VIDEO_YPOS := Floor(PROJECT_HEIGHT/2 - VIDEO_HEIGHT/2)

; program parameters (get these using AHK's Window Spy):
PANEL_YPOS := 590
EFFECTS_PANEL_XPOS := 200
COMPOSITION_STACK_PANEL_XPOS := 570
; other program parameters (there's probably a way to evaluate most of these, but oh well):
TRANSFORM_EFFECT_XPOS := 90
TRANSFORM_EFFECT_YPOS := 120
TRANSFORM_DATA_YPOS := 265
TRANSFORM_DATA_XPOS_X := 50
TRANSFORM_DATA_XPOS_Y := 110
TRANSFORM_DATA_XPOS_W := 165
TRANSFORM_DATA_XPOS_LOCK := 200
TRANSFORM_DATA_XPOS_H := 250



CoordMode, Mouse, Client

; add a Transform effect (note: needs "transform" typed into effects search bar with the default positions)
-::
	MouseGetPos, PosX, PosY
	MouseClick, Left, %EFFECTS_PANEL_XPOS%, %PANEL_YPOS%
	MouseClickDrag, Left, %TRANSFORM_EFFECT_XPOS%, %TRANSFORM_EFFECT_YPOS%, PosX, PosY
Return

; add the relevant data to the Transform effect (note: click the clip beforehand to select it and open the composition stack panel)
=::
	MouseGetPos, PosX, PosY
	;MouseClick, Left, %COMPOSITION_STACK_PANEL_XPOS%, %PANEL_YPOS% ; composition stack panel (unnecessary, since you need to click on the clip anyway)

	MouseClick, Left, %TRANSFORM_DATA_XPOS_H%, %TRANSFORM_DATA_YPOS%, 2
	Send %VIDEO_HEIGHT%
	Send {Enter}

	;MouseClick, Left, %TRANSFORM_DATA_XPOS_LOCK%, %TRANSFORM_DATA_YPOS% ; unlock aspect ratio (unnecessary)

	MouseClick, Left, %TRANSFORM_DATA_XPOS_W%, %TRANSFORM_DATA_YPOS%, 2
	Send %VIDEO_WIDTH%
	Send {Enter}

	MouseClick, Left, %TRANSFORM_DATA_XPOS_Y%, %TRANSFORM_DATA_YPOS%, 2
	Send %NEW_VIDEO_YPOS%
	Send {Enter}

	MouseClick, Left, %TRANSFORM_DATA_XPOS_X%, %TRANSFORM_DATA_YPOS%, 2
	Send %NEW_VIDEO_XPOS%
	Send {Enter}

	MouseMove, PosX, PosY
Return

^Enter::Suspend

^+!e::ExitApp
