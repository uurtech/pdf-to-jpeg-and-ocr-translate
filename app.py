import os
import re
import json
import boto3
from botocore.exceptions import ClientError

# Initialize AWS clients
textract = boto3.client('textract')
bedrock = boto3.client('bedrock-runtime')

def extract_text_from_image(image_path):
    with open(image_path, 'rb') as image:
        response = textract.detect_document_text(Document={'Bytes': image.read()})
    
    extracted_text = ' '.join([item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE'])
    return extracted_text

def translate_text(text):
    prompt = f"Human: First, identify the language of the following text and translate it to Turkish:\n\n{text}\n\nAssistant: Here's the English translation:"
    
    body = {
        "prompt": prompt,
        "max_tokens_to_sample": 500,
        "temperature": 0.7,
        "top_p": 0.9,
    }
    
    response = bedrock.invoke_model(
        modelId="anthropic.claude-v2",  # Using Claude v2 as an example
        body=json.dumps(body)
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['completion'].strip()

def natural_sort_key(s):
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', s)]

def process_images_in_folder(folder_path):
    with open('output.txt', 'a', encoding='utf-8') as f:
        # Get all JPEG files and sort them naturally
        image_files = [file for file in os.listdir(folder_path) if file.lower().endswith(('.jpg', '.jpeg'))]
        image_files.sort(key=natural_sort_key)

        for filename in image_files:
            image_path = os.path.join(folder_path, filename)
            f.write(f"Processing {filename}...\n")
            
            try:
                extracted_text = extract_text_from_image(image_path)
                if extracted_text:
                    translated_result = translate_text(extracted_text)
                    f.write(f"Original text: {extracted_text}\n")
                    f.write(f"Translated result: {translated_result}\n")
                else:
                    f.write("No text found in the image.\n")
            except ClientError as e:
                error_message = str(e)
                f.write(f"Error processing {filename}: {error_message}\n")
            
            f.write("---\n\n")
            f.flush()  # Ensure the content is written immediately

if __name__ == "__main__":
    data_folder = "./data"
    process_images_in_folder(data_folder)
    print("Processing completed. Results saved in output.txt")
