import re
import numpy as np
import joblib
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack
import contractions
import spacy

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
JOBLIB_DIR = os.path.join(BASE_DIR, "joblib")



# Classifier
clf = joblib.load(os.path.join(JOBLIB_DIR, "logistic_fake_review_model.pkl"))

# TF-IDF + NN models
raw_tfidf = joblib.load(os.path.join(JOBLIB_DIR, "raw_tfidf_vectorizer.pkl"))
raw_nn = joblib.load(os.path.join(JOBLIB_DIR, "raw_nn_model.pkl"))

lemm_tfidf = joblib.load(os.path.join(JOBLIB_DIR, "lemm_tfidf_vectorizer.pkl"))
lemm_nn = joblib.load(os.path.join(JOBLIB_DIR, "lemm_nn_model.pkl"))

# Category centroids
category_centroids = joblib.load(os.path.join(JOBLIB_DIR, "category_centroids.pkl"))

# Numeric feature order
numeric_feature_order = joblib.load(os.path.join(JOBLIB_DIR, "numeric_feature_order.pkl"))

# NLP tools
sia = SentimentIntensityAnalyzer()
nlp = spacy.load("en_core_web_sm")


def capital_letter_ratio(text):
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for c in letters if c.isupper()) / len(letters)


def punctuation_ratio(text):
    if not text:
        return 0.0
    return len(re.findall(r"[^\w\s]", text)) / len(text)


def repetition_score(text):
    words = re.findall(r"\b\w+\b", text.lower())
    if not words:
        return 0.0
    return 1 - len(set(words)) / len(words)


def expand_contractions(text):
    return contractions.fix(text) if isinstance(text, str) else ""


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def adjective_ratio(text):
    tokens = word_tokenize(text)
    if not tokens:
        return 0.0
    tags = pos_tag(tokens)
    return sum(1 for _, t in tags if t.startswith("JJ")) / len(tokens)


def sentiment_score(text):
    return sia.polarity_scores(text)["compound"] if text else 0.0


def rating_polarity(r):
    if r >= 4:
        return 1
    if r <= 2:
        return -1
    return 0


def rating_sentiment_mismatch(sentiment, rating):
    rp = rating_polarity(rating)
    if rp == 1 and sentiment < -0.2:
        return 1
    if rp == -1 and sentiment > 0.2:
        return 1
    return 0


def lemmatize(text):
    doc = nlp(text)
    return " ".join(t.lemma_ for t in doc if not t.is_space)


def raw_review_similarity(text):
    vec = raw_tfidf.transform([text])
    distances, _ = raw_nn.kneighbors(vec, n_neighbors=5)
    sims = 1 - distances
    return sims[0].max()


def lemm_review_similarity(text):
    vec = lemm_tfidf.transform([text])
    distances, _ = lemm_nn.kneighbors(vec, n_neighbors=5)
    sims = 1 - distances
    return sims[0].max()


def category_consistency(text, category):
    if category not in category_centroids:
        return 0.0
    vec = lemm_tfidf.transform([text])
    centroid = category_centroids[category]
    return cosine_similarity(vec, centroid)[0][0]


def predict_review(review, rating, category):
    print(category);
    # ---------- RAW ----------
    text_length = len(str(review))
    cap_ratio = capital_letter_ratio(review)
    punct_ratio = punctuation_ratio(review)
    rep_score = repetition_score(review)

    # ---------- CLEAN ----------
    expanded = expand_contractions(review)
    cleaned = clean_text(expanded)

    adj_ratio = adjective_ratio(cleaned)
    sent_score = sentiment_score(cleaned)
    mismatch = rating_sentiment_mismatch(sent_score, rating)
    extreme = 1 if rating in [1, 5] else 0

    # ---------- LEMMATIZED ----------
    lemm = lemmatize(cleaned)

    # ---------- STATEFUL ----------
    raw_sim = raw_review_similarity(review)
    lemm_sim = lemm_review_similarity(lemm)
    cat_score = category_consistency(lemm, category)

    # ---------- NUMERIC VECTOR ----------
    numeric_dict = {
        "text_length": text_length,
        "capital_ratio": cap_ratio,
        "punctuation_ratio": punct_ratio,
        "adjective_ratio": adj_ratio,
        "sentiment_score": sent_score,
        "rating_sentiment_mismatch": mismatch,
        "raw_review_similarity": raw_sim,
        "category_consistency_score": cat_score,
        "review_similarity_score": lemm_sim,
        "repetition_score": rep_score,
        "is_extreme_rating": extreme,
    }

    numeric_values = np.array([[numeric_dict[f] for f in numeric_feature_order]])

    # ---------- FINAL MATRIX ----------
    X_text = lemm_tfidf.transform([lemm])
    X_final = hstack([X_text, numeric_values])

    # ---------- PREDICTION ----------
    pred = clf.predict(X_final)[0]
    prob = clf.predict_proba(X_final)[0, 1]

    return {
        "prediction": "Genuine" if pred == 1 else "Fake",
        "probability": float(prob),
        "features": numeric_dict,
    }
