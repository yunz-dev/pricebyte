"use client"

import React, { useState } from "react";
import Image from "next/image";
import Header from "@/components/header";
import Footer from "@/components/footer";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { TrendingUp, TrendingDown } from 'lucide-react';

interface ProductPageProps {
  params: {
    productId: number;
  };
}

interface StoreProduct {
  storeProductId: number;
  store: string;
  price: number;
  productUrl: string;
  priceHistory: [Date, Date, number][];
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

  // const response = await fetch(`http://localhost:8080/store-product/${params.productId}`);
  // if (!response.ok) {
  //   console.log("Error loading product data")
  // }
  // const productData: ProductData = await response.json();

  const productData: Product = {
    "productId": 32102,
    "name": "Coca-Cola Soft Drink Coke | 2L",
    "brand": "Coca-Cola",
    "category": "Drinks",
    "size": 2,
    "unit": "L",
    "imageUrl": "https://shop.coles.com.au/wcsstore/Coles-CAS/images/1/9/1/191736-zm.jpg",
    "description": "Nothing beats the taste of Coca-Cola Classic. It's the perfect companion whether you are on the go, relaxing at home, enjoying with friends or as a drink with your meal. Refresh yourself with the authentic Coke taste. Designed to go with everything, the taste of Classic Coca-Cola has remained unchanged for more than 130 years. Coca-Cola soft drink is available in cans, mini cans, single serve and sharing size bottles as well as multipacks.",
    "nutrition": {
      "perServing": { 'Energy (Cal)': '187 Cal', 'Energy (kJ)': '780 kJ', 'Protein': '7.35 g',
         'Carbohydrate': '1.05 g', 'Fat - Saturated': '1.23 g', 'Fat - Transfat': '0.03 g',
         'Sugars - Total': '0.81 g', 'Sodium': '0.6 mg', 'Dietary Fibre': '3.48 g',
         'Fat - Total': '16.5 g'
      },
      "per100g": { 'Energy (Cal)': '622 Cal', 'Energy (kJ)': '2600 kJ', 'Protein': '24.5 g',
         'Carbohydrate': '3.5 g', 'Fat - Saturated': '4.1 g', 'Fat - Transfat': '0.1 g',
         'Sugars - Total': '2.7 g', 'Sodium': '2 mg', 'Dietary Fibre': '11.6 g',
         'Fat - Total': '54.9 g' 
      },
    },
    "storeProducts": [
      {
        "storeProductId": 38121,
        "store": "Woolworths",
        "price": 3.5,
        "productUrl": "https://www.woolworths.com.au/shop/productdetails/38121",
        "priceHistory": [
          [new Date('2024-04-05'), new Date('2024-04-18'), 2.99],
          [new Date('2024-04-19'), new Date('2024-05-05'), 2.70],
          [new Date('2024-05-06'), new Date('2024-05-25'), 3.05],
          [new Date('2024-05-26'), new Date('2024-06-10'), 2.55],
          [new Date('2024-06-11'), new Date('2024-06-30'), 3.50],
        ]
      },
      {
        "storeProductId": 191736,
        "store": "Coles",
        "price": 3.8,
        "productUrl": "https://www.coles.com.au/product/coca-cola-soft-drink-coke-2l-191736",
        "priceHistory": [
          [new Date('2024-01-01'), new Date('2024-01-15'), 2.50],
          [new Date('2024-01-16'), new Date('2024-02-10'), 2.25],
          [new Date('2024-02-11'), new Date('2024-03-05'), 2.75],
          [new Date('2024-03-06'), new Date('2024-03-20'), 3.00],
          [new Date('2024-03-21'), new Date('2024-04-15'), 3.8],
        ]
      },
      {
        "storeProductId": 14570,
        "store": "IGA",
        "price": 3.85,
        "productUrl": "https://www.igashop.com.au/product/coca-cola-classic-soft-drink-bottle-14570",
        "priceHistory": [
          [new Date('2024-04-05'), new Date('2024-04-18'), 2.99],
          [new Date('2024-04-19'), new Date('2024-05-05'), 2.70],
          [new Date('2024-05-06'), new Date('2024-05-25'), 3.05],
          [new Date('2024-05-26'), new Date('2024-06-10'), 2.55],
          [new Date('2024-06-11'), new Date('2024-06-30'), 3.85],
        ]
      },
    ]
  }

  const [currStoreProduct, setCurrStoreProduct] = useState<StoreProduct>(productData["storeProducts"][0])
  const minPrice: number = Math.min(...productData.storeProducts.map(storeProduct => storeProduct.price));

  const handleStoreClick = (storeProduct: StoreProduct) => {
    if (currStoreProduct && currStoreProduct.store === storeProduct.store) {
      window.open(storeProduct.productUrl, '_blank');
    } else {
      setCurrStoreProduct(storeProduct);
    }
  };

  return (
    <div className="w-full bg-gray-300">
      <Header/>
      <div className="flex flex-col items-center justify-center w-full min-h-svh px-20 mt-10">
        {/* Product Image and Name */}
        <Card className="grid grid-cols-2 w-full h-full mb-10">
          <div className="flex justify-center items-center" >
            <Image src={productData.imageUrl} alt={productData.name} width={500} height={500}/>
          </div>
          <div className="flex flex-col gap-3">
            <CardHeader>
              <div className="flex flex-row items-center gap-2">
                {productData.storeProducts.map((storeProduct, index) => (
                  <div
                    key={index}
                    onClick={() => handleStoreClick(storeProduct)}
                    className={`
                      flex flex-row gap-1 cursor-pointer text-sm font-semibold py-2 px-4 rounded-full
                      transition-all duration-300 ease-in-out
                      ${currStoreProduct.store === storeProduct.store
                        ? 'shadow-lg bg-gray-300 transition-transform hover:bg-gray-400 hover:-translate-y-1'
                        : 'shadow-lg transition-transform hover:bg-gray-200 hover:-translate-y-1'
                      }
                    `}>
                    <span>{storeProduct.store}</span>
                    {storeProduct.price === minPrice && 
                      <Image src="/Gold Medal.svg" alt="Medal" width={20} height={20}/>
                    }
                  </div>
                ))}
              </div>
              <CardTitle className="text-3xl">{productData.name}</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-3">
              <p className="text-xl font-bold">${currStoreProduct.price.toFixed(2)}</p>
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
              <div className="h-64 flex items-center justify-center text-muted-foreground">
                <div className="text-center">
                  <TrendingDown className="h-12 w-12 mx-auto mb-4 text-primary" />
                  <p className="text-lg font-medium">Price tracking chart would appear here</p>
                  <p className="text-sm">Historical price data and trends over time</p>
                </div>
              </div>
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
