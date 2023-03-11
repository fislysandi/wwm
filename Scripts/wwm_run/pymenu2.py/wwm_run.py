import os
import subprocess
import sys
import tkinter as tk
import tkinter.font as tkfont


class WWMDock(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.withdraw()  # hide the dock initially
        self.items = []
        self.filter_var = tk.StringVar()
        self.filter_var.trace('w', self.filter_items)
        self.selected_item = None

        self.init_gui()

        # add this line for debugging
        print("WWMDock initialized")

    def init_gui(self):
        # set dock position and make it always on top
        self.wm_attributes('-topmost', True)
        self.geometry('+0+0')

        # create search box and bind return key to launch selected item
        self.search_box = tk.Entry(self, textvariable=self.filter_var)
        self.search_box.pack(side='top', fill='x')
        self.search_box.bind('<Return>', self.handle_return)

        # create listbox to display items
        self.listbox = tk.Listbox(self)
        self.listbox.pack(side='top', fill='both', expand=True)
        self.listbox.bind('<ButtonRelease-1>', self.handle_click)
        self.listbox.bind('<Escape>', self.hide)

    def handle_click(self, event):
        """Set selected item and hide dock on list item click."""
        self.selected_item = self.listbox.get(self.listbox.curselection())
        self.hide()

    def handle_return(self, event):
        """Launch selected item on return key press."""
        self.selected_item = self.listbox.get(self.listbox.curselection())
        self.hide()
        self.launch_selected_item()

    def filter_items(self, *args):
        """Filter listbox items based on search box input."""
        search_term = self.filter_var.get().lower()
        self.listbox.delete(0, 'end')
        for item in self.items:
            if search_term in item.lower():
                self.listbox.insert('end', item)
        if len(self.items) > 0:
            self.listbox.selection_set(0)
            self.selected_item = self.listbox.get(0)

    def update_items(self, items):
        """Update listbox items and show dock."""
        self.items = items
        self.filter_items()
        self.deiconify()  # show the dock

    def launch_selected_item(self):
        """Launch selected item."""
        subprocess.run(['open', '-a', self.selected_item])

    def hide(self, *args):
        """Hide dock."""
        self.withdraw()


# Constants
APP_CACHE_FILE = "appcache.txt"
SCRIPTS_FOLDER = "wwm_runner_scripts"
BORDER_WIDTH = 10
FONT_SIZE = 16
MAX_ITEMS = 10


class Item:
    def __init__(self, text, icon_path, command):
        self.text = text
        self.icon_path = icon_path
        self.command = command

    def __lt__(self, other):
        return self.text.lower() < other.text.lower()


#class DMenu:
#    def __init__(self, items):
#        self.items = items
#        self.filtered_items = []
#        self.selected_item = None
#        self.input_text = ""
#
#        self.init_gui()
#
#
#    def init_gui(self):
#        self.win = tk.Tk()
#
#        self.win.overrideredirect(True)  # remove window decorations
#        self.win.geometry("+0+0")  # move window to top-left corner
#        self.win.lift()  # make sure window is on top of all other windows
#        self.win.attributes("-topmost", True)  # keep window on top of all other windows
#
#        self.canvas = tk.Canvas(self.win, bg="black", highlightthickness=0)
#        self.canvas.pack(fill="both", expand=True)
#
#        self.input_text_id = self.canvas.create_text(
#            BORDER_WIDTH, BORDER_WIDTH, anchor="nw", font=("TkFixedFont", FONT_SIZE),
#            fill="white", text="")
#
#        self.items_start_y = FONT_SIZE + BORDER_WIDTH * 2
#        self.items_end_y = self.win.winfo_screenheight() - BORDER_WIDTH
#        self.item_height = FONT_SIZE + BORDER_WIDTH
#        self.max_items = min(MAX_ITEMS, int((self.items_end_y - self.items_start_y) / self.item_height))
#
#        self.input_text_font = tkfont.Font(font=("TkFixedFont", FONT_SIZE))
#        self.item_font = tkfont.Font(font=("TkFixedFont", FONT_SIZE))
#
#        self.win.bind("<Button-1>", self.handle_click)
#        self.win.bind("<Key>", self.handle_keypress)
#        self.win.bind("<Configure>", self.handle_resize)
#
#        self.draw_input_text()
#        self.filter_items()
#        self.draw_items()
#
#    def draw_input_text(self):
#        self.canvas.itemconfig(self.input_text_id, text=self.input_text)
#
#    def draw_items(self):
#        self.canvas.delete("item")
#
#        start = len(self.filtered_items) - self.max_items
#        end = len(self.filtered_items)
#        if start < 0:
#            start = 0
#
#        for i in range(start, end):
#            item = self.filtered_items[i]
#            item_y = self.items_start_y + (i - start) * self.item_height
#            item_text_id = self.canvas.create_text(
#                BORDER_WIDTH, item_y, anchor="nw", font=self.item_font,
#                fill="white", text=item.text, tags="item")
#            self.canvas.itemconfig(item_text_id, width=self.win.winfo_width())
#
#            if item is self.selected_item:
#                self.canvas.itemconfig(item_text_id, fill="black")
#
#
#    def filter_items(self):
#        self.filtered_items = []
#
#        for item in self.items:
#            if self.input_text.lower() in item.text.lower():
#                self.filtered_items.append(item)
#
#        self.filtered_items.sort()
#
#        if self.selected_item not in self.filtered_items:
#            self.selected_item = None
#
#        if not self.filtered_items:
#            self.canvas.itemconfig(self.input_text_id, fill="red")
#        else:
#            self.canvas.itemconfig(self.input_text_id, fill="white")
#
#        self.draw_items()
#
#    def select_item(self, item):
#        if item != self.selected_item:
#            if self.selected_item is not None:
#                self.canvas.itemconfig(self.canvas.find_withtag("item"), fill="white")
#            self.selected_item = item
#            self.canvas.itemconfig(self.canvas.find_withtag("item"), width=self.win.winfo_width())
#
#            item_text_id = self.canvas.find_withtag("item")[self.filtered_items.index(item)]
#            self.canvas.itemconfig(item_text_id, fill="black")
#
#    def handle_click(self, event):
#        item_index = int((event.y - self.items_start_y) / self.item_height)
#        if item_index >= 0 and item_index < len(self.filtered_items):
#            self.select_item(self.filtered_items[item_index])
#            self.running = False
#
#    def handle_keypress(self, event):
#        if event.keysym == "Escape":
#            self.running = False
#        elif event.keysym == "Return":
#            if self.selected_item is not None:
#                self.running = False
#        elif event.keysym == "BackSpace":
#            self.input_text = self.input_text[:-1]
#        elif len(event.keysym) == 1:
#            self.input_text += event.char
#
#        self.filter_items()
#        self.draw_input_text()
#
#    def handle_resize(self, event):
#        self.draw_items()
#
#    def run(self):
#        self.running = True
#        self.draw_input_text()
#        self.draw_items()
#
#        while self.running:
#            self.win.update()
#            self.win.update_idletasks()
#
#        if self.selected_item is None:
#            return None
#
#        return self.selected_item.text


#class DMenu:
#    def __init__(self, items):
#        self.items = []
#        for item in items:
#            self.items.append(DMenuItem(item))
#
#        self.selected_item = self.items[0] if self.items else None
#        self.filtered_items = self.items
#        self.input_text = ""
#
#        self.init_gui()
#
#    def init_gui(self):
#        self.win = tk.Tk()
#
#        self.win.overrideredirect(True)  # remove window decorations
#        self.win.geometry("+0+0")  # move window to top-left corner
#        self.win.lift()  # make sure window is on top of all other windows
#        self.win.attributes("-topmost", True)  # keep window on top of all other windows
#
#        self.canvas = tk.Canvas(self.win, bg="black", highlightthickness=0)
#        self.canvas.pack(fill="both", expand=True)
#
#        self.input_text_id = self.canvas.create_text(
#            BORDER_WIDTH, BORDER_WIDTH, anchor="nw", font=("TkFixedFont", FONT_SIZE),
#            fill="white", text="")
#
#        self.items_start_y = FONT_SIZE + BORDER_WIDTH * 2
#        self.items_end_y = self.win.winfo_screenheight() - BORDER_WIDTH
#        self.item_height = FONT_SIZE + BORDER_WIDTH
#        self.max_items = min(MAX_ITEMS, int((self.items_end_y - self.items_start_y) / self.item_height))
#
#        self.input_text_font = tkfont.Font(font=("TkFixedFont", FONT_SIZE))
#        self.item_font = tkfont.Font(font=("TkFixedFont", FONT_SIZE))
#
#        self.win.bind("<Button-1>", self.handle_click)
#        self.win.bind("<Key>", self.handle_keypress)
#        self.win.bind("<Configure>", self.handle_resize)
#
#        self.draw_input_text()
#        self.filter_items()
#        self.draw_items()
#
#    def draw_input_text(self):
#        self.canvas.itemconfig(self.input_text_id, text=self.input_text)
#
#    def draw_items(self):
#        self.canvas.delete("item")
#
#        start = len(self.filtered_items) - self.max_items
#        end = len(self.filtered_items)
#        if start < 0:
#            start = 0
#
#        for i in range(start, end):
#            item = self.filtered_items[i]
#            item_y = self.items_start_y + (i - start) * self.item_height
#            item_text_id = self.canvas.create_text(
#                BORDER_WIDTH, item_y, anchor="nw", font=self.item_font,
#                fill="white", text=item.text, tags="item")
#            self.canvas.itemconfig(item_text_id, width=self.win.winfo_width())
#
#            if item is self.selected_item:
#                self.canvas.itemconfig(item_text_id, fill="black")
#
#    def filter_items(self):
#        self.filtered_items = []
#
#        for item in self.items:
#            if self.input_text.lower() in item.text.lower():
#                self.filtered_items.append(item)
#
#        self.filtered_items.sort()
#
#        if self.selected_item not in self.filtered_items:
#            self.selected_item = None
#
#        if not self.filtered_items:
#            self.canvas.itemconfig(self.input_text_id, fill="red")
#        else:
#            self.canvas.itemconfig(self.input_text_id, fill="white")
#
#        self.draw_items()
#
#    def select_item(self, item):
#        if item != self.selected_item:
#            if self.selected_item is not None:
#                self.canvas.itemconfig(self.canvas.find_withtag("item"), fill="white")
#            self.selected_item = item
#            self.canvas.itemconfig(self.canvas.find_withtag("item"), width=self.win.winfo_width())
#
#            item_text_id = self.canvas.find_withtag("item")[self.filtered_items.index(item)]
#            self.canvas.itemconfig(item_text_id, fill="black")
#
#    def handle_click(self, event):
#        item = None
#        for i in range(len(self.item_rects)):
#            if self.item_rects[i].collidepoint(event.pos):
#                item = self.filtered_items[i]
#                break
#
#        if item is None:
#            return
#
#        if item.is_folder():
#            self.path.append(item)
#            self.filter_items()
#        else:
#            path = item.get_path()
#            subprocess.Popen(path)
#
#    def handle_back(self):
#        if len(self.path) > 1:
#            self.path.pop()
#            self.filter_items()
#
#    def handle_quit(self):
#        pygame.quit()
#        sys.exit()
#
#    def run(self):
#        self.init_gui()
#        self.filter_items()
#
#        while True:
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    self.handle_quit()
#                elif event.type == pygame.MOUSEBUTTONUP:
#                    self.handle_click(event)
#                elif event.type == pygame.KEYDOWN:
#                    if event.key == pygame.K_BACKSPACE:
#                        self.handle_back()
#                    elif event.key == pygame.K_ESCAPE:
#                        self.handle_quit()
