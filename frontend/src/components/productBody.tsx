import { useState, useEffect } from "react";
import { Button } from "./ui/button";
function ProductBody() {

  const [product, setProduct] = useState({ /* CHANGE DEFAULT DATA */
    store: "Woolworths",
    productName: "A2 Full Cream Milk",
    brand: "A2",
    category: "Dairy",
    price: 5.00,
    unitPrice: 0.00,
    originalPrice: 10.00,
    availability: true,
    imageUrl: "/vite.svg",
    productUrl: "https://www.woolworths.com.au/shop/productdetails/208064",
    weight: "1L",
    description: "a2 Milk® is the brand leader of the fresh liquid milk category in Australia, and naturally contains only the A2 protein, and no A1, thereby allowing more consumers to enjoy its unique digestive and other potential health benefits. a2 Platinum® infant nutrition is a leading brand in grocery and pharmacy channels",
  });

  useEffect(() => {
    fetch("") /* ADD API ENDPOINT URL FOR FETCHING DATA */
      .then(response => response.json())
      .then(result => setProduct(result))
      .catch(error => {
        console.log("Error fetching data: ", error);
      })
  }, []);

  return (
    <div className="flex flex-row gap-20 mid-h-50vh py-20">{/* Product Area */}
      <img src="/vite.svg" className="w-1/2 h-full object-cover" alt="Product Image" />
      <div className="flex flex-col w-full gap-5">
        <p className="text-2xl font-bold">{product.productName}</p>
        <a href={product.productUrl} target="_blank" rel="noreferrer" 
          className="text-gray-500 transition-transform duration-300 hover:-translate-y-1 hover:font-bold">
          {product.store}
        </a>
        {product.price <= product.originalPrice ?
          <div className="flex flex-row gap-5">
            <p className="text-3xl font-bold line-through text-gray-500">${product.originalPrice.toFixed(2)}</p>
            <p className="text-3xl font-bold">${product.price.toFixed(2)}</p>
          </div> :
          <p className="text-3xl font-bold">${product.price.toFixed(2)}</p>
        }
        <p className="text-base font-bold">Product Description</p>
        <p className="text-base">{product.description}</p>
        <Button className="bg-black text-white w-[60%] hover:bg-gray-400 hover:-translate-y-2">Add to Cart</Button>
      </div>
    </div>
  )
}

export default ProductBody;