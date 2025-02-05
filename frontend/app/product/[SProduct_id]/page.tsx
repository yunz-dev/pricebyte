import Image from "next/image";
import Header from "@/components/header";
import Footer from "@/components/footer";
import ProductSpecs from "@/components/productSpecs";


interface ProductPageProps {
  params: {
    store_product_id: number;
  };
}

export default function Product({ params }: ProductPageProps) {


  return (
    <div className="flex flex-col w-full">

    </div>
  );
}
