from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    category = Column(String)
    price = Column(Integer)

    reviews = relationship("Review", back_populates="product", cascade="all, delete")


class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    reviewer = Column(String)
    rating = Column(Integer)
    review = Column(Text)
    product = relationship("Product", back_populates="reviews")
    

class ReviewPrediction(Base):
    __tablename__ = "review_predictions"

    id = Column(Integer, primary_key=True)
    review_id = Column(
        Integer, ForeignKey("reviews.review_id", ondelete="CASCADE"), nullable=True
    )
    reviewer = Column(String)
    rating = Column(Integer)
    review_text = Column(Text)
    label = Column(String, nullable=False)  # "Fake" / "Genuine"
    probability = Column(Float, nullable=False)  # confidence score
    model_version = Column(String, default="v1.0")  # useful for future retraining
    predicted_at = Column(DateTime, default=datetime.utcnow)
    features = relationship(
        "ReviewFeature",
        back_populates="prediction",
        uselist=False,
        cascade="all, delete-orphan"
    )


class ReviewFeature(Base):
    __tablename__ = "review_features"

    id = Column(Integer, primary_key=True)
    prediction_id = Column(
        Integer, ForeignKey("review_predictions.id", ondelete="CASCADE"), nullable=False
    )

    # ---------- TEXT STRUCTURE ----------
    text_length = Column(Integer)
    capital_ratio = Column(Float)
    punctuation_ratio = Column(Float)
    repetition_score = Column(Float)

    # ---------- NLP ----------
    sentiment_score = Column(Float)
    adjective_ratio = Column(Float)

    # ---------- FRAUD / CONSISTENCY ----------
    rating_sentiment_mismatch = Column(Integer)
    is_extreme_rating = Column(Integer)
    raw_review_similarity = Column(Float)
    review_similarity_score = Column(Float)
    category_consistency_score = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    prediction = relationship("ReviewPrediction", back_populates="features")
