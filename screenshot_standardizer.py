#!/usr/bin/env python3
"""
Screenshot Standardizer

A tool for processing screenshots to ensure consistent sizing and formatting
for documentation and tutorials, especially for UI elements and data visualizations.
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Standardize screenshots for documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a single file
  python screenshot_standardizer.py input.png
  
  # Process a directory of images
  python screenshot_standardizer.py ./screenshots
  
  # Process with 10px padding around UI elements
  python screenshot_standardizer.py input.png --padding 10
  
  # Process as data visualization with enhanced quality
  python screenshot_standardizer.py plot.png --type viz
  
  # Process at large size with high DPI
  python screenshot_standardizer.py input.png --size large --dpi 200
  
  # Force overwrite existing files
  python screenshot_standardizer.py input.png --force
        """
    )
    
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("output", nargs="?", help="Output file (for single file processing)")
    parser.add_argument("--size", "-s", choices=["small", "medium", "large"], 
                        default="medium",
                        help="Size preset (small=1024px, medium=1440px, large=1920px width)")
    parser.add_argument("--type", "-t", choices=["default", "viz"], 
                        default="default",
                        help="Screenshot type (default or viz for data visualizations)")
    parser.add_argument("--padding", "-p", type=int, default=0,
                        help="Add consistent padding around elements (in pixels)")
    parser.add_argument("--dpi", "-d", type=int, default=144,
                        help="Set DPI for output images (default: 144)")
    parser.add_argument("--no-border", action="store_true",
                        help="Disable borders on processed images")
    parser.add_argument("--force", "-f", action="store_true",
                        help="Force overwrite existing files")
    
    args = parser.parse_args()
    
    # Configuration
    sizes = {
        "small": 1024,
        "medium": 1440,
        "large": 1920
    }
    
    # Get target width
    target_width = sizes.get(args.size, sizes["medium"])
    output_format = "png"
    border_enabled = not args.no_border
    background_color = "#ffffff"
    border_color = "#e0e0e0"
    border_width = 2
    
    # Create output directory if needed
    output_dir = Path("processed-screenshots")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process input (file or directory)
    input_path = Path(args.input)
    
    # Function to process a single image
    def process_image(img_path, out_path):
        # Check if file exists and force flag is not set
        if out_path.exists() and not args.force:
            print(f"Error: File {out_path} already exists. Use --force to overwrite.")
            return False
            
        # Open and process image
        with Image.open(img_path) as img:
            # Add padding if requested
            if args.padding > 0:
                width, height = img.size
                new_width = width + (args.padding * 2)
                new_height = height + (args.padding * 2)
                padded_img = Image.new(
                    img.mode, 
                    (new_width, new_height), 
                    background_color
                )
                padded_img.paste(img, (args.padding, args.padding))
                img = padded_img
            
            # Calculate height while maintaining aspect ratio
            aspect_ratio = img.height / img.width
            target_height = int(target_width * aspect_ratio)
            
            # Convert to RGB if needed
            if img.mode == 'RGBA':
                background = Image.new('RGBA', img.size, background_color)
                img = Image.alpha_composite(background, img).convert('RGB')
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize image (high quality)
            img = img.resize((target_width, target_height), Image.LANCZOS)
            
            # Apply special processing for data visualizations
            if args.type == "viz":
                # Enhance contrast for better readability
                img = ImageEnhance.Contrast(img).enhance(1.08)
                
                # Sharpen slightly for better text readability
                img = ImageEnhance.Sharpness(img).enhance(1.2)
            
            # Add border if enabled
            if border_enabled:
                img = ImageOps.expand(img, border=border_width, fill=border_color)
                
                # Add extra styling for visualizations
                if args.type == "viz":
                    img = ImageOps.expand(img, border=6, fill="#ffffff")
                    img = ImageOps.expand(img, border=1, fill="#e0e0e0")
            
            # Set save options for maximum quality
            save_options = {
                "optimize": True,
                "compress_level": 1
            }
                
            # Save with proper format and DPI
            dpi = (args.dpi, args.dpi)
            img.save(out_path, format=output_format.upper(), dpi=dpi, **save_options)
            
            print(f"Processed: {img_path.name} → {out_path.name}")
            return True
    
    # Process directory or single file
    if input_path.is_dir():
        # Get all image files
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif']
        files = [f for f in input_path.iterdir() 
                if f.is_file() and f.suffix.lower() in image_extensions]
        
        # Process each file
        processed_count = 0
        skipped_count = 0
        
        for file in files:
            output_name = f"{file.stem}_{args.size}.{output_format}"
            output_path = output_dir / output_name
            
            try:
                if process_image(file, output_path):
                    processed_count += 1
                else:
                    skipped_count += 1
            except Exception as e:
                print(f"Error processing {file.name}: {e}")
                skipped_count += 1
                
        print(f"Processed {processed_count} of {len(files)} images")
        if skipped_count > 0:
            print(f"Skipped {skipped_count} files. Use --force to overwrite existing files.")
        
    else:
        # Process single file
        if args.output:
            output_path = Path(args.output)
        else:
            output_name = f"{input_path.stem}_processed.{output_format}"
            output_path = output_dir / output_name
            
        # Create output directory if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file exists and force flag is not set
        if output_path.exists() and not args.force:
            print(f"Error: File {output_path} already exists. Use --force to overwrite.")
            sys.exit(1)
            
        try:
            process_image(input_path, output_path)
        except Exception as e:
            print(f"Error processing {input_path.name}: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()