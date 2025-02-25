'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import { ChevronRight, ChevronLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import Header from '@/components/header';
import Footer from '@/components/footer';

interface SearchResult {
  id: number;
  name: string;
  brand: string;
  category: string;
  size: string;
  unit: string;
  image_url: string;
  description: string;
  similarity_score: number;
  created_at: string;
  updated_at: string;
}

interface SearchResponse {
  results: SearchResult[];
  total_count: number;
  offset: number;
  limit: number;
  has_next: boolean;
}

export default function SearchPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const query = searchParams.get('q') || '';
  const page = parseInt(searchParams.get('page') || '1');
  const limit = 12;
  const offset = (page - 1) * limit;

  useEffect(() => {
    if (query) {
      performSearch(query, offset);
    }
  }, [query, offset]);

  const performSearch = async (searchTerm: string, searchOffset: number = 0) => {
    if (!searchTerm.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `/api/products/search?q=${encodeURIComponent(searchTerm)}&offset=${searchOffset}&limit=${limit}`
      );

      if (!response.ok) {
        throw new Error('Search failed');
      }

      const data: SearchResponse = await response.json();
      setSearchResults(data);
    } catch (err) {
      setError('Failed to search products. Please try again.');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (newPage: number) => {
    const params = new URLSearchParams(searchParams);
    params.set('page', newPage.toString());
    router.push(`/search?${params.toString()}`);
  };

  const totalPages = searchResults ? Math.ceil(searchResults.total_count / limit) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Header />

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {query && (
          <div className="mb-6">
            <h1 className="text-2xl font-semibold text-gray-900 mb-2">
              Search results for "{query}"
            </h1>
          </div>
        )}

        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        )}

        {error && (
          <div className="text-center py-12">
            <p className="text-red-600 mb-4">{error}</p>
            <Button onClick={() => performSearch(query, offset)}>
              Try again
            </Button>
          </div>
        )}

        {searchResults && searchResults.results.length > 0 && (
          <>
            {/* Results Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
              {searchResults.results.map((product) => (
                <Link key={product.id} href={`/product/${product.id}`}>
                  <Card className="h-full hover:shadow-lg transition-shadow cursor-pointer">
                    <CardContent className="p-4">
                      <div className="aspect-square relative mb-4 bg-gray-100 rounded-lg overflow-hidden">
                        <Image
                          src={product.image_url || '/placeholder-product.jpg'}
                          alt={product.name}
                          fill
                          className="object-cover"
                          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw"
                        />
                      </div>
                      
                      <div className="space-y-2">
                        <h3 className="font-semibold text-gray-900 line-clamp-2 text-sm">
                          {product.name}
                        </h3>
                        
                        <p className="text-sm text-gray-600">
                          {product.brand} • {product.size}{product.unit}
                        </p>
                        
                        <p className="text-xs text-gray-500 line-clamp-2">
                          {product.description}
                        </p>
                        
                        <div className="flex items-center justify-between">
                          <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                            {product.category}
                          </span>
                          <span className="text-xs text-gray-500">
                            {Math.round(product.similarity_score * 100)}% match
                          </span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handlePageChange(page - 1)}
                  disabled={page <= 1}
                >
                  <ChevronLeft className="w-4 h-4" />
                  Previous
                </Button>
                
                <div className="flex items-center gap-2">
                  {Array.from({ length: Math.min(10, totalPages) }, (_, i) => {
                    let pageNum;
                    if (totalPages <= 10) {
                      pageNum = i + 1;
                    } else if (page <= 5) {
                      pageNum = i + 1;
                    } else if (page >= totalPages - 4) {
                      pageNum = totalPages - 9 + i;
                    } else {
                      pageNum = page - 4 + i;
                    }
                    
                    return (
                      <Button
                        key={pageNum}
                        variant={page === pageNum ? "default" : "outline"}
                        size="sm"
                        onClick={() => handlePageChange(pageNum)}
                        className="w-8 h-8 p-0"
                      >
                        {pageNum}
                      </Button>
                    );
                  })}
                </div>
                
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handlePageChange(page + 1)}
                  disabled={page >= totalPages}
                >
                  Next
                  <ChevronRight className="w-4 h-4" />
                </Button>
              </div>
            )}
          </>
        )}

        {searchResults && searchResults.results.length === 0 && !loading && (
          <div className="text-center py-12">
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              No products found
            </h2>
            <p className="text-gray-600 mb-4">
              Try adjusting your search terms or browse our categories.
            </p>
            <Link href="/">
              <Button>Back to home</Button>
            </Link>
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
}