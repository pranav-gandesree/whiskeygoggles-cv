import os
import requests
import pandas as pd
from urllib.parse import urlparse

def download_images(dataset_path, output_dir):
    """Download bottle images from dataset URLs."""
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(dataset_path)
    
    for idx, row in df.iterrows():
        image_url = row['image_url']
        bottle_id = row['id']
        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                filename = os.path.join(output_dir, f"{bottle_id}.jpg")
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Downloaded image for bottle ID {bottle_id}")
            else:
                print(f"Failed to download image for bottle ID {bottle_id}")
        except Exception as e:
            print(f"Error downloading image for bottle ID {bottle_id}: {e}")

def load_dataset(dataset_path):
    """Load the BAXUS dataset into a DataFrame."""
    return pd.read_csv(dataset_path)

# ... existing utils.py content ...

if __name__ == "__main__":
    print("Running utils.py directly")
    # Test a simple function call
    try:
        df = load_dataset('data/dataset.csv')
        print("Successfully called load_dataset")
    except Exception as e:
        print("Error in load_dataset:", e)