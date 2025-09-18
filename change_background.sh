#!/bin/bash
# Script to change diagram background to white using ImageMagick
# Usage: ./change_background.sh input_image [output_image] [fuzz_percentage]

set -e

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
    echo "Error: ImageMagick not found. Please install it first."
    echo "On Ubuntu/Debian: sudo apt-get install imagemagick"
    exit 1
fi

# Check arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 input_image [output_image] [fuzz_percentage]" 
    echo "Example: $0 image1.png image1_white.png 10"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="${2:-${INPUT_FILE%.*}_white_background.${INPUT_FILE##*.}}"
FUZZ_PERCENT="${3:-20}"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found!"
    exit 1
fi

echo "Processing: $INPUT_FILE"
echo "Output: $OUTPUT_FILE"
echo "Fuzz tolerance: ${FUZZ_PERCENT}%"

# Method 1: Change most common color to white (usually background)
echo "Attempting background color change..."

# Get the corner color (likely background)
CORNER_COLOR=$(convert "$INPUT_FILE" -crop 1x1+0+0 txt:- | grep -o '#[0-9A-F]\{6\}' | head -1)

if [ -n "$CORNER_COLOR" ]; then
    echo "Detected background color: $CORNER_COLOR"
    
    # Replace the background color with white
    convert "$INPUT_FILE" \
        -fuzz "${FUZZ_PERCENT}%" \
        -fill white \
        -opaque "$CORNER_COLOR" \
        "$OUTPUT_FILE"
    
    echo "✓ Background successfully changed to white!"
    echo "Original: $INPUT_FILE"
    echo "Modified: $OUTPUT_FILE"
else
    echo "Could not detect background color, using alternative method..."
    
    # Alternative: Use flood fill from corners
    convert "$INPUT_FILE" \
        -fuzz "${FUZZ_PERCENT}%" \
        -fill white \
        -draw "color 0,0 floodfill" \
        "$OUTPUT_FILE"
    
    echo "✓ Background changed using flood fill method!"
fi

# Verify the output file was created
if [ -f "$OUTPUT_FILE" ]; then
    echo "✓ Output file created successfully: $OUTPUT_FILE"
    
    # Display file info
    echo
    echo "File information:"
    identify "$OUTPUT_FILE"
else
    echo "❌ Error: Output file was not created!"
    exit 1
fi