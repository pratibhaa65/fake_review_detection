import pandas as pd
import numpy as np
import re
import contractions
import joblib
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.metrics.pairwise import cosine_similarity

# Load all required models
classifier = joblib.load("../joblib/logistic_fake_review_model.pkl")
tfidf_lemm = joblib.load("../joblib/lemm_tfidf_vectorizer.pkl")
tfidf_raw = joblib.load("../joblib/raw_tfidf_vectorizer.pkl")
nn_raw = joblib.load("../joblib/raw_nn_model.pkl")
nn_lemm = joblib.load("../joblib/lemm_nn_model.pkl")
category_centroids = joblib.load("../joblib/category_centroids.pkl")

sia = SentimentIntensityAnalyzer()

# Helper functions

def capital_letter_ratio(text):
    letters = [c for c in text if c.isalpha()]
    if len(letters) == 0: return 0
    capitals = [c for c in letters if c.isupper()]
    return len(capitals) / len(letters)

def punctuation_ratio(text):
    if not text: return 0
    return len(re.findall(r"[^\w\s]", text)) / len(text)

def repetition_score(text):
    words = re.findall(r'\b\w+\b', str(text).lower())
    if not words: return 0
    return 1 - len(set(words)) / len(words)

def expand_text(text):
    if pd.isna(text): return ""
    return contractions.fix(text)

def clean_text(text):
    if pd.isna(text): return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def adjective_ratio(text):
    if not text.strip(): return 0
    tokens = word_tokenize(text)
    tags = pos_tag(tokens)
    adj_count = sum(1 for w, t in tags if t.startswith('JJ'))
    return adj_count / len(tokens) if tokens else 0

def sentiment_score(text):
    if not text.strip(): return 0
    return sia.polarity_scores(text)['compound']

def rating_polarity(r):
    if r >= 4: return 1
    elif r <= 2: return -1
    return 0

def rating_sentiment_mismatch(sentiment, rating):
    rp = rating_polarity(rating)
    if rp == 1 and sentiment < -0.2: return 1
    if rp == -1 and sentiment > 0.2: return 1
    return 0

def is_extreme_rating(r):
    return 1 if r in [1, 5] else 0

# -----------------------
# Stateful feature computations
# -----------------------

def raw_review_similarity(review_text):
    vec = tfidf_raw.transform([review_text])
    distances, indices = nn_raw.kneighbors(vec)
    sims = 1 - distances
    return sims[0][1:].max()  # max excluding self

def clean_review_similarity(review_text):
    vec = tfidf_lemm.transform([review_text])
    distances, indices = nn_lemm.kneighbors(vec)
    sims = 1 - distances
    return sims[0][1:].max()

def category_consistency_score(cleaned_text, category):
    if category not in category_centroids:
        return 0.0
    vec = tfidf_lemm.transform([cleaned_text])
    centroid = category_centroids[category]
    return cosine_similarity(vec, centroid)[0][0]

# -----------------------
# Main preprocessing + prediction
# -----------------------

def preprocess_and_predict(review_text, rating, category):
    # 1️⃣ Stateless numeric features
    text_len = len(str(review_text))
    capital_ratio = capital_letter_ratio(review_text)
    punct_ratio = punctuation_ratio(review_text)
    repetition = repetition_score(review_text)
    
    expanded = expand_text(review_text)
    cleaned = clean_text(expanded)
    adj_ratio = adjective_ratio(cleaned)
    sentiment = sentiment_score(cleaned)
    rsm = rating_sentiment_mismatch(sentiment, rating)
    extreme_flag = is_extreme_rating(rating)
    
    # 2️⃣ Stateful features
    raw_sim = raw_review_similarity(review_text)
    clean_sim = clean_review_similarity(cleaned)
    cat_score = category_consistency_score(cleaned, category)
    
    # 3️⃣ TF-IDF vector for classifier
    X_tfidf = tfidf_lemm.transform([cleaned])
    
    # 4️⃣ Combine numeric features with TF-IDF
    numeric_features = np.array([[text_len, capital_ratio, punct_ratio, adj_ratio,
                                  sentiment, rsm, raw_sim, cat_score, clean_sim,
                                  repetition, extreme_flag]])
    
    from scipy.sparse import hstack
    X_final_new = hstack([X_tfidf, numeric_features])
    
    # 5️⃣ Predict
    pred_label = classifier.predict(X_final_new)[0]
    pred_prob = classifier.predict_proba(X_final_new)[0][1]  # Probability of being fake
    
    return pred_label, pred_prob

# -----------------------
# Example usage
# -----------------------
new_review = "I love this product! Highly recommended."
new_rating = 5
new_category = "Pet Supplies"

label, prob = preprocess_and_predict(new_review, new_rating, new_category)
print("Predicted Label:", label)
print("Probability:", prob)