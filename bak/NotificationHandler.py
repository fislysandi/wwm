import tkinter as tk
import sys

def create_notification(msg, font, color, text_color, timeout):
    root = tk.Tk()
    root.overrideredirect(True)
    root.withdraw()

    label = tk.Label(root, text=msg, font=(font, 12), bg=color, fg=text_color, padx=10, pady=5)
    label.pack()

    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x_offset = (root.winfo_screenwidth() - width) // 2
    y_offset = (root.winfo_screenheight() - height) // 2

    root.geometry(f"+{x_offset}+{y_offset}")
    root.deiconify()

    root.after(int(float(timeout) * 1000), root.destroy)
    root.mainloop()

if __name__ == "__main__":
    args = sys.argv[1:]
    msg, font, color, text_color, timeout = args
    create_notification(msg, font, color, text_color, timeout)
