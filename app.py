import json
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import logging
from utils.ai_processing import process_image_with_ai

uploads_dir = 'uploads'
# Ensure the uploads directory exists
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

app = Flask(__name__)



app.config['UPLOAD_FOLDER'] = 'uploads/'

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return 'Image OCR API'

@app.route('/scan', methods=['POST'])
def scan_recipe():
    try:
        image_file = request.files['imageFile']
        if not image_file:
            return jsonify({'error': 'Missing required fields'}), 400

        filename = secure_filename(image_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)

        logging.debug(f'Saved image to: {filepath}')

        # Use AI to extract text from the entire image
        ai_response_json = process_image_with_ai(filepath)

        logging.debug(f'Extracted text: {ai_response_json}')

        # Clean up the uploaded file
        os.remove(filepath)
        logging.debug(f'Removed uploaded file: {filepath}')

        return jsonify(ai_response_json), 200
    except Exception as e:
        logging.error(f"Error during scan recipe: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)