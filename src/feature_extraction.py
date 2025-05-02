import pytesseract
import cv2
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from torchvision.models import ResNet50_Weights
from fuzzywuzzy import fuzz
from PIL import Image
import warnings
import numpy as np

warnings.filterwarnings("ignore", category=UserWarning, module="PIL.TiffImagePlugin")

class FeatureExtractor:
    def __init__(self):
        self.model = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def detect_label(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian blur to reduce noise
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        # Use adaptive thresholding for better contour detection
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY_INV, 11, 2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return gray
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        label_roi = gray[y:y+h, x:x+w]
        if label_roi.size == 0:
            return gray
        return label_roi

    def extract_text(self, image_path):
        label_img = self.detect_label(image_path)
        if label_img is None:
            return ""
        # Enhance the image for better OCR
        label_img = cv2.equalizeHist(label_img)
        # Apply additional thresholding for OCR
        thresh = cv2.threshold(label_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        text = pytesseract.image_to_string(thresh, config='--psm 6')
        return text.strip().lower()

    def extract_visual_features(self, image_path):
        img = Image.open(image_path).convert('RGB')
        img_t = self.transform(img)
        batch_t = torch.unsqueeze(img_t, 0)
        with torch.no_grad():
            features = self.model(batch_t)
        return features.squeeze().numpy()

    def compute_text_similarity(self, text1, text2):
        if not text1 or not text2:
            return 0.0
        return fuzz.token_sort_ratio(text1, text2) / 100.0