"""
In-Application Help and Documentation System
==========================================

This module provides comprehensive help and documentation for the Panel Flutter
Analysis GUI tool, including tooltips, context-sensitive help, and user guides.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import webbrowser
from typing import Dict, Optional
from pathlib import Path


class HelpSystem:
    """Comprehensive help and documentation system"""
    
    def __init__(self, parent):
        self.parent = parent
        self.help_window = None
        self.tooltip_windows = []
        
        # Documentation content
        self.help_content = {
            "getting_started": {
                "title": "Getting Started",
                "content": """
# Getting Started with Panel Flutter Analysis

## Overview
This tool provides comprehensive panel flutter analysis capabilities for aerospace applications. It supports both metallic and composite panels with various boundary conditions and analysis methods.

## Quick Start Guide

### 1. Geometry Setup
- Navigate to the **Geometry** tab
- Enter panel dimensions (length, width, thickness)
- Select boundary conditions (SSSS, CCCC, etc.)
- Choose mesh density for analysis

### 2. Material Definition
- Go to the **Materials** tab
- Select material type (Isotropic, Orthotropic, or Laminated)
- Enter material properties
- For laminates: define layer stackup using the layer editor

### 3. Analysis Setup
- Switch to the **Analysis** tab
- Choose analysis method (PK, K, KE methods)
- Set velocity and Mach number ranges
- Configure solver parameters

### 4. Run Analysis
- Click **Run Analysis** to start computation
- Monitor progress in the status bar
- View results in the **Results** tab

### 5. Results Interpretation
- Examine flutter velocity and frequency
- Review stability plots and mode shapes
- Export results for reporting
"""
            },
            
            "geometry": {
                "title": "Geometry Configuration",
                "content": """
# Panel Geometry Setup

## Panel Dimensions
- **Length (a)**: Panel length in flow direction (millimeters)
- **Width (b)**: Panel width perpendicular to flow (millimeters)
- **Thickness (h)**: Panel thickness (millimeters)

## Mesh Parameters
- **Elements X**: Number of elements along length (min: 10)
- **Elements Y**: Number of elements along width (min: 5)
- **Aspect Ratio**: Recommended element aspect ratio: 1-3

## Boundary Conditions
- **SSSS**: Simply supported on all edges (typical for aircraft panels)
- **CCCC**: Clamped on all edges (rigid attachment)
- **CFCF**: Clamped-free-clamped-free (wing-like structure)
- **Custom**: Define individual edge constraints

## Guidelines
- Use sufficient mesh density for accurate results
- Maintain reasonable aspect ratios (length/width < 5)
- Consider manufacturing constraints in thickness selection
"""
            },
            
            "materials": {
                "title": "Material Properties",
                "content": """
# Material Definition

## Isotropic Materials (Metals)
- **Young's Modulus (E)**: Elastic modulus (Pa)
- **Poisson's Ratio (ν)**: Lateral strain ratio (0.0-0.5)
- **Density (ρ)**: Material density (kg/m³)

**Example: Aluminum 7075-T6**
- E = 71.7 GPa
- ν = 0.33
- ρ = 2,810 kg/m³

## Orthotropic Materials (Unidirectional Composites)
- **E₁**: Fiber direction modulus (Pa)
- **E₂**: Transverse direction modulus (Pa)
- **G₁₂**: In-plane shear modulus (Pa)
- **ν₁₂**: Major Poisson's ratio

**Example: Carbon/Epoxy**
- E₁ = 150 GPa
- E₂ = 9.0 GPa
- G₁₂ = 4.8 GPa
- ν₁₂ = 0.3

## Laminated Composites
Use the layer editor to define:
- Individual layer properties
- Ply orientations ([0°, ±45°, 90°])
- Layer thicknesses
- Stacking sequence

The tool automatically computes ABD matrices using Classical Laminate Theory.
"""
            },
            
            "analysis": {
                "title": "Flutter Analysis Methods",
                "content": """
