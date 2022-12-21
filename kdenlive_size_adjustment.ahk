#SingleInstance
#MaxHotkeysPerInterval 10000

VIDEO_WIDTH := 1000
VIDEO_HEIGHT := 800
PROJECT_WIDTH := 1920
PROJECT_HEIGHT := 1080

; TODO: put coords constants up here

NEW_VIDEO_XPOS := Floor(PROJECT_WIDTH/2 - VIDEO_WIDTH/2)
NEW_VIDEO_YPOS := Floor(PROJECT_HEIGHT/2 - VIDEO_HEIGHT/2)

CoordMode, Mouse, Client

-::
	; add a Transform effect (note: needs "transform" typed into effects search bar)
	MouseGetPos, PosX, PosY
	MouseClick, Left, 200, 590 ; effects panel
	MouseClickDrag, Left, 90, 120, PosX, PosY
Return

=::
	; add the relevant data
	MouseGetPos, PosX, PosY
	;MouseClick, Left, 570, 590 ; composition stack panel (unnecessary, since you need to click on the clip anyway)

	MouseClick, Left, 250, 265, 2
	Send %VIDEO_HEIGHT%
	Send {Enter}

	;MouseClick, Left, 200, 265 ; unlock aspect ratio

	MouseClick, Left, 165, 265, 2
	Send %VIDEO_WIDTH%
	Send {Enter}

	MouseClick, Left, 110, 265, 2
	Send %NEW_VIDEO_YPOS%
	Send {Enter}

	MouseClick, Left, 50, 265, 2
	Send %NEW_VIDEO_XPOS%
	Send {Enter}

	MouseMove, PosX, PosY
Return

^Enter::Suspend

^+!e::ExitApp
