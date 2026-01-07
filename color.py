"""
Color generation module using HSV color space.
Generates n unique colors with equidistant hues, fixed saturation (100%), and fixed value (100%).
"""
import colorsys
import tkinter as tk
from tkinter import ttk, messagebox
import math


def generate_colors(n):
    """
    Generate n unique RGB colors using equidistant hues in HSV color space.
    
    Args:
        n (int): Number of colors to generate
        
    Returns:
        list: List of RGB tuples, each tuple contains (R, G, B) values in range 0-255
    """
    if n <= 0:
        return []
    
    if n == 1:
        # Single color: use hue 0 (red)
        hsv = (0.0, 1.0, 1.0)  # Hue=0, Saturation=100%, Value=100%
        rgb = colorsys.hsv_to_rgb(*hsv)
        return [(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))]
    
    # Calculate equidistant hue values
    # Step size: 360 / n to maximize difference between colors
    hue_step = 360.0 / n
    hues = [i * hue_step for i in range(n)]
    
    # Convert to 0-1 range for colorsys (HSV uses 0-1 for all components)
    # Saturation and Value are fixed at 100% (1.0)
    saturation = 1.0  # 100%
    value = 1.0       # 100%
    
    rgb_colors = []
    for hue in hues:
        # Convert hue from 0-360 to 0-1 range
        h = hue / 360.0
        hsv = (h, saturation, value)
        
        # Convert HSV to RGB (colorsys returns values in 0-1 range)
        rgb_normalized = colorsys.hsv_to_rgb(*hsv)
        
        # Convert to 0-255 range
        rgb = (
            int(round(rgb_normalized[0] * 255)),
            int(round(rgb_normalized[1] * 255)),
            int(round(rgb_normalized[2] * 255))
        )
        rgb_colors.append(rgb)
    
    return rgb_colors


