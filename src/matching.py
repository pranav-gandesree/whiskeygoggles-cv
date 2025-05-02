import os
import cv2
import numpy as np
import torch
from src.feature_extraction import FeatureExtractor
from src.preprocess import preprocess_image
from fuzzywuzzy import fuzz
import pandas as pd
from multiprocessing import Pool, cpu_count

class BottleMatcher:
    def __init__(self, dataset_path, images_dir, cache_dir="data/feature_cache"):
        self.df = pd.read_csv(dataset_path)
        self.images_dir = images_dir
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        self.feature_extractor = FeatureExtractor()
        self.visual_features = self._precompute_features()

    def _compute_features_for_bottle(self, args):
        bottle_id, img_path, cache_path = args
        if os.path.exists(cache_path):
            try:
                return (bottle_id, np.load(cache_path))
            except Exception as e:
                print(f"Error loading cached features for bottle ID {bottle_id}: {e}")
        features = self.feature_extractor.extract_visual_features(img_path)
        np.save(cache_path, features)
        return (bottle_id, features)

    def _precompute_features(self):
        features = {}
        tasks = []
        for idx, row in self.df.iterrows():
            bottle_id = row['id']
            img_path = os.path.join(self.images_dir, f"{bottle_id}.jpg")
            if not os.path.exists(img_path):
                continue
            cache_path = os.path.join(self.cache_dir, f"{bottle_id}.npy")
            tasks.append((bottle_id, img_path, cache_path))

        print(f"Processing {len(tasks)} bottles across {cpu_count()} CPU cores...")
        pool = Pool(processes=cpu_count())
        try:
            for i, result in enumerate(pool.imap_unordered(self._compute_features_for_bottle, tasks)):
                if result:
                    bottle_id, feature = result
                    features[bottle_id] = feature
                percentage = (i + 1) / len(tasks) * 100
                print(f"Loading: {percentage:.1f}%", end='\r')
        finally:
            pool.close()
            pool.join()
        print("\nFinished precomputing features.")
        return features

        print(f"Processing {len(tasks)} bottles across {cpu_count()} CPU cores...")
        with Pool(processes=cpu_count()) as pool:
            results = []
            for i, result in enumerate(pool.imap_unordered(self._compute_features_for_bottle, tasks)):
                if result:
                    bottle_id, feature = result
                    features[bottle_id] = feature
                percentage = (i + 1) / len(tasks) * 100
                print(f"Loading: {percentage:.1f}%", end='\r')

        print("\nFinished precomputing features.")
        return features

    def match_bottle(self, image_path, visual_weight=0.7, text_weight=0.3):
        # Extract visual features and text from the input image
        input_features = self.feature_extractor.extract_visual_features(image_path)
        input_text = self.feature_extractor.extract_text(image_path)

        scores = []
        for bottle_id, features in self.visual_features.items():
            # Compute visual similarity
            visual_score = np.dot(input_features, features) / (np.linalg.norm(input_features) * np.linalg.norm(features))
            
            # Get the bottle's name from the dataset and compute text similarity
            bottle_data = self.df[self.df['id'] == bottle_id].iloc[0]
            bottle_name = bottle_data['name'].lower()
            text_score = self.feature_extractor.compute_text_similarity(input_text, bottle_name)
            
            # Combine visual and text scores
            combined_score = (visual_weight * visual_score) + (text_weight * text_score)
            
            scores.append({
                'id': bottle_id,
                'name': bottle_data['name'],
                'type': bottle_data['spirit_type'],
                'confidence': combined_score,
                'fair_price': bottle_data.get('fair_price', None),
                'shelf_price': bottle_data.get('shelf_price', None)
            })

        return sorted(scores, key=lambda x: x['confidence'], reverse=True)[:3]