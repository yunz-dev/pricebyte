import { Button } from "@/components/ui/button"
import Header from "./components/header"
import Footer from "./components/footer"

function App() {
  return (
    <div className="w-full">
      <Header/>
      <div className="flex flex-col items-center justify-center w-full min-h-svh">
        <Button>Look ShadCN is installed</Button>
      </div>
      <Footer />
    </div>
  )
}

export default App