# Flutter Analysis Configuration

## Analysis Methods
- **PK Method**: P-K method (recommended for subsonic)
- **K Method**: K-method for high subsonic/transonic
- **KE Method**: K-E method with extra aerodynamic states
- **PKNL Method**: P-K method with nonlinear effects

## Aerodynamic Theories
- **Piston Theory**: Simple, fast, good for supersonic
- **Van Dyke Theory**: More accurate for low supersonic
- **ZONA Theory**: Advanced panel methods

## Velocity Range
- **Minimum Velocity**: Starting velocity (m/s)
- **Maximum Velocity**: Ending velocity (m/s)
- **Velocity Points**: Number of analysis points (25-50 recommended)

## Mach Number Range
- **Mach Min**: Minimum Mach number
- **Mach Max**: Maximum Mach number
- **Points**: Number of Mach points for analysis

## Solver Parameters
- **Number of Modes**: Structural modes to include (10-20 typical)
- **Max Frequency**: Upper frequency limit (Hz)
- **Convergence Tolerance**: Solution accuracy (1e-6 recommended)

## Guidelines
- Start with PK method for initial analysis
- Use sufficient velocity points for smooth curves
- Include enough modes to capture flutter behavior
"""
            },
            
            "results": {
                "title": "Results Interpretation",
                "content": """
# Understanding Flutter Results

## Key Results
- **Flutter Velocity (Vf)**: Critical velocity where instability occurs
- **Flutter Frequency (ff)**: Frequency at flutter onset
- **Flutter Mode**: Structural mode that becomes unstable

## V-g Diagrams
- **X-axis**: Velocity (m/s)
- **Y-axis**: Damping coefficient (g)
- **Zero crossing**: Indicates flutter onset
- **Negative damping**: Unstable (flutter) region

## V-f Diagrams
- **X-axis**: Velocity (m/s)
- **Y-axis**: Frequency (Hz)
- **Frequency coalescence**: Often precedes flutter

## Safety Factors
- **Aerospace applications**: Use 15% margin above flutter speed
- **Structural modifications**: Consider if Vf < 1.15 × Operating speed
- **Certification requirements**: Follow applicable airworthiness standards

## Troubleshooting
- **No flutter found**: Increase velocity range
- **Multiple flutter points**: Check mode participation
- **Unrealistic results**: Verify material properties and geometry

## Result Validation
- Compare with published test data
- Check mode shapes for physical realism
- Verify boundary condition implementation
"""
            },
            
            "troubleshooting": {
                "title": "Troubleshooting Guide",
                "content": """
# Common Issues and Solutions

## Analysis Fails to Start
- **Check inputs**: Verify all required parameters are entered
- **Material properties**: Ensure positive values for moduli and density
- **Geometry**: Check for zero or negative dimensions
- **Mesh**: Verify adequate mesh density

## Convergence Problems
- **Reduce tolerance**: Try 1e-5 instead of 1e-6
- **Increase iterations**: Raise maximum iteration count
- **Check conditioning**: Very thin panels may have numerical issues

## Unrealistic Results
- **Units consistency**: Verify all inputs use consistent units (SI recommended)
- **Material data**: Double-check material properties against references
- **Boundary conditions**: Ensure appropriate constraints for application

## Performance Issues
- **Reduce mesh density**: Start with coarser mesh for initial studies
- **Limit velocity points**: Use 25-30 points initially
- **Reduce modes**: Start with 10-15 modes

## Getting Help
- **Reference Manual**: Detailed theoretical background
- **Examples**: Built-in validation cases
- **Support**: Contact development team for assistance

