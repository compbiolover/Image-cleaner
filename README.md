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
source your-venv/bin/activate # On Windows: your-venv\Scripts\activate

# Install required dependency
pip install Pillow
```

## Usage

### Basic Examples

```bash
# Process a single file
python main.py --input input.png

# Process a directory of images
python main.py --input ./screenshots

# Process with 10px padding around UI elements
python main.py --input input.png --padding 200

# Process as data visualization with enhanced quality
python main.py --input plot.png --type viz

# Process at large size with high DPI
python main.py --input input.png --size large --dpi 600

# Force overwrite existing files
python main.py --input input.png --force

# Save to a specific output directory 
python main.py --input input.png --outdir ~/Desktop/processed_images

# Use a different image format
python main.py --input input.png --format jpg

# Specify a custom output file (single file mode only)
python main.py --input input.png --output ~/Desktop/processed_image.png

# Enable verbose mode for detailed processing information
python main.py --input input.png --verbose
```

### Command Line Options

- `--input`, `-i`: Input file or directory (required)
- `--output`, `-o`: Output file path (for single file processing only)
- `--outdir`, `-d`: Output directory for processed images (default: processed-screenshots)
- `--size`, `-s`: Choose preset sizes: small (1024px), medium (1440px), or large (1920px)
- `--type`, `-t`: Processing type: default or viz (optimized for data visualizations)
- `--padding`, `-p`: Add consistent padding around elements (in pixels)
- `--dpi`, `-dp`: Set DPI for output images (default: 144)
- `--no-border`: Disable borders on processed images
- `--force`, `-f`: Force overwrite existing files
- `--format`, `-fm`: Output image format: png, jpg/jpeg, or webp (default: png)
- `--verbose`, `-v`: Print detailed processing information

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
python main.py --input path/to/umap_image.png --output test_docs/images/umap_processed.png --type viz --padding 200
python main.py --input path/to/color_picker.png --output test_docs/images/colorpicker_processed.png --padding 200

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