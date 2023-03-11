import tkinter as tk

class NotificationWindow:
    def __init__(self, message):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.geometry("+250+250")
        self.label = tk.Label(self.root, text=message, font=("Calibri", 12), fg="white", bg="gray", padx=10, pady=5)
        self.label.pack()
        self.root.after(1500, self.close)
        self.root.mainloop()

    def close(self):
        self.root.destroy()

if __name__ == "__main__":
    message = "This is a notification message!"
    NotificationWindow(message)
