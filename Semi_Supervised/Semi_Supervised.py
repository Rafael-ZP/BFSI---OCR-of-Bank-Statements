import streamlit as st
import easyocr
import re
import requests
from pdf2image import convert_from_path
from PIL import Image
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import csv
from urllib.parse import urlparse, parse_qs

# Initialize Streamlit app
st.title("Document OCR and Analysis")

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'], gpu=True)

def ensure_directory(directory):
    """Ensure the directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def process_images_with_easyocr(images):
    """Process images with EasyOCR, save text to a CSV, and fetch text for further analysis."""
    ocr_results = {}
    csv_file_path = "/Users/rafaelzieganpalg/Projects/Infosys 5.0/Final_Thing/Supervised/Extractions/extracted_text.csv"
    ensure_directory(os.path.dirname(csv_file_path))  # Ensure directory exists

    # Open the CSV file for writing
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Image", "Extracted Text"])  # Write CSV header

        # Perform OCR on each image
        for i, image in enumerate(images):
            # Perform OCR using EasyOCR
            text = reader.readtext(np.array(image), detail=0)  # Extract text as a list of strings
            combined_text = " ".join(text)  # Combine all lines into a single string
            
            # Save the extracted text to the CSV
            writer.writerow([f"Image_{i + 1}", combined_text])
            ocr_results[f"Image_{i + 1}"] = combined_text  # Add to results dictionary

    st.write(f"OCR results saved to {csv_file_path}")

    # Return the extracted text dictionary
    return ocr_results

def extract_spending_data(ocr_text):
    """Extract spending categories and amounts from the OCR text."""
    categories = ["credit", "debit", "payment", "spending", "expense"]
    spending_data = {}

    # Regex to find numbers and associate them with categories
    for category in categories:
        matches = re.findall(rf"({category}.*?)(\d[\d,]*)", ocr_text, flags=re.IGNORECASE)
        for match in matches:
            category_name = match[0].strip()
            amount = float(match[1].replace(',', ''))
            spending_data[category_name] = spending_data.get(category_name, 0) + amount

    return spending_data

def generate_pie_chart(data):
    """Generate a pie chart for spending categories."""
    if not data:
        return None

    # Pie chart labels and data
    labels = data.keys()
    values = data.values()

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)
    plt.title("Spending Categories")

    # Save chart to a BytesIO object
    chart_buffer = io.BytesIO()
    plt.savefig(chart_buffer, format="png")
    plt.close()  # Avoid Tkinter-related issues

    chart_buffer.seek(0)
    return chart_buffer


# Streamlit UI elements
url_input = st.text_input("Enter the URL of the file:")
input_type = st.selectbox("Select the Document Type:", ["salary slip", "balance slip", "cash slip"])

if st.button("Process"):
    if url_input:
        try:
            # Download the file from the URL
            response = requests.get(url_input)
            response.raise_for_status()  # Raise an error if the request fails

            # Extract the file name from the URL (without query parameters)
            parsed_url = urlparse(url_input)
            file_name = os.path.basename(parsed_url.path)  # Get the base file name
            if '?' in file_name:
                file_name = file_name.split('?')[0]  # Remove query string

            temp_file_path = f"temp/{file_name}"

            # Ensure the temp directory exists
            ensure_directory("temp")

            # Save the file content to the temp directory
            with open(temp_file_path, "wb") as f:
                f.write(response.content)

            st.write(f"File downloaded successfully: {file_name}")

            images = []

            # Process the downloaded file
            if temp_file_path.endswith(".pdf"):
                images_pil = convert_from_path(temp_file_path)
                images.extend(images_pil)
            else:
                image = Image.open(temp_file_path)
                images.append(image)

            # Process images with EasyOCR
            ocr_results = process_images_with_easyocr(images)

            # Extract spending data from OCR results
            all_spending_data = {}
            for image, ocr_text in ocr_results.items():
                spending_data = extract_spending_data(ocr_text)
                all_spending_data.update(spending_data)

            # Display the extracted spending data
            st.subheader("Extracted Spending Data")
            st.write(all_spending_data)

            # Generate and display pie chart for spending categories
            st.subheader("Spending Categories Pie Chart")
            pie_chart_buffer = generate_pie_chart(all_spending_data)
            if pie_chart_buffer:
                st.image(pie_chart_buffer, caption="Spending Categories")

            st.success("Processing Complete!")
        except requests.exceptions.RequestException as e:
            st.error(f"Error downloading the file: {e}")
    else:
        st.error("Please enter a URL.")