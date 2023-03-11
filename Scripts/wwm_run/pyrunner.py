import tkinter as tk
import win32gui
import win32con
import os
import subprocess
import winreg


class DMenu:
    def __init__(self, items, scripts_dir):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.9)
        self.root.bind('<FocusOut>', self.close)
        
        self.scripts_dir = scripts_dir
        
        self.frame = tk.Frame(self.root, bg='black')
        self.frame.pack()
        
        for item in items:
            label = tk.Label(self.frame, text=item, fg='white', bg='black', font=('Helvetica', 14, 'bold'))
            label.pack(padx=5, pady=5)
            label.bind('<Button-1>', lambda event, arg=item: self.on_click(arg))
            
        self.root.mainloop()
        
    def on_click(self, item):
        self.close(None)
        if item.endswith('.py'):
            script_path = os.path.join(self.scripts_dir, item)
            subprocess.Popen(['python', script_path])
        else:
            subprocess.Popen(item)
        
    def close(self, event):
        self.root.destroy()


def get_installed_apps():
    # Open the registry key for installed applications
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'Software\Microsoft\Windows\CurrentVersion\Uninstall') as key:
        apps = {}
        try:
            i = 0
            while True:
                # Iterate over all subkeys (i.e. installed applications)
                sub_key = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, sub_key) as sub_key:
                    # Retrieve the application name and path from the registry
                    app_name = winreg.QueryValueEx(sub_key, 'DisplayName')[0]
                    app_path = winreg.QueryValueEx(sub_key, 'InstallLocation')[0]
                    if app_name and app_path:
                        # Add the application to the dictionary
                        apps[app_name] = app_path
                i += 1
        except WindowsError:
            pass
    return apps

def get_scripts():
    # obtain list of scripts in scripts_dir directory
    scripts_dir = os.path.join(os.environ['A_ScriptDir'], 'scripts', 'pyrunnerscripts')
    script_list = os.listdir(scripts_dir)
    script_list = [item for item in script_list if item.endswith('.py')]
    return script_list

if __name__ == '__main__':
    apps = get_installed_apps()
    scripts = get_scripts()
    items = apps + scripts
    dmenu = DMenu(items, os.path.join(os.environ['A_ScriptDir'], 'scripts', 'pyrunnerscripts'))
