import sys

from PIL import Image

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
    QSpinBox
)


class ImageWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Tools")
        self.resize(600, 450)

        self.create_ui()
        self.connect_signals()

    def create_ui(self):

        # -------------------------
        # Image
        # -------------------------

        self.image_path = QLineEdit()
        self.image_path.setPlaceholderText("Select image")

        self.browse_button = QPushButton("Browse")

        path_layout = QHBoxLayout()

        path_layout.addWidget(self.image_path)
        path_layout.addWidget(self.browse_button)

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

        self.convert_button = QPushButton("Convert")

        # -------------------------
        # Compress
        # -------------------------

        self.quality_box = QSpinBox()

        self.quality_box.setRange(1, 100)
        self.quality_box.setValue(80)

        self.compress_button = QPushButton("Compress")

        # -------------------------
        # Status
        # -------------------------

        self.status_label = QLabel("Ready")

        # -------------------------
        # Layout
        # -------------------------

        layout = QVBoxLayout()

        layout.addLayout(path_layout)

        layout.addWidget(
            QLabel("Convert format:")
        )

        layout.addWidget(
            self.format_box
        )

        layout.addWidget(
            self.convert_button
        )

        layout.addWidget(
            QLabel("Compression quality:")
        )

        layout.addWidget(
            self.quality_box
        )

        layout.addWidget(
            self.compress_button
        )

        layout.addWidget(
            self.status_label
        )

        self.setLayout(layout)

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

    def browse(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp)"
        )

        if file_path:
            self.image_path.setText(file_path)

    # -------------------------
    # Convert
    # -------------------------

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

            image = Image.open(image_path)

            if output_format == "jpg":
                image = image.convert("RGB")

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

    # -------------------------
    # Compress
    # -------------------------

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

            image = Image.open(image_path)

            image = image.convert("RGB")

            quality = self.quality_box.value()

            image.save(
                output_path,
                "JPEG",
                quality=quality,
                optimize=True
            )

            self.status_label.setText(
                "Image compressed successfully!"
            )

        except Exception as error:

            self.status_label.setText(
                f"Error: {error}"
            )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = ImageWindow()
    window.show()

    sys.exit(app.exec())