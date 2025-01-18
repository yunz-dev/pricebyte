from sqlalchemy import JSON, Column, Float, Integer, String, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker
from utils.model import Store, ProductInfo, PriceUpdates

Base = declarative_base()


# Table definitions
class SimpleProduct(Base):
    __tablename__ = "simple_products"

    store = Column(String, primary_key=True)
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

    def __repr__(self):
        return (
            f"<SimpleProduct(store='{self.store}', id={
                self.id}, price={self.price})>"
        )


class ComplexProduct(Base):
    __tablename__ = "products"

    store = Column(String, primary_key=True)
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    details = Column(JSON)

    def __repr__(self):
        return f"<Product(store='{self.store}', id={self.id}, price={self.price})>"


# Main database (only simple products)
class MainDatabase:
    def __init__(self, db_name: str = "main", echo: bool = False):
        self.db_name = db_name
        self.engine = create_engine(f"sqlite:///{db_name}.db", echo=echo)
        self.Session = sessionmaker(bind=self.engine)
        self._setup_database()

    def _setup_database(self):
        """Setup main database with only simple_products table"""
        Base.metadata.create_all(self.engine, tables=[SimpleProduct.__table__])

    def get_session(self):
        """Get a new database session"""
        return self.Session()

    def close_engine(self):
        """Close the database engine"""
        self.engine.dispose()

    def clear_data(self):
        """Clear all data from simple products table"""
        session = self.get_session()
        try:
            session.query(SimpleProduct).delete()
            session.commit()
            print(f"Cleared all data from {self.db_name} database")
        except Exception as e:
            session.rollback()
            print(f"Error clearing data from {self.db_name}: {e}")
        finally:
            session.close()

    def check_if_in_db(self, store: str, id: int) -> bool:
        """Check if a product exists in the database"""
        session = self.get_session()
        try:
            exists = (
                session.query(SimpleProduct).filter_by(
                    store=store, id=id).first()
                is not None
            )
            return exists
        except Exception as e:
            print(f"Error checking if product {store}-{id} exists: {e}")
            return False
        finally:
            session.close()

    def add_simple_product(self, store: str, id: int, name: str, price: float) -> bool:
        """
        Add a simple product if it doesn't exist.
        Returns True if inserted, False if already exists.
        """
        session = self.get_session()
        try:
            # Check if already exists
            existing = (
                session.query(SimpleProduct).filter_by(
                    store=store, id=id).first()
            )
            if existing:
                print(f"Product {store}-{id} already exists in database")
                return False

            # Insert new product
            product = SimpleProduct(
                store=store, id=id, name=name, price=price
            )  # Add name parameter
            session.add(product)
            session.commit()
            print(f"Added simple product: {
                  store}-{id} '{name}' with price {price}")
            return True

        except Exception as e:
            session.rollback()
            print(f"Error adding simple product {store}-{id}: {e}")
            return False
        finally:
            session.close()

    def check_price(self, store: str, id: int, new_price: float) -> bool:
        """
        Check and update price if different.
        Returns True if price was updated, False if same or product doesn't exist.
        """
        session = self.get_session()
        try:
            existing = (
                session.query(SimpleProduct).filter_by(
                    store=store, id=id).first()
            )
            if not existing:
                print(f"Product {store}-{id} not found in database")
                return False

            if existing.price == new_price:
                print(
                    f"Price for {
                        store}-{id} is already {new_price}, no update needed"
                )
                return False

            old_price = existing.price
            existing.price = new_price
            session.commit()
            print(f"Updated price for {
                  store}-{id} from {old_price} to {new_price}")
            return True

        except Exception as e:
            session.rollback()
            print(f"Error checking/updating price for {store}-{id}: {e}")
            return False
        finally:
            session.close()

    def get_simple_products_by_store(self, store: str):
        """Get all simple products for a store"""
        session = self.get_session()
        try:
            return session.query(SimpleProduct).filter_by(store=store).all()
        except Exception as e:
            print(f"Error getting simple products for store {store}: {e}")
            return []
        finally:
            session.close()

    def get_all_simple_products(self):
        """Get all simple products"""
        session = self.get_session()
        try:
            return session.query(SimpleProduct).all()
        except Exception as e:
            print(f"Error getting all simple products: {e}")
            return []
        finally:
            session.close()

    def get_simple_product_count(self):
        """Get count of simple products"""
        session = self.get_session()
        try:
            return session.query(SimpleProduct).count()
        except Exception as e:
            print(f"Error getting simple product count: {e}")
            return 0
        finally:
            session.close()

    def get_product_price(self, store: str, id: int) -> float:
        """Get the current price of a product, returns None if not found"""
        session = self.get_session()
        try:
            product = session.query(SimpleProduct).filter_by(
                store=store, id=id).first()
            return product.price if product else None
        except Exception as e:
            print(f"Error getting price for {store}-{id}: {e}")
            return None
        finally:
            session.close()


