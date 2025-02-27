'use client';

import { useState, useMemo, useCallback } from 'react';
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

  const handleSearch = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  }, [searchQuery, router]);

  // Optimized search query handling
  const optimizedSearchQuery = useMemo(() => {
    return searchQuery.trim();
  }, [searchQuery]);

  return (
    <nav className="w-full bg-blue-600 shadow-lg px-6 py-3 grid grid-cols-3 items-center sticky top-0 z-50">

      {/* Project Title - Left */}
      <div className="flex justify-start">
        <Link href="/" className="flex items-center gap-2 hover:opacity-90 transition-opacity">
          <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
            <ShoppingCart className="w-5 h-5 text-blue-600" />
          </div>
          <span className="text-xl font-bold text-white">PriceByte</span>
        </Link>
      </div>

      {/* Search Bar - Center */}
      <div className="flex justify-center">
        <form onSubmit={handleSearch} className="relative flex items-center max-w-2xl w-full">
          <Search className="absolute left-4 text-gray-400" size={20} />
          <Input 
            type="text" 
            placeholder="Search products, recipes & ideas" 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full h-11 pl-12 pr-6 text-base border-0 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-300 shadow-sm bg-white"
          />
        </form>
      </div>

      {/* Navigation Links - Right */}
      <div className="flex items-center justify-end gap-6">
        <div className="hidden lg:flex items-center gap-4 text-white text-sm font-medium">
          <Link href="/" className="hover:text-blue-200 transition-colors whitespace-nowrap">Browse products</Link>
          <Link href="/" className="hover:text-blue-200 transition-colors whitespace-nowrap">Specials & offers</Link>
          <Link href="/" className="hover:text-blue-200 transition-colors">Help</Link>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-1 text-white text-sm">
            <User className="w-5 h-5" />
            <span className="hidden md:inline whitespace-nowrap">My Account</span>
          </div>
          <div className="relative">
            <ShoppingCart className="w-6 h-6 text-white cursor-pointer hover:text-blue-200 transition-colors" />
            <span className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold">
              0
            </span>
          </div>
        </div>
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