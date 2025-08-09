import spacy

# Load spaCy model (make sure you have run: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

def match_resume_to_jd(resume_text, jd_text):
    """
    Compare resume and job description to get a match percentage and keyword matches.
    """
    # Clean & process text
    resume_doc = nlp(resume_text.lower())
    jd_doc = nlp(jd_text.lower())

    # Extract keywords (nouns + proper nouns)
    resume_keywords = {token.text for token in resume_doc if token.is_alpha and not token.is_stop}
    jd_keywords = {token.text for token in jd_doc if token.is_alpha and not token.is_stop}

    # Find matches
    common_keywords = resume_keywords.intersection(jd_keywords)
    match_percent = round(len(common_keywords) / len(jd_keywords) * 100, 2) if jd_keywords else 0

    return {
        "match_percent": match_percent,
        "common_keywords": list(common_keywords),
        "jd_keywords": list(jd_keywords),
        "resume_keywords": list(resume_keywords)
    }