# Mock database (both simple and complex products)
class MockDatabase:
    def __init__(self, db_name: str = "mock", echo: bool = False):
        self.db_name = db_name
        self.engine = create_engine(f"sqlite:///{db_name}.db", echo=echo)
        self.Session = sessionmaker(bind=self.engine)
        self._setup_database()

    def _setup_database(self):
        """Setup mock database with both simple_products and products tables"""
        Base.metadata.create_all(
            self.engine, tables=[
                SimpleProduct.__table__, ComplexProduct.__table__]
        )

    def get_session(self):
        """Get a new database session"""
        return self.Session()

    def close_engine(self):
        """Close the database engine"""
        self.engine.dispose()

    def clear_data(self):
        """Clear all data from both tables"""
        session = self.get_session()
        try:
            session.query(SimpleProduct).delete()
            session.query(ComplexProduct).delete()
            session.commit()
            print(f"Cleared all data from {self.db_name} database")
        except Exception as e:
            session.rollback()
            print(f"Error clearing data from {self.db_name}: {e}")
        finally:
            session.close()

    def upsert_simple_product(self, store: str, id: int, name: str, price: float):
        """Insert or update a simple product"""
        session = self.get_session()
        try:
            existing = (
                session.query(SimpleProduct).filter_by(
                    store=store, id=id).first()
            )
            if existing:
                existing.name = name  # Add this line
                existing.price = price
                session.commit()
                print(f"Updated simple product: {
                      store}-{id} '{name}' price to {price}")
                return existing
            else:
                product = SimpleProduct(
                    store=store, id=id, name=name, price=price
                )  # Add name parameter
                session.add(product)
                session.commit()
                print(f"Added new simple product: {store}-{id} '{name}'")
                return product
        except Exception as e:
            session.rollback()
            print(f"Error upserting simple product {store}-{id}: {e}")
            return None
        finally:
            session.close()

    def upsert_complex_product(
        self, store: str, id: int, name: str, price: float, details: dict
    ):
        """Insert or update a complex product"""
        session = self.get_session()
        try:
            existing = (
                session.query(ComplexProduct).filter_by(
                    store=store, id=id).first()
            )
            if existing:
                existing.name = name  # Add this line
                existing.price = price
                existing.details = details
                session.commit()
                print(f"Updated complex product: {store}-{id} '{name}'")
                return existing
            else:
                product = ComplexProduct(
                    store=store,
                    id=id,
                    name=name,  # Add name parameter
                    price=price,
                    details=details,
                )
                session.add(product)
                session.commit()
                print(f"Added new complex product: {store}-{id} '{name}'")
                return product
        except Exception as e:
            session.rollback()
            print(f"Error upserting complex product {store}-{id}: {e}")
            return None
        finally:
            session.close()

    def get_simple_products_by_store(self, store: str):
        """Get all simple products for a store"""
        session = self.get_session()
        try:
            return session.query(SimpleProduct).filter_by(store=store).all()
        except Exception as e:
            print(f"Error getting simple products for store {store}: {e}")
            return []
        finally:
            session.close()

    def get_complex_products_by_store(self, store: str):
        """Get all complex products for a store"""
        session = self.get_session()
        try:
            return session.query(ComplexProduct).filter_by(store=store).all()
        except Exception as e:
            print(f"Error getting complex products for store {store}: {e}")
            return []
        finally:
            session.close()

    def get_all_simple_products(self):
        """Get all simple products"""
        session = self.get_session()
        try:
            return session.query(SimpleProduct).all()
        except Exception as e:
            print(f"Error getting all simple products: {e}")
            return []
        finally:
            session.close()

    def get_all_complex_products(self):
        """Get all complex products"""
        session = self.get_session()
        try:
            return session.query(ComplexProduct).all()
        except Exception as e:
            print(f"Error getting all complex products: {e}")
            return []
        finally:
            session.close()

    def get_simple_product_count(self):
        """Get count of simple products"""
        session = self.get_session()
        try:
            return session.query(SimpleProduct).count()
        except Exception as e:
            print(f"Error getting simple product count: {e}")
            return 0
        finally:
            session.close()

    def get_complex_product_count(self):
        """Get count of complex products"""
        session = self.get_session()
        try:
            return session.query(ComplexProduct).count()
        except Exception as e:
            print(f"Error getting complex product count: {e}")
            return 0
        finally:
            session.close()

    def search_products_by_detail(self, key: str, value: str):
        """Search complex products by a detail key-value pair"""
        session = self.get_session()
        try:
            return (
                session.query(ComplexProduct)
                .filter(ComplexProduct.details[key].astext == value)
                .all()
            )
        except Exception as e:
            print(f"Error searching products by detail {key}={value}: {e}")
            return []
        finally:
            session.close()


