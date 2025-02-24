from fuzzywuzzy import fuzz
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from models import Product
from config import SIMILARITY_THRESHOLD
import re


class ProductMatcher:
    def __init__(self, db: Session, threshold: float = 0.91):
        self.db = db
        self.threshold = threshold

    def find_matching_product(
        self, name: str, brand: str, category: str, size: str
    ) -> Optional[Product]:
        candidates = self._get_candidates()

        if not candidates:
            return None

        best_match = None
        best_score = 0

        for candidate in candidates:
            score = self._calculate_similarity_score(
                name, brand, category, size, candidate.name, candidate.brand, candidate.category, candidate.size
            )

            if score > best_score and score >= self.threshold:
                best_score = score
                best_match = candidate

        return best_match

    def search_products_by_name(self, search_name: str, limit: int = 10) -> List[Tuple[Product, float]]:
        """Search for products by name similarity, returning top matches with scores"""
        candidates = self._get_candidates()

        if not candidates:
            return []

        scored_products = []
        search_name_clean = self._clean_text(search_name)

        for candidate in candidates:
            candidate_name_clean = self._clean_text(candidate.name)
            
            # Use token_sort_ratio for name matching (same as in matching logic)
            name_similarity = fuzz.token_sort_ratio(search_name_clean, candidate_name_clean) / 100.0
            
            scored_products.append((candidate, name_similarity))

        # Sort by similarity score descending and return top matches
        scored_products.sort(key=lambda x: x[1], reverse=True)
        return scored_products[:limit]

    def _get_candidates(self) -> List[Product]:
        return self.db.query(Product).all()

    def _calculate_similarity_score(
        self, name1: str, brand1: str, category1: str, size1: str, name2: str, brand2: str, category2: str, size2: str
    ) -> float:
        name1_clean = self._clean_text(name1)
        name2_clean = self._clean_text(name2)

        name_similarity = fuzz.token_sort_ratio(name1_clean, name2_clean) / 100.0

        # Optimized weights - size matters for exact products
        name_weight = 0.5
        brand_weight = 0.25
        category_weight = 0.05
        size_weight = 0.2

        # Brand fuzzy matching
        brand_similarity = 1.0
        if brand1 and brand2:
            brand1_clean = self._clean_brand(brand1)
            brand2_clean = self._clean_brand(brand2)
            brand_similarity = fuzz.token_sort_ratio(brand1_clean, brand2_clean) / 100.0
        elif brand1 or brand2:
            brand_similarity = 0.5

        # Category fuzzy matching
        category_similarity = 1.0
        if category1 and category2:
            category_similarity = fuzz.token_sort_ratio(category1.lower(), category2.lower()) / 100.0
        elif category1 or category2:
            category_similarity = 0.6

        # Size comparison
        size_similarity = 1.0
        if size1 and size2:
            size_similarity = self._compare_sizes(size1, size2)
        elif size1 or size2:
            size_similarity = 0.7

        total_score = (
            name_weight * name_similarity
            + brand_weight * brand_similarity
            + category_weight * category_similarity
            + size_weight * size_similarity
        )

        return total_score

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""

        text = text.lower()

        # Remove size units first
        text = re.sub(r"\b\d+g\b|\b\d+kg\b|\b\d+ml\b|\b\d+l\b", "", text)

        # Remove ALL non-alphanumeric characters (spaces, punctuation, etc.)
        text = re.sub(r"[^a-z0-9]", "", text)

        return text

    def _clean_brand(self, brand: str) -> str:
        if not brand:
            return ""
        
        # Remove ALL non-alphanumeric characters (spaces, punctuation, dashes, etc.)
        brand = brand.lower()
        brand = re.sub(r"[^a-z0-9]", "", brand)
        
        return brand

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
                    ratio = min(normalized1, normalized2) / max(
                        normalized1, normalized2
                    )
                    return ratio

        return fuzz.ratio(size1_clean, size2_clean) / 100.0

    def _extract_number(self, text: str) -> Optional[float]:
        match = re.search(r"(\d+(?:\.\d+)?)", text)
        if match:
            return float(match.group(1))
        return None

    def _extract_unit(self, text: str) -> str:
        if "kg" in text:
            return "kg"
        elif "g" in text and "kg" not in text:
            return "g"
        elif "l" in text and "ml" not in text:
            return "l"
        elif "ml" in text:
            return "ml"
        elif "pack" in text or "pk" in text:
            return "pack"
        return ""

    def _are_compatible_units(self, unit1: str, unit2: str) -> bool:
        weight_units = {"g", "kg"}
        volume_units = {"ml", "l"}

        return (unit1 in weight_units and unit2 in weight_units) or (
            unit1 in volume_units and unit2 in volume_units
        )

    def _normalize_to_grams(self, value: float, unit: str) -> Optional[float]:
        if unit == "g":
            return value
        elif unit == "kg":
            return value * 1000
        elif unit == "ml":
            return value
        elif unit == "l":
            return value * 1000
        return None

