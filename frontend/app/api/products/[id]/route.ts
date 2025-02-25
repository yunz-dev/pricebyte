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
  longDescription?: string;
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
    longDescription?: string;
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
    let currentPrice = basePrice * 0.7; // Start at 70% of base price

    // Generate monthly entries from 2022 to 2024
    for (let year = startYear; year <= endYear; year++) {
      for (let month = 0; month < 12; month++) {
        // Calculate overall trend (gradual increase over time)
        const monthIndex = (year - startYear) * 12 + month;
        const totalMonths = (endYear - startYear + 1) * 12;
        const progressRatio = monthIndex / totalMonths;

        // Base upward trend (from 70% to 95% of base price)
        const trendTarget = basePrice * (0.7 + progressRatio * 0.25);

        // Add random variation around the trend
        const randomVariation = (Math.random() - 0.5) * 0.1; // ±5% random variation
        let targetPrice = trendTarget * (1 + randomVariation);

        // Smooth transition from current price to target (prevents big jumps)
        const smoothingFactor = 0.3; // How much to move toward target each month
        currentPrice = currentPrice * (1 - smoothingFactor) + targetPrice * smoothingFactor;

        // Add occasional discount spikes (simulate sales/discounts)
        const isDiscountMonth = Math.random() < 0.12; // 12% chance
        let finalPrice = currentPrice;
        if (isDiscountMonth) {
          const discountAmount = 0.15 + Math.random() * 0.15; // 15-30% discount
          finalPrice = currentPrice * (1 - discountAmount);
        }

        // Add small random daily fluctuations
        const dailyVariation = (Math.random() - 0.5) * 0.05; // ±2.5% daily variation
        finalPrice *= (1 + dailyVariation);

        // Round to 2 decimal places
        finalPrice = Math.round(finalPrice * 100) / 100;

        // Update current price for next iteration (only if not a discount month)
        if (!isDiscountMonth) {
          currentPrice = finalPrice;
        }

        const startDate = new Date(year, month, 1);
        const endDate = new Date(year, month + 1, 0); // Last day of current month

        fakeData.push({
          startDate: startDate.toISOString(),
          endDate: endDate.toISOString(),
          price: finalPrice
        });
      }
    }
  }

  // Return fake data first, then real data
  return [...fakeData, ...convertedData];
}

function createWoolworthsFromColes(colesProduct: ApiStoreProduct): ApiStoreProduct {
  // Generate a slightly different price (±5-15% variation)
  const priceVariation = 0.05 + Math.random() * 0.1; // 5-15%
  const priceMultiplier = Math.random() > 0.5 ? (1 + priceVariation) : (1 - priceVariation);
  const woolworthsPrice = Math.round(colesProduct.current_price * priceMultiplier * 100) / 100;

  // Generate a new store product ID
  const woolworthsId = colesProduct.id + 10000; // Simple offset to avoid conflicts

  return {
    ...colesProduct,
    id: woolworthsId,
    store: 'woolworths',
    store_name: colesProduct.store_name, // Keep the same store_name as Coles
    store_product_id: `WW${colesProduct.store_product_id.slice(2)}`, // Replace prefix
    current_price: woolworthsPrice,
    // Keep most raw_details the same, but could modify specific fields if needed
    raw_details: {
      ...colesProduct.raw_details,
      // Remove Coles-specific data that might not apply to Woolworths
      nutrition: undefined, // Remove Coles nutrition format
      // Keep nutrition_facts if it exists for the generic format
    },
    // Generate different price history based on the new price
    price_history: colesProduct.price_history.map(entry => ({
      ...entry,
      price: Math.round(entry.price * priceMultiplier * 100) / 100
    }))
  };
}

function addWoolworthsProductIfColesExists(apiData: ApiProduct): ApiProduct {
  console.log('Checking for Coles product...');
  console.log('Available stores:', apiData.store_products.map(sp => sp.store));

  // Check if we have a Coles product
  const colesProduct = apiData.store_products.find(sp => sp.store.toLowerCase() === 'coles');

  if (colesProduct) {
    console.log('Found Coles product!');

    // Check if Woolworths already exists
    const woolworthsExists = apiData.store_products.some(sp => sp.store.toLowerCase() === 'woolworths');

    console.log('Woolworths already exists:', woolworthsExists);

    if (!woolworthsExists) {
      console.log('Creating Woolworths product from Coles...');
      // Create Woolworths version from Coles
      const woolworthsProduct = createWoolworthsFromColes(colesProduct);

      const enhancedData = {
        ...apiData,
        store_products: [...apiData.store_products, woolworthsProduct]
      };

      console.log('Added Woolworths! New store count:', enhancedData.store_products.length);
      console.log('Updated stores:', enhancedData.store_products.map(sp => sp.store));

      return enhancedData;
    }
  } else {
    console.log('No Coles product found');
  }

  console.log('Returning original data without changes');
  return apiData;
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

function getLongDescription(apiData: ApiProduct): string | undefined {
  // Try to get long description from any store product that has it
  for (const storeProduct of apiData.store_products) {
    if (storeProduct.raw_details?.longDescription) {
      return storeProduct.raw_details.longDescription;
    }
  }

  // Return undefined if no long description found
  return undefined;
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

    // Add Woolworths product if Coles exists but Woolworths doesn't
    const enhancedApiData = addWoolworthsProductIfColesExists(apiData);

    const storeProducts = enhancedApiData.store_products;
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
    for (const storeProduct of enhancedApiData.store_products) {
      const nutrition = getNutritionData(storeProduct);
      if (Object.keys(nutrition.perServing).length > 0 || Object.keys(nutrition.per100g).length > 0) {
        nutritionData = nutrition;
        break;
      }
    }

    // Get long description if available
    const longDescription = getLongDescription(enhancedApiData);

    // Convert API data to Product format
    const product: Product = {
      productId: enhancedApiData.id,
      name: enhancedApiData.name,
      brand: enhancedApiData.brand,
      category: capitalizeFirstLetter(enhancedApiData.category),
      size: parseSize(enhancedApiData.size),
      unit: enhancedApiData.unit,
      imageUrl: enhancedApiData.image_url || '',
      description: enhancedApiData.description,
      longDescription: longDescription,
      nutrition: nutritionData,
      storeProducts: convertStoreProducts(enhancedApiData.store_products)
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