# Factory function
def create_database(db_type: str, name: str = "", echo: bool = False):
    """Factory function to create database instances"""
    if name == "":
        name = db_type

    if db_type.lower() == "main":
        return MainDatabase(name, echo)
    elif db_type.lower() == "mock":
        return MockDatabase(name, echo)
    else:
        raise ValueError(f"Unknown database type: {
                         db_type}. Use 'main' or 'mock'.")


def price_update_to_simple_product(price_update: PriceUpdates) -> SimpleProduct:
    """Convert PriceUpdates pydantic model to SimpleProduct SQLAlchemy model"""
    return SimpleProduct(
        store=price_update.store.value,
        id=price_update.store_product_id,
        name=price_update.product_name,
        price=price_update.price,
    )


def product_info_to_complex_product(product_info: ProductInfo) -> ComplexProduct:
    """Convert ProductInfo pydantic model to ComplexProduct SQLAlchemy model"""
    return ComplexProduct(
        store=product_info.store.value,
        id=product_info.store_product_id,
        name=product_info.product_name,
        price=product_info.price,
        details=product_info.details,
    )


def simple_product_to_price_update(simple_product: SimpleProduct) -> PriceUpdates:
    """Convert SimpleProduct SQLAlchemy model to PriceUpdates pydantic model"""
    return PriceUpdates(
        store_product_id=simple_product.id,
        store=Store(simple_product.store),
        product_name=simple_product.name,
        price=simple_product.price,
    )


def complex_product_to_product_info(complex_product: ComplexProduct) -> ProductInfo:
    """Convert ComplexProduct SQLAlchemy model to ProductInfo pydantic model"""
    return ProductInfo(
        store_product_id=complex_product.id,
        store=Store(complex_product.store),
        product_name=complex_product.name,
        price=complex_product.price,
        details=complex_product.details,
    )


def test_databases():
    """Test both MainDatabase and MockDatabase functionality"""
    print("=== TESTING DATABASES ===\n")

    # Test MainDatabase
    print("1. Testing MainDatabase:")
    main_db = MainDatabase("test_main")
    main_db.clear_data()

    # Test adding products
    result1 = main_db.add_simple_product("ALDI", 1, "iPhone 15", 799.99)
    result2 = main_db.add_simple_product("Coles", 1, "Samsung Galaxy", 699.99)
    result3 = main_db.add_simple_product(
        "ALDI", 1, "iPhone 15", 849.99)  # Duplicate

    print(f"Added iPhone to ALDI: {result1}")
    print(f"Added Samsung to Coles: {result2}")
    print(f"Added duplicate iPhone to ALDI: {result3}")

    # Test price checking
    price_updated1 = main_db.check_price("ALDI", 1, 799.99)  # Same price
    price_updated2 = main_db.check_price("ALDI", 1, 829.99)  # Different price

    print(f"Price update (same): {price_updated1}")
    print(f"Price update (different): {price_updated2}")

    # Show all products
    products = main_db.get_all_simple_products()
    print(f"Total products in MainDB: {len(products)}")
    for product in products:
        print(f"  {product}")

    print("\n" + "-" * 50 + "\n")

    # Test MockDatabase
    print("2. Testing MockDatabase:")
    mock_db = MockDatabase("test_mock")
    mock_db.clear_data()

    # Test upsert methods
    mock_db.upsert_simple_product("Woolworths", 1, "MacBook Pro", 1999.99)
    mock_db.upsert_complex_product(
        "Woolworths",
        1,
        "MacBook Pro",
        1999.99,
        {"category": "laptop", "brand": "Apple", "memory": "16GB"},
    )

    # Update existing
    mock_db.upsert_simple_product(
        "Woolworths", 1, "MacBook Pro M3", 2199.99
    )  # Price change
    mock_db.upsert_complex_product(
        "Woolworths",
        1,
        "MacBook Pro M3",
        2199.99,
        {"category": "laptop", "brand": "Apple", "memory": "16GB", "chip": "M3"},
    )

    # Add more products
    mock_db.upsert_simple_product("IGA", 2, "Dell XPS", 1299.99)
    mock_db.upsert_complex_product(
        "IGA",
        2,
        "Dell XPS",
        1299.99,
        {"category": "laptop", "brand": "Dell", "memory": "32GB"},
    )

    # Show results
    simple_products = mock_db.get_all_simple_products()
    complex_products = mock_db.get_all_complex_products()

    print(f"Simple products in MockDB: {len(simple_products)}")
    for product in simple_products:
        print(f"  {product}")

    print(f"\nComplex products in MockDB: {len(complex_products)}")
    for product in complex_products:
        print(f"  {product} - Details: {product.details}")

    # Test search functionality
    laptop_products = mock_db.search_products_by_detail("category", "laptop")
    print(f"\nLaptop products found: {len(laptop_products)}")

    print("\n=== ALL TESTS COMPLETED ===")


