# WWM

Forked from [yalibian/i3-windows](https://github.com/yalibian/i3-windows#readme), to extend it into a full minimal window manager .

- Switch to virtual desktops 1-9 using `⊞-#` and backfill # of desktops if needed
- Move active windows to virtual desktops 1-9 using `⊞-shift-#` and backfill desktops if needed
- Cycle through workspaces(virtual-desktops) with win + z,win + x
- Delete Workspaces with win + shift + w
- Add Workspaces with win + a
- adjust your system sound with win + mousewheel
- Close windows with `win+w`
- Open Windows Termianl with `win+t`

# Known issue 

- when an application is launched with admin priveleges and you focus on the window script stops working.


# Dependencies

- Windows 10
- [AutoHotkey](https://autohotkey.com/download/) v1.1+
- [VirtualDesktopAccessor.dll](https://github.com/Ciantic/VirtualDesktopAccessor)
- ctypes
- win32con
- subprocess
- pycaw
- tkinter
- tkinter.font
- winreg
- sys
- win32api
- os
- win32gui
- comtypes


- to install of those dependencies type pip3 install ctypes  subprocess pycaw tkinter .font winreg sys pywin32 os ast comtypes

## Running on boot

You can make the script run on every boot with either of these methods.

### Simple (Non-administrator method)

1. Press `Win + R`, enter `shell:startup`, press `OK`
2. Create a shortcut to the `desktop_switcher.ahk` file here

### Advanced (Administrator method)

Windows prevents hotkeys from working in windows that were launched with higher elevation than the AutoHotKey script (such as CMD or Powershell terminals that were launched as Administrator). As a result, Windows Desktop Switcher hotkeys will only work within these windows if the script itself is `Run as Administrator`, due to the way Windows is designed. 

You can do this by creating a scheduled task to invoke the script at logon. You may use 'Task Scheduler', or create the task in powershell as demonstrated.
```
# Run the following commands in an Administrator powershell prompt. 
# Be sure to specify the correct path to your desktop_switcher.ahk file. 

$A = New-ScheduledTaskAction -Execute "PATH\TO\desktop_switcher.ahk"
$T = New-ScheduledTaskTrigger -AtLogon
$P = New-ScheduledTaskPrincipal -GroupId "BUILTIN\Administrators" -RunLevel Highest
$S = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0
$D = New-ScheduledTask -Action $A -Principal $P -Trigger $T -Settings $S
Register-ScheduledTask WindowsDesktopSwitcher -InputObject $D
```

The task is now registered and will run on the next logon, and can be viewed or modified in 'Task Scheduler'. 

## Original credits

- Thanks to [Ciantic/VirtualDesktopAccessor](https://github.com/Ciantic/VirtualDesktopAccessor) (for the DLL) and [sdias/win-10-virtual-desktop-enhancer](https://github.com/sdias/win-10-virtual-desktop-enhancer) (for the DLL usage samples) our code can move windows between desktops.

## Possible developments

- Full rewrite in guile scheme/common lisp
- Add tiling window manager capabilites
- Add application launcher that will mimic all of the behaviour and extensibility of dmenu with common lisp/guile scheme
- write a better notificaion handler that will look pretier 
- add theming support
- Solve the problem with Priveleged applications making the script stop working
