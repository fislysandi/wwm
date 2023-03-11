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

class DropdownMenu:
    def __init__(self, items, parent=None):
        self.parent = parent
        self.items = items
        self.filtered_items = items
        self.selected_item = None
        self.init_gui()


class DMenu:
    def __init__(self, items):
        self.items = items
        self.filtered_items = items
        self.selected_item = None
        self.init_gui()

    def init_gui(self):
        self.win = tk.Toplevel()
        self.win.overrideredirect(True)
        self.win.attributes("-alpha", 0.9)
        self.win.attributes("-topmost", True)
        self.win.attributes("-disabled", True)

        self.input_text_font = tkfont.Font(family="TkFixedFont", size=FONT_SIZE)

        self.input_var = tk.StringVar()
        self.input_var.trace("w", lambda name, index, mode: self.filter_items())
        self.input_field = tk.Entry(
            self.win, textvariable=self.input_var, font=self.input_text_font
        )
        self.input_field.pack(pady=5, padx=5, fill=tk.X)

        self.item_frame = tk.Frame(self.win, bd=0, relief=tk.FLAT)
        self.item_frame.pack(fill=tk.BOTH, expand=True)

        self.win.bind("<Escape>", lambda event: self.win.destroy())
        self.win.bind("<Return>", lambda event: self.select_item())
        self.win.bind("<Up>", lambda event: self.move_selection(-1))
        self.win.bind("<Down>", lambda event: self.move_selection(1))
        self.win.bind("<Configure>", self.handle_resize)

        self.input_field.focus_set()

    def filter_items(self):
        self.filtered_items = []
        for item in self.items:
            if self.input_var.get().lower() in item.lower():
                self.filtered_items.append(item)
        self.redraw_items()

    def redraw_items(self):
        for child in self.item_frame.winfo_children():
            child.destroy()

        for i, item in enumerate(self.filtered_items[:MAX_ITEMS]):
            bg = "white" if i != self.selected_item else "blue"
            label = tk.Label(self.item_frame, text=item, bg=bg)
            label.pack(fill=tk.X)

    def move_selection(self, amount):
        self.selected_item = (
            self.selected_item + amount
            if self.selected_item is not None
            else 0
        )
        if self.selected_item < 0:
            self.selected_item = len(self.filtered_items) - 1
        elif self.selected_item >= len(self.filtered_items):
            self.selected_item = 0
        self.redraw_items()

    def handle_resize(self, event):
        x, y = win32gui.GetCursorPos()
        self.win.geometry(f"+{x - BORDER_WIDTH}+{y - BORDER_WIDTH}")
        self.win.deiconify()
        self.input_field.focus_set()

    def select_item(self):
        if self.selected_item is None:
            self.selected_item = 0
        self.selected_item = min(
            max(self.selected_item, 0), len(self.filtered_items) - 1
        )
        self.win.destroy()

    def run(self):
        self.win.mainloop()
        if self.selected_item is not None:
            return self.filtered_items[self.selected_item]



