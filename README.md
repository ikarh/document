# Document Background Color Changer

This repository provides tools to change diagram background colors to white while preserving all other elements (text, shapes, and lines).

## Problem Solved

Mengubah background diagram pada gambar menjadi warna putih sambil memastikan semua elemen lain (teks, shape, dan garis) tetap terlihat jelas dan tidak berubah posisi.

## Available Tools

### 1. Python Script (change_background.py)
Advanced background color detection and replacement using PIL/Pillow.

**Usage:**
```bash
python change_background.py input_image [output_image] [tolerance]
```

**Example:**
```bash
python change_background.py image1.png image1_white.png 30
```

**Features:**
- Automatic background color detection from image corners
- Configurable color tolerance
- Supports various image formats (PNG, JPEG, etc.)
- Preserves transparency when possible

### 2. Shell Script (change_background.sh)
ImageMagick-based solution for quick background changes.

**Usage:**
```bash
./change_background.sh input_image [output_image] [fuzz_percentage]
```

**Example:**
```bash
./change_background.sh image1.png image1_white.png 10
```

**Features:**
- Fast processing using ImageMagick
- Automatic corner color detection
- Fallback flood fill method
- Cross-platform compatibility

## Requirements

### For Python script:
```bash
pip install Pillow numpy
```

### For Shell script:
```bash
sudo apt-get install imagemagick  # Ubuntu/Debian
brew install imagemagick          # macOS
```

## Sample Images

- `image1.png` - Original diagram with colored background
- `image1_white_background.png` - Result using ImageMagick convert
- `image1_python_white.png` - Result using Python script
- `image1_shell_white.png` - Result using Shell script

## How It Works

1. **Background Detection**: Both tools detect the background color by sampling the corners of the image
2. **Color Replacement**: Replace the detected background color with white using configurable tolerance
3. **Element Preservation**: All text, shapes, and lines maintain their original colors and positions
4. **Format Support**: Works with PNG, JPEG, and other common image formats

## Tips for Best Results

- Use higher tolerance values (30-50) for images with gradient backgrounds
- Use lower tolerance values (5-15) for images with solid color backgrounds  
- PNG format preserves transparency better than JPEG
- Test different tolerance values if the initial result isn't perfect