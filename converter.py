import os
from pdf2image import convert_from_path

# Specify the path to poppler utilities
poppler_path = "/opt/homebrew/bin"  # This is the default path for Homebrew installations on M1 Macs

def convert_pdf_to_images(pdf_path, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Convert PDF to images
    images = convert_from_path(pdf_path, poppler_path=poppler_path)

    # Save each image with an incremental name
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'page_{i+1:03d}.jpg')
        image.save(image_path, 'JPEG')
        print(f'Saved: {image_path}')

if __name__ == "__main__":
    pdf_path = "input.pdf"  # Replace with your PDF file path
    output_folder = "data"
    
    convert_pdf_to_images(pdf_path, output_folder)
    print("Conversion completed.")
