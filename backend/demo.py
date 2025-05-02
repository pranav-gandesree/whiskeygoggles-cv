import sys
import os
import multiprocessing

base_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, base_dir)

from src.matching import BottleMatcher

if __name__ == '__main__':
    multiprocessing.freeze_support()
    matcher = BottleMatcher("data/dataset.csv", "data/images")
    sample_images = ["test_image1.jpg", "test_image2.jpg"]
    for img_path in sample_images:
        print(f"\nTesting {img_path}")
        matches = matcher.match_bottle(img_path)
        for match in matches:
            print(f"ID: {match['id']}, Name: {match['name']}, "
                  f"Type: {match['type']}, Confidence: {match['confidence']:.2f}")