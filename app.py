import streamlit as st
from matcher import match_resume_to_job
from resume_suggestions import get_suggestions
from utils import extract_text_from_pdf, visualize_keyword_density
import base64
import tempfile
import os

st.set_page_config(page_title="AI Resume Matcher", layout="wide")

st.title("📄 AI Resume vs Job Description Matcher")

# Upload resume and JD
resume_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste the Job Description")

if resume_file and jd_text:
    # Extract resume text
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(resume_file.read())
        resume_text = extract_text_from_pdf(tmp_file.name)
        os.unlink(tmp_file.name)

    # Match Score
    score, section_scores, keyword_matches = match_resume_to_job(resume_text, jd_text)
    
    st.success(f"✅ Overall Match Score: {score}%")

    # Section-wise scores
    st.subheader("📌 Section-wise Match")
    for section, sec_score in section_scores.items():
        st.markdown(f"**{section}**: {sec_score}%")

    # Keyword Density Heatmap
    st.subheader("🔍 Keyword Density Heatmap")
    fig = visualize_keyword_density(resume_text, jd_text)
    st.pyplot(fig)

    # Suggestions
    st.subheader("🛠 Resume Improvement Suggestions")
    suggestions = get_suggestions(resume_text, jd_text)
    for s in suggestions:
        st.markdown(f"- {s}")

    # Download Report (basic PDF)
    st.subheader("📥 Downloadable Report")
    report = f"""Match Score: {score}%
Suggestions:
{chr(10).join(suggestions)}
"""
    b64 = base64.b64encode(report.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="report.txt">Download Report</a>'
    st.markdown(href, unsafe_allow_html=True)
