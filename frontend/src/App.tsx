import { Button } from "@/components/ui/button"
import Header from "./components/header"
import Footer from "./components/footer"
import ProductSpecs from "./components/productSpecs"
function App() {
  return (
    <div className="w-full">
      <Header/>
      <div className="flex flex-col items-center justify-center w-full min-h-svh px-30">
        <ProductSpecs />

      </div>
      <Footer />
    </div>
  )
}

export default App
