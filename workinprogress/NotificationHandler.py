import tkinter as tk
import sys
import pygetwindow as gw

def create_notification(msg, font, color, text_color, timeout):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)

    desktop_name = get_current_virtual_desktop_name()
    if not msg:
        msg = f"Current virtual desktop: {desktop_name}"

    root.geometry("+350+80")
    label = tk.Label(root, text=msg, font=(font, 12), bg=color, fg=text_color, padx=10, pady=5)
    label.pack()

    root.after(int(float(timeout) * 1000), root.destroy)
    root.mainloop()

def get_current_virtual_desktop_name():
    vdm = pythonwindow.vdm.VirtualDesktopManager()
    active_desktop = vdm.get_active_desktop()
    desktop_name = active_desktop.name
    return desktop_name

if __name__ == "__main__":
    msg = sys.argv[1]
    font = sys.argv[2]
    color = sys.argv[3]
    text_color = sys.argv[4]
    timeout = sys.argv[5]

    create_notification(msg, font, color, text_color, timeout)
