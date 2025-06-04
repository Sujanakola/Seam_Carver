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
