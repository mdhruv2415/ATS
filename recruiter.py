from dotenv import load_dotenv
load_dotenv()

import base64
import streamlit as st
import os, io
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text 

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images=pdf2image.convert_from_bytes(uploaded_file.read())
        first_page=images[0] 

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("Please upload a PDF file")


# st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System", anchor=False, divider='red')
input_text = st.text_area("Enter the Job Description for the desired role", key="input")
uploaded_file = st.file_uploader("Upload your Resume in PDF Format...", type=["pdf"])

if uploaded_file is not None:
    st.write("Resume/CV Uploaded Successfully")

col1, col2 = st.columns([1,1])

with col1:
    submit1 = st.button("Detailed Review", use_container_width=True, type="secondary")
with col2:
    submit2 = st.button("Percentage Match", use_container_width=True, type="primary")

input_prompt1 = """
            You are an experienced HR Manager with tech experience in the field of Data 
            Science, Full Stack Web Development, Big Data Engineer, Devops, Data Analyst, 
            your task is to review the provided resume against the job description for these
            profiles.
            Please share your professional evaluation on whether the candidate's profile aligns with the role.
            Highlight the strengths and weaknesses of the applicant in relation to the specified job roles.
"""

input_prompt2 = """
You are an skilled ATS(Applicant Tracking System) scanner with a deep understanding of Data 
            Science, Full Stack Web Development, Big Data Engineer, Devops, Data Analyst and deep ATS functionality, 
            your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches the
            job description. First the output should come as percentage and then keywords missing 
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("Detailed Review")
        st.write(response)
    else:
        st.write("Please upload a resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("Percentage Match: ")
        st.write(response)
    else:
        st.write("Please upload a resume")