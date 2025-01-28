import streamlit as st
import subprocess
import sys


st.title("Financial Document Analyzer")

st.subheader("Choose an analysis method:")

if st.button("From Document (Supervised)"):
    st.info("Launching the supervised OCR Streamlit application...")
    script_path = "/Users/rafaelzieganpalg/Projects/Infosys 5.0/Final_Thing/Supervised/Supervised.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", script_path])

elif st.button("From Web URL (Semi-Supervised)"):
    st.info("Launching the Semi-Supervised OCR Streamlit application...")
    script_path = "/Users/rafaelzieganpalg/Projects/Infosys 5.0/Final_Thing/Semi_Supervised/Attempt_1.py"
    subprocess.run([sys.executable, "-m", "streamlit","run",script_path])
    

elif st.button("From AI (Unsupervised)"):
    st.info("Launching the Unsupervised OCR Streamlit application...")
    script_path = "/Users/rafaelzieganpalg/Projects/Infosys 5.0/Final_Thing/UnSupervised/Attempt_3.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", script_path])