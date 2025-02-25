'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from "@/components/ui/button";
import { Sheet, SheetTrigger, SheetContent } from "@/components/ui/sheet";
import { Menu } from "lucide-react";
import { Input } from "@/components/ui/input"
import { Search, User, ShoppingCart } from "lucide-react";


export default function Header() {
  const [searchQuery, setSearchQuery] = useState('');
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  return (
    <nav className="w-full bg-white shadow-md px-10 py-4 flex items-center sticky top-0 z-50">

      {/* Project Title - Left */}
      <div className="flex-shrink-0">
        <Link href="/" className="text-lg font-semibold hover:text-blue-600 transition-colors">
          Pricebyte
        </Link>
      </div>

      {/* Search Bar - Center */}
      <div className="flex-1 flex justify-center px-8">
        <form onSubmit={handleSearch} className="relative flex items-center max-w-2xl w-full">
          <Search className="absolute left-4 text-gray-400" size={20} />
          <Input 
            type="text" 
            placeholder="Search products" 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full h-12 pl-12 pr-6 text-lg border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm"
          />
        </form>
      </div>

      {/* Icons - Right */}
      <div className="flex items-center gap-5 flex-shrink-0">
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