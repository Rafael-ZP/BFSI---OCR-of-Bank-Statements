# BFSI_OCR-of-Bank-Statements

## Overview
**BFSI_OCR-of-Bank-Statements** is a financial document processing system that extracts, categorizes, and visualizes data from various banking and financial documents using **OCR (Optical Character Recognition)** and **LLMs (Large Language Models)**. The project supports **supervised, semi-supervised, and unsupervised** learning techniques to analyze financial data.

<img width="1512" alt="image" src="https://github.com/user-attachments/assets/ff2cc45e-eca4-4bc1-88a5-e89405781b5e" />


## Project Structure

BFSI_OCR/         
│── Semi_Supervised/
│   ├── Api_Integration.py      # Fetches financial data via APIs
│   ├── init.py
│── Supervised/
│   ├── Supervised.py           # Processes structured data like bank statements
│   ├── init.py
│── Unsupervised/
│   ├── OCR_LLM.py              # Uses LLM to categorize uncategorized data
│   ├── init.py
│── App.py                      # Main application entry point

---

## Features

### 🏦 **Supervised Data Processing**
- Uses OCR on structured financial documents like **bank statements, cheques, and payslips**.
- Categorizes transactions (e.g., **food spendings, ATM withdrawals**).
- **Visualizes trends** in income and expenditures.

### 🌐 **Semi-Supervised API Data Processing**
- Fetches **real-time financial data** from bank APIs.
- Applies rule-based filtering for **categorization and analysis**.
- **Ensures data security and compliance** (e.g., GDPR).

### 🧠 **Unsupervised Data Processing with LLM**
- Uses **Large Language Models (LLMs)** for **auto-categorization**.
- Detects **patterns in transaction history**.
- Handles **uncategorized transactions efficiently**.

---

## Installation

```sh
git clone https://github.com/Rafael-ZP/BFSI_OCR-of-Bank-Statements.git
cd BFSI_OCR
pip install -r requirements.txt
```

Usage

Running the Application
```
python App.py
```
Screenshots

<img width="1512" alt="image" src="https://github.com/user-attachments/assets/4c58a66b-6fcb-4850-9478-78ad0c39c533" />


<img width="1512" alt="image" src="https://github.com/user-attachments/assets/3e13ec1b-544e-49ad-99cc-68e8802caf2e" />


Contributing

Contributions are welcome! Feel free to submit a pull request.

License

MIT License

This `README.md`:
✅ Explains the project  
✅ Includes the folder structure  
✅ Describes features & installation  
✅ Provides usage instructions  
✅ Adds placeholders for **screenshots**  
