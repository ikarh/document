#!/usr/bin/env python3
"""
Script to change diagram background color to white while preserving all other elements.
This script handles various image formats and ensures text, shapes, and lines remain visible.
"""

import os
import sys
from PIL import Image, ImageEnhance
import numpy as np

def change_background_to_white(input_path, output_path, tolerance=30):
    """
    Change background color of an image to white while preserving other elements.
    
    Args:
        input_path (str): Path to input image
        output_path (str): Path to save output image
        tolerance (int): Color tolerance for background detection
    """
    try:
        # Open the image
        img = Image.open(input_path).convert('RGBA')
        data = np.array(img)
        
        # Get the most common color (likely the background)
        # Sample corners to determine background color
        corners = [
            data[0, 0],  # top-left
            data[0, -1], # top-right  
            data[-1, 0], # bottom-left
            data[-1, -1] # bottom-right
        ]
        
        # Use the most common corner color as background
        from collections import Counter
        bg_color = Counter([tuple(corner[:3]) for corner in corners]).most_common(1)[0][0]
        
        # Create mask for background pixels
        r, g, b = bg_color
        mask = (
            (np.abs(data[:, :, 0].astype(int) - r) <= tolerance) &
            (np.abs(data[:, :, 1].astype(int) - g) <= tolerance) &
            (np.abs(data[:, :, 2].astype(int) - b) <= tolerance)
        )
        
        # Change background to white
        data[mask] = [255, 255, 255, 255]  # White with full opacity
        
        # Convert back to image and save
        result_img = Image.fromarray(data, 'RGBA')
        
        # Convert to RGB if output format doesn't support transparency
        if output_path.lower().endswith(('.jpg', '.jpeg')):
            # Create white background for JPEG
            white_bg = Image.new('RGB', result_img.size, (255, 255, 255))
            white_bg.paste(result_img, mask=result_img.split()[-1])  # Use alpha channel as mask
            result_img = white_bg
        
        result_img.save(output_path)
        print(f"Successfully changed background to white: {input_path} -> {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")
        return False

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2:
        print("Usage: python change_background.py <input_image> [output_image] [tolerance]")
        print("Example: python change_background.py image1.png image1_white.png 30")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    # Generate output path if not provided
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        name, ext = os.path.splitext(input_path)
        output_path = f"{name}_white_background{ext}"
    
    # Get tolerance if provided
    tolerance = int(sys.argv[3]) if len(sys.argv) >= 4 else 30
    
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found!")
        sys.exit(1)
    
    success = change_background_to_white(input_path, output_path, tolerance)
    if success:
        print(f"Background successfully changed to white!")
        print(f"Original: {input_path}")
        print(f"Modified: {output_path}")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()