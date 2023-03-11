;see https://autohotkey.com/board/topic/3248-stuck-ctrl-key/ if issues with keys sticking
#SingleInstance Force ; The script will Reload if launched while already running
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases
#KeyHistory 0 ; Ensures user privacy when debugging is not needed
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability
NotifHandler := "%A_ScriptDir%\NotificationHandler.py"


; Globals
DesktopCount := 6        ; Windows starts with 2 desktops at boot
CurrentDesktop := 1      ; Desktop count is 1-indexed (Microsoft numbers them this way)
DesktopSwitchCount := 0  ; the number that get bound to the variable to quickly switch between desktops


; DLL
hVirtualDesktopAccessor := DllCall("LoadLibrary", "Str", A_ScriptDir . "\VirtualDesktopAccessor.dll", "Ptr")
global IsWindowOnDesktopNumberProc := DllCall("GetProcAddress", Ptr, hVirtualDesktopAccessor, AStr, "IsWindowOnDesktopNumber", "Ptr")
global MoveWindowToDesktopNumberProc := DllCall("GetProcAddress", Ptr, hVirtualDesktopAccessor, AStr, "MoveWindowToDesktopNumber", "Ptr")
global GoToDesktopNumberProc := DllCall("GetProcAddress", Ptr, hVirtualDesktopAccessor, AStr, "GoToDesktopNumber", "Ptr")

; Main
SetKeyDelay, 75
mapDesktopsFromRegistry()
OutputDebug, [loading] desktops: %DesktopCount% current: %CurrentDesktop%

#Include %A_ScriptDir%\user_config.ahk
return

;
; This function examines the registry to build an accurate list of the current virtual desktops and which one we're currently on.
; Current desktop UUID appears to be in HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\SessionInfo\1\VirtualDesktops
; List of desktops appears to be in HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VirtualDesktops
;
mapDesktopsFromRegistry() 
{
    global CurrentDesktop, DesktopCount

    ; Get the current desktop UUID. Length should be 32 always, but there's no guarantee this couldn't change in a later Windows release so we check.
    IdLength := 32
    SessionId := getSessionId()
    if (SessionId) {
        RegRead, CurrentDesktopId, HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\SessionInfo\%SessionId%\VirtualDesktops, CurrentVirtualDesktop
        if (CurrentDesktopId) {
            IdLength := StrLen(CurrentDesktopId)
        }
    }

    ; Get a list of the UUIDs for all virtual desktops on the system
    RegRead, DesktopList, HKEY_CURRENT_USER, SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VirtualDesktops, VirtualDesktopIDs
    if (DesktopList) {
        DesktopListLength := StrLen(DesktopList)
        ; Figure out how many virtual desktops there are
        DesktopCount := floor(DesktopListLength / IdLength)
    }
    else {
        DesktopCount := 1
    }

    ; Parse the REG_DATA string that stores the array of UUID's for virtual desktops in the registry.
    i := 0
    while (CurrentDesktopId and i < DesktopCount) {
        StartPos := (i * IdLength) + 1
        DesktopIter := SubStr(DesktopList, StartPos, IdLength)
        ;OutputDebug, The iterator is pointing at %DesktopIter% and count is %i%.

        ; Break out if we find a match in the list. If we didn't find anything, keep the
        ; old guess and pray we're still correct :-D.
        if (DesktopIter = CurrentDesktopId) {
            CurrentDesktop := i + 1
            ;OutputDebug, Current desktop number is %CurrentDesktop% with an ID of %DesktopIter%.
            break
        }
        i++
    }
}

;
; This functions finds out ID of current session.
;
getSessionId()
{
    ProcessId := DllCall("GetCurrentProcessId", "UInt")
    if ErrorLevel {
        OutputDebug, Error getting current process id: %ErrorLevel%
        return
    }
    OutputDebug, Current Process Id: %ProcessId%

    DllCall("ProcessIdToSessionId", "UInt", ProcessId, "UInt*", SessionId)
    if ErrorLevel {
        OutputDebug, Error getting session id: %ErrorLevel%
        return
    }
    OutputDebug, Current Session Id: %SessionId%
    return SessionId
}


;
; This function creates a new virtual desktop and switches to it
;
createVirtualDesktop()
{
    global CurrentDesktop, DesktopCount
    Send, #^d
    DesktopCount++
    CurrentDesktop := DesktopCount
    OutputDebug, [create] desktops: %DesktopCount% current: %CurrentDesktop%
}


_createEnoughDesktops(targetDesktop) {
    global DesktopCount

    ; Create virtual desktop if it does not exist
    while (targetDesktop > DesktopCount) {
        createVirtualDesktop()
    }
    return
}

