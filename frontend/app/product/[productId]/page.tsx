"use client"

import React, { useState, useEffect } from "react";
import Image from "next/image";
import Header from "@/components/header";
import Footer from "@/components/footer";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { TrendingUp, TrendingDown, BarChart3, FileText } from 'lucide-react';
import PriceHistory from "@/components/priceHistory";

async function getProduct(id: string): Promise<Product | null> {
  try {
    const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000';
    const response = await fetch(`${baseUrl}/api/products/${id}`, {
      cache: 'no-store',
    });

    if (!response.ok) {
      if (response.status === 404) {
        return null;
      }
      throw new Error('Failed to fetch product');
    }

    return response.json();
  } catch (error) {
    console.error('Error fetching product:', error);
    throw error;
  }
}

interface ProductPageProps {
  params: Promise<{
    productId: string;
  }>;
}

interface StoreProduct {
  storeProductId: number;
  store: string;
  standardPrice: number;
  productUrl: string;
  priceHistory: {
    startDate: string;
    endDate: string;
    price: number;
  }[];
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
  nutrition: {
    perServing: { [key: string]: string };
    per100g: { [key: string]: string };
  };
  storeProducts: StoreProduct[];
}

export default function Product({ params }: ProductPageProps) {
  const [productData, setProductData] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const resolvedParams = await params;
        const data = await getProduct(resolvedParams.productId);
        console.log(data);
        if (data) {
          setProductData(data);
        } else {
          setError('Product not found');
        }
      } catch (err) {
        setError('Failed to load product');
        console.error('Error fetching product:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [params]);



  const [currStoreProduct, setCurrStoreProduct] = useState<StoreProduct | null>(null);

  useEffect(() => {
    if (productData && productData.storeProducts.length > 0) {
      setCurrStoreProduct(productData.storeProducts[0]);
    }
  }, [productData]);

  if (loading) {
    return (
      <div className="w-full bg-gray-300">
        <Header />
        <div className="flex flex-col items-center justify-center w-full min-h-svh px-20 mt-10">
          <div className="text-xl">Loading...</div>
        </div>
        <Footer />
      </div>
    );
  }

  if (error || !productData) {
    return (
      <div className="w-full bg-gray-300">
        <Header />
        <div className="flex flex-col items-center justify-center w-full min-h-svh px-20 mt-10">
          <div className="text-xl text-red-500">{error || 'Product not found'}</div>
        </div>
        <Footer />
      </div>
    );
  }

  if (!currStoreProduct) {
    return (
      <div className="w-full bg-gray-300">
        <Header />
        <div className="flex flex-col items-center justify-center w-full min-h-svh px-20 mt-10">
          <div className="text-xl">No store products available</div>
        </div>
        <Footer />
      </div>
    );
  }

  const minPrice: number = Math.min(...productData.storeProducts.map(storeProduct => storeProduct.standardPrice));

  const getStoreColors = (storeName: string, isSelected: boolean) => {
    const store = storeName.toLowerCase();
    
    if (store === 'coles') {
      return isSelected 
        ? 'bg-red-500 text-white hover:bg-red-600' 
        : 'bg-red-100 text-red-800 hover:bg-red-200 border border-red-300';
    } else if (store === 'aldi') {
      return isSelected 
        ? 'bg-orange-500 text-white hover:bg-orange-600' 
        : 'bg-orange-100 text-orange-800 hover:bg-orange-200 border border-orange-300';
    } else if (store === 'woolworths') {
      return isSelected 
        ? 'bg-green-500 text-white hover:bg-green-600' 
        : 'bg-green-100 text-green-800 hover:bg-green-200 border border-green-300';
    } else if (store === 'iga') {
      return isSelected 
        ? 'bg-gray-500 text-white hover:bg-gray-600' 
        : 'bg-gray-100 text-gray-800 hover:bg-gray-200 border border-gray-300';
    } else {
      return isSelected 
        ? 'bg-blue-500 text-white hover:bg-blue-600' 
        : 'bg-blue-100 text-blue-800 hover:bg-blue-200 border border-blue-300';
    }
  };

  const handleStoreClick = (storeProduct: StoreProduct) => {
    // Always open the product URL when clicking a store badge
    if (storeProduct.productUrl) {
      window.open(storeProduct.productUrl, '_blank');
    }
    
    // Also update the selected store for price history display
    setCurrStoreProduct(storeProduct);
  };

  return (
    <div className="w-full bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen">
      <Header />
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Main Product Card */}
        <Card className="grid lg:grid-cols-2 gap-8 mb-8 p-8 shadow-xl bg-white rounded-2xl border-0">
          {/* Product Image */}
          <div className="flex justify-center items-center bg-gray-50 rounded-xl p-8">
            {productData.imageUrl ? (
              <Image 
                src={productData.imageUrl} 
                alt={productData.name} 
                width={400} 
                height={400} 
                className="rounded-lg object-contain max-w-full max-h-[400px]"
              />
            ) : (
              <div className="w-[400px] h-[400px] bg-gray-200 flex items-center justify-center rounded-xl">
                <span className="text-gray-500 text-lg font-medium">No image available</span>
              </div>
            )}
          </div>
          
          <div className="flex flex-col justify-between">
            {/* Store Options */}
            <div className="space-y-6">
              <div>
                <h3 className="text-sm font-semibold text-gray-600 uppercase tracking-wider mb-4">Available At</h3>
                <div className="flex flex-wrap gap-3">
                  {productData.storeProducts.map((storeProduct, index) => {
                    const isSelected = currStoreProduct.store === storeProduct.store;
                    const isLowestPrice = storeProduct.standardPrice === minPrice;
                    
                    return (
                      <div
                        key={index}
                        onClick={() => handleStoreClick(storeProduct)}
                        className={`
                          flex items-center gap-2 cursor-pointer text-sm font-semibold py-3 px-5 rounded-xl
                          shadow-lg transition-all duration-300 ease-in-out transform
                          hover:scale-105 hover:shadow-xl hover:-translate-y-1
                          ${getStoreColors(storeProduct.store, isSelected)}
                          ${isLowestPrice ? 'ring-2 ring-yellow-400 ring-offset-2' : ''}
                        `}>
                        <div className="flex flex-col items-start">
                          <span className="font-bold">{storeProduct.store}</span>
                          <span className="text-xs opacity-90">${storeProduct.standardPrice.toFixed(2)}</span>
                        </div>
                        {isLowestPrice && (
                          <div className="flex items-center justify-center w-6 h-6 bg-yellow-400 rounded-full">
                            <span className="text-yellow-900 text-xs font-bold">★</span>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
              
              {/* Product Details */}
              <div className="space-y-4">
                <h1 className="text-4xl font-bold text-gray-900 leading-tight">{productData.name}</h1>
                <div className="flex items-center gap-3">
                  <span className="text-3xl font-bold text-blue-600">${currStoreProduct.standardPrice.toFixed(2)}</span>
                  <span className="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                    {productData.size} {productData.unit}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <span className="font-medium">Brand:</span>
                  <span>{productData.brand}</span>
                  <span className="mx-2">•</span>
                  <span className="font-medium">Category:</span>
                  <span>{productData.category}</span>
                </div>
              </div>
            </div>
            
            {/* Product Description */}
            <div className="mt-6 space-y-4">
              <div>
                <p className="text-gray-600 text-sm leading-relaxed">{productData.description}</p>
              </div>
              
              {productData.longDescription && (
                <div className="p-6 bg-blue-50 rounded-xl">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Detailed Information</h3>
                  <div 
                    className="text-gray-700 leading-relaxed prose prose-sm max-w-none"
                    dangerouslySetInnerHTML={{ __html: productData.longDescription }}
                  />
                </div>
              )}
            </div>
          </div>
        </Card>

        {/* Price History and Nutrition Section */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Price History Section */}
          <Card className="p-6 shadow-xl bg-white rounded-2xl border-0">
            <CardHeader className="pb-6">
              <CardTitle className="flex items-center gap-3 text-2xl font-bold text-gray-900">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <TrendingUp className="h-6 w-6 text-blue-600" />
                </div>
                Price History
              </CardTitle>
              <p className="text-gray-600 text-sm">Track price changes over time for {currStoreProduct.store}</p>
            </CardHeader>
            <CardContent>
              <PriceHistory params={{ priceHistory: currStoreProduct.priceHistory }} />
            </CardContent>
          </Card>

          {/* Nutrition Facts */}
          <Card className="p-6 shadow-xl bg-white rounded-2xl border-0">
            <CardHeader className="pb-6">
              <CardTitle className="flex items-center gap-3 text-2xl font-bold text-gray-900">
                <div className="p-2 bg-green-100 rounded-lg">
                  <BarChart3 className="h-6 w-6 text-green-600" />
                </div>
                Nutrition Facts
              </CardTitle>
              <p className="text-gray-600 text-sm">Nutritional information per serving and per 100g</p>
            </CardHeader>
            <CardContent>
              {Object.keys(productData.nutrition.perServing).length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b-2 border-gray-200">
                        <th className="text-left py-4 font-semibold text-gray-900">Nutrient</th>
                        <th className="text-right py-4 font-semibold text-gray-900">Per Serving</th>
                        <th className="text-right py-4 font-semibold text-gray-900">Per 100g</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.keys(productData.nutrition.perServing).map((nutrient) => (
                        <tr key={nutrient} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                          <td className="py-3 font-medium text-gray-900">{nutrient}</td>
                          <td className="py-3 text-right font-medium text-gray-700">{productData.nutrition.perServing[nutrient]}</td>
                          <td className="py-3 text-right font-medium text-gray-700">{productData.nutrition.per100g[nutrient]}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="text-center py-12">
                  <FileText className="h-8 w-8 text-gray-400 mx-auto mb-3" />
                  <div className="text-gray-500 font-medium">No nutrition information available</div>
                  <div className="text-gray-400 text-sm mt-1">Nutrition data will appear here when available</div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
      <Footer />
    </div>
  );
}
