from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

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
