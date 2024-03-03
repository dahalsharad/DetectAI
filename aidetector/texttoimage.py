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
from pathlib import Path
from pygments.formatters import ImageFormatter
from pygments import highlight
from pygments.lexers import TextLexer

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

def create_image(lines, output_file):
    lexer = TextLexer()
    png = highlight('\n'.join(lines), lexer, ImageFormatter(line_numbers=False))
    Path(output_file).write_bytes(png)

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
    

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(text_file, "r+") as text_file_open:
        text_file_open.seek(0)
        text_file_open.truncate()

        # Process each line
        for line in lines:
            # Split the line into words
            words = line.split()

            # Check if the line has more than 20 words
            if len(words) > 20:
                # Insert newline character after every 20 words
                new_lines = [' '.join(words[i:i+20]) for i in range(0, len(words), 20)]
                text_file_open.write('\n'.join(new_lines) + '\n')
            else:
                # If less than or equal to 20 words, write the line as it is
                text_file_open.write(line)


    with open(text_file, "r") as text_file_open:
    # Read lines from the file
        lines = text_file_open.readlines()

        # Iterate through the lines in groups of 48
        for i in range(0, len(lines), 48):
            # Extract 48 lines or fewer if there are fewer than 48 lines left
            group_of_lines = lines[i:i+48]
            
            # Create an image for the group of lines
            output_file = f"{output_folder}/page_{i + 1}.jpg"
            create_image(group_of_lines, output_file)



# create_highlighted_pdf()