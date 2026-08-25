# AmirTools

AmirTools is a simple desktop utility application built with Python and PyQt6.

The project provides useful tools for working with PDF and image files, with a focus on keeping the interface simple and easy to use.

## Features

### PDF
- Convert PDF pages to PNG images
- Pack converted images into a ZIP file
- Progress tracking during conversion

### Image
- Convert images between different formats
- Compress images with adjustable quality
- More image tools will be added later

## Technologies

- Python
- PyQt6
- PyMuPDF
- Pillow
- ZIPFile
- joblib
- sklearn (sickit-learn):
    - train_test_split
    - RandomForestRegressor
    - metrics
- Pandas
- numpy
- math
- os

## Project Structure

```text
AmirTools/
├── main.py
├── pdf.py
├── image.py
├── ml.py
├── gerenate_dataset.py
├── dataset.csv
├── compressoin_model.pkl
└── README.md
```
## How to use?
In your folder :

```bash
git clone "https://github.com/amirmahdialmasi/amirrx-tools"
git pull
```

### I hope enjoyable from app