## Best Practices
- Always start with simple cases to verify setup
- Use published validation data when available
- Document analysis assumptions and limitations
- Perform sensitivity studies on key parameters
"""
            }
        }
        
        # Tooltip content for GUI elements
        self.tooltips = {
            # Geometry tab tooltips
            "length_entry": "Panel length in flow direction (millimeters). Typical range: 100-10000 mm",
            "width_entry": "Panel width perpendicular to flow (millimeters). Typical range: 50-5000 mm", 
            "thickness_entry": "Panel thickness (millimeters). For metals: 1-10 mm, composites: 0.1-5 mm",
            "boundary_combo": "Select boundary conditions: SSSS (simply supported), CCCC (clamped), etc.",
            "mesh_x_entry": "Number of elements along length. Minimum 10, recommended 20-50",
            "mesh_y_entry": "Number of elements along width. Minimum 5, recommended 10-25",
            
            # Materials tab tooltips
            "material_type": "Select material type: Isotropic (metals), Orthotropic (UD composite), Laminate (multi-layer)",
            "youngs_modulus": "Elastic modulus in Pa. Aluminum: ~70 GPa, Steel: ~200 GPa, CFRP: ~150 GPa",
            "poisson_ratio": "Lateral strain ratio. Range: 0-0.5. Metals: ~0.3, composites: 0.25-0.35",
            "density": "Material density in kg/m³. Al: ~2800, Steel: ~7800, CFRP: ~1600",
            "e1_entry": "Fiber direction modulus (Pa) for orthotropic materials",
            "e2_entry": "Transverse direction modulus (Pa) for orthotropic materials", 
            "g12_entry": "In-plane shear modulus (Pa) for orthotropic materials",
            "nu12_entry": "Major Poisson's ratio for orthotropic materials",
            
            # Analysis tab tooltips
            "method_combo": "Analysis method: PK (general), K (transonic), KE (advanced), PKNL (nonlinear)",
            "aero_combo": "Aerodynamic theory: Piston (simple), Van Dyke (accurate), ZONA (advanced)",
            "velocity_min": "Minimum analysis velocity (m/s). Start below expected flutter velocity",
            "velocity_max": "Maximum analysis velocity (m/s). End well above expected flutter velocity",
            "velocity_points": "Number of velocity points. More points = smoother curves but longer analysis",
            "mach_min": "Minimum Mach number for analysis. Typical: 0.3-0.8",
            "mach_max": "Maximum Mach number for analysis. Typical: 0.8-3.0",
            "num_modes": "Number of structural modes. Include enough to capture flutter mode",
            "max_frequency": "Upper frequency limit (Hz). Set above expected flutter frequency",
            
            # Results tab tooltips
            "flutter_velocity": "Critical velocity where flutter instability occurs",
            "flutter_frequency": "Frequency at which flutter develops",
            "flutter_mode": "Structural mode number that becomes unstable",
            "vg_plot": "Velocity-damping plot. Flutter occurs where damping crosses zero",
            "vf_plot": "Velocity-frequency plot. Shows frequency variation with velocity",
            "export_button": "Export results to various formats (CSV, PDF, images)"
        }
    
    def show_help_window(self, topic: str = "getting_started"):
        """Show main help window with specified topic"""
        if self.help_window and self.help_window.winfo_exists():
            self.help_window.lift()
            self.load_topic(topic)
            return
            
        self.help_window = tk.Toplevel(self.parent)
        self.help_window.title("Panel Flutter Analysis - Help & Documentation")
        self.help_window.geometry("900x700")
        self.help_window.iconname("Help")
        
        # Create main frame
        main_frame = ttk.Frame(self.help_window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create topic navigation
        nav_frame = ttk.LabelFrame(main_frame, text="Topics", padding=10)
        nav_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Topic buttons
        topics = [
            ("Getting Started", "getting_started"),
            ("Geometry Setup", "geometry"),
            ("Materials", "materials"),
            ("Analysis Methods", "analysis"),
            ("Results", "results"),
            ("Troubleshooting", "troubleshooting")
        ]
        
        for topic_name, topic_key in topics:
            btn = ttk.Button(nav_frame, text=topic_name, width=15,
                           command=lambda k=topic_key: self.load_topic(k))
            btn.pack(fill='x', pady=2)
        
        # Add separator
        ttk.Separator(nav_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Additional help buttons
        ttk.Button(nav_frame, text="User Manual", 
                  command=self.open_user_manual).pack(fill='x', pady=2)
        ttk.Button(nav_frame, text="Examples", 
                  command=self.show_examples).pack(fill='x', pady=2)
        ttk.Button(nav_frame, text="About", 
                  command=self.show_about).pack(fill='x', pady=2)
        
        # Create content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(side='right', fill='both', expand=True)
        
        # Title label
        self.title_label = ttk.Label(content_frame, text="", font=('Arial', 16, 'bold'))
        self.title_label.pack(anchor='w', pady=(0, 10))
        
        # Content text area
        self.content_text = scrolledtext.ScrolledText(content_frame, wrap='word', 
                                                     width=70, height=35, font=('Consolas', 10))
        self.content_text.pack(fill='both', expand=True)
        
        # Load initial topic
        self.load_topic(topic)
        
        # Center window
        self.help_window.transient(self.parent)
        self.help_window.grab_set()
    
    def load_topic(self, topic: str):
        """Load help topic content"""
        if topic in self.help_content:
            content = self.help_content[topic]
            self.title_label.config(text=content["title"])
            
            # Clear and insert new content
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(1.0, content["content"])
            
            # Apply some basic formatting
            self._format_content()
    
    def _format_content(self):
        """Apply basic formatting to help content"""
        # Configure tags for formatting
        self.content_text.tag_config("heading1", font=('Arial', 14, 'bold'), foreground='#2563EB')
        self.content_text.tag_config("heading2", font=('Arial', 12, 'bold'), foreground='#1F2937')
        self.content_text.tag_config("heading3", font=('Arial', 11, 'bold'), foreground='#374151')
        self.content_text.tag_config("code", font=('Consolas', 9), background='#F3F4F6')
        self.content_text.tag_config("emphasis", font=('Arial', 10, 'bold'))
        
        # Find and tag headings
        content = self.content_text.get(1.0, tk.END)
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_start = f"{i+1}.0"
            line_end = f"{i+1}.end"
            
            if line.startswith('# '):
                self.content_text.tag_add("heading1", line_start, line_end)
            elif line.startswith('## '):
                self.content_text.tag_add("heading2", line_start, line_end)
            elif line.startswith('### '):
                self.content_text.tag_add("heading3", line_start, line_end)
            elif line.startswith('- **') and line.endswith('**'):
                # Bold list items
                self.content_text.tag_add("emphasis", line_start, line_end)
    
    def create_tooltip(self, widget, text: str, delay: int = 500):
        """Create tooltip for a widget"""
        tooltip = ToolTip(widget, text, delay)
        self.tooltip_windows.append(tooltip)
        return tooltip
    
    def add_context_help(self, widget, help_key: str):
        """Add context-sensitive help to a widget"""
        if help_key in self.tooltips:
            self.create_tooltip(widget, self.tooltips[help_key])
        
        # Add right-click context help
        def show_context_help(event):
            self.show_context_help_popup(help_key, event.x_root, event.y_root)
        
        widget.bind("<Button-3>", show_context_help)  # Right-click
        widget.bind("<F1>", lambda e: self.show_help_window())  # F1 for general help
    
    def show_context_help_popup(self, help_key: str, x: int, y: int):
        """Show context help popup"""
        if help_key not in self.tooltips:
            return
            
        popup = tk.Toplevel(self.parent)
        popup.wm_overrideredirect(True)
        popup.geometry(f"+{x+10}+{y+10}")
        
        # Create content
        text = self.tooltips[help_key]
        label = tk.Label(popup, text=text, background='#FFFFCC', 
                        relief='solid', borderwidth=1, wraplength=300,
                        justify='left', font=('Arial', 9))
        label.pack()
        
        # Auto-close after 5 seconds
        popup.after(5000, popup.destroy)
        
        # Close on click
        popup.bind("<Button-1>", lambda e: popup.destroy())
    
    def show_examples(self):
        """Show example cases"""
        examples_window = tk.Toplevel(self.help_window)
        examples_window.title("Example Cases")
        examples_window.geometry("600x500")
        
        # Add examples content
        text_area = scrolledtext.ScrolledText(examples_window, wrap='word')
        text_area.pack(fill='both', expand=True, padx=10, pady=10)
        
        examples_content = """
