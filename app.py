import streamlit as st
from matcher import match_resume_to_jd
from utils.pdf_reader import extract_text_from_pdf
from utils.text_cleaner import clean_text
from resume_suggestions import get_resume_improvement_suggestions

st.set_page_config(page_title="AI Resume Matcher", layout="wide")

st.title("📄 AI Resume Matcher")
st.write("Upload your resume and paste the job description to see how well you match!")

# Upload resume
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if st.button("Match Resume"):
    if resume_file and job_description.strip():
        # Extract and clean resume text
        resume_text = extract_text_from_pdf(resume_file)
        resume_text = clean_text(resume_text)

        # Match
        match_result = match_resume_to_jd(resume_text, job_description)

        # Show results
        st.subheader("Match Results")
        st.metric("Match Percentage", f"{match_result['match_percent']}%")

        st.subheader("Common Keywords")
        st.write(", ".join(match_result['common_keywords']))

        # Suggestions from OpenAI
        st.subheader("Improvement Suggestions")
        suggestions = get_resume_improvement_suggestions(resume_text, job_description)
        st.write(suggestions)

    else:
        st.warning("Please upload a resume and paste a job description.")
