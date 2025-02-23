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
    nutrition?: {
      breakdown: Array<{
        title: string;
        nutrients: Array<{
          nutrient: string;
          value: string;
        }>;
      }>;
    };
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

// Nutrition conversion types
interface ColesNutritionBreakdown {
  title: string;
  nutrients: Array<{
    nutrient: string;
    value: string;
  }>;
}

interface ColesNutrition {
  breakdown: ColesNutritionBreakdown[];
}

// Helper functions
function parseSize(sizeStr: string): number {
  const match = sizeStr.match(/(\d+(?:\.\d+)?)/);
  return match ? parseFloat(match[1]) : 0;
}

function convertNutritionFacts(nutritionData: Record<string, any> | ColesNutrition): NutritionInfo {
  const defaultNutrition: NutritionInfo = {
    perServing: {},
    per100g: {}
  };

  if (!nutritionData) {
    return defaultNutrition;
  }

  // Check if it's Coles format (has breakdown array)
  if ('breakdown' in nutritionData && Array.isArray(nutritionData.breakdown)) {
    return convertColesNutrition(nutritionData as ColesNutrition);
  }

  // Handle original format (raw_details.nutrition_facts)
  return convertOriginalNutrition(nutritionData);
}

function convertColesNutrition(nutrition: ColesNutrition): NutritionInfo {
  const result: NutritionInfo = {
    perServing: {},
    per100g: {}
  };

  nutrition.breakdown.forEach(section => {
    const isPerServing = section.title.toLowerCase().includes('serving');
    const isPer100g = section.title.toLowerCase().includes('100g') || section.title.toLowerCase().includes('100ml');

    if (isPerServing || isPer100g) {
      const targetSection = isPerServing ? result.perServing : result.per100g;

      section.nutrients.forEach(nutrient => {
        let key = nutrient.nutrient;
        let value = nutrient.value;

        // Standardize some common nutrient names
        switch (key.toLowerCase()) {
          case 'energy':
            key = value.includes('kJ') ? 'Energy (kJ)' : 'Energy (Cal)';
            break;
          case 'fat - total':
            key = 'Fat - Total';
            break;
          case 'fat - saturated':
            key = 'Fat - Saturated';
            break;
          case 'sugars - total':
            key = 'Sugars - Total';
            break;
          case 'carbohydrate':
            key = 'Carbohydrate';
            break;
          case 'protein':
            key = 'Protein';
            break;
          case 'sodium':
            key = 'Sodium';
            break;
          case 'gluten':
            key = 'Gluten';
            break;
        }

        targetSection[key] = value;
      });
    }
  });

  return result;
}

function convertOriginalNutrition(nutritionFacts: Record<string, any>): NutritionInfo {
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
    if (nutritionFacts.carbohydrate) {
      perServing['Carbohydrate'] = nutritionFacts.carbohydrate;
    }
    if (nutritionFacts.sugar) {
      perServing['Sugars - Total'] = nutritionFacts.sugar;
    }
    if (nutritionFacts.saturated_fat) {
      perServing['Fat - Saturated'] = nutritionFacts.saturated_fat;
    }

    defaultNutrition.perServing = perServing;
    defaultNutrition.per100g = { ...perServing };
  }

  return defaultNutrition;
}

// function convertPriceHistory(apiPriceHistory: ApiPriceHistory[]): PriceHistoryEntry[] {
//   return apiPriceHistory.map(entry => ({
//     startDate: new Date(entry.start_date).toISOString(),
//     endDate: entry.end_date ? new Date(entry.end_date).toISOString() : new Date().toISOString(),
//     price: entry.price
//   }));
// }
//

// we use a fake one for now...
function convertPriceHistory(apiPriceHistory: ApiPriceHistory[]): PriceHistoryEntry[] {
  // Convert the actual API data first
  const convertedData = apiPriceHistory.map(entry => ({
    startDate: new Date(entry.start_date).toISOString(),
    endDate: entry.end_date ? new Date(entry.end_date).toISOString() : new Date().toISOString(),
    price: entry.price
  }));

  // If we have real data, generate fake data based on the earliest entry's price
  let fakeData: PriceHistoryEntry[] = [];

  if (convertedData.length > 0) {
    const basePrice = convertedData[0].price;
    const startYear = 2022;
    const endYear = 2024;

    // Generate monthly entries from 2022 to 2024
    for (let year = startYear; year <= endYear; year++) {
      for (let month = 0; month < 12; month++) {
        // Calculate total months from start to determine trend
        const monthIndex = (year - startYear) * 12 + month;
        const totalMonths = (endYear - startYear + 1) * 12;

        // Base trend: gradually increase price over time (start at 70% of base price)
        const trendMultiplier = 0.7 + (monthIndex / totalMonths) * 0.25; // 0.7 to 0.95
        let currentPrice = basePrice * trendMultiplier;

        // Add occasional discount spikes (simulate sales/discounts)
        // Random chance for discount in certain months (e.g., holiday seasons)
        const isDiscountMonth = Math.random() < 0.15; // 15% chance
        if (isDiscountMonth) {
          currentPrice *= 0.75; // 25% discount
        }

        // Round to 2 decimal places
        currentPrice = Math.round(currentPrice * 100) / 100;

        const startDate = new Date(year, month, 1);
        const endDate = new Date(year, month + 1, 0); // Last day of current month

        fakeData.push({
          startDate: startDate.toISOString(),
          endDate: endDate.toISOString(),
          price: currentPrice
        });
      }
    }
  }

  // Return fake data first, then real data
  return [...fakeData, ...convertedData];
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

function getNutritionData(storeProduct: ApiStoreProduct): NutritionInfo {
  // Try Coles format first (raw_details.nutrition)
  if (storeProduct.raw_details?.nutrition?.breakdown) {
    return convertNutritionFacts(storeProduct.raw_details.nutrition);
  }

  // Fall back to original format (raw_details.nutrition_facts)
  if (storeProduct.raw_details?.nutrition_facts) {
    return convertNutritionFacts(storeProduct.raw_details.nutrition_facts);
  }

  // Return empty nutrition if no data found
  return { perServing: {}, per100g: {} };
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
    console.log('API Data:', apiData);

    const storeProducts = apiData.store_products;
    for (let i = 0; i < storeProducts.length; i++) {
      console.log(`Store Product ${i} (${storeProducts[i].store}):`);

      // Check for Coles nutrition format
      const colesNutrition = storeProducts[i]?.raw_details?.nutrition?.breakdown;
      if (colesNutrition) {
        console.log('Coles nutrition breakdown:', colesNutrition);
      }

      // Check for original nutrition format
      const originalNutrition = storeProducts[i]?.raw_details?.nutrition_facts;
      if (originalNutrition) {
        console.log('Original nutrition facts:', originalNutrition);
      }

      if (!colesNutrition && !originalNutrition) {
        console.log('No nutrition data found');
      }
    }

    // Get nutrition data from the first store product that has it
    let nutritionData: NutritionInfo = { perServing: {}, per100g: {} };
    for (const storeProduct of apiData.store_products) {
      const nutrition = getNutritionData(storeProduct);
      if (Object.keys(nutrition.perServing).length > 0 || Object.keys(nutrition.per100g).length > 0) {
        nutritionData = nutrition;
        break;
      }
    }

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
      nutrition: nutritionData,
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
