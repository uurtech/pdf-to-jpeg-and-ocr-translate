import os
import fitz  # PyMuPDF

def convert_pdf_to_images(pdf_path, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Iterate through each page
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document[page_number]

        # Convert page to image
        pix = page.get_pixmap()

        # Save image
        image_path = os.path.join(output_folder, f'page_{page_number + 1:03d}.jpg')
        pix.save(image_path)
        print(f'Saved: {image_path}')

    # Close the PDF file
    pdf_document.close()

if __name__ == "__main__":
    pdf_path = "./data.pdf"  # Replace with your PDF file path
    output_folder = "data"
    
    convert_pdf_to_images(pdf_path, output_folder)
    print("Conversion completed.")
