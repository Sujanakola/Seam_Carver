# Seam Carver

## Overview

Seam Carver is an intelligent image resizing tool that uses the seam carving algorithm to resize images while preserving important content and minimizing distortion. Unlike traditional resizing methods that simply scale or crop images, seam carving removes or inserts seams—paths of least importance—allowing for content-aware resizing.

## Features

- **Content-aware image resizing**  
- Preserves important regions of the image  
- Supports both image reduction and enlargement  
- Energy calculation based on pixel importance  
- Removes vertical and horizontal seams  
- Simple and efficient implementation  

## How It Works

The algorithm calculates an energy map of the image representing the importance of each pixel. It then identifies seams with the lowest energy (least important paths) and removes or adds them to resize the image intelligently without distorting key content.

## Installation

1. Clone this repository:  
   ```bash
   git clone https://github.com/yourusername/seam-carver.git

2. Navigate to the project directory:
   ```bash
   cd seam-carver
3. Install dependencies (if applicable, e.g., Python libraries):
   ```bash
   pip install -r requirements.txt

## Run the seam carving process on an input image:
   ```bash
   python seam_carver.py --input path/to/image.jpg --output path/to/resized_image.jpg --width 800 --height 600

## Parameters

- `--input`:  
  Path to the original image file.

- `--output`:  
  Path where the resized image will be saved.

- `--width`:  
  Desired width of the output image (in pixels).

- `--height`:  
  Desired height of the output image (in pixels).