# Example Cases

## Example 1: Aluminum Panel
- **Geometry**: 500mm × 300mm × 2mm
- **Material**: Aluminum 7075-T6 (E=71.7 GPa, ν=0.33, ρ=2810 kg/m³)
- **Boundary**: Simply supported (SSSS)
- **Expected Flutter**: ~150-200 m/s

## Example 2: Carbon Fiber Panel  
- **Geometry**: 300mm × 200mm × 1mm
- **Material**: CFRP [0°/±45°/90°]s
- **Boundary**: Clamped (CCCC)
- **Expected Flutter**: ~120-180 m/s

## Example 3: Composite Wing Panel
- **Geometry**: 1000mm × 400mm × 8mm
- **Material**: Glass/Epoxy [±45°/0°/90°]₂s
- **Boundary**: CFCF (wing-like)
- **Expected Flutter**: ~80-120 m/s

## Validation Cases
These examples are validated against:
- Published experimental data
- Commercial software results
- Analytical solutions where available

Use these cases to verify your installation and understand typical results.
"""
        
        text_area.insert(1.0, examples_content)
        text_area.config(state='disabled')
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Panel Flutter Analysis Tool v1.0

A comprehensive tool for panel flutter analysis in aerospace applications.

Features:
• Advanced flutter analysis methods (PK, K, KE)
• Support for metallic and composite materials
• Classical Laminate Theory for composites
• Professional GUI with modern design
• Comprehensive validation and testing

Developed for critical aerospace applications with emphasis on accuracy and reliability.

© 2025 Panel Flutter Analysis Development Team
        """
        
        messagebox.showinfo("About Panel Flutter Analysis", about_text)
    
    def open_user_manual(self):
        """Open user manual in browser or PDF viewer"""
        manual_path = Path(__file__).parent.parent.parent / "docs" / "user_manual.html"
        
        if manual_path.exists():
            webbrowser.open(f"file://{manual_path.absolute()}")
        else:
            messagebox.showinfo("User Manual", 
                              "User manual not found. It will be available in the final release.")