_switchDesktopToTarget(targetDesktop)
{
    ; Globals variables should have been updated via updateGlobalVariables() prior to entering this function
    global CurrentDesktop, DesktopCount
    
    ; Don't attempt to switch to an invalid desktop
    if (targetDesktop < 1) {
        OutputDebug, [invalid] target: %targetDesktop% current: %CurrentDesktop%
        return
    }

    if (targetDesktop == CurrentDesktop) {
        return
    }

    _createEnoughDesktops(targetDesktop)

    ; Fixes the issue of active windows in intermediate desktops capturing the switch shortcut and therefore delaying or stopping the switching sequence. This also fixes the flashing window button after switching in the taskbar. More info: https://github.com/pmb6tz/windows-desktop-switcher/pull/19
    WinActivate, ahk_class Shell_TrayWnd

    DllCall(GoToDesktopNumberProc, UInt, targetDesktop - 1)

    ; Makes the WinActivate fix less intrusive
    Sleep, 50
    focusTheForemostWindow(targetDesktop)
}

updateGlobalVariables()
{
    ; Re-generate the list of desktops and where we fit in that. We do this because
    ; the user may have switched desktops via some other means than the script.
    mapDesktopsFromRegistry()
}

switchDesktopByNumber(targetDesktop)
{
    global CurrentDesktop, DesktopCount
    updateGlobalVariables()
    _switchDesktopToTarget(targetDesktop)
}

focusTheForemostWindow(targetDesktop) 
{
    foremostWindowId := getForemostWindowIdOnDesktop(targetDesktop)
    WinActivate, ahk_id %foremostWindowId%
}

getForemostWindowIdOnDesktop(n)
{
    n := n - 1 ; Desktops start at 0, while in script it's 1

    ; winIDList contains a list of windows IDs ordered from the top to the bottom for each desktop.
    WinGet winIDList, list
    Loop % winIDList {
        windowID := % winIDList%A_Index%
        windowIsOnDesktop := DllCall(IsWindowOnDesktopNumberProc, UInt, windowID, UInt, n)
        ; Select the first (and foremost) window which is in the specified desktop.
        if (windowIsOnDesktop == 1) {
            return windowID
        }
    }
}

MoveCurrentWindowToDesktop(desktopNumber) {
    global CurrentDesktop, DesktopCount
    WinGet, activeHwnd, ID, A

    ;updateGlobalVariables()
    
    _createEnoughDesktops(desktopNumber)
    DllCall(MoveWindowToDesktopNumberProc, UInt, activeHwnd, UInt, desktopNumber - 1)

    ;OutputDebug, Moving current window %activeHwnd% to %desktopNumber%

    ;output := DllCall(MoveWindowToDesktopNumberProc, UInt, activeHwnd, UInt, desktopNumber - 1)
    ;if output {
    ;    OutputDebug, success
    ;} else {
    ;    OutputDebug, failed
    ;}

    ;switchDesktopByNumber(desktopNumber)
    ;WinActivate, ahk_id activeHwnd
    
    ;focusTheForemostWindow(CurrentDesktop)
    switchDesktopByNumber(desktopNumber)
}

closeWindow(){
    global CurrentDesktop
	
    WinClose, A
    focusTheForemostWindow(CurrentDesktop)
}

quitWindow(){
    ;quite current window
    WinClose, A
	NotifHandler("Window Killed", "Arial", "#FFFFFF", "#000000", "0.9")
}


toggleMaximize(){
    WinGet, maximized, MinMax, A

    if maximized {
        WinRestore A
    } else {
        WinMaximize A
    }
}


GoToPrevDesktop() {
	;NotifHandler("Going To The Previous Desktop")
    Send, #^{Right}
	NotifHandler("Next Desktop", "Arial", "#FFFFFF", "#000000", "0.9")
}

GoToNextDesktop() {
	;NotifHandler"Going To The Next Desktop")
    Send, #^{Left}
	NotifHandler("Previous Desktop", "Arial", "#FFFFFF", "#000000", "0.9")
}

AddNewVirtDesktop() {
	;NotifHandler("Added New Virtual Desktop")
    Send, #^d
		NotifHandler("Adding new Virtual desktop", "Arial", "#FFFFFF", "#000000", "0.5")
}

DelVirtDesktop() {
	;NotifHandler("Deleted the current virtual desktop")
    Send, #^{f4}
	NotifHandler("Deleted the current desktop", "Arial", "#FFFFFF", "#000000", "0.5")
}


NotifHandler(msg="", font="", color="", text_color="", timer="") {
    Run, pythonw.exe "%A_ScriptDir%\NotificationHandler.py" "%msg%" "%font%" "%color%" "%text_color%" "%timer%"
    return
}


;RenameVirtDesktop() {
;    InputBox, NewName, Rename Virtual Desktop, Enter the new name for the virtual desktop:
;    WinGet, CurrentDesktop, ID, A
;    VirtualDesktopName := "VD" CurrentDesktop
;    SendMessage, 0x50D, 0, &VirtualDesktopName,, ahk_id %CurrentDesktop%
;    SendMessage, 0x50D, 0, &NewName,, ahk_id %CurrentDesktop%
;    ("Virtual Desktop Renamed to " . NewName)
;}




updateGlobalVariables()



