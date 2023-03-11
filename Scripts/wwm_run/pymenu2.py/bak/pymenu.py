import os
import subprocess
import tkinter as tk
import win32api
import win32con
import win32gui
import sys
import tkinter.font as tkfont


BORDER_WIDTH = 2
FONT_SIZE = 16
MAX_ITEMS = 10






class Item:
    def __init__(self, text):
        self.text = text




class DMenu:
    def __init__(self, items):
        self.running = True
        self.items = [Item(text) for text in items]
        self.filtered_items = self.items
        self.selected_item = None
        self.input_text = ""
        self.win = tk.Tk()
        self.win.overrideredirect(1)
        self.win.attributes("-topmost", True)
        self.win.bind("<FocusOut>", lambda event: self.win.focus_force())
        self.canvas = tk.Canvas(
            self.win,
            bg="black",
            highlightthickness=0,
            width=400,
            height=FONT_SIZE * MAX_ITEMS + BORDER_WIDTH * 2,
        )
        self.input_text_id = self.canvas.create_text(
            BORDER_WIDTH, BORDER_WIDTH, anchor="w", text=self.input_text
        )

        self.canvas.pack()

        self.win.bind("<Key>", self.handle_keypress)
        self.win.bind("<Configure>", self.handle_resize)
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", lambda event: self.handle_item_hover(event, self.filtered_items[int(event.y / FONT_SIZE)]))
        self.canvas.bind("<Leave>", self.handle_item_hover_exit)

        self.win.update()

        self.draw_items()

    def draw_input_text(self):
        self.canvas.itemconfig(self.input_text_id, text=self.input_text)

    def draw_items(self):
        self.canvas.delete("item")

        for i, item in enumerate(self.filtered_items[:MAX_ITEMS]):
            x1, y1, x2, y2 = BORDER_WIDTH, BORDER_WIDTH + i * FONT_SIZE, 400 - BORDER_WIDTH, BORDER_WIDTH + (i + 1) * FONT_SIZE
            fill = "white" if item == self.selected_item else "black"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="", tags="item")
            self.canvas.create_text(x1 + FONT_SIZE / 2, y1 + FONT_SIZE / 2, anchor="w", text=item.text, fill="white", tags="item")

        self.draw_input_text()

    def handle_item_hover(self, event, item):
        self.canvas.itemconfig("item", fill="black", outline="")
        self.canvas.itemconfig(event.widget.find_withtag("current"), fill="white")
        self.selected_item = item

    def handle_item_hover_exit(self, event):
        self.canvas.itemconfig("item", fill="black", outline="")
        self.selected_item = None

    def handle_click(self, event):
        if self.selected_item is not None:
            self.running = False

    def handle_resize(self, event):
        self.canvas.coords(self.input_text_id, BORDER_WIDTH, BORDER_WIDTH)

        self.draw_items()

    def handle_keypress(self, event):
        key = event.char

        if key == "\r":
            self.running = False
        elif key == "\x7f":
            self.input_text = self.input_text[:-1]
            self.draw_input_text()
        elif key:
            self.input_text += key
            self.draw_input_text()

        self.filter_items()
        self.draw_items()

class DMenuError(Exception):
    pass


def dmenu(items):
    if not items:
        raise DMenuError("dmenu: no items provided")

    dmenu = DMenu(items)
    dmenu.win.mainloop()

    if not dmenu.running:
        return dmenu.selected_item.text

    raise DMenuError("dmenu: user cancelled menu selection")


class DMenuItem:
    def __init__(self, text):
        self.text = text
        self.width = None

    def measure_width(self, font):
        self.width = font.measure(self.text)

    def __lt__(self, other):
        return self.text < other.text


