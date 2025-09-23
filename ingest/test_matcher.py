import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Product
from matcher import ProductMatcher

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_matcher.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def matcher(db_session):
    return ProductMatcher(db_session, threshold=0.8)

class TestProductMatcher:
    def test_exact_match(self, matcher, db_session):
        product = Product(
            name="Japanese Infusion Salmon Portion",
            brand="Huon",
            category="seafood",
            size="200g"
        )
        db_session.add(product)
        db_session.commit()
        
        match = matcher.find_matching_product(
            "Japanese Infusion Salmon Portion",
            "Huon",
            "seafood",
            "200g"
        )
        
        assert match is not None
        assert match.id == product.id
    
    def test_similar_name_match(self, matcher, db_session):
        product = Product(
            name="Japanese Fusion Salmon Portion",
            brand="Huon",
            category="seafood",
            size="200g"
        )
        db_session.add(product)
        db_session.commit()
        
        match = matcher.find_matching_product(
            "Japanese Infusion Salmon Portion",
            "Huon",
            "seafood",
            "200g"
        )
        
        assert match is not None
        assert match.id == product.id
    
    def test_no_match_different_brand(self, matcher, db_session):
        product = Product(
            name="Japanese Infusion Salmon Portion",
            brand="Huon",
            category="seafood",
            size="200g"
        )
        db_session.add(product)
        db_session.commit()
        
        match = matcher.find_matching_product(
            "Japanese Infusion Salmon Portion",
            "Different Brand",
            "seafood",
            "200g"
        )
        
        assert match is None
    
    def test_no_match_very_different_name(self, matcher, db_session):
        product = Product(
            name="Japanese Infusion Salmon Portion",
            brand="Huon",
            category="seafood",
            size="200g"
        )
        db_session.add(product)
        db_session.commit()
        
        match = matcher.find_matching_product(
            "Completely Different Product",
            "Huon",
            "seafood",
            "200g"
        )
        
        assert match is None
    
    def test_size_compatibility(self, matcher, db_session):
        product = Product(
            name="Test Product",
            brand="TestBrand",
            category="test",
            size="1kg"
        )
        db_session.add(product)
        db_session.commit()
        
        match = matcher.find_matching_product(
            "Test Product",
            "TestBrand",
            "test",
            "1000g"
        )
        
        assert match is not None
    
    def test_clean_text(self, matcher):
        text = "Japanese Infusion Salmon 200g Portion!!"
        cleaned = matcher._clean_text(text)
        
        assert "200g" not in cleaned
        assert "japanese" in cleaned
        assert "infusion" in cleaned
        assert "salmon" in cleaned
        assert "portion" in cleaned
    
    def test_extract_number(self, matcher):
        assert matcher._extract_number("200g") == 200.0
        assert matcher._extract_number("1.5kg") == 1.5
        assert matcher._extract_number("no numbers") is None
    
    def test_extract_unit(self, matcher):
        assert matcher._extract_unit("200g") == "g"
        assert matcher._extract_unit("1.5kg") == "kg"
        assert matcher._extract_unit("500ml") == "ml"
        assert matcher._extract_unit("2l") == "l"
        assert matcher._extract_unit("6 pack") == "pack"
    
    def test_are_compatible_units(self, matcher):
        assert matcher._are_compatible_units("g", "kg") == True
        assert matcher._are_compatible_units("ml", "l") == True
        assert matcher._are_compatible_units("g", "l") == False
        assert matcher._are_compatible_units("pack", "g") == False
    
    def test_normalize_to_grams(self, matcher):
        assert matcher._normalize_to_grams(1, "kg") == 1000
        assert matcher._normalize_to_grams(500, "g") == 500
        assert matcher._normalize_to_grams(1, "l") == 1000
        assert matcher._normalize_to_grams(500, "ml") == 500
        assert matcher._normalize_to_grams(1, "pack") is None
    
    def test_compare_sizes_exact_match(self, matcher):
        similarity = matcher._compare_sizes("200g", "200g")
        assert similarity == 1.0
    
    def test_compare_sizes_compatible_units(self, matcher):
        similarity = matcher._compare_sizes("1kg", "1000g")
        assert similarity == 1.0
    
    def test_compare_sizes_different_amounts(self, matcher):
        similarity = matcher._compare_sizes("200g", "400g")
        assert similarity == 0.5
    
    def test_compare_sizes_incompatible_units(self, matcher):
        similarity = matcher._compare_sizes("200g", "200ml")
        assert 0 < similarity < 1
    
    def test_calculate_similarity_score(self, matcher):
        score = matcher._calculate_similarity_score(
            "Japanese Infusion Salmon", "Huon", "seafood", "200g",
            "Japanese Fusion Salmon", "Huon", "seafood", "200g"
        )
        assert score > 0.8
        
        score = matcher._calculate_similarity_score(
            "Japanese Infusion Salmon", "Huon", "seafood", "200g",
            "Completely Different Product", "Different Brand", "beverages", "500g"
        )
        assert score < 0.5