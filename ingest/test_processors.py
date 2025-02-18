import pytest
from processors import ColesProcessor, AldiProcessor, WoolworthsProcessor, ProcessorFactory

class TestColesProcessor:
    def setup_method(self):
        self.processor = ColesProcessor()
    
    def test_process_complete_data(self):
        data = {
            "name": "Japanese Infusion Salmon Portion",
            "brand": "Huon",
            "size": "200g",
            "description": "HUON JAPANESE FUSION SALMON 200G",
            "merchandiseHeir": {
                "category": "PREPACKAGED SEAFOOD"
            },
            "images": [
                {
                    "full": {
                        "path": "/wcsstore/Coles-CAS/images/8/9/0/8909349.jpg"
                    }
                }
            ]
        }
        
        name, brand, category, size, unit, image_url, description = self.processor.process(data)
        
        assert name == "Japanese Infusion Salmon Portion"
        assert brand == "Huon"
        assert category == "PREPACKAGED SEAFOOD"
        assert size == "200g"
        assert unit == "g"
        assert image_url == "https://shop.coles.com.au/wcsstore/Coles-CAS/images/8/9/0/8909349.jpg"
        assert description == "HUON JAPANESE FUSION SALMON 200G"
    
    def test_process_online_heirs_category(self):
        data = {
            "name": "Test Product",
            "onlineHeirs": [
                {
                    "category": "World Foods"
                }
            ]
        }
        
        name, brand, category, size, unit, image_url, description = self.processor.process(data)
        
        assert category == "World Foods"
    
    def test_extract_unit_kg(self):
        assert self.processor._extract_unit("2kg") == "kg"
        assert self.processor._extract_unit("1.5kg") == "kg"
    
    def test_extract_unit_grams(self):
        assert self.processor._extract_unit("500g") == "g"
        assert self.processor._extract_unit("200g") == "g"
    
    def test_extract_unit_liters(self):
        assert self.processor._extract_unit("1L") == "l"
        assert self.processor._extract_unit("2l") == "l"
    
    def test_extract_unit_milliliters(self):
        assert self.processor._extract_unit("500ml") == "ml"
        assert self.processor._extract_unit("250ML") == "ml"
    
    def test_extract_unit_pack(self):
        assert self.processor._extract_unit("6 pack") == "pack"
        assert self.processor._extract_unit("12pk") == "pack"

class TestAldiProcessor:
    def setup_method(self):
        self.processor = AldiProcessor()
    
    def test_process_complete_data(self):
        data = {
            "name": "Simply Nature Almond Milk",
            "brand": "Simply Nature",
            "category": "Dairy",
            "weight": "1L",
            "description": "High quality almond milk",
            "image_url": "https://example.com/image.jpg"
        }
        
        name, brand, category, size, unit, image_url, description = self.processor.process(data)
        
        assert name == "Simply Nature Almond Milk"
        assert brand == "Simply Nature"
        assert category == "Dairy"
        assert size == "1L"
        assert unit == "l"
        assert image_url == "https://example.com/image.jpg"
        assert description == "High quality almond milk"
    
    def test_process_missing_fields(self):
        data = {
            "name": "Test Product"
        }
        
        name, brand, category, size, unit, image_url, description = self.processor.process(data)
        
        assert name == "Test Product"
        assert brand == ""
        assert category == ""
        assert size == ""
        assert unit == ""
        assert image_url == ""
        assert description == ""

class TestWoolworthsProcessor:
    def setup_method(self):
        self.processor = WoolworthsProcessor()
    
    def test_process_complete_data(self):
        data = {
            "name": "Woolworths Test Product",
            "brand": "Woolworths",
            "category": "Pantry",
            "size": "500g",
            "description": "Test description",
            "image_url": "https://example.com/woolworths.jpg"
        }
        
        name, brand, category, size, unit, image_url, description = self.processor.process(data)
        
        assert name == "Woolworths Test Product"
        assert brand == "Woolworths"
        assert category == "Pantry"
        assert size == "500g"
        assert unit == "g"
        assert image_url == "https://example.com/woolworths.jpg"
        assert description == "Test description"

class TestProcessorFactory:
    def test_get_coles_processor(self):
        processor = ProcessorFactory.get_processor("coles")
        assert isinstance(processor, ColesProcessor)
    
    def test_get_aldi_processor(self):
        processor = ProcessorFactory.get_processor("aldi")
        assert isinstance(processor, AldiProcessor)
    
    def test_get_woolworths_processor(self):
        processor = ProcessorFactory.get_processor("woolworths")
        assert isinstance(processor, WoolworthsProcessor)
    
    def test_invalid_store_raises_error(self):
        with pytest.raises(ValueError, match="No processor found for store"):
            ProcessorFactory.get_processor("invalid_store")
    
    def test_normalize_category_meat(self):
        assert ProcessorFactory.normalize_category("MEAT") == "meat"
        assert ProcessorFactory.normalize_category("Fresh Meat") == "meat"
    
    def test_normalize_category_seafood(self):
        assert ProcessorFactory.normalize_category("SEAFOOD") == "seafood"
        assert ProcessorFactory.normalize_category("PREPACKAGED SEAFOOD") == "seafood"
    
    def test_normalize_category_dairy(self):
        assert ProcessorFactory.normalize_category("DAIRY") == "dairy"
        assert ProcessorFactory.normalize_category("Dairy Products") == "dairy"
    
    def test_normalize_category_produce(self):
        assert ProcessorFactory.normalize_category("FRUITS") == "produce"
        assert ProcessorFactory.normalize_category("VEGETABLES") == "produce"
        assert ProcessorFactory.normalize_category("PRODUCE") == "produce"
    
    def test_normalize_category_unknown(self):
        assert ProcessorFactory.normalize_category("Unknown Category") == "Unknown Category"
        assert ProcessorFactory.normalize_category("") == ""