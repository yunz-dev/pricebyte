export function transformApiResponseToProduct(apiResponse: any): any {
  // Extract nutrition data from raw_details if available
  const extractNutrition = (rawDetails: any) => {
    if (!rawDetails?.nutrition_facts) {
      return {
        perServing: {},
        per100g: {}
      };
    }

    const nutritionFacts = rawDetails.nutrition_facts;

    // Map the nutrition data to the expected format
    const perServing: any = {};
    const per100g: any = {};

    // Handle the nutrition mapping - you may need to adjust these based on your actual data
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

    return {
      perServing,
      per100g
    };
  };

  // Transform price history
  const transformPriceHistory = (priceHistory: any[]) => {
    if (!priceHistory || !Array.isArray(priceHistory)) return [];

    return priceHistory.map(item => ({
      startDate: item.start_date ? `${item.start_date}T00:00:00.000Z` : null,
      endDate: item.end_date ? `${item.end_date}T00:00:00.000Z` : null,
      price: item.price
    }));
  };

  // Transform store products
  const transformStoreProducts = (storeProducts: any[]) => {
    if (!storeProducts || !Array.isArray(storeProducts)) return [];

    return storeProducts.map(storeProduct => ({
      storeProductId: storeProduct.id,
      store: storeProduct.store.charAt(0).toUpperCase() + storeProduct.store.slice(1), // Capitalize store name
      standardPrice: storeProduct.current_price,
      productUrl: storeProduct.product_url,
      priceHistory: transformPriceHistory(storeProduct.price_history)
    }));
  };

  // Parse size and unit from the size string
  const parseSizeAndUnit = (sizeString: string) => {
    if (!sizeString) return { size: null, unit: null };

    // Extract number and unit from strings like "611g", "2L", etc.
    const match = sizeString.match(/^(\d+(?:\.\d+)?)\s*([a-zA-Z]+)$/);
    if (match) {
      return {
        size: parseFloat(match[1]),
        unit: match[2]
      };
    }

    return { size: null, unit: sizeString };
  };

  const { size, unit } = parseSizeAndUnit(apiResponse.size || '');

  // Get nutrition from the first store product's raw_details if available
  const firstStoreProduct = apiResponse.store_products?.[0];
  const nutrition = extractNutrition(firstStoreProduct?.raw_details);

  return {
    productId: apiResponse.id,
    name: apiResponse.name,
    brand: apiResponse.brand,
    category: apiResponse.category,
    size: size,
    unit: unit,
    imageUrl: apiResponse.image_url || '',
    description: apiResponse.description,
    nutrition: nutrition,
    storeProducts: transformStoreProducts(apiResponse.store_products)
  };
}

// Example usage:
// const transformedProduct = transformApiResponseToProduct(apiResponse);
