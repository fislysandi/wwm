import tkinter as tk

def button_clicked():
    print("Button clicked!")

window = tk.Tk()
window.title("Hello World")
button = tk.Button(window, text="Click me!", command=button_clicked)
button.pack()
window.mainloop()
