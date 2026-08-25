import sys
import os
import math
import joblib
import numpy as np

from PIL import Image, ImageFilter

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QComboBox,
    QSpinBox,
    QCheckBox
)


# =========================
# Model
# =========================

MODEL_FILE = "compression_model.pkl"

try:

    model = joblib.load(
        MODEL_FILE
    )

except Exception:

    model = None


# =========================
# Image Window
# =========================

class ImageWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Image Tools"
        )

        self.resize(
            600,
            600
        )

        self.create_ui()

        self.connect_signals()


    # =========================
    # UI
    # =========================

    def create_ui(self):

        # -------------------------
        # Image
        # -------------------------

        self.image_path = QLineEdit()

        self.image_path.setPlaceholderText(
            "Select image"
        )

        self.browse_button = QPushButton(
            "Browse"
        )

        path_layout = QHBoxLayout()

        path_layout.addWidget(
            self.image_path
        )

        path_layout.addWidget(
            self.browse_button
        )


        # -------------------------
        # Convert
        # -------------------------

        self.format_box = QComboBox()

        self.format_box.addItems([
            "JPG",
            "PNG",
            "WEBP",
            "BMP"
        ])

        self.convert_button = QPushButton(
            "Convert"
        )


        # -------------------------
        # Compress
        # -------------------------

        self.quality_box = QSpinBox()

        self.quality_box.setRange(
            1,
            100
        )

        self.quality_box.setValue(
            80
        )

        self.compress_button = QPushButton(
            "Compress"
        )


        # -------------------------
        # Smart Compression
        # -------------------------

        self.smart_button = QPushButton(
            "🤖 Smart Quality"
        )

        self.smart_button.setToolTip(
            "Use Machine Learning to recommend "
            "the best compression quality."
        )


        # -------------------------
        # Resize
        # -------------------------

        self.width_box = QSpinBox()

        self.width_box.setRange(
            1,
            10000
        )

        self.width_box.setValue(
            1920
        )


        self.height_box = QSpinBox()

        self.height_box.setRange(
            1,
            10000
        )

        self.height_box.setValue(
            1080
        )


        self.aspect_ratio_checkbox = QCheckBox(
            "Keep Aspect Ratio"
        )

        self.aspect_ratio_checkbox.setChecked(
            True
        )


        self.resize_button = QPushButton(
            "Resize Image"
        )


        # -------------------------
        # Status
        # -------------------------

        self.status_label = QLabel(
            "Ready"
        )


        # -------------------------
        # Layout
        # -------------------------

        layout = QVBoxLayout()

        layout.addLayout(
            path_layout
        )


        # Convert

        layout.addWidget(
            QLabel("Convert format:")
        )

        layout.addWidget(
            self.format_box
        )

        layout.addWidget(
            self.convert_button
        )


        # Compress

        layout.addWidget(
            QLabel("Compression quality:")
        )

        layout.addWidget(
            self.quality_box
        )

        layout.addWidget(
            self.smart_button
        )

        layout.addWidget(
            self.compress_button
        )


        # Resize

        layout.addWidget(
            QLabel("Resize width:")
        )

        layout.addWidget(
            self.width_box
        )

        layout.addWidget(
            QLabel("Resize height:")
        )

        layout.addWidget(
            self.height_box
        )

        layout.addWidget(
            self.aspect_ratio_checkbox
        )

        layout.addWidget(
            self.resize_button
        )


        # Status

        layout.addWidget(
            self.status_label
        )

        self.setLayout(
            layout
        )


    # =========================
    # Signals
    # =========================

    def connect_signals(self):

        self.browse_button.clicked.connect(
            self.browse
        )

        self.convert_button.clicked.connect(
            self.convert
        )

        self.compress_button.clicked.connect(
            self.compress
        )

        self.smart_button.clicked.connect(
            self.smart_quality
        )

        self.resize_button.clicked.connect(
            self.resize_image
        )


    # =========================
    # Browse
    # =========================

    def browse(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp)"
        )

        if file_path:

            self.image_path.setText(
                file_path
            )


    # =========================
    # Feature Extraction
    # =========================

    def extract_features(
        self,
        image_path
    ):

        image = Image.open(
            image_path
        ).convert(
            "RGB"
        )


        # -------------------------
        # Size
        # -------------------------

        width, height = image.size


        # -------------------------
        # Grayscale
        # -------------------------

        grayscale = image.convert(
            "L"
        )

        pixels = np.array(
            grayscale
        )


        # -------------------------
        # Brightness
        # -------------------------

        brightness = pixels.mean()


        # -------------------------
        # Contrast
        # -------------------------

        contrast = pixels.std()


        # -------------------------
        # Color Variance
        # -------------------------

        rgb_pixels = np.array(
            image
        )

        color_variance = (
            rgb_pixels.var()
        )


        # -------------------------
        # Edge Density
        # -------------------------

        edges = grayscale.filter(
            ImageFilter.FIND_EDGES
        )

        edge_pixels = np.array(
            edges
        )

        edge_density = (
            (edge_pixels > 30).mean()
        )


        # -------------------------
        # Entropy
        # -------------------------

        histogram = (
            grayscale.histogram()
        )

        total = sum(
            histogram
        )

        entropy = 0

        for count in histogram:

            if count == 0:
                continue

            probability = (
                count / total
            )

            entropy -= (
                probability *
                math.log2(
                    probability
                )
            )


        # -------------------------
        # Original Size
        # -------------------------

        original_size = os.path.getsize(
            image_path
        )


        return {
            "width": width,
            "height": height,
            "original_size": original_size,
            "brightness": brightness,
            "contrast": contrast,
            "color_variance": color_variance,
            "edge_density": edge_density,
            "entropy": entropy
        }


    # =========================
    # Smart Quality
    # =========================

    def smart_quality(self):

        image_path = self.image_path.text()


        if not image_path:

            self.status_label.setText(
                "Please select an image."
            )

            return


        if model is None:

            self.status_label.setText(
                "ML model not found. "
                "Run ml.py first."
            )

            return


        try:

            features = (
                self.extract_features(
                    image_path
                )
            )


            feature_order = [
                "width",
                "height",
                "original_size",
                "brightness",
                "contrast",
                "color_variance",
                "edge_density",
                "entropy"
            ]


            values = [
                features[name]
                for name in feature_order
            ]


            X = np.array(
                [values]
            )


            prediction = model.predict(
                X
            )[0]


            prediction = round(
                prediction
            )


            prediction = max(
                1,
                min(
                    100,
                    prediction
                )
            )


            self.quality_box.setValue(
                prediction
            )


            self.status_label.setText(
                f"AI recommended quality: "
                f"{prediction}"
            )


        except Exception as error:

            self.status_label.setText(
                f"ML Error: {error}"
            )


    # =========================
    # Convert
    # =========================

    def convert(self):

        image_path = self.image_path.text()


        if not image_path:

            self.status_label.setText(
                "Please select an image."
            )

            return


        output_format = (
            self.format_box
            .currentText()
            .lower()
        )


        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            f"{output_format.upper()} Files (*.{output_format})"
        )


        if not output_path:

            return


        try:

            image = Image.open(
                image_path
            )


            if output_format == "jpg":

                image = image.convert(
                    "RGB"
                )


            image.save(
                output_path,
                format=output_format.upper()
            )


            self.status_label.setText(
                "Image converted successfully!"
            )


        except Exception as error:

            self.status_label.setText(
                f"Error: {error}"
            )


    # =========================
    # Compress
    # =========================

    def compress(self):

        image_path = self.image_path.text()


        if not image_path:

            self.status_label.setText(
                "Please select an image."
            )

            return


        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Compressed Image",
            "",
            "JPG Files (*.jpg)"
        )


        if not output_path:

            return


        try:

            image = Image.open(
                image_path
            )

            image = image.convert(
                "RGB"
            )


            quality = (
                self.quality_box.value()
            )


            image.save(
                output_path,
                "JPEG",
                quality=quality,
                optimize=True
            )


            self.status_label.setText(
                f"Image compressed successfully! "
                f"Quality: {quality}"
            )


        except Exception as error:

            self.status_label.setText(
                f"Error: {error}"
            )


    # =========================
    # Resize
    # =========================

    def resize_image(self):

        image_path = self.image_path.text()


        if not image_path:

            self.status_label.setText(
                "Please select an image."
            )

            return


        width = (
            self.width_box.value()
        )

        height = (
            self.height_box.value()
        )


        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Resized Image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp)"
        )


        if not output_path:

            return


        try:

            image = Image.open(
                image_path
            )


            if self.aspect_ratio_checkbox.isChecked():

                image.thumbnail(
                    (width, height)
                )

            else:

                image = image.resize(
                    (width, height)
                )


            image.save(
                output_path
            )


            self.status_label.setText(
                "Image resized successfully!"
            )


        except Exception as error:

            self.status_label.setText(
                f"Error: {error}"
            )


# =========================
# Run
# =========================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    window = ImageWindow()

    window.show()

    sys.exit(
        app.exec()
    )