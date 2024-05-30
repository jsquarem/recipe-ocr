from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import pytesseract
import cv2
import numpy as np

def preprocess_image(image_path):
    # Open the image using PIL
    image = Image.open(image_path)
    
    # Convert to grayscale
    grayscale = ImageOps.grayscale(image)
    
    # Convert to numpy array for OpenCV processing
    img_array = np.array(grayscale)
    
    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(img_array, (5, 5), 0)
    
    # Apply adaptive thresholding to get a binary image
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Use morphological operations to remove shadows
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Convert back to PIL image
    processed_image = Image.fromarray(morph)
    
    return processed_image

def preprocess_image_with_filters(image_path, filters):
    image = Image.open(image_path)

    # Apply filters
    if filters['blur']:
        image = image.filter(ImageFilter.GaussianBlur(radius=filters['blur']))
    if filters['brightness']:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(filters['brightness'] / 100.0)
    if filters['contrast']:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(filters['contrast'] / 100.0)
    if filters['grayscale']:
        image = ImageOps.grayscale(image)

    return image

def extract_text_from_image(image):
    try:
        if isinstance(image, str):
            image = Image.open(image)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error processing image: {e}")
        raise
