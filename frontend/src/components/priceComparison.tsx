import { useState, useEffect } from "react";
import { Card } from "./ui/card";

export default function PriceComparison() {

  const [data, setData] = useState([
    { store: "Woolworths", storeLogo: "/vite.svg", price: 0.00, lastUpdated: "2025-01-29T15:30:00.000Z" },
    { store: "IGA", storeLogo: "/vite.svg", price: 1.00, lastUpdated: "2025-02-25T15:30:00.000Z" },
    { store: "Coles", storeLogo: "/vite.svg", price: 2.00, lastUpdated: "2025-01-12T15:30:00.000Z" },
    { store: "Aldi", storeLogo: "/vite.svg", price: 3.00, lastUpdated: "2025-03-16T15:30:00.000Z" }
  ]);
  
  useEffect(() => {
    fetch("") /* ADD API ENDPOINT URL FOR FETCHING DATA */
      .then(response => response.json())
      .then(result => setData(result))
      .catch(error => {
        console.log("Error fetching data: ", error);
      })
  }, []);
  
  return (
    <div className="flex flex-col w-full gap-5">
      <p className="text-lg font-bold">Price Comparison</p>
      <div className="flex flex-col w-full gap-y-5">
        {data.map((item, index) => (
          <Card key={index} className="flex flex-row justify-between items-center w-full bg-white px-10">  
            <div className="flex flex-row gap-5">
              <img src={item.storeLogo}></img> {/* Store Icon */}
              <div className="flex flex-col gap-1"> {/* Store Name and Last Updated */}
                <p className="font-bold">{item.store}</p>
                <p>Last Updated: {new Date(item.lastUpdated).toLocaleDateString("en-GB")}</p> {/* Product Price */}
              </div>
            </div>
            <p className="font-bold">${item.price.toFixed(2)}</p>
          </Card>
        ))}
      </div>
    </div>
  )
}