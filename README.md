# Whisky Goggles

A computer vision system to identify whisky bottles from label images and record pricing information using the BAXUS dataset of 501 bottles. The system uses OCR and visual feature extraction to match bottles and allows users to input pricing data via a CLI or Flask-based web app.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Project](#running-the-project)
- [Notes](#notes)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Bottle Identification**: Matches whisky bottle labels using OCR and visual feature extraction.
- **Pricing Data Recording**: Stores user-input pricing data in `data/pricing_data.csv`.
- **CLI Interface**: Command-line tool for quick image matching and pricing input.
- **Web Application**: Flask-based web app for uploading images and viewing matches.
- **BAXUS Dataset**: Leverages a dataset of 501 whisky bottles for matching.

## Project Structure
```
WhiskyGoggles/
├── data/
│   ├── dataset.csv           # BAXUS dataset
│   ├── images/              # Downloaded bottle images
│   ├── pricing_data.csv     # Recorded pricing data
├── src/
│   ├── preprocess.py        # Image preprocessing
│   ├── feature_extraction.py # OCR and visual feature extraction
│   ├── matching.py          # Bottle matching logic
│   ├── utils.py             # Helper functions
│   ├── main.py              # CLI script
├── web/
│   ├── app.py               # Flask web app
│   ├── templates/           # HTML templates
│   ├── static/              # Uploaded images
├── requirements.txt         # Python dependencies
├── demo.py                  # Demo script
├── download_images_script.py # Script to download dataset images
├── README.md                # Project documentation
```

## Prerequisites
- **Python 3.8+**
- **Tesseract OCR**: Required for text extraction from label images.
- **Internet Connection**: Needed to download bottle images from the dataset.

## Setup Instructions
1. **Install Tesseract OCR**
   - **Windows**:
     - Download from [UB Mannheim Tesseract builds](https://github.com/UB-Mannheim/tesseract/wiki).
     - Add the installation path (e.g., `C:\Program Files\Tesseract-OCR`) to your system PATH in Environment Variables.
   - **macOS**:
     ```bash
     brew install tesseract
     ```
   - **Ubuntu/Linux**:
     ```bash
     sudo apt-get install tesseract-ocr libtesseract-dev
     ```

2. **Install Python Dependencies**
   Install the required Python libraries listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Place the Dataset**
   Ensure the BAXUS dataset CSV is placed at:
   ```bash
   data/dataset.csv
   ```

4. **Download Bottle Images**
   Run the provided script to download bottle images from URLs in `dataset.csv`:
   ```bash
   python download_images_script.py
   ```
   Images will be saved to `data/images/`.

## Running the Project
1. **CLI Demo**
   Test the system with sample images:
   ```bash
   python demo.py
   ```

2. **CLI Program**
   Run the main CLI program for image matching:
   ```bash
   python src/main.py
   ```
   Enter the full path to an input image when prompted.

3. **Web Application**
   Start the Flask web app:
   ```bash
   python web/app.py
   ```
   Visit `http://localhost:5000` in your browser to upload a whisky bottle label image, view matches, and input pricing data.

## Notes
- Ensure Tesseract is installed and added to your system PATH before running.
- Use clear, high-resolution label images for optimal matching accuracy.
- Broken image URLs in `dataset.csv` will be skipped during download.
- Pricing data is saved to `data/pricing_data.csv`.
- The first-time startup may be slow due to feature extraction and model loading.

## Troubleshooting
- **Tesseract not found**: Verify Tesseract installation and ensure its path is in your system PATH.
- **Image download errors**: Check your internet connection or validate URLs in `dataset.csv`.
- **Slow first load**: Normal behavior due to initial feature extraction and model loading.
- **Web app not loading**: Ensure port `5000` is free and dependencies are installed.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

