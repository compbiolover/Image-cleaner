# Screenshot Standardizer

A tool for processing screenshots to ensure consistent sizing, formatting, and padding for documentation and tutorials.

## Overview

This Python script helps standardize screenshots taken from different Mac devices with varying screen resolutions. It solves common documentation problems by:

- Resizing images to consistent dimensions
- Standardizing DPI settings
- Adding consistent padding around UI elements
- Optimizing data visualizations (UMAPs, scatter plots, etc.)
- Preventing accidental file overwrites

Perfect for teams working on documentation where screenshots come from multiple sources and need visual consistency.

## Installation

### Requirements

- Python 3.6+
- Pillow library

```bash
# Create a virtual environment (optional but recommended)
python -m venv your-venv
source your-venv/bin/activate  # On Windows: your-venv\Scripts\activate

# Install required dependency
pip install Pillow
```

## Usage

### Basic Examples

```bash
# Process a single file
python main.py input.png

# Process a directory of images
python main.py ./screenshots

# Process with 10px padding around UI elements
python main.py input.png --padding 200

# Process as data visualization with enhanced quality
python main.py plot.png --type viz

# Process at large size with high DPI
python main.py input.png --size large --dpi 600

# Force overwrite existing files
python main.py input.png --force
```

### Command Line Options

- `--size`, `-s`: Choose preset sizes: small (1024px), medium (1440px), or large (1920px)
- `--type`, `-t`: Processing type: default or viz (optimized for data visualizations)
- `--padding`, `-p`: Add consistent padding around elements (in pixels)
- `--dpi`, `-d`: Set DPI for output images (default: 144)
- `--no-border`: Disable borders on processed images
- `--force`, `-f`: Force overwrite existing files

## Why Use This Tool?

- **Consistency**: Creates uniform visuals in documentation despite screenshots coming from different devices
- **Professionalism**: Properly formatted images with consistent padding improve documentation quality
- **Efficiency**: Batch process multiple screenshots at once
- **Visualization Optimization**: Special processing for data plots improves clarity and readability

## Output

Processed images are saved to a `processed-screenshots` directory by default. The naming convention adds the size preset to the filename, like `original_medium.png`.

## Creating Test Documentation

To test how processed images look in a documentation context, create a sample markdown file:

```bash
mkdir -p test_docs/images

# Process example images
python main.py path/to/umap_image.png --output test_docs/images/umap_processed.png --type viz --padding 200
python main.py path/to/color_picker.png --output test_docs/images/colorpicker_processed.png --padding 200

# Create test markdown
touch test_docs/sample_documentation.md
```

Example markdown content:

```markdown
# Gene Expression Analysis Tool

## UMAP Visualization

The UMAP visualization allows researchers to explore gene expression patterns across samples.

![UMAP Visualization](images/umap_processed.png)

## Color Picker Interface

The color picker lets users customize the visualization palette according to their preferences.

![Color Picker](images/colorpicker_processed.png)

## Comparing Both Features

When using the visualization tool, researchers can adjust the color scale to highlight specific expression levels in the UMAP plot.
```

This test will help you verify that your processed images have consistent visual appearance in real documentation.
