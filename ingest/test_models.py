import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from models import Base, Product, StoreProduct, PriceHistory

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_models.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

class TestProduct:
    def test_create_product(self, db_session):
        product = Product(
            name="Test Product",
            brand="Test Brand",
            category="test",
            size="200g",
            unit="g",
            description="Test description"
        )
        
        db_session.add(product)
        db_session.commit()
        
        assert product.id is not None
        assert product.name == "Test Product"
        assert product.brand == "Test Brand"
        assert product.created_at is not None
        assert product.updated_at is not None
    
    def test_product_relationships(self, db_session):
        product = Product(name="Test Product")
        db_session.add(product)
        db_session.flush()
        
        store_product = StoreProduct(
            store="coles",
            store_product_id="123",
            product_id=product.id,
            store_name="Test Product",
            current_price=5.99
        )
        
        db_session.add(store_product)
        db_session.commit()
        
        assert len(product.store_products) == 1
        assert product.store_products[0].store == "coles"

class TestStoreProduct:
    def test_create_store_product(self, db_session):
        product = Product(name="Test Product")
        db_session.add(product)
        db_session.flush()
        
        store_product = StoreProduct(
            store="coles",
            store_product_id="123456",
            product_id=product.id,
            store_name="Coles Test Product",
            current_price=9.99,
            availability=True,
            raw_details={"test": "data"}
        )
        
        db_session.add(store_product)
        db_session.commit()
        
        assert store_product.id is not None
        assert store_product.store == "coles"
        assert store_product.store_product_id == "123456"
        assert store_product.current_price == 9.99
        assert store_product.availability == True
        assert store_product.raw_details == {"test": "data"}
        assert store_product.created_at is not None
    
    def test_store_product_relationships(self, db_session):
        product = Product(name="Test Product")
        db_session.add(product)
        db_session.flush()
        
        store_product = StoreProduct(
            store="coles",
            store_product_id="123",
            product_id=product.id,
            store_name="Test Product",
            current_price=5.99
        )
        db_session.add(store_product)
        db_session.flush()
        
        price_history = PriceHistory(
            store_product_id=store_product.id,
            price=5.99,
            start_date=date.today()
        )
        
        db_session.add(price_history)
        db_session.commit()
        
        assert store_product.product.name == "Test Product"
        assert len(store_product.price_history) == 1
        assert store_product.price_history[0].price == 5.99

class TestPriceHistory:
    def test_create_price_history(self, db_session):
        product = Product(name="Test Product")
        db_session.add(product)
        db_session.flush()
        
        store_product = StoreProduct(
            store="coles",
            store_product_id="123",
            product_id=product.id,
            store_name="Test Product",
            current_price=5.99
        )
        db_session.add(store_product)
        db_session.flush()
        
        price_history = PriceHistory(
            store_product_id=store_product.id,
            price=5.99,
            start_date=date(2023, 1, 1),
            end_date=date(2023, 1, 31)
        )
        
        db_session.add(price_history)
        db_session.commit()
        
        assert price_history.id is not None
        assert price_history.price == 5.99
        assert price_history.start_date == date(2023, 1, 1)
        assert price_history.end_date == date(2023, 1, 31)
        assert price_history.created_at is not None
    
    def test_price_history_relationships(self, db_session):
        product = Product(name="Test Product")
        db_session.add(product)
        db_session.flush()
        
        store_product = StoreProduct(
            store="coles",
            store_product_id="123",
            product_id=product.id,
            store_name="Test Product",
            current_price=5.99
        )
        db_session.add(store_product)
        db_session.flush()
        
        price_history = PriceHistory(
            store_product_id=store_product.id,
            price=5.99,
            start_date=date.today()
        )
        
        db_session.add(price_history)
        db_session.commit()
        
        assert price_history.store_product.store == "coles"
        assert price_history.store_product.product.name == "Test Product"

class TestDatabaseOperations:
    def test_query_products_by_category(self, db_session):
        product1 = Product(name="Seafood Product", category="seafood")
        product2 = Product(name="Meat Product", category="meat")
        product3 = Product(name="Another Seafood", category="seafood")
        
        db_session.add_all([product1, product2, product3])
        db_session.commit()
        
        seafood_products = db_session.query(Product).filter(
            Product.category == "seafood"
        ).all()
        
        assert len(seafood_products) == 2
        assert all(p.category == "seafood" for p in seafood_products)
    
    def test_query_store_products_by_store(self, db_session):
        product = Product(name="Test Product")
        db_session.add(product)
        db_session.flush()
        
        coles_product = StoreProduct(
            store="coles", store_product_id="1", 
            product_id=product.id, store_name="Test", current_price=5.99
        )
        aldi_product = StoreProduct(
            store="aldi", store_product_id="2", 
            product_id=product.id, store_name="Test", current_price=4.99
        )
        
        db_session.add_all([coles_product, aldi_product])
        db_session.commit()
        
        coles_products = db_session.query(StoreProduct).filter(
            StoreProduct.store == "coles"
        ).all()
        
        assert len(coles_products) == 1
        assert coles_products[0].store == "coles"