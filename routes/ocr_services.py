from flask import Blueprint, request, jsonify
import os
import fitz  # PyMuPDF
import easyocr
from werkzeug.utils import secure_filename
import global_settings as gs
from PIL import Image


ocr_services_blueprint = Blueprint('ocr_services', __name__)

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])  # Add other languages if needed


def extract_images_from_pdf(pdf_path):
    """Extract images from a PDF file."""
    doc = fitz.open(pdf_path)
    base_name = os.path.splitext(os.path.basename(doc.name))[0]
    images_path = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        # pix = page.get_pixmap()  # Render page to image
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        # Create output file path
        output_path = os.path.join(gs.output_images_path, f"{base_name}_page_{page_num + 1}.png")

        # Save image
        pix.save(output_path)
        images_path.append(output_path)
    doc.close()
    return images_path


def extract_text_from_image(image_bytes):
    """Extract text from an image using EasyOCR."""
    with open("temp_image.jpg", "wb") as img_file:
        img_file.write(image_bytes)
    text = reader.readtext("temp_image.jpg", detail=0)
    os.remove("temp_image.jpg")
    return " ".join(text)


@ocr_services_blueprint.route("/extract-text", methods=['POST'])
def extract_text():
    """API endpoint to extract text from images or PDFs."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(gs.upload_folder_path, filename)
    file.save(file_path)

    extracted_text = {}
    try:
        if filename.lower().endswith('.pdf'):
            # Process PDF file
            images_path = extract_images_from_pdf(file_path)
            for path in images_path:
                with open(path, "rb") as img_file:
                    image_bytes = img_file.read()
                text = extract_text_from_image(image_bytes)
                page_no = path.split('_page_')
                extracted_text[f"Page {page_no[1]}"] = text
        else:
            # Process image file
            with open(file_path, "rb") as img_file:
                image_bytes = img_file.read()
            text = extract_text_from_image(image_bytes)
            extracted_text["Image"] = text
    finally:
        os.remove(file_path)  # Clean up uploaded file

    return jsonify({"extracted_text": extracted_text})