class ToolTip:
    """Tooltip widget for showing help on hover"""
    
    def __init__(self, widget, text: str, delay: int = 500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.timer_id = None
        
        # Bind events
        self.widget.bind('<Enter>', self._on_enter)
        self.widget.bind('<Leave>', self._on_leave)
        self.widget.bind('<Motion>', self._on_motion)
    
    def _on_enter(self, event=None):
        """Handle mouse enter"""
        self._schedule_tooltip()
    
    def _on_leave(self, event=None):
        """Handle mouse leave"""
        self._cancel_tooltip()
        self._hide_tooltip()
    
    def _on_motion(self, event=None):
        """Handle mouse motion"""
        self._cancel_tooltip()
        self._hide_tooltip()
        self._schedule_tooltip()
    
    def _schedule_tooltip(self):
        """Schedule tooltip to appear"""
        self._cancel_tooltip()
        self.timer_id = self.widget.after(self.delay, self._show_tooltip)
    
    def _cancel_tooltip(self):
        """Cancel scheduled tooltip"""
        if self.timer_id:
            self.widget.after_cancel(self.timer_id)
            self.timer_id = None
    
    def _show_tooltip(self):
        """Show the tooltip"""
        if self.tooltip_window:
            return
            
        # Get widget position
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        
        # Create tooltip window
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.geometry(f"+{x}+{y}")
        
        # Create tooltip content
        label = tk.Label(self.tooltip_window, 
                        text=self.text,
                        background='#FFFFCC',
                        relief='solid',
                        borderwidth=1,
                        wraplength=300,
                        justify='left',
                        font=('Arial', 9))
        label.pack()
    
    def _hide_tooltip(self):
        """Hide the tooltip"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class QuickStartWizard:
    """Quick start wizard for new users"""
    
    def __init__(self, parent):
        self.parent = parent
        self.wizard_window = None
        self.current_step = 0
        self.steps = [
            self._step_welcome,
            self._step_geometry, 
            self._step_materials,
            self._step_analysis,
            self._step_complete
        ]
    
    def show_wizard(self):
        """Show the quick start wizard"""
        self.wizard_window = tk.Toplevel(self.parent)
        self.wizard_window.title("Quick Start Wizard")
        self.wizard_window.geometry("700x500")
        self.wizard_window.transient(self.parent)
        self.wizard_window.grab_set()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.wizard_window)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.main_frame, length=400, mode='determinate')
        self.progress.pack(pady=(0, 20))
        
        # Content frame
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill='both', expand=True)
        
        # Navigation buttons
        nav_frame = ttk.Frame(self.main_frame)
        nav_frame.pack(fill='x', pady=(20, 0))
        
        self.back_button = ttk.Button(nav_frame, text="Back", command=self._go_back)
        self.back_button.pack(side='left')
        
        self.next_button = ttk.Button(nav_frame, text="Next", command=self._go_next)
        self.next_button.pack(side='right')
        
        # Start first step
        self._show_step()
    
    def _show_step(self):
        """Show current step"""
        # Update progress
        progress_value = (self.current_step / (len(self.steps) - 1)) * 100
        self.progress['value'] = progress_value
        
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Show current step
        self.steps[self.current_step]()
        
        # Update navigation buttons
        self.back_button['state'] = 'normal' if self.current_step > 0 else 'disabled'
        
        if self.current_step < len(self.steps) - 1:
            self.next_button['text'] = 'Next'
        else:
            self.next_button['text'] = 'Finish'
    
    def _go_back(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self._show_step()
    
    def _go_next(self):
        """Go to next step"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self._show_step()
        else:
            self.wizard_window.destroy()
    
    def _step_welcome(self):
        """Welcome step"""
        ttk.Label(self.content_frame, text="Welcome to Panel Flutter Analysis", 
                 font=('Arial', 16, 'bold')).pack(pady=20)
        
        welcome_text = """
This wizard will guide you through setting up your first flutter analysis.

Panel flutter is a critical aeroelastic phenomenon that must be considered in aerospace applications. This tool provides accurate analysis capabilities for both metallic and composite panels.

The analysis process involves:
1. Defining panel geometry
2. Specifying material properties  
3. Configuring analysis parameters
4. Running the analysis and interpreting results

Click Next to continue...
        """
        
        text_widget = tk.Text(self.content_frame, wrap='word', height=15, width=70)
        text_widget.pack(fill='both', expand=True)
        text_widget.insert(1.0, welcome_text)
        text_widget.config(state='disabled')
    
    def _step_geometry(self):
        """Geometry setup step"""
        ttk.Label(self.content_frame, text="Step 1: Panel Geometry", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Example geometry setup
        geometry_frame = ttk.LabelFrame(self.content_frame, text="Typical Panel Dimensions")
        geometry_frame.pack(fill='x', pady=10)
        
        ttk.Label(geometry_frame, text="Aircraft fuselage panel: 500mm × 300mm × 2mm").pack(anchor='w', padx=10, pady=5)
        ttk.Label(geometry_frame, text="Wing panel: 1000mm × 400mm × 8mm").pack(anchor='w', padx=10, pady=5)
        ttk.Label(geometry_frame, text="Control surface: 300mm × 200mm × 1mm").pack(anchor='w', padx=10, pady=5)
        
        tips_frame = ttk.LabelFrame(self.content_frame, text="Tips")
        tips_frame.pack(fill='x', pady=10)
        
        tips_text = """• Use millimeters (mm) for all dimensions
• Consider manufacturing constraints
• Ensure realistic length-to-thickness ratios (> 100)
• Account for structural boundaries in real application"""
        
        ttk.Label(tips_frame, text=tips_text, justify='left').pack(anchor='w', padx=10, pady=5)
    
    def _step_materials(self):
        """Materials setup step"""
        ttk.Label(self.content_frame, text="Step 2: Material Properties", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Material examples
        materials_frame = ttk.LabelFrame(self.content_frame, text="Common Materials")
        materials_frame.pack(fill='both', expand=True, pady=10)
        
        materials_text = """
Aluminum 7075-T6:
  • Young's Modulus: 71.7 GPa
  • Poisson's Ratio: 0.33
  • Density: 2,810 kg/m³

Carbon Fiber/Epoxy (Unidirectional):
  • E₁ (fiber): 150 GPa
  • E₂ (transverse): 9.0 GPa
  • G₁₂: 4.8 GPa
  • ν₁₂: 0.3
  • Density: 1,600 kg/m³

Steel (mild):
  • Young's Modulus: 200 GPa
  • Poisson's Ratio: 0.30
  • Density: 7,850 kg/m³
        """
        
        text_widget = tk.Text(materials_frame, wrap='word', height=12, width=60, font=('Consolas', 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        text_widget.insert(1.0, materials_text)
        text_widget.config(state='disabled')
    
    def _step_analysis(self):
        """Analysis setup step"""
        ttk.Label(self.content_frame, text="Step 3: Analysis Configuration", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        config_frame = ttk.LabelFrame(self.content_frame, text="Recommended Settings")
        config_frame.pack(fill='x', pady=10)
        
        config_text = """• Analysis Method: PK (good general choice)
• Velocity Range: 50-250 m/s (typical for aircraft panels)
• Velocity Points: 25-30 (balance accuracy vs. speed)
• Number of Modes: 15-20 (capture flutter behavior)
• Mach Range: 0.3-2.0 (subsonic to supersonic)"""
        
        ttk.Label(config_frame, text=config_text, justify='left').pack(anchor='w', padx=10, pady=10)
        
        safety_frame = ttk.LabelFrame(self.content_frame, text="Safety Considerations")
        safety_frame.pack(fill='x', pady=10)
        
        safety_text = """⚠️ IMPORTANT: Always apply appropriate safety factors
• Aerospace applications: 15% margin above flutter speed
• Modify design if flutter speed < 1.15 × operating speed
• Verify results with published data when available"""
        
        ttk.Label(safety_frame, text=safety_text, justify='left', foreground='red').pack(anchor='w', padx=10, pady=10)
    
    def _step_complete(self):
        """Completion step"""
        ttk.Label(self.content_frame, text="Setup Complete!", 
                 font=('Arial', 16, 'bold'), foreground='green').pack(pady=20)
        
        complete_text = """
You're now ready to perform flutter analysis!

Next steps:
1. Go to the Geometry tab and enter your panel dimensions
2. Define material properties in the Materials tab
3. Configure analysis parameters in the Analysis tab
4. Click "Run Analysis" to start the computation
5. Review results in the Results tab

Remember:
• Start with simple cases to verify your setup
• Use the Help system (F1) for detailed guidance
• Refer to examples for typical parameter ranges
• Validate critical results against published data

Good luck with your analysis!
        """
        
        text_widget = tk.Text(self.content_frame, wrap='word', height=15, width=70)
        text_widget.pack(fill='both', expand=True)
        text_widget.insert(1.0, complete_text)
        text_widget.config(state='disabled')