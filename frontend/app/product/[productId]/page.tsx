"use client"

import React, { useState, useEffect } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Header from "@/components/header";
import Footer from "@/components/footer";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { TrendingUp, TrendingDown, BarChart3, FileText, Brain, ExternalLink, ShoppingCart } from 'lucide-react';
import PriceHistory from "@/components/priceHistory";
import { ProductPageSkeleton, BreadcrumbSkeleton } from "@/components/skeletons";

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
  storeName: string;
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
  const router = useRouter();
  const [productData, setProductData] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showFullDescription, setShowFullDescription] = useState(false);

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
      <div className="w-full bg-gray-50 min-h-screen">
        <Header />
        <BreadcrumbSkeleton />
        <ProductPageSkeleton />
        <Footer />
      </div>
    );
  }

  if (error || !productData) {
    return (
      <div className="w-full bg-gray-50 min-h-screen flex flex-col">
        <Header />
        <div className="flex-1 flex flex-col items-center justify-center px-4 py-20">
          <div className="max-w-2xl text-center">
            <div className="w-32 h-32 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-8">
              <div className="w-16 h-16 text-red-600">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <circle cx="12" cy="12" r="10" />
                  <circle cx="8" cy="10" r="1.5" fill="white" />
                  <circle cx="16" cy="10" r="1.5" fill="white" />
                  <path d="M8 16s1.5-2 4-2 4 2 4 2" stroke="white" strokeWidth="2" fill="none" strokeLinecap="round" />
                </svg>
              </div>
            </div>
            <h1 className="text-6xl font-black text-gray-900 mb-4">404</h1>
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Product Not Found</h2>
            <p className="text-xl text-gray-600 mb-8 leading-relaxed">
              Oops! The product you're looking for doesn't exist or has been removed from our catalog.
            </p>
            <div className="space-y-4">
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/">
                  <Button size="lg" className="bg-blue-600 hover:bg-blue-700 px-8 py-4 text-lg">
                    Back to Home
                  </Button>
                </Link>
                <Link href="/search?q=">
                  <Button size="lg" variant="outline" className="px-8 py-4 text-lg border-2">
                    Browse Products
                  </Button>
                </Link>
              </div>
              <p className="text-sm text-gray-500 mt-6">
                Try searching for something else or check out our popular categories
              </p>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  if (!currStoreProduct) {
    return (
      <div className="w-full bg-gray-50">
        <Header />
        <div className="flex flex-col items-center justify-center w-full min-h-screen px-20">
          <div className="text-xl text-gray-600">No store products available</div>
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
        ? 'bg-red-600 text-white hover:bg-red-700 shadow-lg'
        : 'bg-white text-red-600 hover:bg-red-50 border-2 border-red-600';
    } else if (store === 'woolworths') {
      return isSelected
        ? 'bg-green-600 text-white hover:bg-green-700 shadow-lg'
        : 'bg-white text-green-600 hover:bg-green-50 border-2 border-green-600';
    } else if (store === 'aldi') {
      return isSelected
        ? 'bg-orange-600 text-white hover:bg-orange-700 shadow-lg'
        : 'bg-white text-orange-600 hover:bg-orange-50 border-2 border-orange-600';
    } else if (store === 'iga') {
      return isSelected
        ? 'bg-gray-600 text-white hover:bg-gray-700 shadow-lg'
        : 'bg-white text-gray-600 hover:bg-gray-50 border-2 border-gray-600';
    } else {
      return isSelected
        ? 'bg-blue-600 text-white hover:bg-blue-700 shadow-lg'
        : 'bg-white text-blue-600 hover:bg-blue-50 border-2 border-blue-600';
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
    <div className="w-full bg-gray-50 min-h-screen flex flex-col">
      <Header />

      {/* Breadcrumb */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-4 py-3 max-w-7xl">
          <nav className="text-sm text-gray-600">
            <button
              onClick={() => router.push('/')}
              className="hover:text-blue-600 transition-colors"
            >
              Home
            </button>
            <span className="mx-2">›</span>
            <button
              onClick={() => router.push(`/search?q=${encodeURIComponent(productData.category)}`)}
              className="hover:text-blue-600 transition-colors"
            >
              {productData.category}
            </button>
            <span className="mx-2">›</span>
            <span className="text-gray-900">{currStoreProduct.storeName}</span>
          </nav>
        </div>
      </div>

      <div className="flex-1 container mx-auto px-4 py-6 max-w-7xl">
        <div className="grid lg:grid-cols-12 gap-6">

          {/* Product Images and Price History - Left Column */}
          <div className="lg:col-span-7">
            <div className="sticky top-24 space-y-6">
              {/* Product Image */}
              <div className="bg-white rounded-2xl p-8 shadow-sm border">
                <div className="aspect-square bg-gray-50 rounded-xl flex items-center justify-center">
                  {productData.imageUrl ? (
                    <Image
                      src={productData.imageUrl}
                      alt={productData.name}
                      width={500}
                      height={500}
                      className="rounded-lg object-contain max-w-full max-h-full"
                    />
                  ) : (
                    <div className="text-center">
                      <div className="w-24 h-24 bg-gray-200 rounded-full mx-auto mb-4 flex items-center justify-center">
                        <ShoppingCart className="w-8 h-8 text-gray-400" />
                      </div>
                      <span className="text-gray-500 text-lg font-medium">No image available</span>
                    </div>
                  )}
                </div>
              </div>

              {/* Price History Section */}
              <Card className="p-6 shadow-sm bg-white rounded-2xl border">
                <CardHeader className="pb-6">
                  <CardTitle className="flex items-center gap-3 text-xl font-bold text-gray-900">
                    <div className="p-2 bg-blue-600 rounded-lg">
                      <TrendingUp className="h-5 w-5 text-white" />
                    </div>
                    Price History
                  </CardTitle>
                  <p className="text-gray-600 text-sm">Track price changes over time for {currStoreProduct.store}</p>
                </CardHeader>
                <CardContent>
                  <PriceHistory params={{ priceHistory: currStoreProduct.priceHistory }} />

                  {/* AI Insights Section */}
                  <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-100">
                    <div className="flex items-center gap-2 mb-3">
                      <div className="p-2 bg-blue-600 rounded-lg">
                        <Brain className="h-4 w-4 text-white" />
                      </div>
                      <h4 className="font-semibold text-gray-900">AI Insights</h4>
                    </div>
                    <div className="space-y-2 text-sm">
                      <p className="text-gray-700">
                        <span className="font-medium text-blue-700">Price Trend:</span> This product has been showing a gradual upward trend over the past 6 months, with an average increase of 3.2%.
                      </p>
                      <p className="text-gray-700">
                        <span className="font-medium text-blue-700">Next Discount:</span> Based on historical patterns, this item typically goes on sale every 6-8 weeks. The next expected discount period is <span className="font-semibold text-blue-600">February 15-28, 2025</span>.
                      </p>
                      <p className="text-gray-700">
                        <span className="font-medium text-blue-700">Savings Tip:</span> You could save up to 15-20% by waiting for the next promotional period, or consider bulk buying when on special.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Product Info - Right Column */}
          <div className="lg:col-span-5">
            <div className="bg-white rounded-2xl p-6 shadow-sm border mb-4">

              {/* Product Header */}
              <div className="mb-5">
                <div className="flex items-center gap-2 mb-3">
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium">
                    {productData.category}
                  </span>
                  <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded-full text-xs">
                    {productData.brand}
                  </span>
                </div>
                <h1 className="text-2xl lg:text-3xl font-bold text-gray-900 leading-tight mb-3">
                  {currStoreProduct.storeName}
                </h1>
                <p className="text-gray-600 text-sm leading-relaxed mb-2">
                  {productData.description}
                </p>
                <p className="text-xs text-gray-500 italic">
                  Generic Name: {productData.name}
                </p>
              </div>

              {/* Price and Size */}
              <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-100">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-2xl lg:text-3xl font-bold text-blue-600 mb-1">
                      ${currStoreProduct.standardPrice.toFixed(2)}
                    </div>
                    <div className="text-xs text-gray-600">
                      {productData.size} {productData.unit} • From {currStoreProduct.store}
                      {/* {productData.size} • From {currStoreProduct.store} */}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-gray-500 mb-1">Price per unit</div>
                    <div className="text-sm font-semibold text-gray-700">
                      ${(currStoreProduct.standardPrice / productData.size).toFixed(2)} per {productData.unit}
                    </div>
                  </div>
                </div>
              </div>

              {/* Store Selection */}
              <div className="mb-6">
                <h3 className="text-base font-bold text-gray-900 mb-3">Choose Your Store</h3>
                <div className="grid gap-3">
                  {productData.storeProducts.map((storeProduct, index) => {
                    const isSelected = currStoreProduct.store === storeProduct.store;
                    const isLowestPrice = storeProduct.standardPrice === minPrice;

                    return (
                      <div
                        key={index}
                        onClick={() => handleStoreClick(storeProduct)}
                        className={`
                          relative cursor-pointer p-3 rounded-lg transition-all duration-200
                          ${getStoreColors(storeProduct.store, isSelected)}
                          ${isLowestPrice ? 'ring-2 ring-yellow-400 ring-offset-2' : ''}
                          hover:scale-[1.02] hover:shadow-lg
                        `}
                      >
                        {/* Store Page Link Icon */}
                        {storeProduct.productUrl && (
                          <a
                            href={storeProduct.productUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            onClick={(e) => e.stopPropagation()}
                            className="absolute -top-1 -left-1 w-6 h-6 bg-gray-800 hover:bg-gray-900 text-white rounded-full flex items-center justify-center shadow-lg hover:shadow-xl transition-all duration-200 z-10"
                            title={`View ${productData.name} at ${storeProduct.store}`}
                          >
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        )}

                        {isLowestPrice && (
                          <div className="absolute -top-1 -right-1 bg-yellow-400 text-yellow-900 px-2 py-1 rounded-full text-xs font-bold flex items-center gap-1">
                            ★ Best Price
                          </div>
                        )}
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="font-bold text-base">{storeProduct.store}</div>
                            <div className="text-xs opacity-90">
                              Click to view stats
                            </div>
                          </div>
                          <div className="text-right">
                            <div className="font-bold text-lg">
                              ${storeProduct.standardPrice.toFixed(2)}
                            </div>
                            <div className="text-xs opacity-90">
                              ${(storeProduct.standardPrice / productData.size).toFixed(2)} per {productData.unit}
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Product Details */}
              {productData.longDescription && (
                <div className="mb-4">
                  <h3 className="text-base font-bold text-gray-900 mb-3">Product Details</h3>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="text-gray-700 leading-relaxed text-sm">
                      {productData.longDescription.length > 300 ? (
                        <>
                          <div
                            dangerouslySetInnerHTML={{
                              __html: showFullDescription
                                ? productData.longDescription
                                : productData.longDescription.substring(0, 300) + '...'
                            }}
                          />
                          <Button
                            variant="link"
                            onClick={() => setShowFullDescription(!showFullDescription)}
                            className="p-0 h-auto text-blue-600 hover:text-blue-700 mt-2 text-sm"
                          >
                            {showFullDescription ? 'Show less' : 'Show more details'}
                          </Button>
                        </>
                      ) : (
                        <div
                          dangerouslySetInnerHTML={{ __html: productData.longDescription }}
                        />
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Nutrition Facts */}
            <Card className="p-4 shadow-sm bg-white rounded-2xl border">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 text-base font-bold text-gray-900">
                  <div className="p-2 bg-blue-600 rounded-lg">
                    <BarChart3 className="h-4 w-4 text-white" />
                  </div>
                  Nutrition Facts
                </CardTitle>
                <p className="text-gray-600 text-xs">Nutritional information per serving and per 100g</p>
              </CardHeader>
              <CardContent>
                {Object.keys(productData.nutrition.perServing).length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b-2 border-gray-200">
                          <th className="text-left py-3 font-semibold text-gray-900 text-sm">Nutrient</th>
                          <th className="text-right py-3 font-semibold text-gray-900 text-sm">Per Serving</th>
                          <th className="text-right py-3 font-semibold text-gray-900 text-sm">Per 100g</th>
                        </tr>
                      </thead>
                      <tbody>
                        {Object.keys(productData.nutrition.perServing).map((nutrient) => (
                          <tr key={nutrient} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                            <td className="py-2 font-medium text-gray-900 text-sm">{nutrient}</td>
                            <td className="py-2 text-right font-medium text-gray-700 text-sm">{productData.nutrition.perServing[nutrient]}</td>
                            <td className="py-2 text-right font-medium text-gray-700 text-sm">{productData.nutrition.per100g[nutrient]}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <FileText className="h-6 w-6 text-gray-400 mx-auto mb-2" />
                    <div className="text-gray-500 font-medium text-sm">No nutrition information available</div>
                    <div className="text-gray-400 text-xs mt-1">Nutrition data will appear here when available</div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
