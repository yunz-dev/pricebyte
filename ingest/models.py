from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Date, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, date
from config import DATABASE_URL

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    brand = Column(Text)
    category = Column(Text, index=True)
    size = Column(Text)
    unit = Column(Text)
    image_url = Column(Text)
    description = Column(Text)
    vector_embedding = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    store_products = relationship("StoreProduct", back_populates="product")

class StoreProduct(Base):
    __tablename__ = "store_products"
    
    id = Column(Integer, primary_key=True, index=True)
    store = Column(String(50), nullable=False)
    store_product_id = Column(String(100), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    store_name = Column(Text, nullable=False)
    current_price = Column(Float)
    product_url = Column(Text)
    availability = Column(Boolean, default=True)
    raw_details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    product = relationship("Product", back_populates="store_products")
    price_history = relationship("PriceHistory", back_populates="store_product")

class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True, index=True)
    store_product_id = Column(Integer, ForeignKey("store_products.id"), nullable=False)
    price = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False, default=date.today)
    end_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    store_product = relationship("StoreProduct", back_populates="price_history")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)