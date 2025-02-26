'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Search, ShoppingCart } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import Footer from '@/components/footer';

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
    <div className="h-screen overflow-hidden bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 text-white flex items-center px-4">
      <div className="max-w-6xl mx-auto text-center w-full">
        {/* Logo/Brand */}
        <div className="mb-16">
          <div className="flex items-center justify-center gap-4 mb-8">
            <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center shadow-2xl">
              <ShoppingCart className="w-10 h-10 text-blue-600" />
            </div>
            <h1 className="text-8xl font-black tracking-tight">PriceByte</h1>
          </div>
          <p className="text-3xl text-blue-100 font-light leading-relaxed">
            Australia's favourite way to compare grocery prices
          </p>
        </div>

        {/* Search Form */}
        <form onSubmit={handleSearch} className="mb-12">
          <div className="relative max-w-4xl mx-auto">
            <div className="relative">
              <Input
                type="text"
                placeholder="Search thousands of products..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full h-20 pl-8 pr-24 text-2xl rounded-full border-0 focus:ring-4 focus:ring-blue-300/50 shadow-2xl bg-white text-gray-900 font-medium placeholder:text-gray-500"
              />
              <Button
                type="submit"
                size="lg"
                className="absolute right-3 top-3 h-14 w-14 rounded-full p-0 bg-blue-600 hover:bg-blue-700 shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-200"
              >
                <Search className="w-7 h-7" />
              </Button>
            </div>
          </div>
        </form>

        {/* Quick Search Suggestions */}
        <div>
          <p className="text-2xl text-blue-100 mb-8 font-light">Popular searches:</p>
          <div className="flex flex-wrap justify-center gap-4">
            {['Bananas', 'Milk', 'Bread', 'Chicken', 'Rice'].map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => {
                  setSearchQuery(suggestion);
                  router.push(`/search?q=${encodeURIComponent(suggestion)}`);
                }}
                className="px-8 py-4 text-lg font-medium bg-white/15 hover:bg-white/25 rounded-full transition-all duration-200 backdrop-blur-sm border border-white/20 hover:border-white/40 transform hover:scale-105 hover:shadow-xl"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
