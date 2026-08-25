from pathlib import Path
import csv
import math
import os
import random
import tempfile

import numpy as np

from PIL import Image, ImageDraw, ImageFilter


# =========================
# Settings
# =========================

IMAGE_COUNT = 100
IMAGE_SIZE = (800, 600)

OUTPUT_FOLDER = Path("generated_images")
DATASET_FILE = Path("dataset.csv")

QUALITIES = range(30, 96, 5)

MIN_PSNR = 35


# =========================
# Generate Image
# =========================

def generate_image(index):

    width, height = IMAGE_SIZE

    image = Image.new(
        "RGB",
        IMAGE_SIZE,
        (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    )

    draw = ImageDraw.Draw(image)

    image_type = random.choice([
        "simple",
        "shapes",
        "noise",
        "detailed"
    ])

    if image_type == "simple":

        for _ in range(10):

            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )

            draw.rectangle(
                (
                    random.randint(0, width // 2),
                    random.randint(0, height // 2),
                    random.randint(width // 2, width),
                    random.randint(height // 2, height)
                ),
                fill=color
            )

    elif image_type == "shapes":

        for _ in range(100):

            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )

            x1 = random.randint(0, width - 1)
            y1 = random.randint(0, height - 1)

            x2 = random.randint(x1, width - 1)
            y2 = random.randint(y1, height - 1)

            shape = random.choice([
                "rectangle",
                "ellipse"
            ])

            if shape == "rectangle":

                draw.rectangle(
                    (x1, y1, x2, y2),
                    fill=color
                )

            else:

                draw.ellipse(
                    (x1, y1, x2, y2),
                    fill=color
                )

    elif image_type == "noise":

        pixels = image.load()

        for y in range(height):

            for x in range(width):

                pixels[x, y] = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )

    elif image_type == "detailed":

        for _ in range(1000):

            x = random.randint(
                0,
                width - 1
            )

            y = random.randint(
                0,
                height - 1
            )

            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )

            draw.point(
                (x, y),
                fill=color
            )

    output_path = (
        OUTPUT_FOLDER /
        f"image_{index}.png"
    )

    image.save(
        output_path,
        "PNG"
    )

    return output_path


# =========================
# Feature Extraction
# =========================

def extract_features(image):

    image = image.convert("RGB")

    width, height = image.size

    grayscale = image.convert("L")

    pixels = np.array(
        grayscale
    )

    brightness = pixels.mean()

    contrast = pixels.std()

    rgb_pixels = np.array(
        image
    )

    color_variance = rgb_pixels.var()

    edges = grayscale.filter(
        ImageFilter.FIND_EDGES
    )

    edge_pixels = np.array(
        edges
    )

    edge_density = (
        (edge_pixels > 30).mean()
    )

    histogram = grayscale.histogram()

    total = sum(histogram)

    entropy = 0

    for count in histogram:

        if count == 0:
            continue

        probability = count / total

        entropy -= (
            probability *
            math.log2(probability)
        )

    return {
        "width": width,
        "height": height,
        "brightness": brightness,
        "contrast": contrast,
        "color_variance": color_variance,
        "edge_density": edge_density,
        "entropy": entropy
    }


# =========================
# MSE
# =========================

def calculate_mse(
    original,
    compressed
):

    original = original.convert(
        "RGB"
    )

    compressed = compressed.convert(
        "RGB"
    )

    if original.size != compressed.size:

        compressed = compressed.resize(
            original.size
        )

    original_pixels = original.load()
    compressed_pixels = compressed.load()

    width, height = original.size

    total_error = 0

    for y in range(height):

        for x in range(width):

            r1, g1, b1 = original_pixels[x, y]
            r2, g2, b2 = compressed_pixels[x, y]

            total_error += (
                (r1 - r2) ** 2 +
                (g1 - g2) ** 2 +
                (b1 - b2) ** 2
            )

    return total_error / (
        width * height * 3
    )


# =========================
# PSNR
# =========================

def calculate_psnr(mse):

    if mse == 0:
        return 100

    return 10 * math.log10(
        (255 ** 2) / mse
    )


# =========================
# Find Recommended Quality
# =========================

def find_recommended_quality(
    results
):

    valid = [
        row
        for row in results
        if row["psnr"] >= MIN_PSNR
    ]

    if valid:

        best = min(
            valid,
            key=lambda row:
            row["compressed_size"]
        )

        return best["quality"]

    best = max(
        results,
        key=lambda row:
        row["psnr"]
    )

    return best["quality"]


# =========================
# Analyze Image
# =========================

def analyze_image(
    image_path
):

    image = Image.open(
        image_path
    ).convert("RGB")

    features = extract_features(
        image
    )

    original_size = os.path.getsize(
        image_path
    )

    results = []

    for quality in QUALITIES:

        with tempfile.NamedTemporaryFile(
            suffix=".jpg",
            delete=False
        ) as temp:

            temp_path = temp.name

        try:

            image.save(
                temp_path,
                "JPEG",
                quality=quality,
                optimize=True
            )

            compressed_size = os.path.getsize(
                temp_path
            )

            compressed = Image.open(
                temp_path
            )

            mse = calculate_mse(
                image,
                compressed
            )

            psnr = calculate_psnr(
                mse
            )

            results.append({
                "quality": quality,
                "compressed_size": compressed_size,
                "psnr": psnr
            })

        finally:

            os.remove(
                temp_path
            )

    recommended_quality = (
        find_recommended_quality(
            results
        )
    )

    return {
        **features,
        "original_size": original_size,
        "recommended_quality":
            recommended_quality
    }


# =========================
# Main
# =========================

def main():

    OUTPUT_FOLDER.mkdir(
        exist_ok=True
    )

    rows = []

    print("Generating dataset...")
    print()

    for index in range(
        1,
        IMAGE_COUNT + 1
    ):

        image_path = generate_image(
            index
        )

        data = analyze_image(
            image_path
        )

        rows.append(data)

        print(
            f"[{index}/{IMAGE_COUNT}] "
            f"{image_path.name} → "
            f"Quality: "
            f"{data['recommended_quality']}"
        )

    fieldnames = [
        "width",
        "height",
        "original_size",
        "brightness",
        "contrast",
        "color_variance",
        "edge_density",
        "entropy",
        "recommended_quality"
    ]

    with open(
        DATASET_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            rows
        )

    print()
    print("Dataset created successfully!")
    print(f"Images: {IMAGE_COUNT}")
    print(f"Rows: {len(rows)}")
    print(f"File: {DATASET_FILE}")


if __name__ == "__main__":
    main()