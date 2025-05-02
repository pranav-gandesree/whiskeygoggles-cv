import sys
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_dir)

from flask import Flask, request, render_template, redirect, url_for, flash
from src.matching import BottleMatcher
import pandas as pd
import shutil
import time
import uuid

app = Flask(__name__)
app.secret_key = 'whiskygoggles_secret_key'  # For flash messages
matcher = None  # Initialize as None at module level

# Create necessary directories if they don't exist
def create_directories():
    os.makedirs("web/static/uploads", exist_ok=True)
    os.makedirs("web/static/images", exist_ok=True)

def init_matcher():
    global matcher
    if matcher is None:
        matcher = BottleMatcher("data/dataset.csv", "data/images")
        # Copy dataset images to static folder for web display
        copy_dataset_images()

def copy_dataset_images():
    """Copy dataset images to static folder for web display"""
    dataset_images_dir = "data/images"
    web_images_dir = "web/static/images"
    
    # Create the web images directory if it doesn't exist
    os.makedirs(web_images_dir, exist_ok=True)
    
    # Copy all images from dataset to web static folder
    for filename in os.listdir(dataset_images_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            src_path = os.path.join(dataset_images_dir, filename)
            dst_path = os.path.join(web_images_dir, filename)
            # Only copy if file doesn't exist or is newer
            if not os.path.exists(dst_path) or os.path.getmtime(src_path) > os.path.getmtime(dst_path):
                shutil.copy2(src_path, dst_path)

@app.before_request
def before_request():
    create_directories()
    init_matcher()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Check if file is provided
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            
            file = request.files['file']
            
            # Check if file is selected
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            
            # Check if store name is provided
            if not request.form.get('store'):
                flash('Store name is required')
                return redirect(request.url)
            
            # Check if price is provided and valid
            try:
                price = float(request.form.get('price', 0))
                if price <= 0:
                    flash('Please enter a valid price')
                    return redirect(request.url)
            except ValueError:
                flash('Please enter a valid price')
                return redirect(request.url)
            
            # Generate a unique filename to prevent conflicts
            unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
            upload_path = os.path.join('web/static/uploads', unique_filename)
            
            # Save the uploaded file
            file.save(upload_path)
            
            # Process the image
            matches = matcher.match_bottle(upload_path)
            
            # If no matches were found
            if not matches:
                flash('No matches found for this bottle')
                return redirect(request.url)
            
            # Save pricing data to CSV
            store = request.form['store']
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
            
            # Render the result page with matches and image path
            return render_template('result.html', 
                                  matches=matches, 
                                  image_path=f"uploads/{unique_filename}")
                                  
        except Exception as e:
            flash(f"An error occurred: {str(e)}")
            return redirect(request.url)
    
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if _name_ == '_main_':
    app.run(debug=True)