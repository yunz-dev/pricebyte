'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Search, ShoppingCart } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('');
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-to-b from-blue-50 to-white">
      <div className="w-full max-w-2xl text-center">
        {/* Logo/Brand */}
        <div className="mb-8">
          <div className="flex items-center justify-center gap-2 mb-4">
            <ShoppingCart className="w-8 h-8 text-blue-600" />
            <h1 className="text-4xl font-bold text-gray-900">PriceByte</h1>
          </div>
          <p className="text-lg text-gray-600">Compare prices across stores</p>
        </div>

        {/* Search Form */}
        <form onSubmit={handleSearch} className="mb-8">
          <div className="relative max-w-xl mx-auto">
            <div className="relative">
              <Input
                type="text"
                placeholder="Search for products..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full h-12 pl-4 pr-12 text-lg rounded-full border-2 border-gray-200 focus:border-blue-500 focus:ring-0 shadow-lg"
              />
              <Button
                type="submit"
                size="sm"
                className="absolute right-1 top-1 h-10 w-10 rounded-full p-0"
              >
                <Search className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </form>

        {/* Quick Search Suggestions */}
        <div className="mb-8">
          <p className="text-sm text-gray-500 mb-3">Popular searches:</p>
          <div className="flex flex-wrap justify-center gap-2">
            {['Bananas', 'Milk', 'Bread', 'Chicken', 'Rice'].map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => {
                  setSearchQuery(suggestion);
                  router.push(`/search?q=${encodeURIComponent(suggestion)}`);
                }}
                className="px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-full transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <div className="text-center">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <Search className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Smart Search</h3>
            <p className="text-sm text-gray-600">Find products across multiple stores instantly</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <ShoppingCart className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Price Compare</h3>
            <p className="text-sm text-gray-600">Compare prices to find the best deals</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <span className="text-purple-600 font-bold">$</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Save Money</h3>
            <p className="text-sm text-gray-600">Track price history and save on groceries</p>
          </div>
        </div>
      </div>
    </div>
  );
}
