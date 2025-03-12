import { useState, useEffect } from "react";

export default function ProductSpecs() {
  
  const [data, setData] = useState({ /* CHANGE DEFAULT DATA */
    store: "Woolworths",
    category: "Dairy",
    brand: "A2",
    unitPrice: 0,
    weight: "1L",
    availability: false,
  });

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
      <p className="text-lg font-bold">Specifications</p>
      <div className="grid grid-cols-2 w-full gap-x-20 gap-y-3">
        {Object.entries(data).map(([key, value]) => (
          <div key={key} className="flex justify-between px-4 py-2 border-b border-gray-300">
            <span className="capitalize">{key.replace(/([A-Z])/g, " $1")}:</span>
            <span className="font-semibold" >{typeof value === "boolean" ? (value ? "Yes" : "No") : value}</span>
          </div>
        ))}
      </div> 
    </div>
  )
}