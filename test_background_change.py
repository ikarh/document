#!/usr/bin/env python3
"""
Test script to validate background color changes work correctly
"""

import os
import sys
from PIL import Image
import numpy as np

def analyze_image_colors(image_path):
    """Analyze the colors in an image and return statistics"""
    try:
        img = Image.open(image_path).convert('RGB')
        data = np.array(img)
        
        # Get unique colors and their counts
        pixels = data.reshape(-1, 3)
        unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
        
        # Sort by frequency
        sorted_indices = np.argsort(counts)[::-1]
        most_common_colors = unique_colors[sorted_indices]
        color_counts = counts[sorted_indices]
        
        return {
            'total_pixels': len(pixels),
            'unique_colors': len(unique_colors),
            'most_common_color': tuple(most_common_colors[0]),
            'white_pixels': np.sum((pixels == [255, 255, 255]).all(axis=1)),
            'top_5_colors': [(tuple(color), count) for color, count in zip(most_common_colors[:5], color_counts[:5])]
        }
    except Exception as e:
        return {'error': str(e)}

def test_background_changes():
    """Test all generated images to ensure background changes worked"""
    print("🧪 Testing Background Color Changes")
    print("=" * 50)
    
    images_to_test = [
        'image1.png',
        'image1_white_background.png', 
        'image1_python_white.png',
        'image1_shell_white.png'
    ]
    
    results = {}
    
    for img_path in images_to_test:
        if os.path.exists(img_path):
            print(f"\n📊 Analyzing: {img_path}")
            stats = analyze_image_colors(img_path)
            results[img_path] = stats
            
            if 'error' in stats:
                print(f"❌ Error: {stats['error']}")
                continue
                
            print(f"   Total pixels: {stats['total_pixels']:,}")
            print(f"   Unique colors: {stats['unique_colors']}")
            print(f"   Most common color: {stats['most_common_color']}")
            print(f"   White pixels: {stats['white_pixels']:,} ({stats['white_pixels']/stats['total_pixels']*100:.1f}%)")
            
            # Check if background was successfully changed to white
            if img_path != 'image1.png':  # Skip original
                white_percentage = stats['white_pixels'] / stats['total_pixels'] * 100
                if white_percentage > 30:  # Expect significant white background
                    print(f"   ✅ Background successfully changed to white!")
                else:
                    print(f"   ⚠️  Low white percentage, may need adjustment")
        else:
            print(f"❌ Image not found: {img_path}")
    
    print(f"\n📋 Summary:")
    print(f"   Original image: {'✅' if 'image1.png' in results else '❌'}")
    print(f"   ImageMagick result: {'✅' if 'image1_white_background.png' in results else '❌'}")
    print(f"   Python script result: {'✅' if 'image1_python_white.png' in results else '❌'}")
    print(f"   Shell script result: {'✅' if 'image1_shell_white.png' in results else '❌'}")
    
    return results

if __name__ == "__main__":
    test_background_changes()