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
  python screenshot_standardizer.py --input input.png
  
  # Process a directory of images
  python screenshot_standardizer.py --input ./screenshots
  
  # Process with 10px padding and custom output directory
  python screenshot_standardizer.py --input input.png --padding 10 --outdir ~/Desktop/docs/images
  
  # Process as data visualization with enhanced quality and specific output file
  python screenshot_standardizer.py --input plot.png --type viz --output ~/Desktop/docs/enhanced_plot.png
  
  # Process at large size with high DPI
  python screenshot_standardizer.py --input input.png --size large --dpi 200
  
  # Force overwrite existing files
  python screenshot_standardizer.py --input input.png --force
  
  # Specify output format
  python screenshot_standardizer.py --input input.png --format jpg
        """
    )
    
    parser.add_argument("--input", "-i", required=True,
                        help="Input file or directory")
    parser.add_argument("--output", "-o", 
                        help="Output file path (for single file processing only)")
    parser.add_argument("--outdir", "-d", default="processed-screenshots",
                        help="Output directory for processed images (default: processed-screenshots)")
    parser.add_argument("--size", "-s", choices=["small", "medium", "large"], 
                        default="medium",
                        help="Size preset (small=1024px, medium=1440px, large=1920px width)")
    parser.add_argument("--type", "-t", choices=["default", "viz"], 
                        default="default",
                        help="Screenshot type (default or viz for data visualizations)")
    parser.add_argument("--padding", "-p", type=int, default=0,
                        help="Add consistent padding around elements (in pixels)")
    parser.add_argument("--dpi", 
                        type=int, default=144,
                        help="Set DPI for output images (default: 144)")
    parser.add_argument("--no-border", action="store_true",
                        help="Disable borders on processed images")
    parser.add_argument("--force", "-f", action="store_true",
                        help="Force overwrite existing files")
    parser.add_argument("--format", "-fm", choices=["png", "jpg", "jpeg", "webp"],
                        default="png",
                        help="Output image format (default: png)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print detailed processing information")
    
    args = parser.parse_args()
    
    # Configuration
    sizes = {
        "small": 1024,
        "medium": 1440,
        "large": 1920
    }
    
    # Get target width
    target_width = sizes.get(args.size, sizes["medium"])
    
    # Set output format (normalize jpg/jpeg)
    output_format = args.format.lower()
    if output_format == "jpg":
        output_format = "jpeg"
        
    border_enabled = not args.no_border
    background_color = "#ffffff"
    border_color = "#e0e0e0"
    border_width = 2
    
    # Properly handle input path - expand user directory (~ notation) and make absolute
    input_path = Path(os.path.expanduser(args.input)).resolve()
    
    # Properly handle output directory - expand user directory and make absolute
    output_dir = Path(os.path.expanduser(args.outdir)).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.verbose:
        print(f"Input path: {input_path}")
        print(f"Output directory: {output_dir}")
        print(f"Size preset: {args.size} ({target_width}px width)")
        print(f"Output format: {args.format}")
    
    # Function to process a single image
    def process_image(img_path, out_path):
        # Check if file exists and force flag is not set
        if out_path.exists() and not args.force:
            print(f"Error: File {out_path} already exists. Use --force to overwrite.")
            return False
            
        try:
            # Open and process image
            with Image.open(img_path) as img:
                if args.verbose:
                    print(f"Processing {img_path}...")
                    print(f"Original size: {img.size}, Mode: {img.mode}")
                
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
                    if args.verbose:
                        print(f"Added {args.padding}px padding. New size: {img.size}")
                
                # Calculate height while maintaining aspect ratio
                aspect_ratio = img.height / img.width
                target_height = int(target_width * aspect_ratio)
                
                # Convert to RGB if needed
                if img.mode == 'RGBA' and output_format != 'png':
                    background = Image.new('RGBA', img.size, background_color)
                    img = Image.alpha_composite(background, img).convert('RGB')
                elif img.mode != 'RGB' and img.mode != 'RGBA':
                    img = img.convert('RGB')
                
                # Resize image (high quality)
                img = img.resize((target_width, target_height), Image.LANCZOS)
                if args.verbose:
                    print(f"Resized to: {img.size}")
                
                # Apply special processing for data visualizations
                if args.type == "viz":
                    # Enhance contrast for better readability
                    img = ImageEnhance.Contrast(img).enhance(1.08)
                    
                    # Sharpen slightly for better text readability
                    img = ImageEnhance.Sharpness(img).enhance(1.2)
                    if args.verbose:
                        print("Applied visualization enhancements")
                
                # Add border if enabled
                if border_enabled:
                    img = ImageOps.expand(img, border=border_width, fill=border_color)
                    
                    # Add extra styling for visualizations
                    if args.type == "viz":
                        img = ImageOps.expand(img, border=6, fill="#ffffff")
                        img = ImageOps.expand(img, border=1, fill="#e0e0e0")
                    if args.verbose:
                        print(f"Added borders. Final size: {img.size}")
                
                # Set save options based on format
                save_options = {}
                if output_format == "png":
                    save_options = {
                        "optimize": True,
                        "compress_level": 1  # Lower compression for better quality
                    }
                elif output_format == "jpeg":
                    save_options = {
                        "quality": 95,
                        "optimize": True,
                        "subsampling": 0  # Better quality for text
                    }
                elif output_format == "webp":
                    save_options = {
                        "quality": 90,
                        "lossless": False
                    }
                    
                # Save with proper format and DPI
                dpi = (args.dpi, args.dpi)
                
                # Create parent directories if they don't exist
                out_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save the image
                img.save(out_path, format=output_format.upper(), dpi=dpi, **save_options)
                
                print(f"Processed: {img_path.name} → {out_path}")
                return True
                
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            return False
    
    # Process directory or single file
    if input_path.is_dir():
        # Cannot use --output option with directory input
        if args.output:
            print("Error: --output option can only be used with a single input file, not a directory.")
            print("Use --outdir instead to specify an output directory for batch processing.")
            sys.exit(1)
            
        # Get all image files
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
        files = [f for f in input_path.iterdir() 
                if f.is_file() and f.suffix.lower() in image_extensions]
        
        if args.verbose:
            print(f"Found {len(files)} image files in {input_path}")
        
        if not files:
            print(f"No image files found in directory: {input_path}")
            sys.exit(1)
        
        # Process each file
        processed_count = 0
        skipped_count = 0
        
        for file in files:
            # Use format extension instead of original extension
            extension = "." + args.format.lower()  # Use original format string to maintain .jpg
            
            output_name = f"{file.stem}_{args.size}{extension}"
            output_path = output_dir / output_name
            
            if args.verbose:
                print(f"\nProcessing file: {file}")
                print(f"Output path: {output_path}")
            
            if process_image(file, output_path):
                processed_count += 1
            else:
                skipped_count += 1
                
        print(f"\nSummary: Processed {processed_count} of {len(files)} images")
        if skipped_count > 0:
            print(f"Skipped {skipped_count} files. Use --force to overwrite existing files.")
        
    else:
        # Process single file
        if args.output:
            # Expand user home directory and convert to absolute path
            output_path = Path(os.path.expanduser(args.output)).resolve()
        else:
            # Use format extension instead of original extension
            extension = "." + args.format.lower()  # Use original format string to maintain .jpg
            
            output_name = f"{input_path.stem}_processed{extension}"
            output_path = output_dir / output_name
            
        if args.verbose:
            print(f"\nProcessing single file: {input_path}")
            print(f"Output path: {output_path}")
            
        if not process_image(input_path, output_path):
            sys.exit(1)

if __name__ == "__main__":
    main()