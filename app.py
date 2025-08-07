import streamlit as st
from matcher import match_resume_to_jd
from resume_suggestions import get_suggestions
from utils import generate_heatmap, generate_keyword_density, save_uploaded_file
from database import save_to_db
from fpdf import FPDF
import os

st.set_page_config(page_title="AI Resume vs JD Matcher", layout="wide")

st.title("📄 AI Resume vs Job Description Matcher")

# Upload Resume
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
jd_text = st.text_area("Paste the Job Description here", height=200)

if uploaded_file and jd_text:
    file_path = save_uploaded_file(uploaded_file)
    
    # Matching
    match_results = match_resume_to_jd(file_path, jd_text)
    st.subheader("✅ Section-wise Matching")
    for section, score in match_results["section_scores"].items():
        st.write(f"**{section}**: {score:.2f}%")
        st.progress(score / 100)

    # Heatmap
    st.subheader("📊 Visual Match Heatmap")
    heatmap_fig = generate_heatmap(match_results["section_scores"])
    st.pyplot(heatmap_fig)

    # Keyword Density
    st.subheader("🔍 Keyword Density in Resume")
    keyword_fig = generate_keyword_density(file_path)
    st.pyplot(keyword_fig)

    # Suggestions
    st.subheader("🛠️ Suggestions to Improve Resume")
    for tip in get_suggestions(file_path, jd_text):
        st.warning(tip)

    # Downloadable Report
    if st.button("📥 Download PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="AI Resume vs JD Match Report", ln=True, align='C')
        for section, score in match_results["section_scores"].items():
            pdf.cell(200, 10, txt=f"{section}: {score:.2f}%", ln=True)
        pdf_path = "match_report.pdf"
        pdf.output(pdf_path)
        with open(pdf_path, "rb") as f:
            st.download_button("Download Match Report", f, file_name="resume_match_report.pdf")
    
    # Save to DB
    save_to_db(uploaded_file.name, jd_text, match_results["overall_score"])
else:
    st.info("Please upload a resume and paste the job description.")
