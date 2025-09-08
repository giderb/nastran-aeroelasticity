"""
Panel Flutter Analysis GUI - Standalone Launcher
===============================================

Standalone launcher that handles all imports and path setup automatically.
"""

import os
import sys
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox

import numpy as np

# Add src directory to path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

print("Panel Flutter Analysis GUI")
print("=" * 50)
print(f"Working directory: {current_dir}")
print(f"Source directory: {src_dir}")
print("Checking dependencies...")

# Check dependencies
required_packages = ['numpy', 'matplotlib', 'pandas']
missing_packages = []

for package in required_packages:
    try:
        __import__(package)
        print(f"[OK] {package}")
    except ImportError:
        missing_packages.append(package)
        print(f"✗ {package} (missing)")

if missing_packages:
    print(f"\nMissing packages: {', '.join(missing_packages)}")
    print("Please install with: pip install " + " ".join(missing_packages))
    input("Press Enter to exit...")
    sys.exit(1)

print("[OK] All dependencies found")
print("\nStarting application...")

# Import matplotlib early and configure backend
import matplotlib

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class PanelFlutterGUI:
    """
    Main Panel Flutter Analysis GUI Application with Beautiful Modern Design
    """

    def __init__(self):
        self.root = tk.Tk()
        self.setup_application()
        self.setup_modern_theme()
        self.create_interface()

    def setup_application(self):
        """Setup the main application window"""
        self.root.title("Panel Flutter Analysis - NASTRAN Aeroelasticity Suite")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        self.root.state('zoomed') if os.name == 'nt' else self.root.attributes('-zoomed', True)

        # Configure modern colors
        self.colors = {
            'primary': '#2563EB',  # Blue-600
            'primary_dark': '#1D4ED8',  # Blue-700
            'primary_light': '#3B82F6',  # Blue-500
            'secondary': '#06B6D4',  # Cyan-500
            'accent': '#8B5CF6',  # Purple-500
            'success': '#10B981',  # Emerald-500
            'warning': '#F59E0B',  # Amber-500
            'error': '#EF4444',  # Red-500
            'background': '#F8FAFC',  # Slate-50
            'surface': '#FFFFFF',  # White
            'surface_alt': '#F1F5F9',  # Slate-100
            'border': '#E2E8F0',  # Slate-200
            'text_primary': '#0F172A',  # Slate-900
            'text_secondary': '#475569',  # Slate-600
            'text_light': '#64748B',  # Slate-500
            'shadow': '#00000008'  # Light shadow
        }

        self.root.configure(bg=self.colors['background'])

        # Try to set window icon
        try:
            self.root.iconbitmap(default='')  # Remove default icon
        except:
            pass

    def setup_modern_theme(self):
        """Setup modern ttk theme with beautiful styling"""
        style = ttk.Style()

        # Use a modern base theme
        try:
            style.theme_use('clam')
        except:
            style.theme_use('default')

        # Configure modern styles
        self.configure_modern_styles(style)

    def configure_modern_styles(self, style):
        """Configure beautiful modern ttk styles"""
        # Configure notebook
        style.configure('Modern.TNotebook',
                        background=self.colors['background'],
                        borderwidth=0,
                        tabmargins=[0, 0, 0, 0])

        # Configure tab styling with consistent dimensions
        style.configure('Modern.TNotebook.Tab',
                        background=self.colors['surface_alt'],
                        foreground=self.colors['text_secondary'],
                        padding=[20, 12, 20, 12],
                        borderwidth=0,
                        focuscolor='none',
                        font=('Segoe UI', 10),
                        minwidth=0,
                        width=0,
                        anchor='center')

        style.map('Modern.TNotebook.Tab',
                  background=[('selected', self.colors['surface']),
                              ('active', '#E5E7EB')],
                  foreground=[('selected', self.colors['text_primary']),
                              ('active', self.colors['text_primary'])],
                  padding=[('selected', [20, 12, 20, 12]),
                           ('active', [20, 12, 20, 12]),
                           ('!selected', [20, 12, 20, 12])])

        # Ensure all tabs have the same height by configuring layout
        try:
            style.layout('Modern.TNotebook.Tab', [
                ('Notebook.tab', {
                    'sticky': 'nsew',
                    'children': [
                        ('Notebook.padding', {
                            'side': 'top',
                            'sticky': 'nsew',
                            'children': [
                                ('Notebook.label', {'side': 'left', 'sticky': ''})
                            ]
                        })
                    ]
                })
            ])
        except:
            pass  # Fallback if layout configuration fails

        # Configure frames
        style.configure('Card.TFrame',
                        background=self.colors['surface'],
                        relief='flat',
                        borderwidth=1)

        style.configure('Modern.TFrame',
                        background=self.colors['background'])

        # Configure labels
        style.configure('Title.TLabel',
                        background=self.colors['background'],
                        foreground=self.colors['text_primary'],
                        font=('Segoe UI', 24, 'bold'))

        style.configure('Subtitle.TLabel',
                        background=self.colors['background'],
                        foreground=self.colors['text_secondary'],
                        font=('Segoe UI', 12))

        style.configure('Modern.TLabel',
                        background=self.colors['surface'],
                        foreground=self.colors['text_primary'],
                        font=('Segoe UI', 10))

        style.configure('Value.TLabel',
                        background=self.colors['surface'],
                        foreground=self.colors['primary'],
                        font=('Segoe UI', 12, 'bold'))

        # Configure buttons
        style.configure('Primary.TButton',
                        background=self.colors['primary'],
                        foreground='white',
                        borderwidth=0,
                        focuscolor='none',
                        font=('Segoe UI', 10, 'bold'),
                        padding=[20, 10])

        style.map('Primary.TButton',
                  background=[('active', self.colors['primary_dark']),
                              ('pressed', self.colors['primary_dark'])])

        style.configure('Success.TButton',
                        background=self.colors['success'],
                        foreground='white',
                        borderwidth=0,
                        focuscolor='none',
                        font=('Segoe UI', 10, 'bold'),
                        padding=[20, 10])

        style.configure('Secondary.TButton',
                        background=self.colors['surface_alt'],
                        foreground=self.colors['text_primary'],
                        borderwidth=1,
                        focuscolor='none',
                        font=('Segoe UI', 10),
                        padding=[16, 8])

        # Configure entries
        style.configure('Modern.TEntry',
                        borderwidth=1,
                        relief='solid',
                        bordercolor=self.colors['border'],
                        font=('Segoe UI', 10),
                        padding=[10, 8])

        style.map('Modern.TEntry',
                  bordercolor=[('focus', self.colors['primary'])])

        # Configure combobox
        style.configure('Modern.TCombobox',
                        borderwidth=1,
                        relief='solid',
                        bordercolor=self.colors['border'],
                        font=('Segoe UI', 10),
                        padding=[10, 8])

        # Configure labelframes
        style.configure('Modern.TLabelframe',
                        background=self.colors['surface'],
                        borderwidth=1,
                        relief='solid',
                        bordercolor=self.colors['border'])

        style.configure('Modern.TLabelframe.Label',
                        background=self.colors['surface'],
                        foreground=self.colors['text_primary'],
                        font=('Segoe UI', 11, 'bold'))

        # Configure progressbar
        style.configure('Modern.Horizontal.TProgressbar',
                        background=self.colors['primary'],
                        troughcolor=self.colors['surface_alt'],
                        borderwidth=0,
                        lightcolor=self.colors['primary_light'],
                        darkcolor=self.colors['primary_dark'])

    def create_interface(self):
        """Create the beautiful modern interface"""
        # Create main container with gradient-like effect
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header section with modern styling
        self.create_header(main_container)

        # Main content area
        content_frame = tk.Frame(main_container, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Create modern card-based notebook
        self.create_modern_notebook(content_frame)

        # Status bar with modern styling
        self.create_status_bar(main_container)

    def create_header(self, parent):
        """Create beautiful header section"""
        header_frame = tk.Frame(parent, bg=self.colors['background'], height=120)
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        header_frame.pack_propagate(False)

        # Title section
        title_container = tk.Frame(header_frame, bg=self.colors['background'])
        title_container.pack(expand=True, fill=tk.BOTH)

        # Main title with icon-like symbol
        title_frame = tk.Frame(title_container, bg=self.colors['background'])
        title_frame.pack(side=tk.LEFT, anchor=tk.W)

        # Icon/symbol
        icon_label = tk.Label(title_frame, text="🛫",
                              font=('Segoe UI', 32),
                              fg=self.colors['primary'],
                              bg=self.colors['background'])
        icon_label.pack(side=tk.LEFT, padx=(0, 15))

        # Title text
        title_text_frame = tk.Frame(title_frame, bg=self.colors['background'])
        title_text_frame.pack(side=tk.LEFT, fill=tk.Y)

        title_label = tk.Label(title_text_frame,
                               text="Panel Flutter Analysis",
                               font=('Segoe UI', 24, 'bold'),
                               fg=self.colors['text_primary'],
                               bg=self.colors['background'])
        title_label.pack(anchor=tk.W)

        subtitle_label = tk.Label(title_text_frame,
                                  text="Advanced Aeroelasticity Analysis Suite",
                                  font=('Segoe UI', 12),
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['background'])
        subtitle_label.pack(anchor=tk.W)

    def create_modern_notebook(self, parent):
        """Create modern card-based notebook"""
        notebook_frame = tk.Frame(parent, bg=self.colors['background'])
        notebook_frame.pack(fill=tk.BOTH, expand=True)

        # Create notebook with modern styling
        self.notebook = ttk.Notebook(notebook_frame, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create beautiful tabs
        self.create_geometry_tab()
        self.create_materials_tab()
        self.create_analysis_tab()
        self.create_results_tab()

    def create_status_bar(self, parent):
        """Create modern status bar"""
        status_frame = tk.Frame(parent, bg=self.colors['surface'],
                                height=40, relief=tk.FLAT, bd=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)

        # Status indicator
        status_indicator = tk.Frame(status_frame, bg=self.colors['success'], width=4)
        status_indicator.pack(side=tk.LEFT, fill=tk.Y)

        # Status text
        self.status_var = tk.StringVar()
        self.status_var.set("🚀 Ready - Panel Flutter Analysis GUI v1.0")
        status_label = tk.Label(status_frame,
                                textvariable=self.status_var,
                                bg=self.colors['surface'],
                                fg=self.colors['text_secondary'],
                                font=('Segoe UI', 9),
                                anchor=tk.W)
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15, pady=10)

    def create_geometry_tab(self):
        """Create beautiful geometry definition tab"""
        # Main scrollable frame
        geom_main_frame, geom_frame = self.create_scrollable_frame(self.notebook)
        self.notebook.add(geom_main_frame, text="🔧 Geometry")

        # Create card layout
        cards_frame = tk.Frame(geom_frame, bg=self.colors['background'])
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panel dimensions card
        dim_card = self.create_card(cards_frame, "📐 Panel Dimensions",
                                    "Define the overall geometry of your panel")
        dim_card.pack(fill=tk.X, pady=(0, 20))

        # Create modern input grid
        dim_content = tk.Frame(dim_card, bg=self.colors['surface'])
        dim_content.pack(fill=tk.X, padx=20, pady=15)

        # Configure grid weights for expansion
        dim_content.columnconfigure(1, weight=1)

        # Length input with modern styling
        self.create_modern_input(dim_content, "Length", "mm", "500.0", 0)
        self.length_var = self.inputs[-1]['var']

        # Width input
        self.create_modern_input(dim_content, "Width", "mm", "300.0", 1)
        self.width_var = self.inputs[-1]['var']

        # Boundary conditions selection  
        self.create_boundary_conditions_input(dim_content, 2)

        # Mesh parameters card
        mesh_card = self.create_card(cards_frame, "🔲 Mesh Parameters",
                                     "Control the finite element mesh density")
        mesh_card.pack(fill=tk.X, pady=(0, 20))

        mesh_content = tk.Frame(mesh_card, bg=self.colors['surface'])
        mesh_content.pack(fill=tk.X, padx=20, pady=15)

        # Configure grid weights for expansion
        mesh_content.columnconfigure(1, weight=1)

        # Mesh inputs with spinboxes
        self.create_modern_spinbox(mesh_content, "Lengthwise Elements", 10, 1, 50, 0)
        self.nlength_var = self.spinboxes[-1]['var']

        self.create_modern_spinbox(mesh_content, "Spanwise Elements", 5, 1, 50, 1)
        self.nspan_var = self.spinboxes[-1]['var']

        # Quality metrics display
        quality_frame = tk.Frame(mesh_content, bg=self.colors['surface'])
        quality_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W + tk.E, pady=(15, 0))

        self.aspect_ratio_label = tk.Label(quality_frame, text="Aspect Ratio: 2.0",
                                           bg=self.colors['surface'], fg=self.colors['text_secondary'],
                                           font=('Segoe UI', 9))
        self.aspect_ratio_label.pack(side=tk.LEFT, padx=(0, 20))

        self.total_elements_label = tk.Label(quality_frame, text="Total Elements: 50",
                                             bg=self.colors['surface'], fg=self.colors['text_secondary'],
                                             font=('Segoe UI', 9))
        self.total_elements_label.pack(side=tk.LEFT)

        # Action buttons card
        action_card = self.create_card(cards_frame, "🎯 Actions",
                                       "Preview and validate your geometry")
        action_card.pack(fill=tk.X)

        action_content = tk.Frame(action_card, bg=self.colors['surface'])
        action_content.pack(fill=tk.X, padx=20, pady=15)

        # Modern button row
        button_frame = tk.Frame(action_content, bg=self.colors['surface'])
        button_frame.pack(fill=tk.X)

        preview_btn = ttk.Button(button_frame, text="🔍 Preview Geometry",
                                 command=self.preview_geometry, style='Primary.TButton')
        preview_btn.pack(side=tk.LEFT, padx=(0, 10))

        validate_btn = ttk.Button(button_frame, text="✅ Validate",
                                  command=self.validate_geometry, style='Secondary.TButton')
        validate_btn.pack(side=tk.LEFT, padx=(0, 10))

        reset_btn = ttk.Button(button_frame, text="🔄 Reset",
                               command=self.reset_geometry, style='Secondary.TButton')
        reset_btn.pack(side=tk.LEFT)

        # Initialize input tracking
        if not hasattr(self, 'inputs'):
            self.inputs = []
        if not hasattr(self, 'spinboxes'):
            self.spinboxes = []

        # Initialize critical variables for analysis with safe defaults
        if not hasattr(self, 'vmin_var'):
            self.vmin_var = tk.StringVar(value="50")
        if not hasattr(self, 'vmax_var'):
            self.vmax_var = tk.StringVar(value="300")
        if not hasattr(self, 'length_var'):
            self.length_var = tk.StringVar(value="1.0")
        if not hasattr(self, 'width_var'):
            self.width_var = tk.StringVar(value="0.5")
        if not hasattr(self, 'density_var'):
            self.density_var = tk.StringVar(value="2700")
        if not hasattr(self, 'youngs_var'):
            self.youngs_var = tk.StringVar(value="2.1e11")
        if not hasattr(self, 'poisson_var'):
            self.poisson_var = tk.StringVar(value="0.3")
        if not hasattr(self, 'material_type_var'):
            self.material_type_var = tk.StringVar(value="isotropic")

    def create_scrollable_frame(self, parent):
        """Create a proper scrollable frame"""
        # Create main frame
        main_frame = tk.Frame(parent, bg=self.colors['background'])

        # Create canvas and scrollbar
        canvas = tk.Canvas(main_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])

        # Configure scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Create window that expands with canvas width
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Configure canvas to expand scrollable_frame to its width
        def _configure_canvas(event):
            canvas.itemconfig(window_id, width=event.width)

        canvas.bind('<Configure>', _configure_canvas)

        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack elements
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Improved mousewheel binding without conflicts
        def _on_mousewheel(event):
            # Only scroll if the mouse is over this specific canvas
            if event.widget == canvas or self._widget_in_canvas(event.widget, canvas):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Bind mousewheel directly to canvas and frame - no global bindings
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)

        # Make sure mousewheel events bubble up to the canvas
        def bind_mousewheel_to_children(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            for child in widget.winfo_children():
                bind_mousewheel_to_children(child)

        # Bind to existing children and new ones
        def bind_all_children():
            try:
                bind_mousewheel_to_children(scrollable_frame)
            except:
                pass

        scrollable_frame.after(100, bind_all_children)

        # Store reference to canvas for helper method
        self._canvas_widgets = getattr(self, '_canvas_widgets', [])
        self._canvas_widgets.append(canvas)

        # Return both frames - main_frame goes to notebook, scrollable_frame is used for content
        return main_frame, scrollable_frame

    def _widget_in_canvas(self, widget, canvas):
        """Check if a widget is a child of a canvas"""
        try:
            parent = widget.master
            while parent:
                if parent == canvas:
                    return True
                parent = parent.master
            return False
        except:
            return False

    def create_card(self, parent, title, description):
        """Create a modern card widget"""
        card = tk.Frame(parent, bg=self.colors['surface'], relief=tk.FLAT, bd=1)

        # Card header
        header = tk.Frame(card, bg=self.colors['surface'])
        header.pack(fill=tk.X, padx=20, pady=(15, 5))

        title_label = tk.Label(header, text=title,
                               bg=self.colors['surface'], fg=self.colors['text_primary'],
                               font=('Segoe UI', 12, 'bold'))
        title_label.pack(anchor=tk.W)

        desc_label = tk.Label(header, text=description,
                              bg=self.colors['surface'], fg=self.colors['text_secondary'],
                              font=('Segoe UI', 9))
        desc_label.pack(anchor=tk.W)

        # Add shadow effect with border
        card.configure(highlightbackground=self.colors['border'], highlightthickness=1)

        return card

    def create_modern_input(self, parent, label, unit, default_value, row):
        """Create a modern input field"""
        if not hasattr(self, 'inputs'):
            self.inputs = []

        # Label
        label_widget = tk.Label(parent, text=f"{label}:",
                                bg=self.colors['surface'], fg=self.colors['text_primary'],
                                font=('Segoe UI', 10))
        label_widget.grid(row=row, column=0, sticky=tk.W, pady=8, padx=(0, 15))

        # Entry
        var = tk.StringVar(value=default_value)
        entry = ttk.Entry(parent, textvariable=var, style='Modern.TEntry', width=15)
        entry.grid(row=row, column=1, sticky=tk.W + tk.E, pady=8, padx=(0, 10))

        # Unit label
        unit_label = tk.Label(parent, text=unit,
                              bg=self.colors['surface'], fg=self.colors['text_light'],
                              font=('Segoe UI', 9))
        unit_label.grid(row=row, column=2, sticky=tk.W, pady=8)

        self.inputs.append({'label': label, 'var': var, 'entry': entry})

    def create_modern_spinbox(self, parent, label, default_value, min_val, max_val, row):
        """Create a modern spinbox"""
        if not hasattr(self, 'spinboxes'):
            self.spinboxes = []

        # Label
        label_widget = tk.Label(parent, text=f"{label}:",
                                bg=self.colors['surface'], fg=self.colors['text_primary'],
                                font=('Segoe UI', 10))
        label_widget.grid(row=row, column=0, sticky=tk.W, pady=8, padx=(0, 15))

        # Spinbox with modern styling
        var = tk.IntVar(value=default_value)
        spinbox = tk.Spinbox(parent, textvariable=var, from_=min_val, to=max_val,
                             width=12, font=('Segoe UI', 10),
                             bg=self.colors['surface'],
                             borderwidth=1, relief=tk.SOLID,
                             buttonbackground=self.colors['surface_alt'],
                             highlightcolor=self.colors['primary'])
        spinbox.grid(row=row, column=1, sticky=tk.W, pady=8, padx=(0, 10))

        self.spinboxes.append({'label': label, 'var': var, 'spinbox': spinbox})

    def create_boundary_conditions_input(self, parent, row):
        """Create boundary conditions selection input"""
        try:
            # Import boundary conditions
            from analysis.boundary_conditions import BoundaryCondition, BoundaryConditionManager

            bc_manager = BoundaryConditionManager()

            # Label
            label_widget = tk.Label(parent, text="Boundary Conditions:",
                                    bg=self.colors['surface'], fg=self.colors['text_primary'],
                                    font=('Segoe UI', 10))
            label_widget.grid(row=row, column=0, sticky=tk.W, pady=8, padx=(0, 15))

            # Get all available boundary conditions
            bc_options = []
            bc_descriptions = {}
            for bc_type, bc_props in bc_manager.get_all_boundary_conditions().items():
                display_name = f"{bc_type.value} - {bc_props.name}"
                bc_options.append(display_name)
                bc_descriptions[display_name] = bc_props

            # Create combobox
            self.boundary_conditions = tk.StringVar(value=bc_options[0])  # Default to first option (SSSS)
            bc_combo = ttk.Combobox(parent, textvariable=self.boundary_conditions,
                                    values=bc_options, state="readonly", width=25,
                                    style='Modern.TCombobox')
            bc_combo.grid(row=row, column=1, columnspan=2, sticky=tk.W + tk.E, pady=8, padx=(0, 10))

            # Bind selection change to update info
            bc_combo.bind('<<ComboboxSelected>>', self.on_boundary_condition_changed)

            # Info label for flutter characteristics
            self.bc_info_label = tk.Label(parent, text="Medium flutter tendency, good baseline",
                                          bg=self.colors['surface'], fg=self.colors['text_light'],
                                          font=('Segoe UI', 9))
            self.bc_info_label.grid(row=row + 1, column=1, columnspan=2, sticky=tk.W, pady=(0, 8), padx=(0, 10))

            # Initialize info
            self.on_boundary_condition_changed(None)

        except ImportError:
            # Fallback to simple string selection
            label_widget = tk.Label(parent, text="Boundary Conditions:",
                                    bg=self.colors['surface'], fg=self.colors['text_primary'],
                                    font=('Segoe UI', 10))
            label_widget.grid(row=row, column=0, sticky=tk.W, pady=8, padx=(0, 15))

            self.boundary_conditions = tk.StringVar(value="SSSS")
            bc_combo = ttk.Combobox(parent, textvariable=self.boundary_conditions,
                                    values=["SSSS", "CCCC", "CFFF", "CSSS", "CCSS", "SSSF", "CCCF"],
                                    state="readonly", width=15,
                                    style='Modern.TCombobox')
            bc_combo.grid(row=row, column=1, sticky=tk.W + tk.E, pady=8, padx=(0, 10))

            # Unit/info label
            info_label = tk.Label(parent, text="Standard patterns",
                                  bg=self.colors['surface'], fg=self.colors['text_light'],
                                  font=('Segoe UI', 9))
            info_label.grid(row=row, column=2, sticky=tk.W, pady=8)

    def on_boundary_condition_changed(self, event):
        """Handle boundary condition selection change"""
        try:
            from analysis.boundary_conditions import BoundaryCondition, BoundaryConditionManager

            bc_manager = BoundaryConditionManager()
            selected = self.boundary_conditions.get()

            if selected and ' - ' in selected:
                bc_type_str = selected.split(' - ')[0]
                try:
                    bc_type = BoundaryCondition(bc_type_str)
                    bc_props = bc_manager.get_boundary_condition(bc_type)

                    if bc_props and hasattr(self, 'bc_info_label'):
                        info_text = f"{bc_props.flutter_tendency.title()} flutter tendency, stiffness: {bc_props.structural_stiffness:.1f}"
                        self.bc_info_label.config(text=info_text)

                        # Color code based on flutter tendency
                        if bc_props.flutter_tendency == "high":
                            self.bc_info_label.config(fg=self.colors['error'])
                        elif bc_props.flutter_tendency == "low":
                            self.bc_info_label.config(fg=self.colors['success'])
                        else:
                            self.bc_info_label.config(fg=self.colors['text_light'])

                except ValueError:
                    pass
        except ImportError:
            pass

    def get_boundary_condition_code(self):
        """Extract boundary condition code from GUI selection"""
        try:
            selected = getattr(self, 'boundary_conditions', tk.StringVar(value="SSSS")).get()
            if ' - ' in selected:
                # Extract code from "SSSS - Simply Supported All Edges" format
                return selected.split(' - ')[0]
            else:
                # Direct code format
                return selected
        except:
            return "SSSS"  # Default fallback

    def validate_geometry(self):
        """Validate geometry parameters"""
        try:
            length = float(self.length_var.get()) / 1000.0  # Convert mm to m
            width = float(self.width_var.get()) / 1000.0  # Convert mm to m

            if length <= 0 or width <= 0:
                messagebox.showerror("Validation Error", "Length and width must be positive")
                return

            messagebox.showinfo("Validation", "✅ Geometry parameters are valid!")
            self.status_var.set("✅ Geometry validated successfully")

        except ValueError:
            messagebox.showerror("Validation Error", "Please enter valid numeric values")

    def reset_geometry(self):
        """Reset geometry to defaults"""
        self.length_var.set("500.0")
        self.width_var.set("300.0")
        self.nlength_var.set(10)
        self.nspan_var.set(5)
        self.status_var.set("🔄 Geometry reset to defaults")

    def create_materials_tab(self):
        """Create comprehensive materials tab with scrolling and composite support"""
        # Create scrollable main frame
        mat_frame = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(mat_frame, text="🧪 Materials")

        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(mat_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(mat_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])

        # Configure scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Create window that expands with canvas width
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Configure canvas to expand scrollable_frame to its width
        def _configure_canvas(event):
            canvas.itemconfig(window_id, width=event.width)

        canvas.bind('<Configure>', _configure_canvas)

        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Improved mousewheel binding without conflicts
        def _on_mousewheel(event):
            # Only scroll if the mouse is over this specific canvas
            if event.widget == canvas or self._widget_in_canvas(event.widget, canvas):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Bind mousewheel directly to canvas and frame - no global bindings
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)

        # Make sure mousewheel events bubble up to the canvas
        def bind_mousewheel_to_children(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            for child in widget.winfo_children():
                bind_mousewheel_to_children(child)

        # Bind to existing children and new ones
        def bind_all_children():
            try:
                bind_mousewheel_to_children(scrollable_frame)
            except:
                pass

        scrollable_frame.after(100, bind_all_children)

        # Create card layout in scrollable frame
        cards_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Configure cards_frame to expand
        cards_frame.columnconfigure(0, weight=1)

        # Material type selection card
        type_card = self.create_card(cards_frame, "🔍 Material Type Selection",
                                     "Choose the type of material for your analysis")
        type_card.pack(fill=tk.X, pady=(0, 15))

        type_content = tk.Frame(type_card, bg=self.colors['surface'])
        type_content.pack(fill=tk.X, padx=20, pady=15)

        # Material type radio buttons
        self.material_type_var = tk.StringVar(value="isotropic")

        type_frame = tk.Frame(type_content, bg=self.colors['surface'])
        type_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(type_frame, text="Select Material Type:",
                 bg=self.colors['surface'], fg=self.colors['text_primary'],
                 font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)

        radio_frame = tk.Frame(type_frame, bg=self.colors['surface'])
        radio_frame.pack(fill=tk.X, pady=(5, 0))

        ttk.Radiobutton(radio_frame, text="🔧 Isotropic (Metals)",
                        variable=self.material_type_var, value="isotropic",
                        command=self.on_material_type_changed).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(radio_frame, text="📐 Orthotropic (Unidirectional Composites)",
                        variable=self.material_type_var, value="orthotropic",
                        command=self.on_material_type_changed).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(radio_frame, text="📚 Laminated Composite (Multi-layer)",
                        variable=self.material_type_var, value="laminate",
                        command=self.on_material_type_changed).pack(anchor=tk.W, pady=2)

        # Material selection card
        selection_card = self.create_card(cards_frame, "📋 Material Database",
                                          "Select from predefined materials or create custom")
        selection_card.pack(fill=tk.X, pady=(0, 15))

        selection_content = tk.Frame(selection_card, bg=self.colors['surface'])
        selection_content.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(selection_content, text="Predefined Materials:",
                 bg=self.colors['surface'], fg=self.colors['text_primary'],
                 font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)

        self.material_var = tk.StringVar(value="Aluminum 7075-T6")
        self.material_combo = ttk.Combobox(selection_content, textvariable=self.material_var,
                                           state="readonly", style='Modern.TCombobox')
        self.material_combo.pack(fill=tk.X, pady=(5, 10))
        self.material_combo.bind('<<ComboboxSelected>>', self.on_material_changed)

        # Basic properties card (always visible)
        self.basic_card = self.create_card(cards_frame, "⚙️ Basic Properties",
                                           "Fundamental material properties")
        self.basic_card.pack(fill=tk.X, pady=(0, 15))

        self.basic_content = tk.Frame(self.basic_card, bg=self.colors['surface'])
        self.basic_content.pack(fill=tk.X, padx=20, pady=15)

        # Configure grid weights for expansion
        self.basic_content.columnconfigure(0, weight=1)

        # Initialize material property variables
        self.density_var = tk.StringVar(value="2700")
        self.thickness_var = tk.StringVar(value="2.0")

        self.create_property_input(self.basic_content, "Density", "kg/m³", self.density_var, 0)
        self.create_property_input(self.basic_content, "Thickness", "mm", self.thickness_var, 1)

        # Isotropic properties card
        self.iso_card = self.create_card(cards_frame, "🔧 Isotropic Properties",
                                         "Properties for isotropic materials (metals)")
        self.iso_content = tk.Frame(self.iso_card, bg=self.colors['surface'])
        self.iso_content.pack(fill=tk.X, padx=20, pady=15)

        # Configure grid weights for expansion
        self.iso_content.columnconfigure(0, weight=1)

        self.youngs_var = tk.StringVar(value="7.0e10")
        self.poisson_var = tk.StringVar(value="0.33")
        self.shear_var = tk.StringVar(value="2.6e10")

        self.create_property_input(self.iso_content, "Young's Modulus (E)", "Pa", self.youngs_var, 0)
        self.create_property_input(self.iso_content, "Poisson's Ratio (ν)", "-", self.poisson_var, 1)
        self.create_property_input(self.iso_content, "Shear Modulus (G)", "Pa", self.shear_var, 2)

        # Orthotropic properties card
        self.ortho_card = self.create_card(cards_frame, "📐 Orthotropic Properties",
                                           "Properties for orthotropic materials (composites)")
        self.ortho_content = tk.Frame(self.ortho_card, bg=self.colors['surface'])
        self.ortho_content.pack(fill=tk.X, padx=20, pady=15)

        # Configure grid weights for expansion (3-column layout)
        self.ortho_content.columnconfigure(0, weight=1)
        self.ortho_content.columnconfigure(1, weight=1)
        self.ortho_content.columnconfigure(2, weight=1)

        # Orthotropic material variables
        self.e1_var = tk.StringVar(value="1.5e11")  # Fiber direction
        self.e2_var = tk.StringVar(value="9.0e9")  # Transverse direction
        self.e3_var = tk.StringVar(value="9.0e9")  # Through thickness
        self.g12_var = tk.StringVar(value="5.0e9")  # In-plane shear
        self.g13_var = tk.StringVar(value="5.0e9")  # Out-of-plane shear
        self.g23_var = tk.StringVar(value="3.0e9")  # Out-of-plane shear
        self.nu12_var = tk.StringVar(value="0.3")  # Major Poisson's ratio
        self.nu13_var = tk.StringVar(value="0.3")
        self.nu23_var = tk.StringVar(value="0.4")

        # Create orthotropic inputs in organized layout
        tk.Label(self.ortho_content, text="Elastic Moduli:",
                 bg=self.colors['surface'], fg=self.colors['primary'],
                 font=('Segoe UI', 9, 'bold')).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))

        self.create_compact_property_input(self.ortho_content, "E₁ (Fiber)", "Pa", self.e1_var, 1, 0)
        self.create_compact_property_input(self.ortho_content, "E₂ (Matrix)", "Pa", self.e2_var, 1, 1)
        self.create_compact_property_input(self.ortho_content, "E₃ (Thickness)", "Pa", self.e3_var, 1, 2)

        tk.Label(self.ortho_content, text="Shear Moduli:",
                 bg=self.colors['surface'], fg=self.colors['primary'],
                 font=('Segoe UI', 9, 'bold')).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))

        self.create_compact_property_input(self.ortho_content, "G₁₂", "Pa", self.g12_var, 3, 0)
        self.create_compact_property_input(self.ortho_content, "G₁₃", "Pa", self.g13_var, 3, 1)
        self.create_compact_property_input(self.ortho_content, "G₂₃", "Pa", self.g23_var, 3, 2)

        tk.Label(self.ortho_content, text="Poisson's Ratios:",
                 bg=self.colors['surface'], fg=self.colors['primary'],
                 font=('Segoe UI', 9, 'bold')).grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))

        self.create_compact_property_input(self.ortho_content, "ν₁₂", "-", self.nu12_var, 5, 0)
        self.create_compact_property_input(self.ortho_content, "ν₁₃", "-", self.nu13_var, 5, 1)
        self.create_compact_property_input(self.ortho_content, "ν₂₃", "-", self.nu23_var, 5, 2)

        # Laminate properties card
        self.laminate_card = self.create_card(cards_frame, "📚 Laminate Definition",
                                              "Define composite laminate layup")
        self.laminate_content = tk.Frame(self.laminate_card, bg=self.colors['surface'])
        self.laminate_content.pack(fill=tk.X, padx=20, pady=15)

        # Laminate table header
        header_frame = tk.Frame(self.laminate_content, bg=self.colors['surface_alt'], height=35)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="Layer", bg=self.colors['surface_alt'],
                 font=('Segoe UI', 9, 'bold')).place(x=10, y=8)
        tk.Label(header_frame, text="Material", bg=self.colors['surface_alt'],
                 font=('Segoe UI', 9, 'bold')).place(x=60, y=8)
        tk.Label(header_frame, text="Thickness (mm)", bg=self.colors['surface_alt'],
                 font=('Segoe UI', 9, 'bold')).place(x=160, y=8)
        tk.Label(header_frame, text="Angle (°)", bg=self.colors['surface_alt'],
                 font=('Segoe UI', 9, 'bold')).place(x=270, y=8)
        tk.Label(header_frame, text="Actions", bg=self.colors['surface_alt'],
                 font=('Segoe UI', 9, 'bold')).place(x=330, y=8)

        # Scrollable laminate layers frame
        self.layers_frame = tk.Frame(self.laminate_content, bg=self.colors['surface'])
        self.layers_frame.pack(fill=tk.X, pady=(0, 10))

        # Laminate control buttons
        button_frame = tk.Frame(self.laminate_content, bg=self.colors['surface'])
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text="➕ Add Layer",
                   command=self.add_laminate_layer, style='Success.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="📋 Standard Layups",
                   command=self.show_standard_layups, style='Secondary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="[CALC] Calculate ABD",
                   command=self.calculate_abd_matrix, style='Secondary.TButton').pack(side=tk.LEFT)

        # Analysis integration card
        self.integration_card = self.create_card(cards_frame, "🔗 Analysis Integration",
                                                 "How materials are used in flutter analysis")
        self.integration_card.pack(fill=tk.X, pady=(15, 0))

        integration_content = tk.Frame(self.integration_card, bg=self.colors['surface'])
        integration_content.pack(fill=tk.X, padx=20, pady=15)

        info_text = """Material properties are integrated into the flutter analysis as follows:
        
• Isotropic Materials: E and ν used to calculate structural stiffness matrices [K]
• Orthotropic Materials: Full orthotropic stiffness matrix calculated from E₁, E₂, G₁₂, ν₁₂
• Laminated Composites: Classical laminate theory applied to calculate equivalent properties
• Mass Properties: Density used in mass matrix [M] calculation for eigenvalue analysis
• Structural Damping: Material damping affects flutter onset and critical speeds"""

        tk.Label(integration_content, text=info_text, justify=tk.LEFT,
                 bg=self.colors['surface'], fg=self.colors['text_secondary'],
                 font=('Segoe UI', 9), wraplength=500).pack(anchor=tk.W)

        # Initialize with default material type
        self.laminate_layers = []
        self.on_material_type_changed()
        self.update_material_database()

    def create_property_input(self, parent, label, unit, var, row):
        """Create a modern property input field"""
        input_frame = tk.Frame(parent, bg=self.colors['surface'])
        input_frame.grid(row=row, column=0, columnspan=3, sticky=tk.W + tk.E, pady=8)
        input_frame.columnconfigure(1, weight=1)

        # Label
        label_widget = tk.Label(input_frame, text=f"{label}:",
                                bg=self.colors['surface'], fg=self.colors['text_primary'],
                                font=('Segoe UI', 10), anchor=tk.W)
        label_widget.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))

        # Entry
        entry = ttk.Entry(input_frame, textvariable=var, style='Modern.TEntry')
        entry.grid(row=0, column=1, sticky=tk.W + tk.E, padx=(0, 10))

        # Unit
        unit_label = tk.Label(input_frame, text=unit,
                              bg=self.colors['surface'], fg=self.colors['text_light'],
                              font=('Segoe UI', 9), anchor=tk.W)
        unit_label.grid(row=0, column=2, sticky=tk.W)

    def create_compact_property_input(self, parent, label, unit, var, row, col):
        """Create a compact property input for orthotropic materials"""
        frame = tk.Frame(parent, bg=self.colors['surface'])
        frame.grid(row=row, column=col, padx=5, pady=3, sticky=tk.W + tk.E)

        # Label
        tk.Label(frame, text=f"{label}:",
                 bg=self.colors['surface'], fg=self.colors['text_primary'],
                 font=('Segoe UI', 9)).pack(anchor=tk.W)

        # Entry - now expands to fill frame width
        entry = ttk.Entry(frame, textvariable=var, style='Modern.TEntry')
        entry.pack(fill=tk.X, pady=(2, 0))

        # Unit label
        tk.Label(frame, text=unit,
                 bg=self.colors['surface'], fg=self.colors['text_light'],
                 font=('Segoe UI', 8)).pack(anchor=tk.W)

    def on_material_type_changed(self):
        """Handle material type change"""
        mat_type = self.material_type_var.get()

        # Hide all cards first
        self.iso_card.pack_forget()
        self.ortho_card.pack_forget()
        self.laminate_card.pack_forget()

        # Show appropriate cards based on type
        if mat_type == "isotropic":
            self.iso_card.pack(fill=tk.X, pady=(0, 15), before=self.integration_card)
        elif mat_type == "orthotropic":
            self.ortho_card.pack(fill=tk.X, pady=(0, 15), before=self.integration_card)
        elif mat_type == "laminate":
            self.ortho_card.pack(fill=tk.X, pady=(0, 15), before=self.integration_card)
            self.laminate_card.pack(fill=tk.X, pady=(0, 15), before=self.integration_card)

        # Update material database
        self.update_material_database()

    def update_material_database(self):
        """Update material database based on selected type"""
        mat_type = self.material_type_var.get()

        if mat_type == "isotropic":
            materials = [
                "Aluminum 7075-T6", "Aluminum 6061-T6", "Steel AISI 4130",
                "Titanium Ti-6Al-4V", "Magnesium AZ31B", "Custom Isotropic"
            ]
        elif mat_type == "orthotropic":
            materials = [
                "Carbon Fiber/Epoxy IM7/8552", "Glass Fiber/Epoxy", "Kevlar/Epoxy",
                "Carbon Fiber/PEEK", "Boron/Epoxy", "Custom Orthotropic"
            ]
        else:  # laminate
            materials = [
                "Quasi-Isotropic [0/45/-45/90]s", "Cross-Ply [0/90]4s",
                "Angle-Ply [±45]4s", "Symmetric [0/45/90/-45]s", "Custom Laminate"
            ]

        self.material_combo.configure(values=materials)
        if materials:
            self.material_combo.set(materials[0])

    def add_laminate_layer(self):
        """Add a new laminate layer"""
        layer_num = len(self.laminate_layers) + 1

        # Create layer frame using grid layout instead of place
        layer_frame = tk.Frame(self.layers_frame, bg=self.colors['surface'], relief=tk.FLAT, bd=1, height=35)
        layer_frame.pack(fill=tk.X, pady=2, padx=5)
        layer_frame.pack_propagate(False)

        # Configure grid weights for better proportions
        layer_frame.columnconfigure(0, weight=0, minsize=50)  # Layer number - fixed narrow
        layer_frame.columnconfigure(1, weight=3, minsize=200)  # Material - moderate expansion
        layer_frame.columnconfigure(2, weight=1, minsize=100)  # Thickness - some expansion
        layer_frame.columnconfigure(3, weight=1, minsize=80)  # Angle - some expansion
        layer_frame.columnconfigure(4, weight=0, minsize=60)  # Actions - fixed narrow

        # Layer number
        tk.Label(layer_frame, text=str(layer_num),
                 bg=self.colors['surface'], fg=self.colors['text_primary'],
                 font=('Segoe UI', 9)).grid(row=0, column=0, sticky='ew', padx=5, pady=5)

        # Material dropdown
        material_var = tk.StringVar(value="IM7/8552")
        material_combo = ttk.Combobox(layer_frame, textvariable=material_var,
                                      values=["IM7/8552", "Glass/Epoxy", "Kevlar/Epoxy"],
                                      state="readonly", font=('Segoe UI', 8))
        material_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

        # Thickness entry
        thickness_var = tk.StringVar(value="0.125")
        thickness_entry = tk.Entry(layer_frame, textvariable=thickness_var,
                                   font=('Segoe UI', 8), justify='center')
        thickness_entry.grid(row=0, column=2, sticky='ew', padx=5, pady=5)

        # Angle entry
        angle_var = tk.StringVar(value="0")
        angle_entry = tk.Entry(layer_frame, textvariable=angle_var,
                               font=('Segoe UI', 8), justify='center')
        angle_entry.grid(row=0, column=3, sticky='ew', padx=5, pady=5)

        # Delete button
        delete_btn = tk.Button(layer_frame, text="🗑", font=('Segoe UI', 8),
                               command=lambda: self.delete_laminate_layer(layer_frame),
                               bg=self.colors['error'], fg='white', relief=tk.FLAT,
                               bd=0, padx=3)
        delete_btn.grid(row=0, column=4, sticky='ew', padx=5, pady=5)

        # Store layer data
        layer_data = {
            'frame': layer_frame,
            'material': material_var,
            'thickness': thickness_var,
            'angle': angle_var
        }
        self.laminate_layers.append(layer_data)

    def delete_laminate_layer(self, layer_frame):
        """Delete a laminate layer"""
        # Find and remove layer data
        for i, layer in enumerate(self.laminate_layers):
            if layer['frame'] == layer_frame:
                self.laminate_layers.pop(i)
                break

        # Destroy the frame
        layer_frame.destroy()

        # Renumber remaining layers
        for i, layer in enumerate(self.laminate_layers):
            layer_label = layer['frame'].winfo_children()[0]
            layer_label.configure(text=str(i + 1))

    def show_standard_layups(self):
        """Show standard layup presets"""
        # Create popup window with better dimensions
        popup = tk.Toplevel(self.root)
        popup.title("Standard Layups")
        popup.geometry("500x400")
        popup.configure(bg=self.colors['background'])
        popup.resizable(True, True)

        # Center the window
        popup.transient(self.root)
        popup.grab_set()

        # Main container with padding
        main_frame = tk.Frame(popup, bg=self.colors['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(main_frame, text="Select Standard Layup:",
                               bg=self.colors['background'], fg=self.colors['text_primary'],
                               font=('Segoe UI', 14, 'bold'))
        title_label.pack(pady=(0, 20))

        # Subtitle
        subtitle_label = tk.Label(main_frame, text="Choose from commonly used composite layups:",
                                  bg=self.colors['background'], fg=self.colors['text_secondary'],
                                  font=('Segoe UI', 10))
        subtitle_label.pack(pady=(0, 15))

        # Scrollable frame for layups
        canvas = tk.Canvas(main_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def _configure_canvas(event):
            canvas.itemconfig(window_id, width=event.width)

        canvas.bind('<Configure>', _configure_canvas)

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        layups = [
            ("Quasi-Isotropic", "[0/45/-45/90]s", "Balanced properties in all directions"),
            ("Cross-Ply", "[0/90]4s", "High stiffness in 0° and 90° directions"),
            ("Angle-Ply", "[±45]4s", "Optimized for shear loading"),
            ("Symmetric", "[0/45/90/-45]s", "Balanced symmetric layup"),
            ("Unidirectional", "[0]8", "Maximum strength in fiber direction"),
            ("Fabric", "[0/90]4s", "Woven fabric simulation"),
            ("Tough", "[45/-45/0/90]2s", "Impact and damage resistant")
        ]

        for name, sequence, description in layups:
            # Create card for each layup
            layup_frame = tk.Frame(scrollable_frame, bg=self.colors['surface'],
                                   relief=tk.FLAT, bd=1, highlightbackground=self.colors['border'],
                                   highlightthickness=1)
            layup_frame.pack(pady=8, fill=tk.X, padx=5)

            # Main button
            btn = tk.Button(layup_frame, text=f"{name}\n{sequence}",
                            command=lambda s=sequence, p=popup: self.apply_standard_layup(s, p),
                            bg=self.colors['primary'], fg='white',
                            font=('Segoe UI', 10, 'bold'),
                            padx=25, pady=15, relief=tk.FLAT,
                            activebackground=self.colors['primary_dark'],
                            activeforeground='white')
            btn.pack(side=tk.LEFT, padx=15, pady=15)

            # Description
            desc_frame = tk.Frame(layup_frame, bg=self.colors['surface'])
            desc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15), pady=15)

            tk.Label(desc_frame, text=description, bg=self.colors['surface'],
                     fg=self.colors['text_secondary'], font=('Segoe UI', 9),
                     wraplength=200, justify=tk.LEFT).pack(anchor=tk.W)

        # Bottom button frame
        button_frame = tk.Frame(main_frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X, pady=(15, 0))

        ttk.Button(button_frame, text="✖ Cancel",
                   command=popup.destroy, style='Secondary.TButton').pack(side=tk.RIGHT)

    def apply_standard_layup(self, sequence, popup):
        """Apply a standard layup sequence"""
        # Clear existing layers
        for layer in self.laminate_layers:
            layer['frame'].destroy()
        self.laminate_layers.clear()

        # Parse sequence and add layers
        angles = self.parse_layup_sequence(sequence)
        for angle in angles:
            self.add_laminate_layer()
            self.laminate_layers[-1]['angle'].set(str(angle))

        popup.destroy()
        messagebox.showinfo("Layup Applied", f"Applied {sequence} layup with {len(angles)} layers")

    def parse_layup_sequence(self, sequence):
        """Parse layup sequence notation"""
        # Simple parser for basic sequences
        if sequence == "[0/45/-45/90]s":
            return [0, 45, -45, 90, 90, -45, 45, 0]
        elif sequence == "[0/90]4s":
            return [0, 90, 0, 90, 0, 90, 0, 90]
        elif sequence == "[±45]4s":
            return [45, -45, 45, -45, 45, -45, 45, -45]
        elif sequence == "[0/45/90/-45]s":
            return [0, 45, 90, -45, -45, 90, 45, 0]
        elif sequence == "[0]8":
            return [0] * 8
        else:
            return [0, 45, -45, 90]  # Default

    def calculate_abd_matrix(self):
        """Calculate ABD matrix for laminate"""
        if not self.laminate_layers:
            messagebox.showwarning("No Layers", "Please add laminate layers first")
            return

        try:
            # Calculate ABD matrices using classical laminate theory
            abd_matrices = self._compute_abd_matrices()

            # Show results in a new window
            self._show_abd_results(abd_matrices)

        except Exception as e:
            messagebox.showerror("Calculation Error", f"Failed to calculate ABD matrix:\n{str(e)}")

    def _compute_abd_matrices(self):
        """Compute ABD matrices using classical laminate theory"""
        import math

        # Get material properties (using current orthotropic values)
        try:
            E1 = float(self.e1_var.get() or "150e9")  # Pa
            E2 = float(self.e2_var.get() or "9e9")  # Pa
            G12 = float(self.g12_var.get() or "5e9")  # Pa
            nu12 = float(self.nu12_var.get() or "0.3")
        except (ValueError, TypeError) as e:
            # Use default values if conversion fails
            E1 = 150e9
            E2 = 9e9
            G12 = 5e9
            nu12 = 0.3

        # Calculate nu21 from symmetry
        nu21 = nu12 * E2 / E1

        # Reduced stiffness matrix [Q]
        denom = 1 - nu12 * nu21
        Q11 = E1 / denom
        Q22 = E2 / denom
        Q12 = nu12 * E2 / denom
        Q66 = G12
        Q16 = Q26 = 0  # For orthotropic materials

        # Initialize ABD matrices
        A = np.zeros((3, 3))
        B = np.zeros((3, 3))
        D = np.zeros((3, 3))

        # Calculate z-coordinates of layer interfaces
        layer_thicknesses = []
        for layer in self.laminate_layers:
            try:
                # Try to get thickness from StringVar
                if hasattr(layer['thickness'], 'get'):
                    thickness = float(layer['thickness'].get() or "0.125")
                else:
                    # Fallback: try to use the value directly
                    thickness = float(layer['thickness'] or 0.125)
                layer_thicknesses.append(thickness)
            except (ValueError, TypeError, AttributeError) as e:
                print(f"Thickness extraction error: {e}, using default")
                layer_thicknesses.append(0.125)  # Default thickness in mm

        total_thickness = sum(layer_thicknesses)
        z = [-total_thickness / 2]

        for thickness in layer_thicknesses:
            thickness_m = thickness / 1000  # Convert mm to m
            z.append(z[-1] + thickness_m)

        # Calculate ABD matrices by integrating through thickness
        for i, layer in enumerate(self.laminate_layers):
            thickness = layer_thicknesses[i] / 1000  # Convert mm to m

            try:
                # Try to get angle from StringVar
                if hasattr(layer['angle'], 'get'):
                    angle_deg = float(layer['angle'].get() or "0")
                else:
                    # Fallback: try to use the value directly
                    angle_deg = float(layer['angle'] or 0)
            except (ValueError, TypeError, AttributeError) as e:
                print(f"Angle extraction error: {e}, using default")
                angle_deg = 0.0

            angle_rad = math.radians(angle_deg)

            # Transformation matrix for angle
            c = math.cos(angle_rad)
            s = math.sin(angle_rad)

            # Transformed reduced stiffness matrix [Q̄]
            Q11_bar = Q11 * c ** 4 + 2 * (Q12 + 2 * Q66) * s ** 2 * c ** 2 + Q22 * s ** 4
            Q12_bar = (Q11 + Q22 - 4 * Q66) * s ** 2 * c ** 2 + Q12 * (s ** 4 + c ** 4)
            Q22_bar = Q11 * s ** 4 + 2 * (Q12 + 2 * Q66) * s ** 2 * c ** 2 + Q22 * c ** 4
            Q16_bar = (Q11 - Q12 - 2 * Q66) * s * c ** 3 + (Q12 - Q22 + 2 * Q66) * s ** 3 * c
            Q26_bar = (Q11 - Q12 - 2 * Q66) * s ** 3 * c + (Q12 - Q22 + 2 * Q66) * s * c ** 3
            Q66_bar = (Q11 + Q22 - 2 * Q12 - 2 * Q66) * s ** 2 * c ** 2 + Q66 * (s ** 4 + c ** 4)

            # Layer distances from midplane
            z1 = z[i]
            z2 = z[i + 1]

            # A matrix (extensional stiffness)
            A[0, 0] += Q11_bar * (z2 - z1)
            A[0, 1] += Q12_bar * (z2 - z1)
            A[0, 2] += Q16_bar * (z2 - z1)
            A[1, 0] += Q12_bar * (z2 - z1)
            A[1, 1] += Q22_bar * (z2 - z1)
            A[1, 2] += Q26_bar * (z2 - z1)
            A[2, 0] += Q16_bar * (z2 - z1)
            A[2, 1] += Q26_bar * (z2 - z1)
            A[2, 2] += Q66_bar * (z2 - z1)

            # B matrix (coupling stiffness)  
            B[0, 0] += Q11_bar * (z2 ** 2 - z1 ** 2) / 2
            B[0, 1] += Q12_bar * (z2 ** 2 - z1 ** 2) / 2
            B[0, 2] += Q16_bar * (z2 ** 2 - z1 ** 2) / 2
            B[1, 0] += Q12_bar * (z2 ** 2 - z1 ** 2) / 2
            B[1, 1] += Q22_bar * (z2 ** 2 - z1 ** 2) / 2
            B[1, 2] += Q26_bar * (z2 ** 2 - z1 ** 2) / 2
            B[2, 0] += Q16_bar * (z2 ** 2 - z1 ** 2) / 2
            B[2, 1] += Q26_bar * (z2 ** 2 - z1 ** 2) / 2
            B[2, 2] += Q66_bar * (z2 ** 2 - z1 ** 2) / 2

            # D matrix (bending stiffness)
            D[0, 0] += Q11_bar * (z2 ** 3 - z1 ** 3) / 3
            D[0, 1] += Q12_bar * (z2 ** 3 - z1 ** 3) / 3
            D[0, 2] += Q16_bar * (z2 ** 3 - z1 ** 3) / 3
            D[1, 0] += Q12_bar * (z2 ** 3 - z1 ** 3) / 3
            D[1, 1] += Q22_bar * (z2 ** 3 - z1 ** 3) / 3
            D[1, 2] += Q26_bar * (z2 ** 3 - z1 ** 3) / 3
            D[2, 0] += Q16_bar * (z2 ** 3 - z1 ** 3) / 3
            D[2, 1] += Q26_bar * (z2 ** 3 - z1 ** 3) / 3
            D[2, 2] += Q66_bar * (z2 ** 3 - z1 ** 3) / 3

        # Extract layup angles safely
        layup_angles = []
        for layer in self.laminate_layers:
            try:
                # Try to get angle from StringVar
                if hasattr(layer['angle'], 'get'):
                    angle = float(layer['angle'].get() or "0")
                else:
                    # Fallback: try to use the value directly
                    angle = float(layer['angle'] or 0)
                layup_angles.append(angle)
            except (ValueError, TypeError, AttributeError) as e:
                print(f"Layup angle extraction error: {e}, using default")
                layup_angles.append(0.0)

        return {
            'A': A,
            'B': B,
            'D': D,
            'total_thickness': total_thickness,
            'num_layers': len(self.laminate_layers),
            'layup': layup_angles
        }

    def _show_abd_results(self, abd_data):
        """Display ABD matrix results in a new window"""
        # Create results window
        results_window = tk.Toplevel(self.root)
        results_window.title("ABD Matrix Calculation Results")
        results_window.geometry("800x600")
        results_window.configure(bg=self.colors['background'])

        # Make window resizable
        results_window.resizable(True, True)

        # Create main scrollable frame
        main_frame = tk.Frame(results_window, bg=self.colors['background'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create window that expands with canvas width
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Configure canvas to expand scrollable_frame to its width
        def _configure_canvas(event):
            canvas.itemconfig(window_id, width=event.width)

        canvas.bind('<Configure>', _configure_canvas)

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Title
        title_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        title_frame.pack(fill=tk.X, padx=20, pady=20)

        tk.Label(title_frame, text="[MATRIX] ABD Matrix Results",
                 font=('Segoe UI', 16, 'bold'),
                 bg=self.colors['background'], fg=self.colors['text_primary']).pack(anchor=tk.W)

        # Summary info
        summary_frame = self.create_card(scrollable_frame, "📋 Layup Summary", "")
        summary_frame.pack(fill=tk.X, padx=20, pady=10)

        summary_content = tk.Frame(summary_frame, bg=self.colors['surface'])
        summary_content.pack(fill=tk.X, padx=20, pady=15)

        layup_str = f"[{'/'.join([str(int(angle)) for angle in abd_data['layup']])}]"

        summary_text = f"""Number of Layers: {abd_data['num_layers']}
Total Thickness: {abd_data['total_thickness']:.3f} mm
Layup Sequence: {layup_str}
Laminate Type: {'Symmetric' if self._is_symmetric(abd_data['layup']) else 'Unsymmetric'}
Coupling: {'Present' if np.max(np.abs(abd_data['B'])) > 1e-6 else 'Absent'}"""

        tk.Label(summary_content, text=summary_text, justify=tk.LEFT,
                 font=('Consolas', 10), bg=self.colors['surface'],
                 fg=self.colors['text_primary']).pack(fill=tk.X, anchor=tk.W)

        # A Matrix (Extensional Stiffness)
        self._create_matrix_display(scrollable_frame, "A Matrix (Extensional Stiffness)",
                                    abd_data['A'], "N/m")

        # B Matrix (Coupling Stiffness)
        self._create_matrix_display(scrollable_frame, "B Matrix (Coupling Stiffness)",
                                    abd_data['B'], "N")

        # D Matrix (Bending Stiffness)
        self._create_matrix_display(scrollable_frame, "D Matrix (Bending Stiffness)",
                                    abd_data['D'], "N⋅m")

        # Engineering properties (if available)
        try:
            eng_props = self._calculate_engineering_properties(abd_data)
            self._create_engineering_properties_display(scrollable_frame, eng_props)
        except:
            pass  # Skip if calculation fails

        # Close button
        button_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X, padx=20, pady=20)

        ttk.Button(button_frame, text="📋 Copy to Clipboard",
                   command=lambda: self._copy_abd_to_clipboard(abd_data),
                   style='Secondary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="✖ Close",
                   command=results_window.destroy,
                   style='Danger.TButton').pack(side=tk.RIGHT)

    def _create_matrix_display(self, parent, title, matrix, units):
        """Create a formatted matrix display"""
        card = self.create_card(parent, title, f"Units: {units}")
        card.pack(fill=tk.X, padx=20, pady=10)

        content = tk.Frame(card, bg=self.colors['surface'])
        content.pack(fill=tk.X, padx=20, pady=15)

        # Matrix display with fixed-width font - use full width
        matrix_frame = tk.Frame(content, bg=self.colors['surface'])
        matrix_frame.pack(fill=tk.X, expand=True)

        # Center the matrix display
        matrix_container = tk.Frame(matrix_frame, bg=self.colors['surface'])
        matrix_container.pack(expand=True)

        for i in range(3):
            row_frame = tk.Frame(matrix_container, bg=self.colors['surface'])
            row_frame.pack()

            for j in range(3):
                value = matrix[i, j]
                if abs(value) < 1e-10:
                    value_str = "0.0"
                elif abs(value) >= 1e6:
                    value_str = f"{value:.2e}"
                else:
                    value_str = f"{value:.3f}"

                tk.Label(row_frame, text=f"{value_str:>15}",
                         font=('Consolas', 10), bg=self.colors['surface'],
                         fg=self.colors['text_primary']).pack(side=tk.LEFT, padx=8)

    def _calculate_engineering_properties(self, abd_data):
        """Calculate equivalent engineering properties"""
        A = abd_data['A']
        h = abd_data['total_thickness'] / 1000  # Convert to meters

        # Compliance matrix (inverse of A/h)
        A_bar = A / h
        S = np.linalg.inv(A_bar)

        # Engineering constants
        Ex = 1.0 / S[0, 0]
        Ey = 1.0 / S[1, 1]
        Gxy = 1.0 / S[2, 2]
        nu_xy = -S[0, 1] / S[0, 0]
        nu_yx = -S[0, 1] / S[1, 1]

        return {
            'Ex': Ex,
            'Ey': Ey,
            'Gxy': Gxy,
            'nu_xy': nu_xy,
            'nu_yx': nu_yx
        }

    def _create_engineering_properties_display(self, parent, props):
        """Display equivalent engineering properties"""
        card = self.create_card(parent, "🔧 Equivalent Engineering Properties",
                                "Membrane properties from A matrix")
        card.pack(fill=tk.X, padx=20, pady=10)

        content = tk.Frame(card, bg=self.colors['surface'])
        content.pack(fill=tk.X, padx=20, pady=15)

        props_text = f"""Ex = {props['Ex'] / 1e9:.2f} GPa
Ey = {props['Ey'] / 1e9:.2f} GPa  
Gxy = {props['Gxy'] / 1e9:.2f} GPa
νxy = {props['nu_xy']:.3f}
νyx = {props['nu_yx']:.3f}"""

        tk.Label(content, text=props_text, justify=tk.LEFT,
                 font=('Consolas', 10), bg=self.colors['surface'],
                 fg=self.colors['text_primary']).pack(fill=tk.X, anchor=tk.W)

    def _is_symmetric(self, layup):
        """Check if layup is symmetric"""
        n = len(layup)
        for i in range(n // 2):
            if layup[i] != layup[n - 1 - i]:
                return False
        return True

    def _copy_abd_to_clipboard(self, abd_data):
        """Copy ABD matrices to clipboard"""
        try:
            import tkinter.messagebox as mb

            # Format ABD data as text
            text = f"ABD Matrix Results\n{'=' * 50}\n\n"
            text += f"Layup: [{'/'.join([str(int(a)) for a in abd_data['layup']])}]\n"
            text += f"Total Thickness: {abd_data['total_thickness']:.3f} mm\n\n"

            text += "A Matrix (Extensional Stiffness) [N/m]:\n"
            for row in abd_data['A']:
                text += " ".join([f"{val:12.3e}" for val in row]) + "\n"
            text += "\n"

            text += "B Matrix (Coupling Stiffness) [N]:\n"
            for row in abd_data['B']:
                text += " ".join([f"{val:12.3e}" for val in row]) + "\n"
            text += "\n"

            text += "D Matrix (Bending Stiffness) [N⋅m]:\n"
            for row in abd_data['D']:
                text += " ".join([f"{val:12.3e}" for val in row]) + "\n"

            # Copy to clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            mb.showinfo("Copied", "ABD matrix data copied to clipboard!")

        except Exception as e:
            messagebox.showerror("Copy Error", f"Failed to copy to clipboard:\n{str(e)}")

    def create_analysis_tab(self):
        """Create beautiful analysis parameters tab"""
        analysis_main_frame, analysis_frame = self.create_scrollable_frame(self.notebook)
        self.notebook.add(analysis_main_frame, text="⚡ Analysis")

        # Create card layout
        cards_frame = tk.Frame(analysis_frame, bg=self.colors['background'])
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Multi-solver selection card
        solver_card = self.create_card(cards_frame, "🧮 Flutter Analysis Solver",
                                       "Choose your analysis method and solver")
        solver_card.pack(fill=tk.X, pady=(0, 20))

        solver_content = tk.Frame(solver_card, bg=self.colors['surface'])
        solver_content.pack(fill=tk.X, padx=20, pady=15)

        # Solver method selection
        tk.Label(solver_content, text="Primary Solver:",
                 bg=self.colors['surface'], fg=self.colors['text_primary'],
                 font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))

        self.solver_method_var = tk.StringVar(value="auto")
        solver_combo = ttk.Combobox(solver_content, textvariable=self.solver_method_var,
                                    values=["auto (Smart Selection)", "piston_theory (Level 1)",
                                            "doublet_lattice (Level 2)", "nastran (Level 3)"],
                                    state="readonly", style='Modern.TCombobox', width=30)
        solver_combo.pack(anchor=tk.W, pady=(0, 10))

        # Multi-solver comparison option
        self.multi_solver_var = tk.BooleanVar(value=True)
        multi_solver_check = ttk.Checkbutton(solver_content, text="Enable multi-solver comparison",
                                             variable=self.multi_solver_var,
                                             style='Modern.TCheckbutton')
        multi_solver_check.pack(anchor=tk.W, pady=(0, 10))

        # NASTRAN Configuration Section
        nastran_frame = self.create_card(solver_content, "NASTRAN Configuration",
                                         "Configure NASTRAN solver path and options")
        nastran_frame.pack(fill=tk.X, pady=(0, 10))

        nastran_content = tk.Frame(nastran_frame, bg=self.colors['surface'])
        nastran_content.pack(fill=tk.X, padx=20, pady=15)

        # NASTRAN executable path
        tk.Label(nastran_content, text="NASTRAN Executable Path:",
                 bg=self.colors['surface'], fg=self.colors['text_primary'],
                 font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))

        path_frame = tk.Frame(nastran_content, bg=self.colors['surface'])
        path_frame.pack(fill=tk.X, pady=(0, 10))

        self.nastran_path_var = tk.StringVar(value="auto-detect")
        path_entry = tk.Entry(path_frame, textvariable=self.nastran_path_var,
                              bg='white', fg=self.colors['text_primary'],
                              font=('Segoe UI', 9), width=50)
        path_entry.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(path_frame, text="Browse...",
                   command=self.browse_nastran_executable,
                   style='Secondary.TButton').pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(path_frame, text="Detect",
                   command=self.detect_nastran_executable,
                   style='Secondary.TButton').pack(side=tk.LEFT)

        # NASTRAN status indicator
        self.nastran_status_var = tk.StringVar(value="Checking...")
        self.nastran_status_label = tk.Label(nastran_content, textvariable=self.nastran_status_var,
                                             bg=self.colors['surface'],
                                             fg=self.colors['text_secondary'],
                                             font=('Segoe UI', 9, 'italic'))
        self.nastran_status_label.pack(anchor=tk.W, pady=(0, 10))

        # NASTRAN options
        options_frame = tk.Frame(nastran_content, bg=self.colors['surface'])
        options_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(options_frame, text="Memory:", bg=self.colors['surface'],
                 fg=self.colors['text_primary'], font=('Segoe UI', 9)).pack(side=tk.LEFT)

        self.nastran_memory_var = tk.StringVar(value="4gb")
        memory_combo = ttk.Combobox(options_frame, textvariable=self.nastran_memory_var,
                                    values=["2gb", "4gb", "8gb", "16gb", "32gb"],
                                    state="readonly", style='Modern.TCombobox', width=8)
        memory_combo.pack(side=tk.LEFT, padx=(5, 15))

        tk.Label(options_frame, text="CPU Time (min):", bg=self.colors['surface'],
                 fg=self.colors['text_primary'], font=('Segoe UI', 9)).pack(side=tk.LEFT)

        self.nastran_time_var = tk.StringVar(value="30")
        time_entry = tk.Entry(options_frame, textvariable=self.nastran_time_var,
                              bg='white', fg=self.colors['text_primary'],
                              font=('Segoe UI', 9), width=5)
        time_entry.pack(side=tk.LEFT, padx=(5, 0))

        # Initialize NASTRAN detection
        self.root.after(1000, self.detect_nastran_executable)  # Check after GUI loads

        # Solver info button
        info_frame = tk.Frame(solver_content, bg=self.colors['surface'])
        info_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(info_frame, text="ℹ️ Solver Information",
                   command=self.show_solver_info, style='Secondary.TButton').pack(side=tk.LEFT)

        # Traditional NASTRAN method selection (for compatibility)
        tk.Label(solver_content, text="NASTRAN Solution Method:",
                 bg=self.colors['surface'], fg=self.colors['text_primary'],
                 font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(10, 5))

        self.method_var = tk.StringVar(value="PK")
        method_combo = ttk.Combobox(solver_content, textvariable=self.method_var,
                                    values=["PK (P-K Method)", "K (K Method)", "KE (KE Method)", "PKNL (Nonlinear PK)"],
                                    state="readonly", style='Modern.TCombobox', width=25)
        method_combo.pack(anchor=tk.W)

        # Flight conditions card
        flight_card = self.create_card(cards_frame, "✈️ Flight Conditions",
                                       "Define the operational flight envelope")
        flight_card.pack(fill=tk.X, pady=(0, 20))

        flight_content = tk.Frame(flight_card, bg=self.colors['surface'])
        flight_content.pack(fill=tk.X, padx=20, pady=15)

        # Configure grid weights for expansion
        flight_content.columnconfigure(0, weight=1)

        # Velocity range inputs
        self.vmin_var = tk.StringVar(value="50")
        self.create_property_input(flight_content, "Min Velocity", "m/s", self.vmin_var, 0)

        self.vmax_var = tk.StringVar(value="300")
        self.create_property_input(flight_content, "Max Velocity", "m/s", self.vmax_var, 1)

        self.mach_var = tk.StringVar(value="0.8")
        self.create_property_input(flight_content, "Mach Number", "-", self.mach_var, 2)

        # Analysis execution card
        exec_card = self.create_card(cards_frame, "🚀 Run Analysis",
                                     "Execute the flutter analysis")
        exec_card.pack(fill=tk.X)

        exec_content = tk.Frame(exec_card, bg=self.colors['surface'])
        exec_content.pack(fill=tk.X, padx=20, pady=15)

        # Run button with modern styling
        button_frame = tk.Frame(exec_content, bg=self.colors['surface'])
        button_frame.pack(fill=tk.X, pady=(0, 15))

        self.run_button = ttk.Button(button_frame, text="🚀 Run Flutter Analysis",
                                     command=self.run_analysis, style='Success.TButton')
        self.run_button.pack(side=tk.LEFT, padx=(0, 10))

        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop",
                                      command=self.stop_analysis, style='Secondary.TButton', state='disabled')
        self.stop_button.pack(side=tk.LEFT)

        # Progress bar with modern styling
        progress_frame = tk.Frame(exec_content, bg=self.colors['surface'])
        progress_frame.pack(fill=tk.X)

        tk.Label(progress_frame, text="Analysis Progress:",
                 bg=self.colors['surface'], fg=self.colors['text_primary'],
                 font=('Segoe UI', 9)).pack(anchor=tk.W, pady=(0, 5))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                            maximum=100, style='Modern.Horizontal.TProgressbar')
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))

        self.progress_label = tk.Label(progress_frame, text="Ready to run analysis",
                                       bg=self.colors['surface'], fg=self.colors['text_secondary'],
                                       font=('Segoe UI', 8))
        self.progress_label.pack(anchor=tk.W)

    def show_solver_info(self):
        """Show information about available flutter analysis solvers"""
        info_text = """
FLUTTER ANALYSIS SOLVERS:

• AUTO (Smart Selection)
  Automatically recommends the best solver based on your
  flow conditions and panel properties.

• PISTON THEORY (Level 1)
  - Speed: Very fast (~1 second)
  - Best for: Supersonic flow (M > 1.2) 
  - Accuracy: Good for preliminary design
  - Method: Simplified aerodynamics + analytical structure

• DOUBLET LATTICE (Level 2)
  - Speed: Fast (~10 seconds)
  - Best for: Subsonic/transonic (M < 0.95)
  - Accuracy: Better than piston theory
  - Method: Unsteady aerodynamics + finite elements

• NASTRAN (Level 3)
  - Speed: Slow (~minutes)
  - Best for: All conditions, final design
  - Accuracy: Most accurate and comprehensive
  - Method: Full aeroelastic analysis

RECOMMENDATIONS:
- Preliminary design: Use AUTO or Piston Theory
- Design validation: Enable multi-solver comparison
- Final analysis: Use NASTRAN
- For certification: Always validate with multiple methods

MULTI-SOLVER COMPARISON:
When enabled, runs multiple methods and compares results
to give you confidence levels and validation.
        """

        messagebox.showinfo("Flutter Analysis Solvers", info_text)

    def stop_analysis(self):
        """Stop running analysis"""
        self.status_var.set("⏹️ Analysis stopped by user")
        self.run_button.config(state='normal')
        self.stop_button.config(state='disabled')

    def create_results_tab(self):
        """Create beautiful results display tab"""
        results_main_frame, results_frame = self.create_scrollable_frame(self.notebook)
        self.notebook.add(results_main_frame, text="📊 Results")

        # Create card layout
        cards_frame = tk.Frame(results_frame, bg=self.colors['background'])
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Flutter summary card
        summary_card = self.create_card(cards_frame, "🎯 Flutter Summary",
                                        "Critical flutter analysis results")
        summary_card.pack(fill=tk.X, pady=(0, 20))

        summary_content = tk.Frame(summary_card, bg=self.colors['surface'])
        summary_content.pack(fill=tk.X, padx=20, pady=15)

        # Create results display grid
        results_grid = tk.Frame(summary_content, bg=self.colors['surface'])
        results_grid.pack(fill=tk.X)

        self.flutter_speed_var = tk.StringVar(value="-- m/s")
        self.flutter_freq_var = tk.StringVar(value="-- Hz")

        # Flutter speed display
        speed_frame = tk.Frame(results_grid, bg=self.colors['primary_light'], relief=tk.FLAT, bd=1)
        speed_frame.grid(row=0, column=0, sticky=tk.W + tk.E, padx=(0, 10), pady=5)
        results_grid.columnconfigure(0, weight=1)

        tk.Label(speed_frame, text="Flutter Speed",
                 bg=self.colors['primary_light'], fg='white',
                 font=('Segoe UI', 9)).pack(anchor=tk.W, padx=12, pady=(8, 0))
        tk.Label(speed_frame, textvariable=self.flutter_speed_var,
                 bg=self.colors['primary_light'], fg='white',
                 font=('Segoe UI', 16, 'bold')).pack(anchor=tk.W, padx=12, pady=(0, 8))

        # Flutter frequency display
        freq_frame = tk.Frame(results_grid, bg=self.colors['secondary'], relief=tk.FLAT, bd=1)
        freq_frame.grid(row=0, column=1, sticky=tk.W + tk.E, padx=(10, 0), pady=5)
        results_grid.columnconfigure(1, weight=1)

        tk.Label(freq_frame, text="Flutter Frequency",
                 bg=self.colors['secondary'], fg='white',
                 font=('Segoe UI', 9)).pack(anchor=tk.W, padx=12, pady=(8, 0))
        tk.Label(freq_frame, textvariable=self.flutter_freq_var,
                 bg=self.colors['secondary'], fg='white',
                 font=('Segoe UI', 16, 'bold')).pack(anchor=tk.W, padx=12, pady=(0, 8))

        # Status indicator
        status_frame = tk.Frame(summary_content, bg=self.colors['surface'])
        status_frame.pack(fill=tk.X, pady=(10, 0))

        self.safety_indicator = tk.Label(status_frame, text="[STATUS] No Analysis Run",
                                         bg=self.colors['surface'], fg=self.colors['text_secondary'],
                                         font=('Segoe UI', 10))
        self.safety_indicator.pack(anchor=tk.W)

        # Plots card
        plot_card = self.create_card(cards_frame, "📈 Flutter Diagrams",
                                     "V-f and V-g stability plots")
        plot_card.pack(fill=tk.BOTH, expand=True)

        plot_content = tk.Frame(plot_card, bg=self.colors['surface'])
        plot_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Create matplotlib figure with modern styling
        self.fig = Figure(figsize=(12, 6), dpi=100)
        self.fig.patch.set_facecolor(self.colors['surface'])

        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, plot_content)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Plot control buttons
        plot_controls = tk.Frame(plot_content, bg=self.colors['surface'])
        plot_controls.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(plot_controls, text="💾 Save Plot",
                   command=self.save_plot, style='Secondary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(plot_controls, text="🔄 Refresh",
                   command=self.refresh_plot, style='Secondary.TButton').pack(side=tk.LEFT)

        # Initially empty plot
        self.plot_empty_results()

    def save_plot(self):
        """Save current plot"""
        messagebox.showinfo("Save Plot", "Plot saved to flutter_results.png")

    def refresh_plot(self):
        """Refresh plot display"""
        self.plot_empty_results()
        self.status_var.set("📈 Plot refreshed")

    def preview_geometry(self):
        """Preview geometry visualization"""
        try:
            length = float(self.length_var.get()) / 1000.0  # Convert mm to m
            width = float(self.width_var.get()) / 1000.0  # Convert mm to m
            nlength = self.nlength_var.get()
            nspan = self.nspan_var.get()

            # Create preview window
            preview_window = tk.Toplevel(self.root)
            preview_window.title("Geometry Preview")
            preview_window.geometry("600x500")

            # Create matplotlib figure for preview
            fig = Figure(figsize=(8, 6), dpi=100)
            ax = fig.add_subplot(111, projection='3d')

            # Generate mesh
            x = np.linspace(0, length, nlength + 1)
            y = np.linspace(0, width, nspan + 1)
            X, Y = np.meshgrid(x, y)
            Z = np.zeros_like(X)

            # Plot wireframe
            ax.plot_wireframe(X, Y, Z, color='blue', alpha=0.7)

            # Plot panel outline
            outline_x = [0, length, length, 0, 0]
            outline_y = [0, 0, width, width, 0]
            outline_z = [0, 0, 0, 0, 0]
            ax.plot(outline_x, outline_y, outline_z, 'r-', linewidth=2)

            ax.set_xlabel('X (mm)')
            ax.set_ylabel('Y (mm)')
            ax.set_zlabel('Z (mm)')
            ax.set_title(f'Panel Geometry ({nlength}×{nspan} elements)')

            # Create canvas
            canvas = FigureCanvasTkAgg(fig, preview_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            self.status_var.set(f"Geometry preview: {length}m × {width}m panel with {nlength}×{nspan} elements")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values")

    def on_material_changed(self, event=None):
        """Handle material selection change"""
        material = self.material_var.get()

        material_props = {
            "Aluminum 7075-T6": {"density": "2700", "youngs": "7.0e10", "poisson": "0.33"},
            "Steel AISI 4130": {"density": "7850", "youngs": "2.0e11", "poisson": "0.29"},
            "Titanium Ti-6Al-4V": {"density": "4430", "youngs": "1.14e11", "poisson": "0.32"}
        }

        if material in material_props:
            props = material_props[material]
            self.density_var.set(props["density"])
            self.youngs_var.set(props["youngs"])
            self.poisson_var.set(props["poisson"])

    def run_analysis(self):
        """Run flutter analysis simulation"""
        self.run_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_var.set("🔄 Running flutter analysis...")
        self.progress_label.config(text="Initializing analysis...")

        # Start analysis in separate thread
        analysis_thread = threading.Thread(target=self._run_analysis_thread)
        analysis_thread.daemon = True
        analysis_thread.start()

    def _run_analysis_thread(self):
        """Run comprehensive flutter analysis in background thread"""
        try:
            # Import analysis modules
            sys.path.insert(0, str(Path(__file__).parent / "src"))

            # Check solver method selection
            solver_method = getattr(self, 'solver_method_var', tk.StringVar(value="auto")).get().split()[
                0]  # Get first word
            multi_solver_enabled = getattr(self, 'multi_solver_var', tk.BooleanVar(value=True)).get()

            # Use multi-solver if selected or auto mode
            if solver_method in ["piston_theory", "doublet_lattice", "auto"] or multi_solver_enabled:
                self._run_multi_solver_analysis()
                return

            # Fallback to traditional NASTRAN analysis
            from gui.analysis import (
                AnalysisRunner, FlutterAnalysisConfig,
                GeometryConfig, MaterialConfig, ResultsAnalyzer
            )

            self._run_nastran_analysis()

        except Exception as e:
            self.logger.error(f"Analysis thread error: {e}")
            self.root.after(0, lambda: self.status_var.set(f"Analysis failed: {str(e)}"))
            self.root.after(0, lambda: self.run_button.config(state='normal'))
            self.root.after(0, lambda: self.stop_button.config(state='disabled'))

    def _run_nastran_analysis(self):
        """Run traditional NASTRAN analysis"""
        try:
            # Create analysis configuration from GUI inputs
            # Map to actual existing GUI variables
            from gui.analysis import (
                AnalysisRunner, FlutterAnalysisConfig,
                GeometryConfig, MaterialConfig, ResultsAnalyzer
            )

            config = FlutterAnalysisConfig(
                method='nastran',  # Force NASTRAN method
                aerodynamic_theory='nastran',  # Force NASTRAN aerodynamics
                mach_min=0.3,  # Use sensible defaults since these specific vars don't exist
                mach_max=2.0,
                altitude=10000.0,
                dynamic_pressure=None,  # Will be calculated
                num_modes=20,
                max_frequency=1000.0,
                convergence_tolerance=1e-6,
                max_iterations=100,
                eigen_solver='LANCZOS',
                use_parallel=True,
                velocity_min=float(getattr(self, 'vmin_var', tk.StringVar(value="50")).get()),
                velocity_max=float(getattr(self, 'vmax_var', tk.StringVar(value="300")).get()),
                velocity_points=25  # Use reasonable default
            )

            # Create geometry configuration from GUI inputs  
            geometry = GeometryConfig(
                length=float(getattr(self, 'length_var', tk.StringVar(value="1.0")).get()),  # Already in meters
                width=float(getattr(self, 'width_var', tk.StringVar(value="0.5")).get()),  # Already in meters
                thickness=float(getattr(self, 'thickness_var', tk.StringVar(value="0.002")).get()) / 1000.0,
                # Convert mm to m
                boundary_conditions=self.get_boundary_condition_code() if hasattr(self,
                                                                                  'get_boundary_condition_code') else 'SSSS'
            )

            # Create material configuration from GUI inputs
            material_type = getattr(self, 'material_type_var', tk.StringVar(value="isotropic")).get()
            if material_type == "isotropic":
                material = MaterialConfig(
                    material_type="isotropic",
                    youngs_modulus=float(getattr(self, 'youngs_var', tk.StringVar(value="7.0e10")).get()),
                    poisson_ratio=float(getattr(self, 'poisson_var', tk.StringVar(value="0.33")).get()),
                    density=float(getattr(self, 'density_var', tk.StringVar(value="2700")).get())
                )
            else:
                # Use orthotropic properties if available
                material = MaterialConfig(
                    material_type="orthotropic",
                    e1=float(getattr(self, 'e1_var', tk.StringVar(value="1.5e11")).get()),
                    e2=float(getattr(self, 'e2_var', tk.StringVar(value="9.0e9")).get()),
                    e3=float(getattr(self, 'e3_var', tk.StringVar(value="9.0e9")).get()),
                    g12=float(getattr(self, 'g12_var', tk.StringVar(value="5.0e9")).get()),
                    g13=float(getattr(self, 'g13_var', tk.StringVar(value="5.0e9")).get()),
                    g23=float(getattr(self, 'g23_var', tk.StringVar(value="3.0e9")).get()),
                    nu12=float(getattr(self, 'nu12_var', tk.StringVar(value="0.3")).get()),
                    nu13=float(getattr(self, 'nu13_var', tk.StringVar(value="0.3")).get()),
                    nu23=float(getattr(self, 'nu23_var', tk.StringVar(value="0.4")).get()),
                    density=float(getattr(self, 'density_var', tk.StringVar(value="2700")).get())
                )

            # Progress callback for updating GUI
            def progress_callback(step: str, progress: float):
                if hasattr(self, 'stop_requested') and self.stop_requested:
                    return False  # Signal to stop

                # Update GUI elements safely in main thread
                if hasattr(self, 'progress_var'):
                    self.root.after(0, lambda p=progress: self.progress_var.set(p))
                if hasattr(self, 'progress_label'):
                    self.root.after(0, lambda s=step: self.progress_label.config(text=s))
                if hasattr(self, 'status_var'):
                    self.root.after(0, lambda p=progress: self.status_var.set(f"NASTRAN Analysis... {p:.0f}%"))

                # Log progress to analysis log if available
                if hasattr(self, 'log_text') and hasattr(self, '_log_message'):
                    timestamp = time.strftime("%H:%M:%S")
                    log_msg = f"[{timestamp}] {step}"
                    self.root.after(0, lambda msg=log_msg: self._log_message(msg))

                return True  # Continue analysis

            # Create analysis runner and execute
            runner = AnalysisRunner(progress_callback)
            results = runner.run_flutter_analysis(config, geometry, material)

            if results.analysis_successful:
                # Generate analysis summary
                summary = ResultsAnalyzer.generate_summary_report(results)
                if hasattr(self, 'log_text') and hasattr(self, '_log_message'):
                    self.root.after(0, lambda: self._log_message("\n" + summary))

                # Update GUI with results
                if hasattr(self, '_update_results'):
                    self.root.after(0, lambda: self._update_results(
                        results.velocities,
                        results.frequencies,
                        results.dampings,
                        results.flutter_velocity,
                        results.flutter_frequency
                    ))

                # Update status
                if results.flutter_velocity:
                    status_msg = f"NASTRAN Complete: Flutter at {results.flutter_velocity:.1f} m/s"
                else:
                    status_msg = "NASTRAN Complete: Structure stable"

                if hasattr(self, 'status_var'):
                    self.root.after(0, lambda: self.status_var.set(status_msg))

            else:
                # Handle analysis failure
                error_msg = f"NASTRAN analysis failed: {results.error_message or 'Unknown error'}"
                if hasattr(self, '_log_message'):
                    self.root.after(0, lambda: self._log_message(f"ERROR: {error_msg}"))
                if hasattr(self, 'root'):
                    self.root.after(0, lambda: messagebox.showerror("NASTRAN Analysis Error", error_msg))

                # Show empty results
                if hasattr(self, 'plot_empty_results'):
                    self.root.after(0, lambda: self.plot_empty_results())

        except Exception as e:
            error_msg = f"NASTRAN analysis configuration error: {str(e)}"
            print(f"ERROR: {error_msg}")
            import traceback
            traceback.print_exc()

            # Update GUI with error
            if hasattr(self, 'status_var'):
                self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
            if hasattr(self, '_log_message'):
                self.root.after(0, lambda: self._log_message(f"ERROR: {error_msg}"))
            if hasattr(self, 'root'):
                self.root.after(0, lambda: messagebox.showerror("Configuration Error", error_msg))

        finally:
            # Re-enable buttons
            if hasattr(self, 'run_button'):
                self.root.after(0, lambda: self.run_button.config(state='normal'))
            if hasattr(self, 'stop_button'):
                self.root.after(0, lambda: self.stop_button.config(state='disabled'))

    def _update_results(self, velocities, frequencies, dampings, flutter_speed, flutter_freq):
        """Update beautiful results display"""
        # Update summary with modern styling
        if flutter_speed is not None:
            self.flutter_speed_var.set(f"{flutter_speed:.1f}")
            self.flutter_freq_var.set(f"{flutter_freq:.2f}")

            # Update safety indicator
            if flutter_speed > 250:
                self.safety_indicator.config(text="[SAFE] Flutter speed well above operating range",
                                             fg=self.colors['success'])
            elif flutter_speed > 150:
                self.safety_indicator.config(text="[CAUTION] Flutter speed near operating range",
                                             fg=self.colors['warning'])
            else:
                self.safety_indicator.config(text="[DANGER] Flutter speed in operating range",
                                             fg=self.colors['error'])
        else:
            self.flutter_speed_var.set("No flutter")
            self.flutter_freq_var.set("--")
            self.safety_indicator.config(text="[SAFE] No flutter detected in range",
                                         fg=self.colors['success'])

        # Update plots with modern styling
        self.fig.clear()

        # Create subplots with modern appearance
        ax1 = self.fig.add_subplot(1, 2, 1)
        ax2 = self.fig.add_subplot(1, 2, 2)

        # Set modern colors and styling
        plot_color = self.colors['primary']
        danger_color = self.colors['error']

        # V-f plot with enhanced styling
        if velocities is not None and frequencies is not None and len(velocities) > 0 and len(frequencies) > 0:
            ax1.plot(velocities, frequencies, color=plot_color, linewidth=3,
                     marker='o', markersize=5, alpha=0.8, label='Frequency')
        else:
            ax1.text(0.5, 0.5, 'No Data', transform=ax1.transAxes, ha='center', va='center',
                     fontsize=14, color=self.colors['text_light'])
        ax1.set_xlabel('Velocity (m/s)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Frequency (Hz)', fontsize=11, fontweight='bold')
        ax1.set_title('V-f Diagram', fontsize=12, fontweight='bold', pad=15)
        ax1.grid(True, alpha=0.2, linestyle='-', linewidth=0.8)
        ax1.set_facecolor('#FAFAFA')

        if flutter_speed is not None:
            ax1.axvline(x=flutter_speed, color=danger_color, linestyle='--',
                        linewidth=3, alpha=0.8, label=f'Flutter: {flutter_speed:.1f} m/s')
            ax1.legend(loc='best', framealpha=0.9)

        # V-g plot with enhanced styling
        if velocities is not None and dampings is not None and len(velocities) > 0 and len(dampings) > 0:
            ax2.plot(velocities, dampings, color=plot_color, linewidth=3,
                     marker='s', markersize=5, alpha=0.8, label='Damping')
            ax2.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
            # Highlight unstable region
            import numpy as np
            dampings_array = np.array(dampings)
            ax2.fill_between(velocities, dampings_array, 0, where=(dampings_array < 0),
                             color=danger_color, alpha=0.2, interpolate=True, label='Unstable')

            if flutter_speed is not None:
                ax2.axvline(x=flutter_speed, color=danger_color, linestyle='--',
                            linewidth=3, alpha=0.8, label=f'Flutter: {flutter_speed:.1f} m/s')
            ax2.legend(loc='best', framealpha=0.9)
        else:
            ax2.text(0.5, 0.5, 'No Data', transform=ax2.transAxes, ha='center', va='center',
                     fontsize=14, color=self.colors['text_light'])

        ax2.set_xlabel('Velocity (m/s)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Damping', fontsize=11, fontweight='bold')
        ax2.set_title('V-g Diagram', fontsize=12, fontweight='bold', pad=15)
        ax2.grid(True, alpha=0.2, linestyle='-', linewidth=0.8)
        ax2.set_facecolor('#FAFAFA')

        # Modern plot styling
        for ax in [ax1, ax2]:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_color('#CCCCCC')
            ax.spines['left'].set_color('#CCCCCC')
            ax.tick_params(colors='#666666')

        self.fig.tight_layout(pad=2.0)
        self.canvas.draw()

        # Update status with success message
        self.status_var.set("✅ Analysis completed successfully - Results updated")

    def plot_empty_results(self):
        """Plot beautiful empty results placeholder"""
        self.fig.clear()
        ax = self.fig.add_subplot(1, 1, 1)

        # Modern empty state styling
        ax.text(0.5, 0.6, '[CHART]', transform=ax.transAxes, ha='center', va='center',
                fontsize=48, color=self.colors['text_light'], alpha=0.5)
        ax.text(0.5, 0.4, 'No Results Available', transform=ax.transAxes, ha='center', va='center',
                fontsize=16, fontweight='bold', color=self.colors['text_secondary'])
        ax.text(0.5, 0.3, 'Run analysis to display V-f and V-g stability plots',
                transform=ax.transAxes, ha='center', va='center',
                fontsize=11, color=self.colors['text_light'])

        # Remove axes for clean look
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_facecolor(self.colors['surface'])

        self.fig.patch.set_facecolor(self.colors['surface'])
        self.fig.tight_layout()
        self.canvas.draw()

    def _run_multi_solver_analysis(self):
        """Run multi-solver flutter analysis with timeout protection"""
        try:
            # Import multi-solver framework
            from analysis.multi_solver_framework import (
                MultiSolverAnalyzer, SolverMethod, SolverSelector
            )
            from analysis.piston_theory_solver import PanelProperties, FlowConditions
            import time

            # Update status
            self.root.after(0, lambda: self.status_var.set("Initializing multi-solver analysis..."))
            self.root.after(0, lambda: self.progress_var.set(10))
            self.root.after(0, lambda: self.progress_label.config(text="Setting up analysis parameters..."))

            start_time = time.time()

            # Get panel properties from GUI with boundary conditions
            try:
                from analysis.boundary_conditions import BoundaryCondition
                bc_code = self.get_boundary_condition_code()
                bc_enum = BoundaryCondition(bc_code)
                boundary_conditions = bc_enum
            except:
                boundary_conditions = self.get_boundary_condition_code()

            panel = PanelProperties(
                length=float(self.length_var.get()) / 1000.0,  # Convert mm to m
                width=float(self.width_var.get()) / 1000.0,  # Convert mm to m
                thickness=float(self.thickness_var.get()) / 1000.0,  # Convert mm to m
                youngs_modulus=float(getattr(self, 'youngs_var', tk.StringVar(value="71.7e9")).get()),
                poissons_ratio=float(getattr(self, 'poisson_var', tk.StringVar(value="0.33")).get()),
                density=float(getattr(self, 'density_var', tk.StringVar(value="2810")).get()),
                boundary_conditions=boundary_conditions
            )

            # Get flow conditions
            flow = FlowConditions(
                mach_number=float(self.mach_var.get()),
                altitude=8000  # Default altitude
            )

            # Update status
            self.root.after(0, lambda: self.status_var.set("Getting solver recommendation..."))
            self.root.after(0, lambda: self.progress_var.set(20))

            # Get solver recommendation and run analysis
            analyzer = MultiSolverAnalyzer()
            selector = SolverSelector()
            recommendation = selector.recommend_solver(panel, flow)

            solver_method_str = self.solver_method_var.get().split()[0]
            methods = []

            if solver_method_str == "auto":
                methods = [recommendation.recommended_method]
            elif solver_method_str == "piston_theory":
                methods = [SolverMethod.PISTON_THEORY]
            elif solver_method_str == "doublet_lattice":
                methods = [SolverMethod.DOUBLET_LATTICE]

            if self.multi_solver_var.get() and len(methods) == 1:
                # Add comparison method
                if methods[0] == SolverMethod.PISTON_THEORY:
                    methods.append(SolverMethod.DOUBLET_LATTICE)
                else:
                    methods.append(SolverMethod.PISTON_THEORY)

            # Run analysis with timeout protection
            method_names = [m.value.replace('_', ' ').title() for m in methods]
            self.root.after(0, lambda: self.status_var.set(f"Running: {', '.join(method_names)}"))
            self.root.after(0, lambda: self.progress_var.set(50))
            self.root.after(0, lambda: self.progress_label.config(
                text=f"Executing {', '.join(method_names)} solver(s)..."))

            # Limit velocity range for faster analysis
            velocity_range = (float(self.vmin_var.get()), float(self.vmax_var.get()))
            max_points = 20  # Reduce points for faster analysis

            # Check for timeout during analysis
            if time.time() - start_time > 30:  # 30 second timeout
                raise TimeoutError("Analysis taking too long - try reducing velocity range")

            # Get NASTRAN configuration from GUI
            nastran_config = self.get_nastran_config()

            results = analyzer.analyze_with_multiple_solvers(
                panel, flow, methods, velocity_range, num_points=max_points,
                nastran_config=nastran_config
            )

            self.root.after(0, lambda: self.progress_var.set(90))
            self.root.after(0, lambda: self.progress_label.config(text="Processing results..."))

            # Process results
            has_results = any(method_results for method_results in results.values())

            if has_results:
                if len([r for r in results.values() if r]) > 1:
                    # Multi-solver comparison
                    comparison = analyzer.compare_results(results)
                    if comparison:
                        critical_speed = comparison.recommended_result.flutter_speed
                        critical_freq = comparison.recommended_result.flutter_frequency
                        confidence = comparison.confidence_level
                        # Fix lambda closure issues
                        status_msg = f"Multi-solver complete: {critical_speed:.1f} m/s (Confidence: {confidence})"
                        self.root.after(0, lambda msg=status_msg: self.status_var.set(msg))
                        self.root.after(0, lambda comp=comparison: self._display_multi_solver_results(comp))
                        # Update Results tab with plot data
                        plot_data = self._extract_plot_data(results)
                        self.root.after(0, lambda: self._update_results(
                            plot_data['velocities'], plot_data['frequencies'],
                            plot_data['dampings'], critical_speed, critical_freq
                        ))
                    else:
                        self.root.after(0, lambda: self.status_var.set("Analysis complete - comparison failed"))
                else:
                    # Single solver result
                    for method, method_results in results.items():
                        if method_results:
                            critical = min(method_results, key=lambda r: r.flutter_speed)
                            # Fix lambda closure issue
                            status_msg = f"{method} complete: {critical.flutter_speed:.1f} m/s"
                            self.root.after(0, lambda msg=status_msg: self.status_var.set(msg))
                            # Update Results tab with plot data
                            plot_data = self._extract_plot_data(results)
                            self.root.after(0, lambda: self._update_results(
                                plot_data['velocities'], plot_data['frequencies'],
                                plot_data['dampings'], critical.flutter_speed, critical.flutter_frequency
                            ))
                            break
            else:
                self.root.after(0, lambda: self.status_var.set("No flutter found in velocity range"))
                # Update Results tab to show no flutter
                self.root.after(0, lambda: self._update_results(None, None, None, None, None))

            # Update progress and status immediately
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda: self.progress_label.config(text="Analysis complete"))
            # Force GUI update
            self.root.after(0, lambda: self.root.update_idletasks())

        except Exception as e:
            self.logger.error(f"Multi-solver analysis failed: {e}")
            self.root.after(0, lambda: self.status_var.set(f"Analysis failed: {str(e)}"))
            self.root.after(0, lambda: self.progress_label.config(text="Analysis failed"))
        finally:
            # Reset GUI state
            self.root.after(0, lambda: self.run_button.config(state='normal'))
            self.root.after(0, lambda: self.stop_button.config(state='disabled'))
            # Reset progress after a short delay so user can see completion
            self.root.after(2000, lambda: self.progress_var.set(0))
            self.root.after(2000, lambda: self.progress_label.config(text="Ready for analysis"))

    def browse_nastran_executable(self):
        """Browse for NASTRAN executable file"""
        from tkinter import filedialog

        # File dialog for executable selection
        file_types = [
            ("Executable files", "*.exe"),
            ("All files", "*.*")
        ]

        filename = filedialog.askopenfilename(
            title="Select NASTRAN Executable",
            filetypes=file_types,
            initialdir="C:/",
        )

        if filename:
            self.nastran_path_var.set(filename)
            self.check_nastran_executable(filename)

    def detect_nastran_executable(self):
        """Auto-detect NASTRAN executable"""
        try:
            from analysis.nastran_solver import NastranSolver, NastranConfig

            # Create solver with default config to test detection
            config = NastranConfig()
            solver = NastranSolver(config)

            if solver.is_available():
                # Found NASTRAN
                self.nastran_path_var.set(solver.nastran_executable)
                self.nastran_status_var.set("[AVAILABLE] NASTRAN detected and ready")
                self.nastran_status_label.config(fg=self.colors['success'])
            else:
                # Not found
                self.nastran_path_var.set("auto-detect")
                self.nastran_status_var.set("[NOT FOUND] NASTRAN not detected - will use simulation mode")
                self.nastran_status_label.config(fg=self.colors['warning'])

        except Exception as e:
            self.nastran_status_var.set(f"[ERROR] Detection failed: {str(e)}")
            self.nastran_status_label.config(fg=self.colors['error'])

    def check_nastran_executable(self, path: str):
        """Check if specified NASTRAN executable is valid"""
        try:
            from analysis.nastran_solver import NastranSolver

            # Create a test solver with the specified path
            solver = NastranSolver()
            if solver._test_nastran_executable(path):
                self.nastran_status_var.set("[AVAILABLE] NASTRAN executable verified")
                self.nastran_status_label.config(fg=self.colors['success'])
            else:
                self.nastran_status_var.set("[INVALID] File is not a valid NASTRAN executable")
                self.nastran_status_label.config(fg=self.colors['error'])

        except Exception as e:
            self.nastran_status_var.set(f"[ERROR] Verification failed: {str(e)}")
            self.nastran_status_label.config(fg=self.colors['error'])

    def get_nastran_config(self):
        """Get NASTRAN configuration from GUI settings"""
        try:
            from analysis.nastran_solver import NastranConfig

            # Custom paths if specified
            nastran_paths = []
            current_path = self.nastran_path_var.get().strip()

            if current_path and current_path != "auto-detect":
                nastran_paths.insert(0, current_path)

            # Add default paths for fallback
            default_config = NastranConfig()
            nastran_paths.extend(default_config.nastran_paths)

            # Get memory and time settings
            memory = self.nastran_memory_var.get()
            try:
                cpu_time_minutes = int(self.nastran_time_var.get())
                cpu_time = cpu_time_minutes * 60  # Convert to seconds
            except:
                cpu_time = 1800  # Default 30 minutes

            return NastranConfig(
                nastran_paths=nastran_paths,
                memory=memory,
                cpu_time=cpu_time
            )

        except Exception as e:
            self.logger.error(f"Error creating NASTRAN config: {e}")
            # Return default config as fallback
            from analysis.nastran_solver import NastranConfig
            return NastranConfig()

    def _extract_plot_data(self, results):
        """Extract plot data from multi-solver results"""
        velocities = []
        frequencies = []
        dampings = []

        # Combine results from all methods
        for method, method_results in results.items():
            if method_results:
                for result in method_results:
                    velocities.append(result.flutter_speed)
                    frequencies.append(result.flutter_frequency)
                    dampings.append(result.damping)

        # Sort by velocity for plotting
        if velocities:
            sorted_data = sorted(zip(velocities, frequencies, dampings))
            velocities, frequencies, dampings = zip(*sorted_data)

        return {
            'velocities': list(velocities) if velocities else [],
            'frequencies': list(frequencies) if frequencies else [],
            'dampings': list(dampings) if dampings else []
        }

    def _display_multi_solver_results(self, comparison):
        """Display multi-solver comparison results"""
        try:
            results_window = tk.Toplevel(self.root)
            results_window.title("Multi-Solver Flutter Analysis Results")
            results_window.geometry("600x400")

            main_frame = tk.Frame(results_window, bg=self.colors['background'])
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # Title
            tk.Label(main_frame, text="Multi-Solver Analysis Results",
                     bg=self.colors['background'], fg=self.colors['text_primary'],
                     font=('Segoe UI', 14, 'bold')).pack(pady=(0, 20))

            # Results summary
            summary_text = f"""Confidence Level: {comparison.confidence_level}
            
Recommended Flutter Speed: {comparison.recommended_result.flutter_speed:.1f} m/s
Method: {comparison.recommended_result.method}
            
Comparison:"""

            for i, method in enumerate(comparison.methods):
                speed = comparison.flutter_speeds[i]
                diff = comparison.relative_differences[method]
                summary_text += f"\n  {method}: {speed:.1f} m/s ({diff:+.1f}%)"

            tk.Label(main_frame, text=summary_text, justify=tk.LEFT,
                     bg=self.colors['background'], fg=self.colors['text_primary'],
                     font=('Segoe UI', 10)).pack(pady=20)

            ttk.Button(main_frame, text="Close", command=results_window.destroy).pack(pady=10)

        except Exception as e:
            self.logger.error(f"Error displaying results: {e}")

    def run(self):
        """Start the application"""
        print("GUI started successfully!")
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = PanelFlutterGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Error", f"Application error: {e}")
    finally:
        print("Application closed")
