#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Product
from matcher_test import TestProductMatcher
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_product_by_id(db, product_id):
    """Get a product by ID for easy testing"""
    return db.query(Product).filter(Product.id == product_id).first()

def list_products(db, limit=20):
    """List products for reference"""
    products = db.query(Product).limit(limit).all()
    print(f"\n=== Product Database (showing first {limit}) ===")
    for p in products:
        print(f"ID: {p.id:3d} | {p.brand:15s} | {p.name:40s} | {p.category:15s} | {p.size:10s}")

def test_single_match(matcher, name, brand, category, size):
    """Test a single product match and show detailed results"""
    print(f"\n=== Testing Match ===")
    print(f"Input: {brand} - {name} ({category}, {size})")
    
    # Get top matches with scores
    matches = matcher.find_all_matches_with_scores(name, brand, category, size, limit=10)
    
    print(f"\n=== Top 10 Matches (Threshold: {matcher.threshold}) ===")
    for i, (product, score) in enumerate(matches, 1):
        status = "✓ MATCH" if score >= matcher.threshold else "✗ No match"
        print(f"{i:2d}. {score:.3f} {status} | {product.brand:15s} | {product.name:40s} | {product.category:15s} | {product.size:10s}")
    
    # Show detailed breakdown for top match if exists
    if matches:
        top_product, top_score = matches[0]
        print(f"\n=== Score Breakdown for Top Match ===")
        breakdown = matcher.get_score_breakdown(
            name, brand, category, size,
            top_product.name, top_product.brand, top_product.category, top_product.size
        )
        
        print(f"Name:     {breakdown['name_similarity']:.3f} × {matcher.name_weight:.2f} = {breakdown['name_weighted']:.3f}")
        print(f"Brand:    {breakdown['brand_similarity']:.3f} × {matcher.brand_weight:.2f} = {breakdown['brand_weighted']:.3f}")
        print(f"Category: {breakdown['category_similarity']:.3f} × {matcher.category_weight:.2f} = {breakdown['category_weighted']:.3f}")
        print(f"Size:     {breakdown['size_similarity']:.3f} × {matcher.size_weight:.2f} = {breakdown['size_weighted']:.3f}")
        print(f"Total:    {breakdown['total_score']:.3f}")
        print(f"\nCleaned names: '{breakdown['name_clean1']}' vs '{breakdown['name_clean2']}'")
        print(f"Cleaned brands: '{breakdown['brand_clean1']}' vs '{breakdown['brand_clean2']}'")

def compare_products(matcher, id1, id2, db):
    """Compare two specific products by ID"""
    p1 = get_product_by_id(db, id1)
    p2 = get_product_by_id(db, id2)
    
    if not p1 or not p2:
        print("One or both products not found!")
        return
    
    print(f"\n=== Comparing Products ===")
    print(f"Product 1: {p1.brand} - {p1.name} ({p1.category}, {p1.size})")
    print(f"Product 2: {p2.brand} - {p2.name} ({p2.category}, {p2.size})")
    
    breakdown = matcher.get_score_breakdown(
        p1.name, p1.brand, p1.category, p1.size,
        p2.name, p2.brand, p2.category, p2.size
    )
    
    print(f"\n=== Score Breakdown ===")
    print(f"Name:     {breakdown['name_similarity']:.3f} × {matcher.name_weight:.2f} = {breakdown['name_weighted']:.3f}")
    print(f"Brand:    {breakdown['brand_similarity']:.3f} × {matcher.brand_weight:.2f} = {breakdown['brand_weighted']:.3f}")
    print(f"Category: {breakdown['category_similarity']:.3f} × {matcher.category_weight:.2f} = {breakdown['category_weighted']:.3f}")
    print(f"Size:     {breakdown['size_similarity']:.3f} × {matcher.size_weight:.2f} = {breakdown['size_weighted']:.3f}")
    print(f"Total:    {breakdown['total_score']:.3f}")
    
    status = "✓ WOULD MATCH" if breakdown['total_score'] >= matcher.threshold else "✗ Would not match"
    print(f"\n{status} (threshold: {matcher.threshold})")

def main():
    db = SessionLocal()
    
    # Default settings - size matters for exact products
    threshold = 0.91
    name_weight = 0.5
    brand_weight = 0.25
    category_weight = 0.05
    size_weight = 0.2
    
    matcher = TestProductMatcher(db, threshold, name_weight, brand_weight, category_weight, size_weight)
    
    print("=== Product Matcher Test Interface ===")
    print("Commands:")
    print("  list                           - List products")
    print("  test <name> <brand> <cat> <size> - Test matching")
    print("  compare <id1> <id2>            - Compare two products by ID")
    print("  settings                       - Show current settings")
    print("  set threshold <value>          - Set threshold (0.0-1.0)")
    print("  set weights <name> <brand> <cat> <size> - Set weights")
    print("  quit                           - Exit")
    
    while True:
        try:
            cmd = input("\n> ").strip().split()
            if not cmd:
                continue
                
            if cmd[0] == "quit":
                break
            elif cmd[0] == "list":
                list_products(db)
            elif cmd[0] == "test" and len(cmd) == 5:
                test_single_match(matcher, cmd[1], cmd[2], cmd[3], cmd[4])
            elif cmd[0] == "compare" and len(cmd) == 3:
                compare_products(matcher, int(cmd[1]), int(cmd[2]), db)
            elif cmd[0] == "settings":
                print(f"\nCurrent Settings:")
                print(f"  Threshold: {matcher.threshold}")
                print(f"  Weights: name={matcher.name_weight}, brand={matcher.brand_weight}, category={matcher.category_weight}, size={matcher.size_weight}")
            elif cmd[0] == "set" and cmd[1] == "threshold" and len(cmd) == 3:
                matcher.threshold = float(cmd[2])
                print(f"Threshold set to {matcher.threshold}")
            elif cmd[0] == "set" and cmd[1] == "weights" and len(cmd) == 6:
                matcher.name_weight = float(cmd[2])
                matcher.brand_weight = float(cmd[3])
                matcher.category_weight = float(cmd[4])
                matcher.size_weight = float(cmd[5])
                print(f"Weights set to: name={matcher.name_weight}, brand={matcher.brand_weight}, category={matcher.category_weight}, size={matcher.size_weight}")
            else:
                print("Invalid command. Use 'quit' to exit.")
                
        except (ValueError, IndexError):
            print("Invalid input format. Use 'quit' to exit.")
        except KeyboardInterrupt:
            break
    
    db.close()
    print("\nGoodbye!")

if __name__ == "__main__":
    main()