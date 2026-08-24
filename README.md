# PDF to Images ZIP

A simple and lightweight PDF to Images converter built with Python and PyQt6.

The application converts every page of a PDF file into a PNG image and stores the images directly inside a ZIP archive without creating temporary image files.

## Features

* Convert PDF pages to PNG images
* Store images directly in a ZIP file
* Simple PyQt6 graphical interface
* PDF file selection
* ZIP output selection
* Conversion progress bar
* No temporary image files

## Technologies

* Python
* PyQt6
* PyMuPDF
* zipfile

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-folder>
```

Install the required dependencies:

```bash
pip install PyQt6 PyMuPDF
```

Run the application:

```bash
python main.py
```

## How It Works

```text
PDF
 │
 ▼
PyMuPDF
 │
 ├── Page 1 ──→ PNG ┐
 ├── Page 2 ──→ PNG │
 ├── Page 3 ──→ PNG ├──→ ZIP
 └── Page N ──→ PNG ┘
```

The generated images are kept in memory and written directly into the ZIP archive.

## Project Status

Version 1.0 — Basic PDF to Images ZIP conversion is implemented.

## License

This project is open-source and available under the MIT License.
