from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .session import Base


class Platform(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    base_url = Column(String, nullable=False)
    search_url_template = Column(String, nullable=False)

    products_data = relationship("ScrapedProductData", back_populates="platform")
    regression_models = relationship("RegressionModel", back_populates="platform")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    global_query_name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    scraped_data = relationship("ScrapedProductData", back_populates="product")


class ScrapedProductData(Base):
    __tablename__ = "scraped_product_data"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=False)
    url_on_platform = Column(String)
    name_on_platform = Column(String)
    price = Column(Float)
    currency = Column(String(3))
    rating = Column(Float)
    reviews_count = Column(Integer)
    availability_status = Column(String)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    search_position = Column(Integer)

    product = relationship("Product", back_populates="scraped_data")
    platform = relationship("Platform", back_populates="products_data")


class RegressionModel(Base):
    __tablename__ = "regression_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    target_variable = Column(String, nullable=False)
    feature_variables = Column(JSON)  # список факторів
    coefficients_json = Column(JSON)  # коефіцієнти моделі
    intercept = Column(Float)
    r_squared = Column(Float)
    last_trained_at = Column(DateTime)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=True)

    platform = relationship("Platform", back_populates="regression_models")
