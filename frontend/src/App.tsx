import { Button } from "@/components/ui/button"
import Header from "./components/ui/Header"

function App() {
  return (
    <div className="w-full">
      <Header />
      <div className="flex flex-col items-center justify-center w-full min-h-svh">
        <Button>Look ShadCN is installed</Button>
      </div>
    </div>
  )
}

export default App
