"""
Material Panel for Panel Flutter Analysis GUI
============================================

Provides interface for defining material properties including
isotropic, orthotropic, and composite materials.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from ...gui.utils.widgets import LabeledEntry, LabeledSpinbox, ParameterTable
from ...gui.utils.validation import is_valid_float, is_positive_float


class MaterialPanel:
    """
    Panel for material property definition and management.
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.controller = None
        
        # Create main frame
        self.frame = ttk.Frame(parent, style='Modern.TFrame')
        
        self.setup_ui()
        self.bind_events()
        
    def setup_ui(self):
        """Initialize the user interface components."""
        # Material type selection
        type_frame = ttk.LabelFrame(self.frame, text="Material Type", padding=10)
        type_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.material_type_var = tk.StringVar(value="isotropic")
        material_types = ["isotropic", "orthotropic", "composite"]
        
        for i, mat_type in enumerate(material_types):
            rb = ttk.Radiobutton(
                type_frame,
                text=mat_type.capitalize(),
                variable=self.material_type_var,
                value=mat_type,
                command=self.on_material_type_changed
            )
            rb.grid(row=0, column=i, padx=10, pady=5)
            
        # Create notebook for material property tabs
        self.notebook = ttk.Notebook(self.frame, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Basic properties tab
        self.create_basic_properties_tab()
        
        # Advanced properties tab
        self.create_advanced_properties_tab()
        
        # Material database tab
        self.create_material_database_tab()
        
    def create_basic_properties_tab(self):
        """Create basic material properties tab."""
        basic_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(basic_frame, text="Basic Properties")
        
        # General properties frame
        general_frame = ttk.LabelFrame(basic_frame, text="General Properties", padding=10)
        general_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Material name
        self.name_entry = LabeledEntry(general_frame, "Material Name:", width=20)
        self.name_entry.set("Aluminum 7075-T6")
        self.name_entry.pack(anchor=tk.W, pady=2)
        
        # Density
        self.density_entry = LabeledEntry(general_frame, "Density (kg/m³):", is_positive_float, width=15)
        self.density_entry.set("2700")
        self.density_entry.pack(anchor=tk.W, pady=2)
        
        # Mechanical properties frame
        mech_frame = ttk.LabelFrame(basic_frame, text="Mechanical Properties", padding=10)
        mech_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Young's modulus
        self.youngs_modulus_entry = LabeledEntry(mech_frame, "Young's Modulus (Pa):", is_positive_float, width=15)
        self.youngs_modulus_entry.set("7.0e10")
        self.youngs_modulus_entry.pack(anchor=tk.W, pady=2)
        
        # Poisson's ratio
        self.poissons_ratio_entry = LabeledEntry(mech_frame, "Poisson's Ratio:", 
                                                lambda x: self.validate_poisson_ratio(x), width=15)
        self.poissons_ratio_entry.set("0.33")
        self.poissons_ratio_entry.pack(anchor=tk.W, pady=2)
        
        # Shear modulus
        self.shear_modulus_entry = LabeledEntry(mech_frame, "Shear Modulus (Pa):", is_positive_float, width=15)
        self.shear_modulus_entry.set("2.6e10")
        self.shear_modulus_entry.pack(anchor=tk.W, pady=2)
        
        # Geometry properties frame
        geom_frame = ttk.LabelFrame(basic_frame, text="Geometry Properties", padding=10)
        geom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Thickness
        self.thickness_entry = LabeledEntry(geom_frame, "Thickness (mm):", is_positive_float, width=15)
        self.thickness_entry.set("2.0")
        self.thickness_entry.pack(anchor=tk.W, pady=2)
        
        # Calculate derived properties button
        ttk.Button(mech_frame, text="Calculate Derived Properties", 
                  command=self.calculate_derived_properties,
                  style='Modern.TButton').pack(pady=5)
                  
    def create_advanced_properties_tab(self):
        """Create advanced material properties tab."""
        advanced_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(advanced_frame, text="Advanced")
        
        # Orthotropic properties frame (initially hidden)
        self.orthotropic_frame = ttk.LabelFrame(advanced_frame, text="Orthotropic Properties", padding=10)
        self.orthotropic_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # E11, E22, E33
        self.e11_entry = LabeledEntry(self.orthotropic_frame, "E11 (Pa):", is_positive_float, width=15)
        self.e11_entry.pack(anchor=tk.W, pady=2)
        
        self.e22_entry = LabeledEntry(self.orthotropic_frame, "E22 (Pa):", is_positive_float, width=15)
        self.e22_entry.pack(anchor=tk.W, pady=2)
        
        self.e33_entry = LabeledEntry(self.orthotropic_frame, "E33 (Pa):", is_positive_float, width=15)
        self.e33_entry.pack(anchor=tk.W, pady=2)
        
        # G12, G13, G23
        self.g12_entry = LabeledEntry(self.orthotropic_frame, "G12 (Pa):", is_positive_float, width=15)
        self.g12_entry.pack(anchor=tk.W, pady=2)
        
        self.g13_entry = LabeledEntry(self.orthotropic_frame, "G13 (Pa):", is_positive_float, width=15)
        self.g13_entry.pack(anchor=tk.W, pady=2)
        
        self.g23_entry = LabeledEntry(self.orthotropic_frame, "G23 (Pa):", is_positive_float, width=15)
        self.g23_entry.pack(anchor=tk.W, pady=2)
        
        # nu12, nu13, nu23
        self.nu12_entry = LabeledEntry(self.orthotropic_frame, "ν12:", 
                                      lambda x: self.validate_poisson_ratio(x), width=15)
        self.nu12_entry.pack(anchor=tk.W, pady=2)
        
        self.nu13_entry = LabeledEntry(self.orthotropic_frame, "ν13:", 
                                      lambda x: self.validate_poisson_ratio(x), width=15)
        self.nu13_entry.pack(anchor=tk.W, pady=2)
        
        self.nu23_entry = LabeledEntry(self.orthotropic_frame, "ν23:", 
                                      lambda x: self.validate_poisson_ratio(x), width=15)
        self.nu23_entry.pack(anchor=tk.W, pady=2)
        
        # Composite layup frame
        self.composite_frame = ttk.LabelFrame(advanced_frame, text="Composite Layup", padding=10)
        self.composite_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Layup table
        self.layup_table = ParameterTable(self.composite_frame, 
                                         ["Layer", "Material", "Thickness (mm)", "Angle (°)"])
        self.layup_table.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Layup controls
        layup_controls = ttk.Frame(self.composite_frame)
        layup_controls.pack(fill=tk.X, pady=5)
        
        ttk.Button(layup_controls, text="Add Layer", command=self.add_composite_layer,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(layup_controls, text="Remove Layer", command=self.remove_composite_layer,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(layup_controls, text="Move Up", command=self.move_layer_up,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(layup_controls, text="Move Down", command=self.move_layer_down,
                  style='Modern.TButton').pack(side=tk.LEFT, padx=2)
                  
        # Thermal properties frame
        thermal_frame = ttk.LabelFrame(advanced_frame, text="Thermal Properties", padding=10)
        thermal_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.thermal_expansion_entry = LabeledEntry(thermal_frame, "Thermal Expansion (1/K):", 
                                                   is_valid_float, width=15)
        self.thermal_expansion_entry.set("2.3e-5")
        self.thermal_expansion_entry.pack(anchor=tk.W, pady=2)
        
        self.thermal_conductivity_entry = LabeledEntry(thermal_frame, "Thermal Conductivity (W/m·K):", 
                                                      is_positive_float, width=15)
        self.thermal_conductivity_entry.set("130")
        self.thermal_conductivity_entry.pack(anchor=tk.W, pady=2)
        
    def create_material_database_tab(self):
        """Create material database tab."""
        database_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(database_frame, text="Database")
        
        # Material selection frame
        selection_frame = ttk.LabelFrame(database_frame, text="Material Database", padding=10)
        selection_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Material category
        ttk.Label(selection_frame, text="Category:", style='Modern.TLabel').pack(anchor=tk.W)
        self.material_category_var = tk.StringVar(value="aluminum")
        category_combo = ttk.Combobox(selection_frame, textvariable=self.material_category_var,
                                    values=["aluminum", "steel", "titanium", "composite", "other"],
                                    state="readonly", style='Modern.TCombobox')
        category_combo.pack(fill=tk.X, pady=2)
        category_combo.bind('<<ComboboxSelected>>', self.on_category_changed)
        
        # Material selection
        ttk.Label(selection_frame, text="Material:", style='Modern.TLabel').pack(anchor=tk.W, pady=(10, 0))
        self.material_selection_var = tk.StringVar()
        self.material_combo = ttk.Combobox(selection_frame, textvariable=self.material_selection_var,
                                         state="readonly", style='Modern.TCombobox')
        self.material_combo.pack(fill=tk.X, pady=2)
        self.material_combo.bind('<<ComboboxSelected>>', self.on_material_selected)
        
        # Load from database button
        ttk.Button(selection_frame, text="Load Material Properties", 
                  command=self.load_from_database,
                  style='Success.TButton').pack(pady=10)
                  
        # Material properties display
        properties_frame = ttk.LabelFrame(database_frame, text="Properties Preview", padding=10)
        properties_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.properties_text = tk.Text(properties_frame, height=15, width=50, 
                                      font=('Consolas', 9), state=tk.DISABLED)
        self.properties_text.pack(fill=tk.BOTH, expand=True)
        
        # Initialize material database
        self.init_material_database()
        self.on_category_changed()
        
    def init_material_database(self):
        """Initialize the material database."""
        self.material_database = {
            "aluminum": {
                "7075-T6": {
                    "name": "Aluminum 7075-T6",
                    "density": 2700,
                    "youngs_modulus": 7.0e10,
                    "poissons_ratio": 0.33,
                    "shear_modulus": 2.6e10,
                    "thermal_expansion": 2.3e-5,
                    "thermal_conductivity": 130
                },
                "6061-T6": {
                    "name": "Aluminum 6061-T6", 
                    "density": 2700,
                    "youngs_modulus": 6.9e10,
                    "poissons_ratio": 0.33,
                    "shear_modulus": 2.6e10,
                    "thermal_expansion": 2.4e-5,
                    "thermal_conductivity": 167
                }
            },
            "steel": {
                "AISI 4130": {
                    "name": "AISI 4130 Steel",
                    "density": 7850,
                    "youngs_modulus": 2.0e11,
                    "poissons_ratio": 0.29,
                    "shear_modulus": 8.0e10,
                    "thermal_expansion": 1.2e-5,
                    "thermal_conductivity": 42
                }
            },
            "titanium": {
                "Ti-6Al-4V": {
                    "name": "Titanium Ti-6Al-4V",
                    "density": 4430,
                    "youngs_modulus": 1.14e11,
                    "poissons_ratio": 0.32,
                    "shear_modulus": 4.4e10,
                    "thermal_expansion": 8.6e-6,
                    "thermal_conductivity": 6.7
                }
            },
            "composite": {
                "Carbon/Epoxy": {
                    "name": "Carbon Fiber/Epoxy",
                    "density": 1600,
                    "material_type": "orthotropic",
                    "e11": 1.5e11,
                    "e22": 9.0e9,
                    "e33": 9.0e9,
                    "g12": 5.0e9,
                    "g13": 5.0e9,
                    "g23": 3.0e9,
                    "nu12": 0.3,
                    "nu13": 0.3,
                    "nu23": 0.4
                }
            }
        }
        
    def bind_events(self):
        """Bind events to UI components."""
        # Bind Young's modulus and Poisson's ratio changes to auto-calculate shear modulus
        self.youngs_modulus_entry.var.trace('w', self.auto_calculate_shear_modulus)
        self.poissons_ratio_entry.var.trace('w', self.auto_calculate_shear_modulus)
        
    def set_controller(self, controller):
        """Set the controller for this panel."""
        self.controller = controller
        
    def validate_poisson_ratio(self, value):
        """Validate Poisson's ratio is between 0 and 0.5."""
        try:
            val = float(value)
            return 0 <= val < 0.5
        except (ValueError, TypeError):
            return False
            
    def on_material_type_changed(self):
        """Handle material type change."""
        material_type = self.material_type_var.get()
        
        if material_type == "isotropic":
            # Hide orthotropic and composite frames
            self.orthotropic_frame.pack_forget()
            self.composite_frame.pack_forget()
        elif material_type == "orthotropic":
            # Show orthotropic frame, hide composite frame
            self.orthotropic_frame.pack(fill=tk.X, padx=5, pady=5, before=self.composite_frame)
            self.composite_frame.pack_forget()
        elif material_type == "composite":
            # Show both orthotropic and composite frames
            self.orthotropic_frame.pack(fill=tk.X, padx=5, pady=5)
            self.composite_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
        if self.controller:
            self.notify_material_changed()
            
    def auto_calculate_shear_modulus(self, *args):
        """Automatically calculate shear modulus from E and nu."""
        try:
            E = float(self.youngs_modulus_entry.get())
            nu = float(self.poissons_ratio_entry.get())
            G = E / (2 * (1 + nu))
            self.shear_modulus_entry.set(f"{G:.3e}")
        except (ValueError, TypeError):
            pass
            
    def calculate_derived_properties(self):
        """Calculate derived material properties."""
        try:
            # Get basic properties
            E = float(self.youngs_modulus_entry.get())
            nu = float(self.poissons_ratio_entry.get())
            rho = float(self.density_entry.get())
            
            # Calculate derived properties
            G = E / (2 * (1 + nu))
            K = E / (3 * (1 - 2 * nu))  # Bulk modulus
            
            # Speed of sound calculations
            c_longitudinal = np.sqrt(E * (1 - nu) / (rho * (1 + nu) * (1 - 2 * nu)))
            c_shear = np.sqrt(G / rho)
            
            # Display results
            results = f"""
Derived Material Properties:
============================
Shear Modulus (G): {G:.3e} Pa
Bulk Modulus (K): {K:.3e} Pa
Longitudinal Wave Speed: {c_longitudinal:.1f} m/s
Shear Wave Speed: {c_shear:.1f} m/s
            """
            
            messagebox.showinfo("Derived Properties", results)
            
            # Update shear modulus field
            self.shear_modulus_entry.set(f"{G:.3e}")
            
        except (ValueError, TypeError) as e:
            messagebox.showerror("Calculation Error", f"Error calculating properties: {str(e)}")
            
    def on_category_changed(self, event=None):
        """Handle material category change."""
        category = self.material_category_var.get()
        materials = list(self.material_database.get(category, {}).keys())
        
        self.material_combo.configure(values=materials)
        if materials:
            self.material_combo.set(materials[0])
            self.on_material_selected()
            
    def on_material_selected(self, event=None):
        """Handle material selection change."""
        category = self.material_category_var.get()
        material = self.material_selection_var.get()
        
        if category in self.material_database and material in self.material_database[category]:
            properties = self.material_database[category][material]
            self.display_material_properties(properties)
            
    def display_material_properties(self, properties):
        """Display material properties in the text widget."""
        self.properties_text.configure(state=tk.NORMAL)
        self.properties_text.delete(1.0, tk.END)
        
        text = f"Material: {properties.get('name', 'Unknown')}\n"
        text += "=" * 40 + "\n\n"
        
        for key, value in properties.items():
            if key == 'name':
                continue
            if isinstance(value, float):
                if value > 1e6:
                    text += f"{key.replace('_', ' ').title()}: {value:.2e}\n"
                else:
                    text += f"{key.replace('_', ' ').title()}: {value}\n"
            else:
                text += f"{key.replace('_', ' ').title()}: {value}\n"
                
        self.properties_text.insert(1.0, text)
        self.properties_text.configure(state=tk.DISABLED)
        
    def load_from_database(self):
        """Load selected material from database."""
        category = self.material_category_var.get()
        material = self.material_selection_var.get()
        
        if not material:
            messagebox.showwarning("No Selection", "Please select a material from the database")
            return
            
        if category in self.material_database and material in self.material_database[category]:
            properties = self.material_database[category][material]
            
            # Set basic properties
            self.name_entry.set(properties.get('name', ''))
            self.density_entry.set(str(properties.get('density', '')))
            
            if 'youngs_modulus' in properties:
                self.material_type_var.set('isotropic')
                self.youngs_modulus_entry.set(str(properties['youngs_modulus']))
                self.poissons_ratio_entry.set(str(properties['poissons_ratio']))
                self.shear_modulus_entry.set(str(properties.get('shear_modulus', '')))
            elif 'e11' in properties:
                self.material_type_var.set('orthotropic')
                self.e11_entry.set(str(properties['e11']))
                self.e22_entry.set(str(properties['e22']))
                self.e33_entry.set(str(properties['e33']))
                self.g12_entry.set(str(properties['g12']))
                self.g13_entry.set(str(properties['g13']))
                self.g23_entry.set(str(properties['g23']))
                self.nu12_entry.set(str(properties['nu12']))
                self.nu13_entry.set(str(properties['nu13']))
                self.nu23_entry.set(str(properties['nu23']))
                
            # Thermal properties
            if 'thermal_expansion' in properties:
                self.thermal_expansion_entry.set(str(properties['thermal_expansion']))
            if 'thermal_conductivity' in properties:
                self.thermal_conductivity_entry.set(str(properties['thermal_conductivity']))
                
            # Update UI
            self.on_material_type_changed()
            
            messagebox.showinfo("Material Loaded", f"Loaded {properties.get('name', material)} properties")
            
    def add_composite_layer(self):
        """Add a new composite layer."""
        layer_num = len(self.layup_table.tree.get_children()) + 1
        self.layup_table.insert_row([f"Layer {layer_num}", "Carbon/Epoxy", "0.125", "0"])
        
    def remove_composite_layer(self):
        """Remove selected composite layer."""
        selection = self.layup_table.tree.selection()
        if selection:
            self.layup_table.tree.delete(selection[0])
        else:
            messagebox.showwarning("No Selection", "Please select a layer to remove")
            
    def move_layer_up(self):
        """Move selected layer up."""
        messagebox.showinfo("Move Layer", "Layer reordering not yet implemented")
        
    def move_layer_down(self):
        """Move selected layer down."""
        messagebox.showinfo("Move Layer", "Layer reordering not yet implemented")
        
    def get_material_data(self) -> dict:
        """Get current material data."""
        try:
            material_data = {
                'material_type': self.material_type_var.get(),
                'name': self.name_entry.get(),
                'density': float(self.density_entry.get()) if self.density_entry.get() else 0.0,
                'thickness': float(self.thickness_entry.get()) if self.thickness_entry.get() else 0.0
            }
            
            if self.material_type_var.get() == 'isotropic':
                material_data.update({
                    'youngs_modulus': float(self.youngs_modulus_entry.get()) if self.youngs_modulus_entry.get() else 0.0,
                    'poissons_ratio': float(self.poissons_ratio_entry.get()) if self.poissons_ratio_entry.get() else 0.0,
                    'shear_modulus': float(self.shear_modulus_entry.get()) if self.shear_modulus_entry.get() else 0.0
                })
            elif self.material_type_var.get() == 'orthotropic':
                material_data.update({
                    'e11': float(self.e11_entry.get()) if self.e11_entry.get() else 0.0,
                    'e22': float(self.e22_entry.get()) if self.e22_entry.get() else 0.0,
                    'e33': float(self.e33_entry.get()) if self.e33_entry.get() else 0.0,
                    'g12': float(self.g12_entry.get()) if self.g12_entry.get() else 0.0,
                    'g13': float(self.g13_entry.get()) if self.g13_entry.get() else 0.0,
                    'g23': float(self.g23_entry.get()) if self.g23_entry.get() else 0.0,
                    'nu12': float(self.nu12_entry.get()) if self.nu12_entry.get() else 0.0,
                    'nu13': float(self.nu13_entry.get()) if self.nu13_entry.get() else 0.0,
                    'nu23': float(self.nu23_entry.get()) if self.nu23_entry.get() else 0.0
                })
                
            # Thermal properties
            if self.thermal_expansion_entry.get():
                material_data['thermal_expansion'] = float(self.thermal_expansion_entry.get())
            if self.thermal_conductivity_entry.get():
                material_data['thermal_conductivity'] = float(self.thermal_conductivity_entry.get())
                
            return material_data
            
        except (ValueError, TypeError) as e:
            messagebox.showerror("Invalid Data", f"Error reading material data: {str(e)}")
            return {}
            
    def set_material_data(self, material_data: dict):
        """Set material data from external source."""
        try:
            # Set material type first
            self.material_type_var.set(material_data.get('material_type', 'isotropic'))
            
            # Basic properties
            self.name_entry.set(material_data.get('name', ''))
            self.density_entry.set(str(material_data.get('density', '')))
            self.thickness_entry.set(str(material_data.get('thickness', '')))
            
            # Isotropic properties
            if 'youngs_modulus' in material_data:
                self.youngs_modulus_entry.set(str(material_data['youngs_modulus']))
            if 'poissons_ratio' in material_data:
                self.poissons_ratio_entry.set(str(material_data['poissons_ratio']))
            if 'shear_modulus' in material_data:
                self.shear_modulus_entry.set(str(material_data['shear_modulus']))
                
            # Orthotropic properties
            for prop in ['e11', 'e22', 'e33', 'g12', 'g13', 'g23', 'nu12', 'nu13', 'nu23']:
                if prop in material_data:
                    entry = getattr(self, f"{prop}_entry", None)
                    if entry:
                        entry.set(str(material_data[prop]))
                        
            # Thermal properties
            if 'thermal_expansion' in material_data:
                self.thermal_expansion_entry.set(str(material_data['thermal_expansion']))
            if 'thermal_conductivity' in material_data:
                self.thermal_conductivity_entry.set(str(material_data['thermal_conductivity']))
                
            # Update UI
            self.on_material_type_changed()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error setting material data: {str(e)}")
            
    def notify_material_changed(self):
        """Notify controller of material changes."""
        if self.controller:
            material_data = self.get_material_data()
            self.controller.update_materials(material_data)