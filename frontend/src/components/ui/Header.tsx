import { Button } from "@/components/ui/button";
import { Sheet, SheetTrigger, SheetContent } from "@/components/ui/sheet";
import { Menu } from "lucide-react";
import { Input } from "@/components/ui/input"
import { Search, User, ShoppingCart } from "lucide-react";


export default function Header() {

  return (
    <nav className="w-full bg-white shadow-md px-10 py-4 flex justify-between items-center sticky top-0 z-50">

      {/* Project Title */}
      <p className="text-lg">Pricebyte</p>

      {/* Search Bar and Icons */}

      <div className="flex items-center gap-5 bg-white p-2 rounded-lg">
        <div className="relative flex items-center">
          <Search className="absolute left-3 text-gray-400" size={18} />
          <Input type="text" placeholder="Search products" className="pl-10 pr-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-gray-300"/>
        </div>
        <User className="text-gray-500 cursor-pointer hover:text-black" size={20} />
        <ShoppingCart className="text-gray-500 cursor-pointer hover:text-black" size={20} />
      </div>

      {/* Mobile Navigation (Sidebar) */}
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="ghost" size="icon" className="md:hidden">
            <Menu />
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="bg-[var(--grey-color)]">
          <div className="flex flex-col space-y-4 mt-6">
            {/* ADD PAGE LINKS */}
          </div>
        </SheetContent>
      </Sheet>
    </nav>
  );
}
