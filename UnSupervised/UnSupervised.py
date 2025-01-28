import os
import easyocr
import re
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from pdf2image import convert_from_path
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import streamlit as st
from io import BytesIO
from tabulate import tabulate

# Initialize EasyOCR Reader and LLM
reader = easyocr.Reader(['en'], gpu=True)
llm = ChatGroq(
    temperature=0,
    groq_api_key="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",
    model_name="llama-3.3-70b-versatile"
)

CROP_LIMITS = {"upper_percent": 0.00, "lower_percent": 0.00}

def ensure_directory(directory):
    os.makedirs(directory, exist_ok=True)

def crop_percent(image_path, output_path, upper_percent=0.00, lower_percent=0.00):
    with Image.open(image_path) as img:
        width, height = img.size
        crop_upper = height * upper_percent
        crop_lower = height * (1 - lower_percent)
        cropped_img = img.crop((0, crop_upper, width, crop_lower))
        if cropped_img.mode != 'RGB':
            cropped_img = cropped_img.convert('RGB')
        cropped_img.save(output_path, format="JPEG")

def convert_pdf_to_images(pdf_file, output_folder):
    ensure_directory(output_folder)
    images = convert_from_path(pdf_file, dpi=300)
    image_paths = []
    for i, img in enumerate(images):
        output_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
        img.save(output_path, "JPEG")
        image_paths.append(output_path)
    return image_paths

def process_images_with_easyocr(image_paths):
    text_list = []
    for image_path in image_paths:
        cropped_path = os.path.join(os.path.dirname(image_path), f"cropped_{os.path.basename(image_path)}")
        crop_percent(image_path, cropped_path, CROP_LIMITS.get("upper_percent"), CROP_LIMITS.get("lower_percent"))
        ocr_results = reader.readtext(cropped_path)
        recognized_text = " ".join([text for _, text, _ in ocr_results])
        text_list.append((image_path, recognized_text))
    return text_list

def get_prompt_for_document(input_type, ocr_text):
    prompts = {
    "salary slip": "Extract details: gross salary, allowances, net salary.",
    "balance slip": "Extract details: account name, number, balance, date.",
    "cash slip": "Extract details: transaction date, amount, ID, bank.",
    "bank statement": "Extract details: account number, transaction date, transaction type, amount, balance."
}
    return prompts[input_type].replace("{{ocr_text}}", ocr_text)

def extract_data_with_llm(ocr_text, input_type):
    prompt = get_prompt_for_document(input_type, ocr_text)
    # Pass prompt directly as a string, not in a dictionary
    return llm.invoke(prompt).content

def process_user_request(files, input_type):
    extracted_data = {}
    for file in files:
        if file.name.endswith('.pdf'):
            pdf_images = convert_pdf_to_images(file.name, "converted_images")
            ocr_data = process_images_with_easyocr(pdf_images)
        else:
            image_path = os.path.join("/Users/rafaelzieganpalg/Projects/Infosys 5.0/uploaded_files", file.name)
            with open(image_path, "wb") as f:
                f.write(file.getbuffer())
            ocr_data = process_images_with_easyocr([image_path])

        for img_path, ocr_text in ocr_data:
            extracted_data[img_path] = extract_data_with_llm(ocr_text, input_type)
    return extracted_data

def field_wise_comparison_data(data):
    field_data = {}
    for attributes in data.values():
        matches = re.findall(r"(\w+(?: \w+)*):\s*([^\n]+)", attributes)
        for key, value in matches:
            if key not in field_data:
                field_data[key] = []
            try:
                field_data[key].append(float(value.replace(",", "")))
            except ValueError:
                field_data[key].append(value)
    return field_data

def create_chart(data, chart_type, field):
    fig, ax = plt.subplots(figsize=(6, 6))
    if all(isinstance(x, (int, float)) for x in data):
        ax.hist(data, bins='auto', edgecolor='black')
        ax.set_title(f"{field} Distribution (Histogram)")
    else:
        unique_values = list(set(data))
        counts = [data.count(val) for val in unique_values]
        if chart_type == "Pie Chart":
            ax.pie(counts, labels=unique_values, autopct="%1.1f%%", startangle=90)
        elif chart_type == "Bar Chart":
            ax.bar(unique_values, counts)
            ax.set_xticks(range(len(unique_values)))
            ax.set_xticklabels(unique_values, rotation=45)
    return fig

def main():
    st.title("OCR Data Extraction and Visualization")
    st.write("Upload documents to extract specific data and visualize field-wise comparison charts.")

    save_directory = "uploaded_files"
    os.makedirs(save_directory, exist_ok=True)  

# File uploader widget
    uploaded_files = st.file_uploader("Upload Files", type=["jpg", "png", "jpeg", "pdf"], accept_multiple_files=True)
    input_type = st.radio("Select Document Type", ["salary slip", "balance slip", "cash slip", "bank statement"])
    chart_type = st.radio("Select Chart Type", ["Pie Chart", "Bar Chart"])

    if st.button("Process"):
        if uploaded_files:
            extracted_data = process_user_request(uploaded_files, input_type)
            field_data = field_wise_comparison_data(extracted_data)

            st.subheader("Extracted Data Table")
            table_data = [[key, ", ".join(map(str, values))] for key, values in field_data.items()]
            st.text(tabulate(table_data, headers=["Field", "Values"], tablefmt="grid"))

            st.subheader("Charts")
            for field, values in field_data.items():
                fig = create_chart(values, chart_type, field)
                st.pyplot(fig)
        else:
            st.warning("Please upload at least one file.")

if __name__ == "__main__":
    main()
