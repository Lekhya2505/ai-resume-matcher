import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    return ' '.join([token.lemma_ for token in nlp(text.lower()) if not token.is_stop and not token.is_punct])

def get_cosine_similarity(resume_text, jd_text):
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform([resume_text, jd_text])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

def section_wise_match(resume_sections, jd_text):
    section_scores = {}
    for section, text in resume_sections.items():
        score = get_cosine_similarity(text, jd_text)
        section_scores[section] = round(score * 100, 2)
    return section_scores
