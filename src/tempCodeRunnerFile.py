import sys
import os

# Remove potentially conflicting paths
sys.path = [p for p in sys.path if 'pokedex' not in p.lower()]

# Add the base directory to sys.path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_dir)

import os
from src.matching import BottleMatcher
import pandas as pd

def main():
    matcher = BottleMatcher("data/dataset.csv", "data/images")
    image_path = input("Enter path to whisky bottle image: ")
    
    matches = matcher.match_bottle(image_path)
    
    print("\nTop Matches:")
    for match in matches:
        print(f"ID: {match['bottle_id']}, Name: {match['name']}, "
              f"Type: {match['spirit_type']}, Confidence: {match['confidence']:.2f}")
    
    store = input("Enter store name: ")
    price = float(input("Enter price: "))
    pricing_data = {
        'bottle_id': matches[0]['bottle_id'],
        'store': store,
        'price': price,
        'date': pd.Timestamp.now().strftime('%Y-%m-%d')
    }
    
    pricing_df = pd.DataFrame([pricing_data])
    pricing_file = "data/pricing_data.csv"
    if os.path.exists(pricing_file):
        pricing_df.to_csv(pricing_file, mode='a', header=False, index=False)
    else:
        pricing_df.to_csv(pricing_file, index=False)
    print("Pricing data saved!")

if __name__ == "__main__":
    main()
