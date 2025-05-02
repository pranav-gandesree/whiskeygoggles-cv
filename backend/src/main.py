import sys
import os

# Remove potentially conflicting paths
# sys.path = [p for p in sys.path if 'pokedex' not in p.lower()]

# Add the base directory to sys.path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_dir)

import os
from src.matching import BottleMatcher
import pandas as pd

def main():
    matcher = BottleMatcher("data/dataset.csv", "data/images")
    while True:
        image_path = input("Enter path to whisky bottle image (or type 'exit' or 'quit' to stop): ").strip()
        if image_path.lower() in ['exit', 'quit']:
            print("Exiting program.")
            break
        if not os.path.exists(image_path):
            print("Enter the correct path.")
            continue
        
        matches = matcher.match_bottle(image_path)
        
        print("\nTop Matches:")
        for match in matches:
            price_info = f", Fair Price: ${match['fair_price']}, Shelf Price: ${match['shelf_price']}" if match['fair_price'] is not None and match['shelf_price'] is not None else ", Prices: Not available"
            print(f"ID: {match['id']}, Name: {match['name']}, "
                  f"Type: {match['type']}, Confidence: {match['confidence']:.2f}{price_info}")
        
        store = input("Enter store name: ")
        try:
            price = float(input("Enter price: "))
        except ValueError:
            print("Invalid price entered. Skipping pricing data save.")
            continue
        
        pricing_data = {
            'bottle_id': matches[0]['id'],
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
    import multiprocessing
    multiprocessing.freeze_support()
    main()
