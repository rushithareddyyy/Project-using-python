import streamlit as st
import streamlit.components.v1 as components  # Import components for embedding HTML
from streamlit_extras.add_vertical_space import add_vertical_space
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# Load environment variables
load_dotenv()

# Set API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Load and Embed External HTML File
# with open("color.html", "r", encoding="utf-8") as html_file:
#  html_content = html_file.read()
# components.html(html_content, height=600, scrolling=True)  # Embed HTML in Streamlit

# Sidebar
with st.sidebar:
    st.title("Application Tracking System for Resume")
    st.subheader(" About")
    st.write("An advanced ATS tool using Gemini Pro and Streamlit to enhance your resume against job descriptions.")
    st.markdown(""" [GitHub](https://github.com/rushithareddyy) """)
    add_vertical_space(3)
    st.write(" with ❤️ Rushitha Reddy")

st.markdown('<h1 class="header"> ATS Analysis </h1>', unsafe_allow_html=True)
st.text(" Improve Your Resume 🌟")

# Job Description Input
jd = st.text_area(" Paste the Job Description 📄")

# Resume PDF Upload
uploaded_file = st.file_uploader(" Upload Your Resume 📂", type="pdf", help="Please upload a PDF file")

# Submit Button
submit = st.button(" Analyze 🔍 ")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))
        response_data = json.loads(response)
        
        st.markdown('<div class="output-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="header">📊 ATS Evaluation Results</h3>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-item"><span class="score">JD Match: {response_data["JD Match"]}%</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-item"><span class="subheader">Missing Keywords:</span> <span class="keyword">{", ".join(response_data["MissingKeywords"])}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-item"><span class="subheader">Profile Summary:</span> {response_data["Profile Summary"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Suggested Improvements
        st.markdown('<div class="output-container"><h4>✅ Suggested Improvements:</h4>', unsafe_allow_html=True)
        st.write("Here are some suggestions to improve your resume based on the job description:")
        for keyword in response_data['MissingKeywords']:
            st.write(f"- Add **{keyword}** to improve ATS match.")
        
        # Create Improved Resume PDF
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, "Improved Resume Based on ATS Feedback")
        c.drawString(100, 730, f"Job Description Match: {response_data['JD Match']}%")
        c.drawString(100, 710, f"Missing Keywords: {', '.join(response_data['MissingKeywords'])}")
        c.drawString(100, 690, f"Profile Summary: {response_data['Profile Summary']}")
        c.save()
        buffer.seek(0)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        st.download_button("⬇ Download Improved Resume (PDF)", data=buffer, file_name="Improved_Resume.pdf", mime="application/pdf")
        st.markdown('</div>', unsafe_allow_html=True)
