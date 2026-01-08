# UniqueColorGenerator

Stand-alone implementation of algorithm used in multiple of my research projects for demonstrative purposes.

## Overview

This tool generates `n` unique, visually distinct colors using the HSV (Hue, Saturation, Value) color space. The algorithm ensures maximum color separation by distributing hues equidistantly across the hue spectrum (0-360°), while maintaining full saturation and brightness for visual distinction.

## Algorithm

The color generation process follows these steps:

1. **Input**: Integer `n` representing the number of unique colors needed
2. **Hue Calculation**: Calculate equidistant hue values across the 360° spectrum
   - Hue step = 360° / n
   - Hues = [0°, step, 2×step, ..., (n-1)×step]
3. **HSV Parameters**:
   - **Hue**: Variable (0-360°), calculated as above
   - **Saturation**: Fixed at 100% (1.0)
   - **Value**: Fixed at 100% (1.0)
4. **RGB Conversion**: Convert each HSV triplet to RGB (0-255, 0-255, 0-255)
5. **Output**: List of RGB tuples

### Why This Approach?

- **Maximum Visual Separation**: Equidistant hues ensure the largest possible difference between colors
- **Full Saturation & Brightness**: Fixed at 100% ensures vibrant colors to increase distinguishability
- **Deterministic**: Same input `n` always produces the same color set
- **Scalable**: Works for any number of colors from 1 to 100+

## Usage

### GUI Application

Run the interactive GUI to visualize the color generation process:

```bash
python color.py
```

The GUI provides:
- Input field for number of colors (`n`)
- Real-time process visualization showing:
  - HSV parameter calculations
  - Equidistant hue values
  - RGB conversion details
- Visual color swatches in a grid layout
- Detailed table with RGB values, hex codes, and hue angles

### Programmatic Usage

Import the `generate_colors` function for use in your own code:

```python
from color import generate_colors

# Generate 8 unique colors
colors = generate_colors(8)

# Each color is an RGB tuple: (R, G, B) with values 0-255
for i, rgb in enumerate(colors):
    print(f"Color {i+1}: RGB{rgb}")
    # Example output: Color 1: RGB(255, 0, 0)
```

### Example Output

For `n = 6`, the algorithm generates:
- Color 1: Hue = 0° (Red)
- Color 2: Hue = 60° (Yellow)
- Color 3: Hue = 120° (Green)
- Color 4: Hue = 180° (Cyan)
- Color 5: Hue = 240° (Blue)
- Color 6: Hue = 300° (Magenta)

## Technical Details

### HSV to RGB Conversion

The implementation uses Python's built-in `colorsys` module for accurate color space conversion. The conversion process:

1. Normalize hue from 0-360° to 0-1 range
2. Use `colorsys.hsv_to_rgb(h, s, v)` where:
   - `h` = normalized hue (0-1)
   - `s` = saturation (1.0 = 100%)
   - `v` = value (1.0 = 100%)
3. Scale RGB values from 0-1 to 0-255 range
4. Round to nearest integer

### Edge Cases

- **n = 0**: Returns empty list
- **n = 1**: Returns single color (red, hue = 0°)
- **n > 100**: GUI limits to 100 colors for performance (function itself has no limit)

## Requirements

- Python 3.6+
- Standard library only:
  - `colorsys` (HSV to RGB conversion)
  - `tkinter` (GUI - usually included with Python)
  - `math` (for calculations)

No external dependencies required!

## License

This project is licensed under the MIT License. See the LICENSE file for details.
