import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st


data = {
    "AccountStatementOverAPIResponse": {
        "Data": {
            "AccountStatementReportResponseBody": {
                "statusCode": 200,
                "message": "OK",
                "requestTimeEpoch": "1699999999999",
                "requestId": "a1b2c3d4-e5f6-7890-gh12-ijklmnop3456",
                "rowsCount": 5,
                "openingBalance": 5000,
                "closingBalance": 12000,
                "accountNumber": "918020068###123",
                "currency": "INR",
                "data": [
                    {
                        "serialNumber": 1,
                        "transactionDate": "15/03/2023",
                        "pstdDate": "15/03/2023 10:30:45",
                        "transactionParticulars": "IMPS/PAYTM/9876543210/Shopping",
                        "chqNumber": " ",
                        "valueDate": "15/03/2023",
                        "amount": 1500,
                        "drcr": "DR",
                        "balance": 3500,
                        "paymentMode": "IMPS",
                        "utrNumber": "PAY9876543210",
                        "internalReferenceNumber": "IMPSPAY987654",
                        "remittingBranch": "MG ROAD, BANGALORE",
                        "remittingBankName": "HDFC BANK",
                        "remittingAccountNumber": "918020068###123",
                        "remittingAccountName": "John Doe",
                        "remittingIFSC": "HDFC0000123",
                        "benficiaryBranch": "Mumbai",
                        "benficiaryName": "Amazon India",
                        "benficiaryAccountNumber": "123456789012",
                        "benficiaryIFSC": "ICIC0000456",
                        "channel": "IMPS",
                        "timeStamp": "10:30:45",
                        "remarks": "E-commerce Payment",
                        "transactionCurrencyCode": "INR",
                        "entryDate": "15/03/2023 10:30:45",
                        "referenceId": "IMPSPAY987654",
                        "transactionIdentificationCode": "TXN12345"
                    },
                    {
                        "serialNumber": 2,
                        "transactionDate": "16/03/2023",
                        "pstdDate": "16/03/2023 15:20:30",
                        "transactionParticulars": "NEFT/ICIC0001234/Salary Credit",
                        "chqNumber": " ",
                        "valueDate": "16/03/2023",
                        "amount": 20000,
                        "drcr": "CR",
                        "balance": 23500,
                        "paymentMode": "NEFT",
                        "utrNumber": "NEFT123456789",
                        "internalReferenceNumber": "ICICNEFT9876",
                        "remittingBranch": "Whitefield, Bangalore",
                        "remittingBankName": "ICICI BANK",
                        "remittingAccountNumber": "555555555555",
                        "remittingAccountName": "XYZ Pvt Ltd",
                        "remittingIFSC": "ICIC0001234",
                        "benficiaryBranch": "MG Road, Bangalore",
                        "benficiaryName": "John Doe",
                        "benficiaryAccountNumber": "918020068###123",
                        "benficiaryIFSC": "HDFC0000123",
                        "channel": "NEFT",
                        "timeStamp": "15:20:30",
                        "remarks": "March Salary",
                        "transactionCurrencyCode": "INR",
                        "entryDate": "16/03/2023 15:20:30",
                        "referenceId": "ICICNEFT9876",
                        "transactionIdentificationCode": "SAL45678"
                    },
                    {
                        "serialNumber": 3,
                        "transactionDate": "18/03/2023",
                        "pstdDate": "18/03/2023 12:10:55",
                        "transactionParticulars": "ATM Withdrawal - SBI",
                        "chqNumber": " ",
                        "valueDate": "18/03/2023",
                        "amount": 5000,
                        "drcr": "DR",
                        "balance": 18500,
                        "paymentMode": "ATM",
                        "utrNumber": " ",
                        "internalReferenceNumber": "ATM987654321",
                        "remittingBranch": "Koramangala, Bangalore",
                        "remittingBankName": "HDFC BANK",
                        "remittingAccountNumber": "918020068###123",
                        "remittingAccountName": "John Doe",
                        "remittingIFSC": "HDFC0000123",
                        "benficiaryBranch": "SBI ATM",
                        "benficiaryName": "Cash Withdrawal",
                        "benficiaryAccountNumber": " ",
                        "benficiaryIFSC": " ",
                        "channel": "ATM",
                        "timeStamp": "12:10:55",
                        "remarks": "ATM Cash Withdrawal",
                        "transactionCurrencyCode": "INR",
                        "entryDate": "18/03/2023 12:10:55",
                        "referenceId": "ATM987654321",
                        "transactionIdentificationCode": "WITH123"
                    }
                ],
                "paging": {
                    "cursors": {
                        "next": "",
                        "previous": "MjAyMzAzMTgxMjEwNTUzNDAzNTAxNVMzMTc1MTEzMDEwMXx8fDY="
                    }
                }
            }
        },
        "Risk": {},
        "Links": {},
        "Meta": {}
    }
}

def get_transaction_data():
    """
    Extracts transaction data from the API response and returns it as a DataFrame.
    """
    transaction_data = data['AccountStatementOverAPIResponse']['Data']['AccountStatementReportResponseBody']['data']
    df = pd.DataFrame(transaction_data)  # Convert to DataFrame
    df['transactionDate'] = pd.to_datetime(df['transactionDate'], format='%d/%m/%Y')  # Convert dates
    return df

def generate_bar_chart(df):
 
    # Step 2: Bar Graph
    st.write("### Bar Graph: Transaction Amount by Date")
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a colormap (example: 'viridis' colormap)
    colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1'][0:df.shape[0]]

    # Correct way to use plt.bar()
    ax.bar(df['entryDate'], df['amount'], color=colors, label='Transaction Amount')

    # Customize plot
    ax.set_title("Transaction Amounts by Date", fontsize=16)
    ax.set_xlabel("Transaction Date", fontsize=12)
    ax.set_ylabel("Transaction Amount", fontsize=12)
    ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels
    ax.legend(title="Legend")

    # Display the graph in Streamlit
    return fig

def get_visualization():
    df = get_transaction_data()  # Extract data
    fig = generate_bar_chart(df)  # Generate visualization
    return df, fig
