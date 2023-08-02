#SingleInstance
#MaxHotkeysPerInterval 10000

; video parameters:
VIDEO_WIDTH := Floor(960*1.0)
VIDEO_HEIGHT := Floor(640*1.0)
;PROJECT_WIDTH := 1920
;PROJECT_HEIGHT := 1080
; evaluated video parameters:
;NEW_VIDEO_XPOS := Floor(PROJECT_WIDTH/2 - VIDEO_WIDTH/2)
;NEW_VIDEO_YPOS := Floor(PROJECT_HEIGHT/2 - VIDEO_HEIGHT/2)

; program parameters (get these using AHK's Window Spy):
PANEL_YPOS := 580                     ; ypos of where the panels are (assuming the Effects and Effect/Composition Stack panels are in the same group)
EFFECTS_PANEL_XPOS := 200             ; xpos of the Effects panel's tab
COMPOSITION_STACK_PANEL_XPOS := 570   ; xpos of the Effect/Composition Stack panel's tab

TRANSFORM_EFFECT_XPOS := 90           ; xpos of the transform effect item in the Effects panel
TRANSFORM_EFFECT_YPOS := 120          ; ypos of that

TRANSFORM_DATA_YPOS := 265            ; ypos of the transform effect's data, in the Effect/Composition Stack panel
;TRANSFORM_DATA_XPOS_X := 50          ; xpos of the transform effect's X data (not needed anymore)
;TRANSFORM_DATA_XPOS_Y := 110         ;                                Y data (not needed anymore)
TRANSFORM_DATA_XPOS_W := 165          ;                                W data
;TRANSFORM_DATA_XPOS_LOCK := 200      ;                                lock aspect ratio button (not needed)
TRANSFORM_DATA_XPOS_H := 250          ;                                H data

TRANSFORM_DATA_CENTER_Y := 290        ; ypos of the align buttons
TRANSFORM_DATA_CENTER_HORZ_X := 50    ; xpos of center horizontally button
TRANSFORM_DATA_CENTER_VERT_X := 135   ; xpos of center vertically button



CoordMode, Mouse, Client

; add a Transform effect (note: needs "transform" typed into effects search bar with the default positions)
$-::
	MouseGetPos, PosX, PosY
	MouseClick, Left, %EFFECTS_PANEL_XPOS%, %PANEL_YPOS%
	MouseClickDrag, Left, %TRANSFORM_EFFECT_XPOS%, %TRANSFORM_EFFECT_YPOS%, PosX, PosY
Return

; add the relevant data to the Transform effect (note: click the clip beforehand to select it and open the composition stack panel)
$=::
	MouseGetPos, PosX, PosY
	;MouseClick, Left, %COMPOSITION_STACK_PANEL_XPOS%, %PANEL_YPOS% ; composition stack panel (unnecessary, since you need to click on the clip anyway)

	MouseClick, Left, %TRANSFORM_DATA_XPOS_H%, %TRANSFORM_DATA_YPOS%, 2
	Send %VIDEO_HEIGHT%
	Send {Enter}

	;MouseClick, Left, %TRANSFORM_DATA_XPOS_LOCK%, %TRANSFORM_DATA_YPOS% ; unlock aspect ratio (unnecessary)

	MouseClick, Left, %TRANSFORM_DATA_XPOS_W%, %TRANSFORM_DATA_YPOS%, 2
	Send %VIDEO_WIDTH%
	Send {Enter}

	;MouseClick, Left, %TRANSFORM_DATA_XPOS_Y%, %TRANSFORM_DATA_YPOS%, 2
	;Send %NEW_VIDEO_YPOS%
	;Send {Enter}
	MouseClick, Left, %TRANSFORM_DATA_CENTER_HORZ_X%, %TRANSFORM_DATA_CENTER_Y%

	;MouseClick, Left, %TRANSFORM_DATA_XPOS_X%, %TRANSFORM_DATA_YPOS%, 2
	;Send %NEW_VIDEO_XPOS%
	;Send {Enter}
	MouseClick, Left, %TRANSFORM_DATA_CENTER_VERT_X%, %TRANSFORM_DATA_CENTER_Y%

	MouseMove, PosX, PosY
Return

^Enter::Suspend

^+!e::ExitApp
