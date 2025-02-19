"use client"

import React, { useState, useEffect } from "react";
import Image from "next/image";
import Header from "@/components/header";
import Footer from "@/components/footer";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { TrendingUp, TrendingDown } from 'lucide-react';
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

  const handleStoreClick = (storeProduct: StoreProduct) => {
    if (currStoreProduct && currStoreProduct.store === storeProduct.store) {
      if (storeProduct.productUrl) {
        window.open(storeProduct.productUrl, '_blank');
      }
    } else {
      setCurrStoreProduct(storeProduct);
    }
  };

  return (
    <div className="w-full bg-gray-300">
      <Header />
      <div className="flex flex-col items-center justify-center w-full min-h-svh px-20 mt-10">
        <Card className="grid grid-cols-2 w-full h-full mb-10">
          {/* Product Image */}
          <div className="flex justify-center items-center" >
            {productData.imageUrl ? (
              <Image src={productData.imageUrl} alt={productData.name} width={500} height={500} />
            ) : (
              <div className="w-[500px] h-[500px] bg-gray-200 flex items-center justify-center rounded-lg">
                <span className="text-gray-500">No image available</span>
              </div>
            )}
          </div>
          <div className="flex flex-col gap-3">
            {/* Store Options */}
            <CardHeader>
              <div className="flex flex-row items-center gap-2 mb-5">
                {productData.storeProducts.map((storeProduct, index) => (
                  <div
                    key={index}
                    onClick={() => handleStoreClick(storeProduct)}
                    className={`
                      flex flex-row gap-1 cursor-pointer text-sm font-semibold py-2 px-4 rounded-full
                      shadow-xl transition-transform duration-300 ease-in-out
                      ${currStoreProduct.store === storeProduct.store
                        ? 'bg-gray-300 transition-transform hover:bg-gray-400 hover:-translate-y-1'
                        : 'transition-transform hover:bg-gray-200 hover:-translate-y-1'
                      }
                    `}>
                    <span>(${storeProduct.standardPrice.toFixed(2)}) {storeProduct.store}</span>
                    {storeProduct.standardPrice === minPrice &&
                      <Image src="/Gold Medal.svg" alt="Medal" width={20} height={20} />
                    }
                  </div>
                ))}
              </div>
              {/* Product Name and Price */}
              <CardTitle className="text-3xl">{productData.name}</CardTitle>
              <p className="text-xl font-bold">${currStoreProduct.standardPrice.toFixed(2)}</p>
            </CardHeader>
            {/* Product Description */}
            <CardContent className="flex flex-col mt-5 mr-15">
              <p>{productData.description}</p>
            </CardContent>
          </div>
        </Card>

        {/* Price History and Nutrition Section */}
        <div className="flex flex-row w-full gap-10 items-top">
          {/* Price History Section */}
          <Card className="w-full h-full">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-xl">
                <TrendingUp className="h-5 w-5" />
                Price History
              </CardTitle>
            </CardHeader>
            <CardContent>
              <PriceHistory params={{ priceHistory: currStoreProduct.priceHistory }} />
            </CardContent>
          </Card>

          {/* Nutrition Facts */}
          <Card className="w-full h-full">
            <CardHeader>
              <CardTitle className="text-xl">Nutrition Facts</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-border">
                      <th className="text-left py-3 font-medium text-muted-foreground">Nutrient</th>
                      <th className="text-right py-3 font-medium text-muted-foreground">Per Serving</th>
                      <th className="text-right py-3 font-medium text-muted-foreground">Per 100g</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.keys(productData.nutrition.perServing).map((nutrient) => (
                      <tr key={nutrient} className="border-b border-border last:border-b-0">
                        <td className="py-3 font-medium">{nutrient}</td>
                        <td className="py-3 text-right font-medium">{productData.nutrition.perServing[nutrient]}</td>
                        <td className="py-3 text-right font-medium">{productData.nutrition.per100g[nutrient]}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
      <Footer />
    </div>
  );
}