class DMenu:
    def __init__(self, items):
        self.items = [DMenuItem(item) for item in items]
        self.filtered_items = self.items.copy()
        self.selected_item = None
        self.input_text = ""
        self.running = True

        self.init_gui()

    def init_gui(self):
        self.win = tk.Tk()

        self.win.overrideredirect(True)  # remove window decorations
        self.win.geometry("+0+0")  # move window to top-left corner
        self.win.lift()  # make sure window is on top of all other windows
        self.win.attributes("-topmost", True)  # keep window on top of all other windows

        self.canvas = tk.Canvas(self.win, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.input_text_id = self.canvas.create_text(
            BORDER_WIDTH, BORDER_WIDTH, anchor="nw", font=("TkFixedFont", FONT_SIZE),
            fill="white", text="")

        self.items_start_y = FONT_SIZE + BORDER_WIDTH * 2
        self.items_end_y = self.win.winfo_screenheight() - BORDER_WIDTH
        self.item_height = FONT_SIZE + BORDER_WIDTH
        self.max_items = min(MAX_ITEMS, int((self.items_end_y - self.items_start_y) / self.item_height))

        self.input_text_font = tkfont.Font(font=("TkFixedFont", FONT_SIZE))
        self.item_font = tkfont.Font(font=("TkFixedFont", FONT_SIZE))

        self.win.bind("<Button-1>", self.handle_click)
        self.win.bind("<Key>", self.handle_keypress)
        self.win.bind("<Configure>", self.handle_resize)

        self.draw_input_text()
        self.filter_items()
        self.draw_items()

    def draw_input_text(self):
        self.canvas.itemconfig(self.input_text_id, text=self.input_text)

    def draw_items(self):
        self.canvas.delete("item")

        start = len(self.filtered_items) - self.max_items
        end = len(self.filtered_items)
        if start < 0:
            start = 0

        for i in range(start, end):
            item = self.filtered_items[i]
            item_y = self.items_start_y + (i - start) * self.item_height
            item_text_id = self.canvas.create_text(
                BORDER_WIDTH, item_y, anchor="nw", font=self.item_font,
                fill="white", text=item.text, tags="item")
            self.canvas.itemconfig(item_text_id, width=self.win.winfo_width())

            if item is self.selected_item:
                self.canvas.itemconfig(item_text_id, fill="black")

    def filter_items(self):
        self.filtered_items = []

        for item in self.items:
            if self.input_text.lower() in item.text.lower():
                self.filtered_items.append(item)

        self.filtered_items.sort()

        if self.selected_item not in self.filtered_items:
            self.selected_item = None

        if not self.filtered_items:
            self.canvas.itemconfig(self.input_text_id, fill="red")
        else:
            self.canvas.itemconfig(self.input_text_id, fill="white")

        self.draw_items()

    def select_item(self, item):
        if item != self.selected_item:
            if self.selected_item is not None:
                self.canvas.itemconfig(self.canvas.find_withtag("item"), fill="white")
            self.selected_item = item
            self.canvas.itemconfig(self.canvas.find_withtag("item"), width=self.win.winfo_width())

            item_text_id = self.canvas.find_withtag("item")[self.filtered_items.index(item)]
            self.canvas.itemconfig(item_text_id, fill="black")

    def handle_click(self, event):
        item_index = int((event.y - self.items_start_y) / self.item_height)
        if item_index >= 0 and item_index < len(self.filtered_items):
            self.select_item(self.filtered_items[item_index])
            self.running = False

    def handle_keypress(self, event):
        if event.keysym == "Escape":
            self.running = False
        elif event.keysym == "Return":
            if self.selected_item is not None:
                self.running = False
        elif event.keysym == "BackSpace":
            self.input_text = self.input_text[:-1]
        elif len(event.keysym) == 1:
            self.input_text += event.char

        self.filter_items()
        self.draw_input_text()

    def handle_resize(self, event):
        self.draw_items()

    def run(self):
        self.running = True
        self.draw_input_text()
        self.draw_items()

        while self.running:
            self.win.update()
            self.win.update_idletasks()

        if self.selected_item is None:
            return None

        return self.selected_item.text


def dmenu(items):
    win = tk.Tk()
    win.withdraw()
    dmenu = DMenu(items)
    result = dmenu.run()
    win.destroy()


if __name__ == "__main__":
    items = ["apple", "banana", "orange", "pear", "pineapple"]
    result = dmenu(items)
    print(result)
