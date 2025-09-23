from fuzzywuzzy import fuzz
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from models import Product
from config import SIMILARITY_THRESHOLD
import re

class ProductMatcher:
    def __init__(self, db: Session, threshold: float = SIMILARITY_THRESHOLD):
        self.db = db
        self.threshold = threshold
    
    def find_matching_product(self, name: str, brand: str, category: str, size: str) -> Optional[Product]:
        candidates = self._get_candidates(category, brand)
        
        if not candidates:
            return None
        
        best_match = None
        best_score = 0
        
        for candidate in candidates:
            score = self._calculate_similarity_score(
                name, brand, size,
                candidate.name, candidate.brand, candidate.size
            )
            
            if score > best_score and score >= self.threshold:
                best_score = score
                best_match = candidate
        
        return best_match
    
    def _get_candidates(self, category: str, brand: str) -> List[Product]:
        query = self.db.query(Product)
        
        if category:
            query = query.filter(Product.category == category)
        
        if brand:
            query = query.filter(Product.brand == brand)
        
        return query.all()
    
    def _calculate_similarity_score(self, name1: str, brand1: str, size1: str,
                                  name2: str, brand2: str, size2: str) -> float:
        name1_clean = self._clean_text(name1)
        name2_clean = self._clean_text(name2)
        
        name_similarity = fuzz.token_sort_ratio(name1_clean, name2_clean) / 100.0
        
        brand_weight = 0.3
        name_weight = 0.5
        size_weight = 0.2
        
        brand_similarity = 1.0
        if brand1 and brand2:
            brand_similarity = fuzz.ratio(brand1.lower(), brand2.lower()) / 100.0
        elif brand1 or brand2:
            brand_similarity = 0.5
        
        size_similarity = 1.0
        if size1 and size2:
            size_similarity = self._compare_sizes(size1, size2)
        elif size1 or size2:
            size_similarity = 0.7
        
        total_score = (
            name_weight * name_similarity +
            brand_weight * brand_similarity +
            size_weight * size_similarity
        )
        
        return total_score
    
    def _clean_text(self, text: str) -> str:
        if not text:
            return ""
        
        text = text.lower()
        
        text = re.sub(r'\b\d+g\b|\b\d+kg\b|\b\d+ml\b|\b\d+l\b', '', text)
        
        text = re.sub(r'[^\w\s]', ' ', text)
        
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _compare_sizes(self, size1: str, size2: str) -> float:
        if not size1 or not size2:
            return 0.5
        
        size1_clean = size1.lower().strip()
        size2_clean = size2.lower().strip()
        
        if size1_clean == size2_clean:
            return 1.0
        
        num1 = self._extract_number(size1_clean)
        num2 = self._extract_number(size2_clean)
        
        if num1 and num2:
            unit1 = self._extract_unit(size1_clean)
            unit2 = self._extract_unit(size2_clean)
            
            if unit1 == unit2:
                ratio = min(num1, num2) / max(num1, num2)
                return ratio
            
            if self._are_compatible_units(unit1, unit2):
                normalized1 = self._normalize_to_grams(num1, unit1)
                normalized2 = self._normalize_to_grams(num2, unit2)
                
                if normalized1 and normalized2:
                    ratio = min(normalized1, normalized2) / max(normalized1, normalized2)
                    return ratio
        
        return fuzz.ratio(size1_clean, size2_clean) / 100.0
    
    def _extract_number(self, text: str) -> Optional[float]:
        match = re.search(r'(\d+(?:\.\d+)?)', text)
        if match:
            return float(match.group(1))
        return None
    
    def _extract_unit(self, text: str) -> str:
        if 'kg' in text:
            return 'kg'
        elif 'g' in text and 'kg' not in text:
            return 'g'
        elif 'l' in text and 'ml' not in text:
            return 'l'
        elif 'ml' in text:
            return 'ml'
        elif 'pack' in text or 'pk' in text:
            return 'pack'
        return ''
    
    def _are_compatible_units(self, unit1: str, unit2: str) -> bool:
        weight_units = {'g', 'kg'}
        volume_units = {'ml', 'l'}
        
        return (unit1 in weight_units and unit2 in weight_units) or \
               (unit1 in volume_units and unit2 in volume_units)
    
    def _normalize_to_grams(self, value: float, unit: str) -> Optional[float]:
        if unit == 'g':
            return value
        elif unit == 'kg':
            return value * 1000
        elif unit == 'ml':
            return value
        elif unit == 'l':
            return value * 1000
        return None