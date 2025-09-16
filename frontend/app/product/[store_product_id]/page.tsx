"use client"

import { useState, useEffect } from "react";
import Image from "next/image";
import Header from "@/components/header";
import Footer from "@/components/footer";


interface ProductPageProps {
  params: {
    store_product_id: number;
  };
}

export default function Product({ params }: ProductPageProps) {

  const [productData, setProductData] = useState({
    "storeProductId": 2,
    "store": "Woolworths",
    "standardPrice": 3.8,
    "productUrl": "https://woolworths.com.au/product/coke-125l",
    "isActive": true
  });

  useEffect(() => {
    fetch(`http://localhost:8080/store-product/${params.store_product_id}`)
      .then(response => response.json())
      .then(result => setProductData(result))
      .catch(error => {
        console.log("Error fetching data: ", error);
      })
      console.log(productData);
      console.log(params.store_product_id);
  }, []);

  return (
    <div className="w-full bg-gray-300">
      <Header/>
      <div className="flex flex-col items-center justify-center w-full min-h-svh px-30">
        {/* Product Image and Name */}
        <div className="flex flex-row ">
          <div>

          </div>
        </div>
        <div className="flex flex-col bg-white p-8 rounded-lg w-full gap-5">

          {/* Product Specifications */}
          <p className="text-lg text-gray-800 font-bold">Specifications</p>
          <div className="grid grid-cols-2 w-full gap-x-20 gap-y-3">
            {Object.entries(productData).map(([key, value]) => (
              <div key={key} className="flex justify-between text-gray-800 px-4 py-2 border-b border-gray-300">
                <span className="capitalize">{key.replace(/([A-Z])/g, " $1")}:</span>
                <span className="font-semibold" >{typeof value === "boolean" ? (value ? "Yes" : "No") : value}</span>
              </div>
            ))}
          </div> 
        </div>
      </div>
      <Footer />
    </div>
  );
}