def test_helper_functions():
    """Test the conversion helper functions between Pydantic and SQLAlchemy models"""
    print("=== TESTING HELPER FUNCTIONS ===\n")

    # Test data
    test_store = Store.ALDI  # Using your Australian store enum
    test_id = 123
    test_name = "iPhone 15 Pro"
    test_price = 999.99
    test_details = {"brand": "Apple", "color": "Black", "storage": "256GB"}

    print("1. Testing PriceUpdates <-> SimpleProduct conversion:")

    # Create PriceUpdates pydantic model
    price_update = PriceUpdates(
        store_product_id=test_id,
        store=test_store,
        product_name=test_name,
        price=test_price,
    )
    print(f"Original PriceUpdates: {price_update}")

    # Convert to SQLAlchemy SimpleProduct
    simple_product = price_update_to_simple_product(price_update)
    print(f"Converted to SimpleProduct: {simple_product}")
    print(f"  store: {simple_product.store} (type: {
          type(simple_product.store)})")
    print(f"  id: {simple_product.id} (type: {type(simple_product.id)})")
    print(f"  name: {simple_product.name} (type: {type(simple_product.name)})")
    print(f"  price: {simple_product.price} (type: {
          type(simple_product.price)})")

    # Convert back to PriceUpdates
    converted_back = simple_product_to_price_update(simple_product)
    print(f"Converted back to PriceUpdates: {converted_back}")

    # Verify round-trip conversion
    assert price_update.store_product_id == converted_back.store_product_id
    assert price_update.store == converted_back.store
    assert price_update.product_name == converted_back.product_name
    assert price_update.price == converted_back.price
    print("✓ Round-trip conversion successful!\n")

    print("2. Testing ProductInfo <-> ComplexProduct conversion:")

    # Create ProductInfo pydantic model
    product_info = ProductInfo(
        store_product_id=test_id,
        store=test_store,
        product_name=test_name,
        price=test_price,
        details=test_details,
    )
    print(f"Original ProductInfo: {product_info}")

    # Convert to SQLAlchemy ComplexProduct
    complex_product = product_info_to_complex_product(product_info)
    print(f"Converted to ComplexProduct: {complex_product}")
    print(f"  store: {complex_product.store} (type: {
          type(complex_product.store)})")
    print(f"  id: {complex_product.id} (type: {type(complex_product.id)})")
    print(f"  name: {complex_product.name} (type: {
          type(complex_product.name)})")
    print(f"  price: {complex_product.price} (type: {
          type(complex_product.price)})")
    print(
        f"  details: {complex_product.details} (type: {
            type(complex_product.details)})"
    )

    # Convert back to ProductInfo
    converted_back_complex = complex_product_to_product_info(complex_product)
    print(f"Converted back to ProductInfo: {converted_back_complex}")

    # Verify round-trip conversion
    assert product_info.store_product_id == converted_back_complex.store_product_id
    assert product_info.store == converted_back_complex.store
    assert product_info.product_name == converted_back_complex.product_name
    assert product_info.price == converted_back_complex.price
    assert product_info.details == converted_back_complex.details
    print("✓ Round-trip conversion successful!\n")

    print("3. Testing type conversions:")

    # Test enum to string conversion
    assert simple_product.store == test_store.value
    assert complex_product.store == test_store.value
    print("✓ Enum to string conversion works")

    # Test string to enum conversion
    assert converted_back.store == test_store
    assert converted_back_complex.store == test_store
    print("✓ String to enum conversion works")

    # Test price type consistency
    assert isinstance(simple_product.price, float)
    assert isinstance(complex_product.price, float)
    assert isinstance(converted_back.price, float)
    assert isinstance(converted_back_complex.price, float)
    print("✓ Price remains float type throughout conversions")

    print("\n=== ALL HELPER FUNCTION TESTS PASSED ===")


if __name__ == "__main__":
    test_databases()
    test_helper_functions()
