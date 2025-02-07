import streamlit as st
# Set page configuration with dark theme
st.set_page_config(
    page_title="Finance Analyzer Pro",
    layout="wide",
    page_icon="💹",
    initial_sidebar_state="collapsed"
)

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import io
from BFSI_OCR.Supervised.Supervised import save_to_db, load_data, generate_visualization
from BFSI_OCR.Unsupervised.OCR_LLM import main as analyze_bank_statement
from BFSI_OCR.Semi_Supervised.Api_Integration import get_visualization
import streamlit as st

# Custom CSS for the new design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    :root {
        --primary: #6366f1;
        --secondary: #a855f7;
        --background: #0f172a;
        --surface: #1e293b;
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
    background-image: url('https://i.pinimg.com/736x/6d/c7/96/6dc796884f9666ae31af845da7bcef55.jpg'); 
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #ffffff;
    
}
    
    .gradient-text {
        background: linear-gradient(45deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -1px !important;
    }
    
    .card {
        background: var(--surface) !important;
        border-radius: 16px !important;
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.2s;
    }
    
    .card:hover {
        transform: translateY(-5px);
    }
    
    .stButton>button {
        background: linear-gradient(45deg, var(--primary), var(--secondary));
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
        width: 100%;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: scale(1.02);
    }
    
    .stFileUploader {
        background: var(--surface) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .stAlert {
        background: var(--surface) !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = None

# Main header
st.markdown("""
<div style="text-align: center; margin-bottom: 4rem;">
    <h1 style="font-size: 3.5rem; margin: 0;">
        <span>🏦 </span> <span class="gradient-text">BANK SIGHT</span> <span>🔎</span>
    </h1>
    <p style="color: #94a3b8; font-size: 1.1rem;">Advanced Financial Insights Powered by AI</p>
</div>
""", unsafe_allow_html=True)

# Home page
if not st.session_state.page:
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        with st.container():
            st.markdown("""
            <div class="card">
                <h3 style="margin-top:0;">📄 Document Analysis</h3>
                <p style="color: #94a3b8;">Analyze financial statements, payslips, and invoices</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Get Started →", key="doc"):
                st.session_state.page = "documents"

    with col2:
        with st.container():
            st.markdown("""
            <div class="card">
                <h3 style="margin-top:0;">💳 Expense Analysis</h3>
                <p style="color: #94a3b8;">Deep insights from bank statements</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Get Started →", key="expense"):
                st.session_state.page = "expense"

    with col3:
        with st.container():
            st.markdown("""
            <div class="card">
                <h3 style="margin-top:0;">🌐 API Analysis</h3>
                <p style="color: #94a3b8;">Real-time bank API integration</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Get Started →", key="api"):
                st.session_state.page = "api"

    st.markdown("""
    <div style="text-align: justify;
text-align-last: center; margin-top: 4rem; color: white; margin-left: 30rem; margin-right: 30rem">
       <small>
    By using this web application, you acknowledge that the uploaded bank documents will undergo OCR processing. 
    We do not store or share your data, and all processing happens securely within your session. 
    Ensure that you have the necessary authorization to process these documents. 
    Use at your own discretion.
</small>
    </div>
    """, unsafe_allow_html=True)

# Document Analysis Page
elif st.session_state.page == "documents":
    st.markdown("<h2 style='color: white;'>📄 Document Analysis</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3], gap="large")
    
    with col1:
        if st.button("← Back to Main"):
            st.session_state.page = None
            st.rerun()
        
        # Initialize session state for doc type and uploaded file
        if 'doc_type' not in st.session_state:
            st.session_state['doc_type'] = None
        if 'uploaded_files' not in st.session_state:
            st.session_state['uploaded_files'] = None

        doc_type = st.selectbox(
            "Document Type",
            ["profit_loss", "payslips", "invoices"],
            help="Select the type of document you're uploading"
        )
        # Function to clear database tables
        def clear_tables():
            conn = sqlite3.connect('images.db')
            c = conn.cursor()
            tables = ['payslips', 'invoices', 'profit_loss']
            for table in tables:
                c.execute(f"DELETE FROM {table}")
                conn.commit()

            conn.close()
        
        # Reset state when document type changes
        if doc_type != st.session_state['doc_type']:
            st.session_state['doc_type'] = doc_type
            st.session_state['uploaded_files'] = None  # Reset file upload
            clear_tables()  # Clear any previous data from the database

        uploaded_files = st.file_uploader(
            "Upload Document",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=False,
            help="Upload a clear image of your document"
        )

    
        if uploaded_files:
            st.session_state['uploaded_files'] = uploaded_files

        # Initialize data variable
        data = None

        # Process uploaded files only if they exist in session state
        if st.session_state['uploaded_files']:
            save_to_db(doc_type, st.session_state['uploaded_files'])
            st.success("Files uploaded successfully!")

            # Fetch and display data after uploading
            data = load_data(doc_type)
        else:
            st.warning("No files uploaded. Please upload files to view data.")


    with col2:
        if uploaded_files:
            st.markdown("### Analysis Results")

            # Generate and display visualization
            if data is not None and not data.empty:
                fig = generate_visualization(doc_type)

                # Display the visualization
                st.pyplot(fig)

                # Provide download option for the visualization
                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)
                st.download_button("Download Visualization", buf, file_name=f"{doc_type}_visualization.png", mime="image/png")
            else:
                st.info("No data available for visualization.")


        else:
            st.markdown("""
            <div style="background: var(--surface); border-radius: 12px; padding: 2rem; text-align: center;">
                <p style="color: #94a3b8;">Upload a document to begin analysis</p>
            </div>
            """, unsafe_allow_html=True)

   

# Option 2: Bank Statement Analysis
elif st.session_state['page'] == "expense":
    st.markdown("<h2 style='color: white;'>📄 Document Analysis</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3], gap="large")

    with col1:
        if st.button("← Back to Main"):
            st.session_state['page'] = None
            st.rerun()
        
        uploaded_file = st.file_uploader(
            "Upload a Bank Statement (PDF)",
            type=["pdf"],
            accept_multiple_files=False,
            help="Upload a bank statement for analysis"
        )

        if uploaded_file:
            with st.spinner("Analyzing document..."):
                # Processing logic here
                pass

    with col2:
        if uploaded_file:
            st.markdown("### Analysis Results")
            fig = analyze_bank_statement(uploaded_file)
            if fig:
                st.pyplot(fig)

                # Download visualization
                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)
                st.download_button("Download Report", buf, file_name="bank_statement_analysis.png", mime="image/png")
            else:
                st.error("Failed to process the file. Please try again.")
        else:
            st.markdown("""
            <div style="background: var(--surface); border-radius: 12px; padding: 2rem; text-align: center;">
                <p style="color: #94a3b8;">Upload a document to begin analysis</p>
            </div>
            """, unsafe_allow_html=True)

# Option 3: Bank API Analysis
elif st.session_state['page'] == "api":
    st.subheader("Retrieve and Analyze Data via Bank API")

    # Add a back button to go back to the home page
    if st.button("Back to Home"):
        st.session_state['page'] = None
        st.rerun()

    # Heading and Note
    # Heading and Note
    st.markdown(
        '''
        <div class="note-box">
            <h3>This retrieves HDFC Bank Data</h3>
            <p>Data recovery via bank API is an official procedure that requires secure authentication and authorization
            from the bank's system. Typically, the data retrieval process is challenging because:</p>
            <ul>
                <li>Banks require stringent verification mechanisms to prevent unauthorized access.</li>
                <li>The API has limited access and strict rate limiting to avoid misuse.</li>
                <li>The data must be processed and filtered according to privacy regulations, such as GDPR.</li>
                <li>It requires a secure network connection to avoid man-in-the-middle attacks.</li>
                <li>Each API interaction must be logged and reported as per compliance rules.</li>
            </ul>
            <p>Hence, what you see here is just a sample of data retrieved from the HDFC Bank API to demonstrate the
            transaction behavior analysis.</p>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Fetch the extracted data and the generated graph from the backend
    df, fig = get_visualization()

    # Display the extracted DataFrame
    st.write("### Extracted Data from Bank API:")
    st.dataframe(df)

    # Display the bar graph
    st.write("### Bar Graph: Transaction Amount by Date")
    st.pyplot(fig)

    # Optionally add a download button for the graph
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    st.download_button("Download Visualization", buf, file_name="bank_statement_visualization.png", mime="image/png")
