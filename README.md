# Fake Review Detection System

An end-to-end web application for detecting fake product reviews using NLP and machine learning, with a Flask API backend, a Next.js frontend, and a trained inference pipeline.

## Project Summary

This project helps teams collect product reviews while automatically screening suspicious or low-trust submissions.

The system combines:
- Product and review management APIs
- Real-time fake review prediction during review submission
- Rate limiting and duplicate payload checks by client IP
- Storage of prediction logs and extracted features for analysis
- A modern web UI for product browsing, creation, and review submission

## Architecture

- Frontend: Next.js (App Router), React, Tailwind CSS
- Backend: Flask + Flask-CORS
- Database Layer: SQLAlchemy models and session management
- ML/NLP Stack: scikit-learn, spaCy, NLTK, joblib artifacts
- Data/Training Assets: datasets and Jupyter notebooks for preprocessing, training, and inference experiments

### Main Modules

- `backend_service/`
- `frontend/`
- `dataset/`
- `joblib/`
- `preprocessing/`
- `src/` (notebooks)

## How It Works

1. A user creates products from the frontend.
2. Users submit reviews for a product.
3. Backend validates rating/text and checks anti-spam limits.
4. ML inference computes text and behavioral features, then predicts `Genuine` or `Fake`.
5. Prediction + feature row are saved for tracking.
6. Only `Genuine` reviews are inserted into the product reviews table.
7. `Fake` reviews are blocked and a rejection response is returned.

## Core Features

- Product CRUD (create, list, fetch by id, delete)
- Category discovery endpoint
- Review submission with ML-based filtering
- Duplicate/flood control using in-memory request windows
- Review prediction audit trail in `review_predictions`
- Feature storage in `review_features`
- Product-centric UI with category filtering and review modal

## Backend API Snapshot

Base URL: Flask server address (for example `http://localhost:5000`)

- `GET /products` -> List all products
- `POST /products` -> Create product
- `GET /products/<product_id>` -> Fetch a product with reviews
- `DELETE /products/<product_id>` -> Delete a product
- `GET /categories` -> Get distinct product categories
- `POST /products/<product_id>/reviews` -> Add review (runs fake-review detection)
- `DELETE /reviews/<review_id>` -> Delete review

## Data Model (High Level)

- `products`: product metadata
- `reviews`: accepted (genuine) reviews only
- `review_predictions`: prediction result, confidence, model version
- `review_features`: engineered features used for fraud/genuineness scoring

## Local Setup

## 1) Backend

```bash
cd backend_service
pip install -r requirements.txt
python app.py
```

Notes:
- Configure `DATABASE_URL` for SQLAlchemy connection.
- Use `python reset.py` to recreate database tables.

## 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Notes:
- Set `NEXT_PUBLIC_BACKEND_URL` to your Flask API URL.
- Default Next.js local URL is `http://localhost:3000`.

## ML Pipeline Assets

- Trained model/vectorizers/scalers are loaded from `joblib/`.
- Inference logic is in `backend_service/ml/inference.py`.
- Supporting notebooks:
  - `preprocessing/preprocessing.ipynb`
  - `src/train.ipynb`
  - `src/inference.ipynb`

## Current Status

- Frontend is implemented and integrated with backend API URLs.
- Backend has route/controller/model separation and error handlers.
- ML inference is integrated into review creation flow.
- Existing `frontend/README.md` is still the default Next.js template; this root README is the project-level documentation.
