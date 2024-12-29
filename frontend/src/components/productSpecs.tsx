import { useState, useEffect } from "react";

export default function ProductSpecs() {
  
  const [data, setData] = useState({
    store: "",
    category: "",
    brand: "",
    unitPrice: 0,
    weight: "",
    availability: false,
  });

  useEffect(() => {
    fetch("")
      .then(response => response.json())
      .then(result => setData(result))
      .catch(error => {
        console.log("Error fetching data: ", error);
      })
  }, []);

  return (
    <div className="flex flex-col w-full">
      <p className="text-lg text-bold">Specifications</p>
      <div className="grid grid-cols-2 w-full">
        {Object.entries(data).map(([key, value]) => (
          <div key={key} className="flex justify-between p-2 rounded">
            <span className="font-semibold capitalize">{key.replace(/([A-Z])/g, " $1")}:</span>
            <span>{typeof value === "boolean" ? (value ? "Yes" : "No") : value}</span>
          </div>
        ))}
      </div> 
    </div>
  )
}