from flask import Flask, request, send_file, render_template, jsonify
import os
import subprocess
from werkzeug.utils import secure_filename
from PIL import Image
import io
import shutil

app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create static/img directory if it doesn't exist and copy images
STATIC_IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'img')
os.makedirs(STATIC_IMG_DIR, exist_ok=True)

# Copy images from img to static/img if they don't exist in static/img
IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
if os.path.exists(IMG_DIR):
    for img_file in os.listdir(IMG_DIR):
        src = os.path.join(IMG_DIR, img_file)
        dst = os.path.join(STATIC_IMG_DIR, img_file)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)

MAX_IMAGE_SIZE = 800  # Reduced maximum dimension for better memory handling

def preprocess_image(image_path):
    """Resize image if it's too large while maintaining aspect ratio"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if image is in RGBA mode
            if img.mode == 'RGBA':
                img = img.convert('RGB')
                
            width, height = img.size
            if width > MAX_IMAGE_SIZE or height > MAX_IMAGE_SIZE:
                # Calculate new dimensions while maintaining aspect ratio
                if width > height:
                    new_width = MAX_IMAGE_SIZE
                    new_height = int(height * (MAX_IMAGE_SIZE / width))
                else:
                    new_height = MAX_IMAGE_SIZE
                    new_width = int(width * (MAX_IMAGE_SIZE / height))
                
                # Resize and save
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save as JPG to reduce memory footprint
            preprocessed_path = os.path.join(os.path.dirname(image_path), 
                                           'preprocessed_' + os.path.splitext(os.path.basename(image_path))[0] + '.jpg')
            img.save(preprocessed_path, 'JPEG', quality=95)
            return preprocessed_path
    except Exception as e:
        raise Exception(f"Error preprocessing image: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    image = request.files.get('image')
    dimension = request.form.get('dimension')
    iterations = request.form.get('iterations')

    if not image or not dimension or not iterations:
        return {"error": "Missing required fields"}, 400

    input_path = None
    processed_input = None
    output_path = None

    try:
        # Save the uploaded image
        filename = secure_filename(image.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(input_path)

        # Preprocess the image if needed
        processed_input = preprocess_image(input_path)

        # Run the Java SeamCarver command with conservative memory settings
        process = subprocess.run(
            ['java', '-Xmx1024m', '-Xms512m', 
             '-XX:+UseSerialGC', '-XX:+DisableExplicitGC',
             '-XX:MaxHeapFreeRatio=70', '-XX:MinHeapFreeRatio=30',
             'SeamCarver', processed_input, dimension, iterations],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            check=True
        )
        
        # The output file will be created with _resized.png suffix
        base_name = os.path.splitext(processed_input)[0]
        output_path = f"{base_name}_resized.png"
        
        # Check if the output file was created
        if os.path.exists(output_path):
            response = send_file(output_path, mimetype='image/png')
            return response
        else:
            error_msg = f"Output file not found. Java process output: {process.stdout}\nErrors: {process.stderr}"
            return {"error": error_msg}, 500
            
    except subprocess.CalledProcessError as e:
        error_msg = f"Image processing failed: {str(e)}\nOutput: {e.stdout}\nErrors: {e.stderr}"
        return {"error": error_msg}, 500
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}, 500
    finally:
        # Clean up all temporary files
        for path in [input_path, processed_input, output_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass

@app.route('/uploads/<filename>')
def serve_image(filename):
    return send_file(
        os.path.join(UPLOAD_FOLDER, filename),
        mimetype='image/png'
    )

if __name__ == '__main__':
    app.run(debug=True)
