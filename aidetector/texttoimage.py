import os
from PIL import Image, ImageDraw, ImageFont
import math
import docx2txt
from spire.doc import *
from spire.doc.common import *
from pdf2image import convert_from_path
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_highlighted_pdf():
    # Directory containing the images
    image_directory = 'uploads/highlight'

    # Get a list of image files in the directory
    image_files = sorted([f for f in os.listdir(image_directory) if f.endswith(('.jpg', '.jpeg', '.png'))])

    # Create a PDF
    pdf_filename = 'aidetector/static/highlighted_output.pdf'
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Convert each image to PDF page
    for image_file in image_files:
        image_path = os.path.join(image_directory, image_file)
        img = Image.open(image_path)
        width, height = img.size

        # Add a new page with the same size as the image
        c.setPageSize((width, height))
        c.drawImage(image_path, 0, 0, width, height)

        # Add page break
        c.showPage()

    # Save the PDF
    c.save()


def pdf_to_image(pdf_path, output_folder):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert PDF to images
    images = convert_from_path(pdf_path)

    # Save each page as an image
    for i, image in enumerate(images):
        image_path = f"{output_folder}/page_{i + 1}.jpg"  # Change extension as needed
        image.save(image_path, "JPEG")


def file_to_image(extension,text_file,output_folder):
    text = ""
    if extension==".txt":
        
        text_file = text_file + "temp.txt"
        with open(text_file, 'r') as file:
            lines = file.readlines()

    elif extension==".docx":
        text_file = text_file + "temp.docx"
        text = docx2txt.process(text_file)
        lines = text.split("\n")

    elif extension ==".doc":
        text_file = text_file + "temp.doc"
        document = Document()
        document.LoadFromFile("text_file")
        document.SaveToFile("uploads/temp/t.docx", FileFormat.Docx2016)
        document.Close()
        text = docx2txt.process("uploads/temp/t.docx")
        text = text.replace("Evaluation Warning: The document was created with Spire.Doc for Python.", "")
        os.remove("uploads/temp/t.docx")
        lines = text.split("\n")
    
    font_size=14
    lines_per_page=48
    # Load font
    font = ImageFont.load_default()

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    total_lines = len(lines)
    num_pages = math.ceil(total_lines / lines_per_page)

    # Iterate through pages
    for page_num in range(num_pages):
        # Calculate starting and ending line indices for this page
        start_index = page_num * lines_per_page
        end_index = min((page_num + 1) * lines_per_page, total_lines)
        page_lines = lines[start_index:end_index]

        # Calculate image size
        max_line_length = max(len(line) for line in page_lines)
        image_width = max_line_length * font_size
        image_height = len(page_lines) * font_size

        # Create image
        image = Image.new("RGB", (image_width, image_height), "white")
        draw = ImageDraw.Draw(image)

        # Write text to image
        y_offset = 0
        for line in page_lines:
            draw.text((0, y_offset), line, fill="black", font=font)
            y_offset += font_size

        # Save image
        output_filename = os.path.join(output_folder, f"page_{page_num + 1}.png")
        image.save(output_filename)


# create_highlighted_pdf()