class DMenu:
    def __init__(self, items, parent=None):
        self.parent = parent
        self.items = items
        self.filtered_items = items
        self.selected_item = None
        self.init_gui()

    def init_gui(self):
        self.root = tk.Tk()
        self.root.withdraw()

        self.width = MAX_WIDTH
        self.height = (self.root.winfo_screenheight() // 2) + (len(self.items) * ITEM_HEIGHT)

        self.root.geometry("{0}x{1}+0+0".format(self.width, self.height))
        self.root.overrideredirect(True)
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        self.main_frame = tk.Frame(self.root, background=BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=tk.YES)

        self.input_text_var = tk.StringVar()
        self.input_text_var.trace("w", lambda name, index, mode, sv=self.input_text_var: self.filter_items())
        self.input_text_font = tk.font.Font(family="TkFixedFont", size=FONT_SIZE)
        self.input_text = tk.Entry(self.main_frame, textvariable=self.input_text_var, font=self.input_text_font, relief=tk.FLAT, bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR, width=self.width//ITEM_WIDTH_RATIO)
        self.input_text.focus()
        self.input_text.pack(side=tk.TOP, padx=PAD_X, pady=PAD_Y)

        self.listbox_frame = tk.Frame(self.main_frame, background=BG_COLOR)
        self.listbox_frame.pack(fill=tk.BOTH, expand=tk.YES)

        self.listbox_scrollbar = tk.Scrollbar(self.listbox_frame)
        self.listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self.listbox_frame, font=("TkFixedFont", FONT_SIZE), relief=tk.FLAT, bg=BG_COLOR, fg=FG_COLOR, selectbackground=SELECT_BG_COLOR, selectforeground=SELECT_FG_COLOR, width=self.width//ITEM_WIDTH_RATIO, height=len(self.items), yscrollcommand=self.listbox_scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        self.listbox.bind("<<ListboxSelect>>", self.handle_selection)
        self.input_text.bind("<KeyRelease>", self.handle_key_release)
        self.input_text.bind("<Escape>", self.close_window)
        self.root.bind("<Configure>", self.handle_resize)
        self.root.bind("<Button-1>", self.handle_click)

        self.listbox_scrollbar.config(command=self.listbox.yview)

        self.filter_items()
        self.update_display()

    def filter_items(self):
        query = self.input_text_var.get().strip()
        self.filtered_items = [i for i in self.items if query in i]
        self.selected_item = self.filtered_items[0] if len(self.filtered_items) > 0 else None

        self.update_display()

    def handle_selection(self, event):
        selected_idx = int(self.listbox.curselection()[0])
        self.selected_item = self.filtered_items[selected_idx]
        self.update_display()
        self.close_window()

    def handle_key_release(self, event):
        if event.keysym == "Down":
            self.move_selection(1)
        elif event.keysym == "Up":
            self.move_selection(-1)
        elif event.keysym == "Return":
            self.close_window()

    def move_selection(self, delta):
        """
        Move the selection by delta positions (positive or negative).
        """
        if len(self.filtered_items) == 0:
            return

        if self.selected_item is None:
            self.selected_item = 0
        else:
            self.selected_item += delta

        if self.selected_item < 0:
            self.selected_item = len(self.filtered_items) - 1
        elif self.selected_item >= len(self.filtered_items):
            self.selected_item = 0

        self.update_listbox()

    def select_item(self, index):
        """
        Select an item from the list.
        """
        self.selected_item = index
        self.update_listbox()
        self.submit_selection()

    def submit_selection(self):
        """
        Submit the selected item and exit the dmenu.
        """
        if self.selected_item is not None:
            selected_text = self.filtered_items[self.selected_item]
            self.win.destroy()
            self.result = selected_text

    def handle_click(self, event):
        """
        Handle clicks on the listbox.
        """
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            self.select_item(index)

    def handle_resize(self, event):
        """
        Handle window resizes.
        """
        self.resize_gui()

    def handle_keypress(self, event):
        key = event.keysym.lower()
        if key == "escape":
            self.close()
        elif key == "return":
            self.select_item()
        elif key == "up":
            self.move_selection(-1)
        elif key == "down":
            self.move_selection(1)
        elif key == "backspace":
            self.filter_string = self.filter_string[:-1]
            self.filter_items()
        elif len(key) == 1:
            self.filter_string += key
            self.filter_items()

    def handle_resize(self, event):
        self.canvas.config(width=event.width, height=event.height)
        self.draw_items()

    def handle_click(self, event):
        item_index = self.get_item_index_from_coords(event.x, event.y)
        if item_index is not None:
            self.select_item(item_index)

    def select_item(self, index=None):
        if index is not None:
            self.selected_item = self.filtered_items[index]
        elif len(self.filtered_items) > 0:
            self.selected_item = self.filtered_items[self.selection_index]
        else:
            self.selected_item = None
        self.close()

    def move_selection(self, delta):
        if len(self.filtered_items) == 0:
            return
        self.selection_index += delta
        if self.selection_index < 0:
            self.selection_index = 0
        elif self.selection_index >= len(self.filtered_items):
            self.selection_index = len(self.filtered_items) - 1
        self.draw_items()

    def filter_items(self):
        self.selection_index = 0
        self.filtered_items = []
        for item in self.items:
            if self.filter_string.lower() in item.lower():
                self.filtered_items.append(item)
        self.draw_items()

    def get_item_index_from_coords(self, x, y):
        if x < 0 or y < 0 or x > self.canvas_width or y > self.canvas_height:
            return None
        item_index = (y - self.border_width) // self.item_height
        if item_index >= len(self.filtered_items):
            return None
        else:
            return item_index

    def draw_items(self):
        """Draw the list of items in the GUI."""
        self.clear_items()

        for i, item in enumerate(self.filtered_items[:self.max_items]):
            bg = self.bg_color
            fg = self.fg_color

            if i == self.selected_index:
                bg, fg = fg, bg

            self.add_item(item, bg=bg, fg=fg)

    def clear_items(self):
        """Remove all items from the GUI."""
        for widget in self.item_frame.winfo_children():
            widget.destroy()

    def add_item(self, item, bg=None, fg=None):
        """Add an item to the GUI."""
        label = tk.Label(self.item_frame, text=item, font=self.item_font,
                         bg=bg, fg=fg, anchor="w")
        label.pack(fill="x", padx=10, pady=5)

    def handle_resize(self, event):
        """Handle window resize events."""
        self.update_size()

    def update_size(self):
        """Update the size of the GUI based on its contents."""
        self.input_text.config(width=self.width)
        self.item_frame.config(width=self.width)
        self.root.geometry("{}x{}".format(self.width, self.height))

    def filter_items(self):
        """Filter the list of items based on the input text."""
        self.filtered_items = [item for item in self.items
                               if self.input_text.get().lower() in item.lower()]
        self.selected_index = 0

    def move_selection(self, delta):
        """Move the selection up or down in the list."""
        self.selected_index = max(0, min(self.selected_index + delta, len(self.filtered_items) - 1))

    def select_item(self):
        """Select the currently highlighted item."""
        self.selected_item = self.filtered_items[self.selected_index]
        self.root.destroy()

    def handle_keypress(self, event):
        """Handle key press events."""
        key = event.keysym

        if key == "Escape":
            self.selected_item = None
            self.root.destroy()
        elif key == "Return":
            self.select_item()
        elif key == "Up":
            self.move_selection(-1)
        elif key == "Down":
            self.move_selection(1)
        else:
            self.filter_items()

        self.draw_items()

    def handle_click(self, event):
        """Handle click events on the items"""
        # Find out which item was clicked and select it
        item_index = event.widget.index("@%d,%d" % (event.x, event.y))
        self.select_item(item_index)

    def handle_keypress(self, event):
        """Handle keypress events"""
        if event.keysym == "Up":
            self.move_selection(-1)
        elif event.keysym == "Down":
            self.move_selection(1)
        elif event.keysym == "Escape":
            self.cancel()
        elif event.keysym == "Return":
            self.done()

    def handle_resize(self, event):
        """Handle window resize events"""
        self.canvas.config(width=event.width, height=event.height)
        self.draw_items()

    def move_selection(self, delta):
        """Move the selection up or down by delta items"""
        new_index = (self.selected_item + delta) % len(self.filtered_items)
        self.select_item(new_index)

    def select_item(self, item_index):
        """Select a new item and update the GUI"""
        self.selected_item = item_index
        self.draw_items()

    def filter_items(self):
        """Filter the items based on the current input"""
        self.filtered_items = [
            item for item in self.items
            if self.input_text.get().lower() in item.lower()
        ]
        self.selected_item = 0 if self.filtered_items else None
        self.draw_items()

    def done(self):
        self.parent.destroy()

    def init_gui(self):
        self.win = tk.Toplevel(self.parent)
        self.win.wm_overrideredirect(True)
        self.win.attributes("-topmost", True)
        self.win.bind("<FocusOut>", self.on_focus_out)
        self.win.bind("<FocusIn>", self.on_focus_in)
        self.win.bind("<Configure>", self.handle_resize)
        self.win.bind("<KeyPress>", self.handle_keypress)
        self.win.bind("<Button-1>", self.handle_click)
        self.win.bind("<Button-3>", self.done)

        self.input_text_var = tk.StringVar()
        self.input_text_var.trace("w", lambda name, index, mode, var=self.input_text_var: self.on_input_text_changed())

        self.input_text_font = tk.font.Font(family="Arial", size=FONT_SIZE)
        self.input_text_bg_color = "#fff"
        self.input_text_fg_color = "#000"

        self.input_text = tk.Entry(self.win, textvariable=self.input_text_var, font=self.input_text_font, bg=self.input_text_bg_color, fg=self.input_text_fg_color, bd=0)
        self.input_text.pack(side="top", fill="x")

        self.listbox_font = tk.font.Font(family="Arial", size=FONT_SIZE)

        self.listbox = tk.Listbox(self.win, font=self.listbox_font, bg=self.input_text_bg_color, fg=self.input_text_fg_color, selectmode="single", bd=0, highlightthickness=0, relief="flat")
        self.listbox.pack(side="top", fill="both", expand=True)

        self.filtered_items = self.items
        self.draw_items()

        self.update_position()

        self.input_text.focus_set()

    def update_position(self):
        x, y = self.get_position()
        self.win.geometry("+%d+%d" % (x, y))

    def get_position(self):
        x = self.parent.winfo_rootx() + self.parent.winfo_width() // 2 - WIN_WIDTH // 2
        y = self.parent.winfo_rooty() + self.parent.winfo_height() // 2 - WIN_HEIGHT // 2
        return x, y

    def filter_items(self):
        filter_text = self.input_text_var.get().lower()
        self.filtered_items = [item for item in self.items if filter_text in item.lower()]
        self.draw_items()

    def draw_items(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill=self.bg_color, outline="")
        num_items = len(self.filtered_items)
        max_display_items = min(num_items, self.max_items)

        # draw each item
        for i in range(max_display_items):
            item_text = self.filtered_items[i]
            text_color = self.text_color

            # highlight selected item
            if i == self.selected_index:
                self.canvas.create_rectangle(0, i * self.item_height, self.width, (i+1) * self.item_height, fill=self.highlight_color, outline="")
                text_color = self.highlight_text_color

            # draw text
            self.canvas.create_text(self.padding_x, i * self.item_height + self.padding_y, text=item_text, anchor="nw", font=self.item_text_font, fill=text_color)

        # add scrollbar if necessary
        if num_items > self.max_items:
            self.scrollbar.place(x=self.width - self.scrollbar_width, y=0, height=self.height)
            scroll_offset = self.selected_index - self.scroll_offset
            scroll_fraction = float(scroll_offset) / float(num_items - self.max_items)
            scrollbar_pos = int(scroll_fraction * (self.height - self.scrollbar_height))
            self.canvas.yview_moveto(scroll_fraction)
            self.scrollbar.place(y=scrollbar_pos)
        else:
            self.scrollbar.place_forget()

    def filter_items(self):
        filter_text = self.input_var.get().lower()
        self.filtered_items = [item for item in self.items if filter_text in item.lower()]
        self.selected_index = 0
        self.scroll_offset = 0
        self.draw_items()

    def handle_keypress(self, event):
        if event.keysym == "Escape":
            self.selected_item = None
            self.parent.destroy()
        elif event.keysym == "Return":
            self.selected_item = self.filtered_items[self.selected_index]
            self.parent.destroy()
        elif event.keysym in ["Up", "Down"]:
            delta = -1 if event.keysym == "Up" else 1
            self.move_selection(delta)
        elif event.keysym in ["Prior", "Next"]:
            delta = -self.max_items if event.keysym == "Prior" else self.max_items
            self.move_selection(delta)

    def handle_click(self, event):
        index = event.y // self.item_height
        if index >= len(self.filtered_items):
            return
        self.selected_index = index
        self.draw_items()

    def move_selection(self, delta):
        self.selected_index = (self.selected_index + delta) % len(self.filtered_items)
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + self.max_items:
            self.scroll_offset = self.selected_index - self.max_items + 1
        self.draw_items()

    def init_gui(self):
        self.width = self.max_width
        self.height = self.max_items * self.item_height

        # create window
        if self.parent is None:
            self.parent = tk.Tk()
        self.parent.title(self.title)
        self.parent.geometry(f"{self.width}x{self.height}")
        self.parent.configure(background=self.bg_color)

        # create canvas
        self.canvas = tk.Canvas(self.parent, width=self.width, height=self.height, highlightthickness=0)
        self.canvas.pack()

        # bind events
        self.parent.bind("<Key>", self.handle_keypress)
        self.parent.bind("<Configure>", self.handle_resize)
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_motion)

        # create input field
        self.input_var = tk.StringVar()
        self.input_var.trace_add("write", self.filter_items)
        self.input_field = tk.Entry(self.parent, textvariable=self.input_var, font=self.input_text_font, bg=self.input_bg_color, fg=self.input_fg_color, width=self.width)
        self.input_field.pack(side="bottom", fill="x")
        self.input_field.focus()

        # create scrollbar
        self.scrollbar = tk.Scrollbar(self.parent, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # set initial state
        self.selected_index = 0
        self.scroll_offset = 0
        self.filter_items()
        self.draw_items()


    def handle_keypress(self, event):
        pass

    def handle_resize(self, event):
        pass

    def handle_click(self, event):
        pass

    def handle_motion(self, event):
        pass

    def filter_items(self, *args):
        pass

    def draw_items(self):
        pass

    def done(self):
        pass
