import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Centered Window")
        self.master.geometry("300x200")
        self.center_window()
        self.create_widgets()

    def center_window(self):
        # Get the screen dimensions
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width - self.master.winfo_reqwidth()) // 2
        y = (screen_height - self.master.winfo_reqheight()) // 2

        # Set the window position
        self.master.geometry("+{}+{}".format(x, y))

    def create_widgets(self):
        # Create widgets here
        pass

root = tk.Tk()
app = Application(master=root)
app.mainloop()
