import { Button } from "@/components/ui/button"

export default function Hero() {
  return (
    <div className="bg-secondary relative w-screen flex flex-col gap-2 py-20 px-5 sm:px-10 md:px-20 lg:px-30 2xl:px-60">
      <h1 className="text-5xl font-medium">Compare grocery prices across stores</h1>
      <h3>Find the best deals and save money on your groceries</h3>
      <div className="flex flex-row gap-2">
        <Button>Start Shopping</Button>
        <Button variant="outline" className="border-primary">How it works</Button>
      </div>
    </div>
  );
}
