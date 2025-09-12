from sqlalchemy import JSON, Column, Float, Integer, String, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


# Table definitions
class SimpleProduct(Base):
    __tablename__ = "simple_products"

    store = Column(String, primary_key=True)
    id = Column(Integer, primary_key=True)
    price = Column(Float)

    def __repr__(self):
        return (
            f"<SimpleProduct(store='{self.store}', id={
                self.id}, price={self.price})>"
        )


class Product(Base):
    __tablename__ = "products"

    store = Column(String, primary_key=True)
    id = Column(Integer, primary_key=True)
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

    def add_simple_product(self, store: str, id: int, price: float) -> bool:
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
            product = SimpleProduct(store=store, id=id, price=price)
            session.add(product)
            session.commit()
            print(f"Added simple product: {store}-{id} with price {price}")
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
            self.engine, tables=[SimpleProduct.__table__, Product.__table__]
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
            session.query(Product).delete()
            session.commit()
            print(f"Cleared all data from {self.db_name} database")
        except Exception as e:
            session.rollback()
            print(f"Error clearing data from {self.db_name}: {e}")
        finally:
            session.close()

    def upsert_simple_product(self, store: str, id: int, price: float):
        """Insert or update a simple product"""
        session = self.get_session()
        try:
            existing = (
                session.query(SimpleProduct).filter_by(
                    store=store, id=id).first()
            )
            if existing:
                existing.price = price
                session.commit()
                print(f"Updated simple product: {store}-{id} price to {price}")
                return existing
            else:
                product = SimpleProduct(store=store, id=id, price=price)
                session.add(product)
                session.commit()
                print(f"Added new simple product: {store}-{id}")
                return product
        except Exception as e:
            session.rollback()
            print(f"Error upserting simple product {store}-{id}: {e}")
            return None
        finally:
            session.close()

    def upsert_complex_product(self, store: str, id: int, price: float, details: dict):
        """Insert or update a complex product"""
        session = self.get_session()
        try:
            existing = session.query(Product).filter_by(
                store=store, id=id).first()
            if existing:
                existing.price = price
                existing.details = details
                session.commit()
                print(f"Updated complex product: {store}-{id}")
                return existing
            else:
                product = Product(store=store, id=id,
                                  price=price, details=details)
                session.add(product)
                session.commit()
                print(f"Added new complex product: {store}-{id}")
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
            return session.query(Product).filter_by(store=store).all()
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
            return session.query(Product).all()
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
            return session.query(Product).count()
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
                session.query(Product)
                .filter(Product.details[key].astext == value)
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


if __name__ == "__main__":
    pass
