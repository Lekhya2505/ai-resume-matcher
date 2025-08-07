import spacy
from collections import Counter
import re

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text.lower())
    return text

def extract_keywords(text):
    doc = nlp(text)
    return [token.lemma_ for token in doc if token.pos_ in ['NOUN', 'VERB', 'ADJ']]

def match_resume_to_job(resume, jd):
    resume_clean = preprocess_text(resume)
    jd_clean = preprocess_text(jd)

    resume_keywords = extract_keywords(resume_clean)
    jd_keywords = extract_keywords(jd_clean)

    # Match Score Calculation
    match_keywords = set(resume_keywords) & set(jd_keywords)
    score = int(len(match_keywords) / len(set(jd_keywords)) * 100)

    # Section-wise match (placeholder logic)
    section_scores = {
        "Skills": score + 5,
        "Experience": score,
        "Education": score - 5
    }

    keyword_density = Counter(jd_keywords)

    suggestions = "Add more keywords related to: " + ", ".join(set(jd_keywords) - set(resume_keywords))

    return {
        "score": score,
        "section_scores": section_scores,
        "keyword_density": dict(keyword_density),
        "suggestions": suggestions
    }
