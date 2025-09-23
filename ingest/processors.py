from typing import Dict, Any, Optional, Tuple
import re

class BaseProcessor:
    def process(self, data: Dict[str, Any]) -> Tuple[str, str, str, str, str, str]:
        raise NotImplementedError

class ColesProcessor(BaseProcessor):
    def process(self, data: Dict[str, Any]) -> Tuple[str, str, str, str, str, str]:
        name = data.get("name", "")
        brand = data.get("brand", "")
        
        size = data.get("size", "")
        
        description = data.get("description", "")
        
        category = ""
        if "merchandiseHeir" in data:
            category = data["merchandiseHeir"].get("category", "")
        elif "onlineHeirs" in data and data["onlineHeirs"]:
            category = data["onlineHeirs"][0].get("category", "")
        
        image_url = ""
        if "images" in data and data["images"]:
            image_url = data["images"][0].get("full", {}).get("path", "")
            if image_url and not image_url.startswith("http"):
                image_url = f"https://shop.coles.com.au{image_url}"
        
        unit = self._extract_unit(size)
        
        return name, brand, category, size, unit, image_url, description
    
    def _extract_unit(self, size: str) -> str:
        if not size:
            return ""
        
        size_lower = size.lower()
        if "ml" in size_lower:
            return "ml"
        elif "kg" in size_lower:
            return "kg"
        elif "g" in size_lower and "kg" not in size_lower:
            return "g"
        elif "l" in size_lower and "ml" not in size_lower:
            return "l"
        elif "pack" in size_lower or "pk" in size_lower:
            return "pack"
        else:
            return ""

class AldiProcessor(BaseProcessor):
    def process(self, data: Dict[str, Any]) -> Tuple[str, str, str, str, str, str]:
        name = data.get("name", "")
        brand = data.get("brand", "")
        category = data.get("category", "")
        
        size = data.get("weight", "")
        
        description = data.get("description", "")
        
        image_url = data.get("image_url", "")
        
        unit = self._extract_unit(size)
        
        return name, brand, category, size, unit, image_url, description
    
    def _extract_unit(self, size: str) -> str:
        if not size:
            return ""
        
        size_lower = size.lower()
        if "ml" in size_lower:
            return "ml"
        elif "kg" in size_lower:
            return "kg"
        elif "g" in size_lower and "kg" not in size_lower:
            return "g"
        elif "l" in size_lower and "ml" not in size_lower:
            return "l"
        else:
            return ""

class WoolworthsProcessor(BaseProcessor):
    def process(self, data: Dict[str, Any]) -> Tuple[str, str, str, str, str, str]:
        name = data.get("name", "")
        brand = data.get("brand", "")
        category = data.get("category", "")
        size = data.get("size", "")
        description = data.get("description", "")
        image_url = data.get("image_url", "")
        unit = self._extract_unit(size)
        
        return name, brand, category, size, unit, image_url, description
    
    def _extract_unit(self, size: str) -> str:
        if not size:
            return ""
        
        size_lower = size.lower()
        if "ml" in size_lower:
            return "ml"
        elif "kg" in size_lower:
            return "kg"
        elif "g" in size_lower and "kg" not in size_lower:
            return "g"
        elif "l" in size_lower and "ml" not in size_lower:
            return "l"
        else:
            return ""

class ProcessorFactory:
    _processors = {
        "coles": ColesProcessor(),
        "aldi": AldiProcessor(),
        "woolworths": WoolworthsProcessor()
    }
    
    @classmethod
    def get_processor(cls, store: str) -> BaseProcessor:
        processor = cls._processors.get(store.lower())
        if not processor:
            raise ValueError(f"No processor found for store: {store}")
        return processor
    
    @classmethod
    def normalize_category(cls, category: str) -> str:
        if not category:
            return ""
        
        category_lower = category.lower()
        
        category_mapping = {
            "meat": "meat",
            "seafood": "seafood", 
            "prepackaged seafood": "seafood",
            "dairy": "dairy",
            "fruits": "produce",
            "vegetables": "produce", 
            "produce": "produce",
            "bakery": "bakery",
            "frozen": "frozen",
            "pantry": "pantry",
            "beverages": "beverages",
            "snacks": "snacks",
            "health": "health"
        }
        
        for key, normalized in category_mapping.items():
            if key in category_lower:
                return normalized
        
        return category.title()