import cv2
import numpy as np

def preprocess_image(image_path, output_size=(224, 224)):
    """Preprocess an image for label detection and feature extraction."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Failed to load image")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return cv2.resize(gray, output_size)

    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    label_roi = gray[y:y+h, x:x+w]

    if label_roi.size == 0:
        return cv2.resize(gray, output_size)
    
    processed_img = cv2.resize(label_roi, output_size)
    processed_img = cv2.equalizeHist(processed_img)
    
    return processed_img
