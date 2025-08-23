"""
Modern Widgets for Panel Flutter Analysis GUI
============================================

Custom widgets with modern styling and enhanced functionality.
"""

import tkinter as tk
from tkinter import ttk
import os


class ModernMenuBar:
    """
    Modern menu bar with enhanced styling.
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.menu = tk.Menu(parent)
        self.menus = {}
        
    def add_menu(self, name):
        """Add a new menu to the menu bar."""
        menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label=name, menu=menu)
        self.menus[name] = MenuWrapper(menu)
        return self.menus[name]


class MenuWrapper:
    """
    Wrapper for menu with enhanced functionality.
    """
    
    def __init__(self, menu):
        self.menu = menu
        
    def add_command(self, label, command=None, accelerator=None, state="normal", image=None):
        """Add a command to the menu."""
        self.menu.add_command(
            label=label,
            command=command,
            accelerator=accelerator,
            state=state,
            image=image
        )
        
    def add_checkbutton(self, label, variable=None, command=None):
        """Add a checkbutton to the menu."""
        self.menu.add_checkbutton(
            label=label,
            variable=variable,
            command=command
        )
        
    def add_separator(self):
        """Add a separator to the menu."""
        self.menu.add_separator()


class ModernToolBar:
    """
    Modern toolbar with icon buttons.
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent, style='Modern.TFrame')
        self.buttons = []
        self.icons = {}
        
    def add_button(self, text, icon_path=None, command=None, tooltip=None):
        """Add a button to the toolbar."""
        if icon_path and os.path.exists(icon_path):
            try:
                image = tk.PhotoImage(file=icon_path)
                self.icons[text] = image  # Keep reference to prevent garbage collection
                button = ttk.Button(
                    self.frame,
                    text=text,
                    image=image,
                    compound=tk.LEFT,
                    command=command,
                    style='Modern.TButton'
                )
            except tk.TclError:
                button = ttk.Button(
                    self.frame,
                    text=text,
                    command=command,
                    style='Modern.TButton'
                )
        else:
            button = ttk.Button(
                self.frame,
                text=text,
                command=command,
                style='Modern.TButton'
            )
            
        button.pack(side=tk.LEFT, padx=2, pady=2)
        
        if tooltip:
            ToolTip(button, tooltip)
            
        self.buttons.append(button)
        return button
        
    def add_separator(self):
        """Add a separator to the toolbar."""
        separator = ttk.Separator(self.frame, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
    def pack(self, **kwargs):
        """Pack the toolbar frame."""
        self.frame.pack(**kwargs)


class ModernStatusBar:
    """
    Modern status bar with progress indicator.
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent, style='Modern.TFrame', relief=tk.SUNKEN, borderwidth=1)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(
            self.frame,
            textvariable=self.status_var,
            style='Modern.TLabel'
        )
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.frame,
            variable=self.progress_var,
            maximum=100,
            length=200,
            style='Modern.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(side=tk.RIGHT, padx=5, pady=2)
        
        # Initially hide progress bar
        self.progress_bar.pack_forget()
        
    def set_status(self, message):
        """Set the status message."""
        self.status_var.set(message)
        
    def set_progress(self, value):
        """Set the progress value (0-100)."""
        if value > 0:
            self.progress_bar.pack(side=tk.RIGHT, padx=5, pady=2)
            self.progress_var.set(value)
        else:
            self.progress_bar.pack_forget()
            
    def pack(self, **kwargs):
        """Pack the status bar frame."""
        self.frame.pack(**kwargs)


class ToolTip:
    """
    Create a tooltip for a given widget.
    """
    
    def __init__(self, widget, text='Widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.tooltip_window = None
        
    def enter(self, event=None):
        """Show tooltip on mouse enter."""
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        
        # Create tooltip window
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            tw,
            text=self.text,
            justify=tk.LEFT,
            background="#FFFFE0",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Segoe UI", "8", "normal")
        )
        label.pack(ipadx=1)
        
    def leave(self, event=None):
        """Hide tooltip on mouse leave."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class LabeledEntry:
    """
    A labeled entry widget with validation.
    """
    
    def __init__(self, parent, label_text, validate_func=None, width=20):
        self.frame = ttk.Frame(parent, style='Modern.TFrame')
        self.validate_func = validate_func
        
        # Label
        self.label = ttk.Label(
            self.frame,
            text=label_text,
            style='Modern.TLabel'
        )
        self.label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Entry
        self.var = tk.StringVar()
        self.entry = ttk.Entry(
            self.frame,
            textvariable=self.var,
            width=width,
            style='Modern.TEntry'
        )
        self.entry.pack(side=tk.LEFT)
        
        # Validation
        if validate_func:
            self.var.trace('w', self.validate)
            
    def validate(self, *args):
        """Validate the entry value."""
        try:
            value = self.var.get()
            if self.validate_func(value):
                self.entry.configure(style='Modern.TEntry')
            else:
                self.entry.configure(style='Error.TEntry')
        except:
            self.entry.configure(style='Error.TEntry')
            
    def get(self):
        """Get the entry value."""
        return self.var.get()
        
    def set(self, value):
        """Set the entry value."""
        self.var.set(str(value))
        
    def pack(self, **kwargs):
        """Pack the frame."""
        self.frame.pack(**kwargs)
        
    def grid(self, **kwargs):
        """Grid the frame."""
        self.frame.grid(**kwargs)


class LabeledSpinbox:
    """
    A labeled spinbox widget.
    """
    
    def __init__(self, parent, label_text, from_=0, to=100, increment=1, width=10):
        self.frame = ttk.Frame(parent, style='Modern.TFrame')
        
        # Label
        self.label = ttk.Label(
            self.frame,
            text=label_text,
            style='Modern.TLabel'
        )
        self.label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Spinbox
        self.var = tk.DoubleVar()
        self.spinbox = tk.Spinbox(
            self.frame,
            textvariable=self.var,
            from_=from_,
            to=to,
            increment=increment,
            width=width,
            font=('Segoe UI', 9)
        )
        self.spinbox.pack(side=tk.LEFT)
        
    def get(self):
        """Get the spinbox value."""
        return self.var.get()
        
    def set(self, value):
        """Set the spinbox value."""
        self.var.set(value)
        
    def pack(self, **kwargs):
        """Pack the frame."""
        self.frame.pack(**kwargs)
        
    def grid(self, **kwargs):
        """Grid the frame."""
        self.frame.grid(**kwargs)


class ParameterTable:
    """
    A table widget for displaying and editing parameters.
    """
    
    def __init__(self, parent, columns):
        self.frame = ttk.Frame(parent, style='Modern.TFrame')
        self.columns = columns
        
        # Create treeview
        self.tree = ttk.Treeview(
            self.frame,
            columns=columns,
            show='headings',
            style='Modern.Treeview'
        )
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
            
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(
            self.frame,
            orient=tk.VERTICAL,
            command=self.tree.yview,
            style='Modern.Vertical.TScrollbar'
        )
        h_scrollbar = ttk.Scrollbar(
            self.frame,
            orient=tk.HORIZONTAL,
            command=self.tree.xview,
            style='Modern.Horizontal.TScrollbar'
        )
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack widgets
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
    def insert_row(self, values):
        """Insert a row into the table."""
        self.tree.insert('', 'end', values=values)
        
    def clear(self):
        """Clear all rows from the table."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
    def get_selected_values(self):
        """Get values from selected row."""
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0])['values']
        return None
        
    def pack(self, **kwargs):
        """Pack the frame."""
        self.frame.pack(**kwargs)
        
    def grid(self, **kwargs):
        """Grid the frame."""
        self.frame.grid(**kwargs)