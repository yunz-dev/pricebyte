import PriceComparison from "@/components/priceComparison"
import ProductSpecs from "@/components/productSpecs"
import ProductBody from "@/components/productBody"

function ProductPage() {

  return (
    <div className="flex flex-col w-full gap-20"> {/* Main Container */}
      <ProductBody />
      <PriceComparison />
      <ProductSpecs />
    </div>
  )
}

export default ProductPage