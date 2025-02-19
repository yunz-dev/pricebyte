// =============================================================================
// API ROUTE: app/api/products/[id]/route.ts
// =============================================================================

import { NextRequest, NextResponse } from 'next/server';

// Type definitions
interface PriceHistoryEntry {
  startDate: string;
  endDate: string | null;
  price: number;
}

interface StoreProduct {
  storeProductId: number;
  store: string;
  standardPrice: number;
  productUrl: string | null;
  priceHistory: PriceHistoryEntry[];
}

interface NutritionInfo {
  perServing: Record<string, string>;
  per100g: Record<string, string>;
}

interface Product {
  productId: number;
  name: string;
  brand: string;
  category: string;
  size: number;
  unit: string;
  imageUrl: string;
  description: string;
  nutrition: NutritionInfo;
  storeProducts: StoreProduct[];
}

// API Response types
interface ApiPriceHistory {
  price: number;
  start_date: string;
  end_date: string | null;
}

interface ApiStoreProduct {
  id: number;
  store: string;
  store_product_id: string;
  store_name: string;
  current_price: number;
  availability: boolean;
  product_url: string | null;
  raw_details: {
    brand: string;
    category: string;
    description: string;
    weight: string;
    ingredients: string;
    nutrition_facts: Record<string, any>;
    barcode: string;
    availability: string;
    rating: number;
  };
  created_at: string;
  updated_at: string;
  price_history: ApiPriceHistory[];
}

interface ApiProduct {
  id: number;
  name: string;
  brand: string;
  category: string;
  size: string;
  unit: string;
  image_url: string;
  description: string;
  created_at: string;
  updated_at: string;
  store_products: ApiStoreProduct[];
}

// Helper functions
function parseSize(sizeStr: string): number {
  const match = sizeStr.match(/(\d+(?:\.\d+)?)/);
  return match ? parseFloat(match[1]) : 0;
}

function convertNutritionFacts(nutritionFacts: Record<string, any>): NutritionInfo {
  const defaultNutrition: NutritionInfo = {
    perServing: {},
    per100g: {}
  };

  if (nutritionFacts) {
    const perServing: Record<string, string> = {};

    if (nutritionFacts.calories_per_serving) {
      perServing['Energy (Cal)'] = `${nutritionFacts.calories_per_serving} Cal`;
    }
    if (nutritionFacts.protein) {
      perServing['Protein'] = nutritionFacts.protein;
    }
    if (nutritionFacts.fat) {
      perServing['Fat - Total'] = nutritionFacts.fat;
    }
    if (nutritionFacts.sodium) {
      perServing['Sodium'] = nutritionFacts.sodium;
    }

    defaultNutrition.perServing = perServing;
    defaultNutrition.per100g = { ...perServing };
  }

  return defaultNutrition;
}

function convertPriceHistory(apiPriceHistory: ApiPriceHistory[]): PriceHistoryEntry[] {
  return apiPriceHistory.map(entry => ({
    startDate: new Date(entry.start_date).toISOString(),
    endDate: entry.end_date ? new Date(entry.end_date).toISOString() : new Date().toISOString(),
    price: entry.price
  }));
}

function convertStoreProducts(apiStoreProducts: ApiStoreProduct[]): StoreProduct[] {
  return apiStoreProducts.map(storeProduct => ({
    storeProductId: storeProduct.id,
    store: capitalizeFirstLetter(storeProduct.store),
    standardPrice: storeProduct.current_price,
    productUrl: storeProduct.product_url,
    priceHistory: convertPriceHistory(storeProduct.price_history)
  }));
}

function capitalizeFirstLetter(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// API Route Handler
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const resolvedParams = await params;
    const productId = parseInt(resolvedParams.id);

    if (isNaN(productId)) {
      return NextResponse.json(
        { error: 'Invalid product ID' },
        { status: 400 }
      );
    }

    // Fetch from your external API
    const externalApiUrl = process.env.EXTERNAL_API_URL || 'http://localhost:8000';
    const response = await fetch(`${externalApiUrl}/api/products/${productId}`, {
      method: 'GET',
      headers: {
        'accept': 'application/json',
      },
    });

    if (!response.ok) {
      if (response.status === 404) {
        return NextResponse.json(
          { error: 'Product not found' },
          { status: 404 }
        );
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const apiData: ApiProduct = await response.json();
    console.log(apiData);

    // Convert API data to Product format
    const product: Product = {
      productId: apiData.id,
      name: apiData.name,
      brand: apiData.brand,
      category: capitalizeFirstLetter(apiData.category),
      size: parseSize(apiData.size),
      unit: apiData.unit,
      imageUrl: apiData.image_url || '',
      description: apiData.description,
      nutrition: apiData.store_products[0]?.raw_details?.nutrition_facts
        ? convertNutritionFacts(apiData.store_products[0].raw_details.nutrition_facts)
        : { perServing: {}, per100g: {} },
      storeProducts: convertStoreProducts(apiData.store_products)
    };

    return NextResponse.json(product);

  } catch (error) {
    console.error('Error fetching product data:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
