#Include i3wm.ahk
; ====================
; === INSTRUCTIONS ===
; ====================
; 1. Any lines starting with ; are ignored
; 2. After changing this config file run script file "desktop_switcher.ahk"
; 3. Every line is in the format HOTKEY::ACTION

; === SYMBOLS ===
; !   <- Alt
; +   <- Shift
; ^   <- Ctrl
; #   <- Win
; For more, visit https://autohotkey.com/docs/Hotkeys.htm

; === EXAMPLES ===
;!n::switchDesktopToRight()            ; <- <Alt> + <N> will switch to the next desktop (to the right of the current one)
; #!space::switchDesktopToRight()      ;  <- <Win> + <Alt> + <Space> will switch to next desktop
; CapsLock & n::switchDesktopToRight() ;  <- <CapsLock> + <N> will switch to the next desktop (& is necessary when using non-modifier key such as CapsLock)

; ===========================
; === END OF INSTRUCTIONS ===
; ===========================


; cycle through desktops
#z::GoToNextDesktop()
#x::GoToPrevDesktop()
;#F2::RenameVirtDesktop()

; remove/add dekstop
#a::AddNewVirtDesktop()
#^w::DelVirtDesktop()

;switchDesktops
!#z::switchDesktopByNumber(1)
!#x::switchDesktopByNumber(2)
!#c::switchDesktopByNumber(3)
#4::switchDesktopByNumber(4)
#5::switchDesktopByNumber(5)
#6::switchDesktopByNumber(6)
#7::switchDesktopByNumber(7)
#8::switchDesktopByNumber(8)
#9::switchDesktopByNumber(9)

#+1::MoveCurrentWindowToDesktop(1)
#+2::MoveCurrentWindowToDesktop(2)
#+3::MoveCurrentWindowToDesktop(3)
#+4::MoveCurrentWindowToDesktop(4)
#+5::MoveCurrentWindowToDesktop(5)
#+6::MoveCurrentWindowToDesktop(6)
#+7::MoveCurrentWindowToDesktop(7)
#+8::MoveCurrentWindowToDesktop(8)
#+9::MoveCurrentWindowToDesktop(9)

#w::quitWindow()





;#f::toggleMaximize()

; WSL -- create shortcut by dragging from start menu (can't be from a search result)
;#Enter::Run, C:\window-mover.git\Debian GNU-Linux

; Run Commands
#t::Run, C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Terminal.lnk ; pull up the terminal
#^d::Run, D:\personal\pic\General_Pictures\References\concept dump.pur ; pull up refrences
#+e::Run, nvim %A_ScriptDir%\ ; edit user config

; Restart the window manager
#+r::Run, %A_ScriptDir%\i3wm.ahk
; Edit Config files
#^e::Run, nvim %A_ScriptDir%\i3wm.ahk

;hmm it doesnt work i use the shorcut, the window with the script execution cmd appears then dissapears, nothing happens