def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color string."""
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def create_color_gui():
    """
    Create a GUI application to visualize the color generation process.
    """
    root = tk.Tk()
    root.title("Color Generator - HSV to RGB")
    root.geometry("800x700")
    root.resizable(True, True)
    
    # Main frame
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Input section
    input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
    input_frame.pack(fill=tk.X, pady=(0, 10))
    
    ttk.Label(input_frame, text="Number of colors (n):").pack(side=tk.LEFT, padx=5)
    n_var = tk.StringVar(value="8")
    n_entry = ttk.Entry(input_frame, textvariable=n_var, width=10)
    n_entry.pack(side=tk.LEFT, padx=5)
    
    def generate_and_display():
        try:
            n = int(n_var.get())
            if n < 1:
                messagebox.showerror("Error", "Number of colors must be at least 1")
                return
            if n > 100:
                messagebox.showerror("Error", "Number of colors cannot exceed 100")
                return
            
            # Generate colors
            colors = generate_colors(n)
            
            # Clear previous results
            for widget in process_frame.winfo_children():
                widget.destroy()
            for widget in colors_frame.winfo_children():
                widget.destroy()
            
            # Display process information
            process_text = tk.Text(process_frame, height=8, wrap=tk.WORD, font=("Courier", 9))
            process_text.pack(fill=tk.BOTH, expand=True)
            process_scroll = ttk.Scrollbar(process_frame, orient=tk.VERTICAL, command=process_text.yview)
            process_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            process_text.config(yscrollcommand=process_scroll.set)
            
            # Calculate and display process
            if n == 1:
                hue_step = 0
                process_text.insert(tk.END, f"Input: n = {n}\n")
                process_text.insert(tk.END, f"\nHSV Parameters:\n")
                process_text.insert(tk.END, f"  - Hue: 0° (single color)\n")
                process_text.insert(tk.END, f"  - Saturation: 100% (fixed)\n")
                process_text.insert(tk.END, f"  - Value: 100% (fixed)\n")
            else:
                hue_step = 360.0 / n
                process_text.insert(tk.END, f"Input: n = {n}\n")
                process_text.insert(tk.END, f"\nHSV Parameters:\n")
                process_text.insert(tk.END, f"  - Hue range: 0° to 360°\n")
                process_text.insert(tk.END, f"  - Saturation: 100% (fixed)\n")
                process_text.insert(tk.END, f"  - Value: 100% (fixed)\n")
                process_text.insert(tk.END, f"  - Hue step: 360° / {n} = {hue_step:.2f}°\n")
                process_text.insert(tk.END, f"\nEquidistant Hue Values:\n")
                for i, color in enumerate(colors):
                    hue = i * hue_step
                    process_text.insert(tk.END, f"  Color {i+1}: Hue = {hue:.2f}°\n")
            
            process_text.insert(tk.END, f"\nRGB Conversion:\n")
            for i, color in enumerate(colors):
                hex_color = rgb_to_hex(color)
                process_text.insert(tk.END, f"  Color {i+1}: RGB({color[0]}, {color[1]}, {color[2]}) = {hex_color}\n")
            
            process_text.config(state=tk.DISABLED)
            
            # Display colors
            colors_label = ttk.Label(colors_frame, text=f"Generated {n} Colors:", font=("Arial", 12, "bold"))
            colors_label.pack(pady=(0, 10))
            
            # Create a canvas for color swatches
            canvas_frame = ttk.Frame(colors_frame)
            canvas_frame.pack(fill=tk.BOTH, expand=True)
            
            # Calculate grid layout
            cols = min(8, n)  # Maximum 8 columns
            rows = math.ceil(n / cols)
            
            swatch_size = 80
            spacing = 10
            
            canvas_width = cols * (swatch_size + spacing) + spacing
            canvas_height = rows * (swatch_size + spacing + 30) + spacing  # Extra space for labels
            
            color_canvas = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height, bg="white")
            color_canvas.pack()
            
            # Draw color swatches
            for i, color in enumerate(colors):
                row = i // cols
                col = i % cols
                
                x1 = spacing + col * (swatch_size + spacing)
                y1 = spacing + row * (swatch_size + spacing + 30)
                x2 = x1 + swatch_size
                y2 = y1 + swatch_size
                
                # Draw color rectangle
                hex_color = rgb_to_hex(color)
                color_canvas.create_rectangle(x1, y1, x2, y2, fill=hex_color, outline="black", width=1)
                
                # Draw label below
                label_y = y2 + 5
                color_canvas.create_text(
                    x1 + swatch_size // 2, label_y,
                    text=f"#{i+1}",
                    font=("Arial", 8)
                )
                color_canvas.create_text(
                    x1 + swatch_size // 2, label_y + 12,
                    text=hex_color,
                    font=("Courier", 7)
                )
            
            # Create a scrollable frame for the color list
            list_frame = ttk.LabelFrame(colors_frame, text="Color Details", padding="10")
            list_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
            
            # Create treeview for color details
            tree = ttk.Treeview(list_frame, columns=("Index", "RGB", "Hex", "Hue"), show="headings", height=min(10, n))
            tree.heading("Index", text="#")
            tree.heading("RGB", text="RGB")
            tree.heading("Hex", text="Hex")
            tree.heading("Hue", text="Hue (°)")
            
            tree.column("Index", width=50, anchor=tk.CENTER)
            tree.column("RGB", width=150, anchor=tk.CENTER)
            tree.column("Hex", width=100, anchor=tk.CENTER)
            tree.column("Hue", width=100, anchor=tk.CENTER)
            
            for i, color in enumerate(colors):
                hue = i * hue_step if n > 1 else 0
                tree.insert("", tk.END, values=(
                    i + 1,
                    f"({color[0]}, {color[1]}, {color[2]})",
                    rgb_to_hex(color),
                    f"{hue:.2f}"
                ))
            
            tree.pack(fill=tk.BOTH, expand=True)
            
            # Scrollbar for treeview
            tree_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
            tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            tree.config(yscrollcommand=tree_scroll.set)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    generate_button = ttk.Button(input_frame, text="Generate Colors", command=generate_and_display)
    generate_button.pack(side=tk.LEFT, padx=10)
    
    # Process display section
    process_frame = ttk.LabelFrame(main_frame, text="Process", padding="10")
    process_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    
    # Colors display section
    colors_frame = ttk.LabelFrame(main_frame, text="Generated Colors", padding="10")
    colors_frame.pack(fill=tk.BOTH, expand=True)
    
    # Generate initial colors
    generate_and_display()
    
    # Bind Enter key to generate
    n_entry.bind('<Return>', lambda e: generate_and_display())
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    create_color_gui()
