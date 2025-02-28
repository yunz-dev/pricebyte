'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import { ChevronRight, ChevronLeft, ShoppingCart } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import Header from '@/components/header';
import Footer from '@/components/footer';
import { SearchResultsSkeleton } from '@/components/skeletons';

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

// Simple in-memory cache for search results
const searchCache = new Map<string, { data: SearchResponse; timestamp: number }>();
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes
const REQUEST_TIMEOUT = 10000; // 10 seconds

export default function SearchPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const query = searchParams.get('q') || '';
  const page = parseInt(searchParams.get('page') || '1');
  const limit = 12;
  const offset = (page - 1) * limit;

  const performSearch = useCallback(async (searchTerm: string, searchOffset: number = 0) => {
    if (!searchTerm.trim()) return;

    // Cancel previous request if it exists
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    // Create cache key
    const cacheKey = `${searchTerm.trim().toLowerCase()}-${searchOffset}-${limit}`;

    // Check cache first
    const cached = searchCache.get(cacheKey);
    if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
      console.log('Using cached search results');
      setSearchResults(cached.data);
      setError(null);
      return;
    }

    setLoading(true);
    setError(null);

    // Create new abort controller for this request
    const controller = new AbortController();
    abortControllerRef.current = controller;

    try {
      const response = await fetch(
        `/api/products/search?q=${encodeURIComponent(searchTerm)}&offset=${searchOffset}&limit=${limit}`,
        {
          signal: controller.signal,
          headers: {
            'Content-Type': 'application/json',
          }
        }
      );

      if (!response.ok) {
        throw new Error(`Search failed: ${response.status}`);
      }

      const data: SearchResponse = await response.json();

      // Cache the results
      searchCache.set(cacheKey, { data, timestamp: Date.now() });

      // Clean old cache entries (keep only last 50 entries)
      if (searchCache.size > 50) {
        const oldestKey = Array.from(searchCache.keys())[0];
        searchCache.delete(oldestKey);
      }

      setSearchResults(data);
    } catch (err) {
      if (err instanceof Error && err.name === 'AbortError') {
        console.log('Search request was cancelled');
        return; // Don't set error for cancelled requests
      }

      setError('Search is taking longer than usual. Please try again.');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
      abortControllerRef.current = null;
    }
  }, [limit]);

  useEffect(() => {
    if (query) {
      performSearch(query, offset);
    }
  }, [query, offset, performSearch]);

  // Cleanup function to cancel requests on unmount
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  const handlePageChange = (newPage: number) => {
    const params = new URLSearchParams(searchParams);
    params.set('page', newPage.toString());
    router.push(`/search?${params.toString()}`);
  };

  const totalPages = searchResults ? Math.ceil(searchResults.total_count / limit) : 0;

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header />

      {/* Content */}
      <div className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        {query && (
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Search results for "{query}"
            </h1>
            <div className="h-1 w-16 bg-blue-600 rounded-full"></div>
          </div>
        )}

        {loading && (
          <>
            <div className="flex items-center justify-center mb-4">
              <div className="flex items-center gap-2 text-blue-600">
                <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                <span className="text-sm font-medium">Searching products...</span>
              </div>
            </div>
            <SearchResultsSkeleton />
          </>
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
                  <Card className="h-full hover:shadow-xl hover:scale-105 transition-all duration-200 cursor-pointer border-0 shadow-md">
                    <CardContent className="p-5">
                      <div className="aspect-square relative mb-4 bg-gray-50 rounded-xl overflow-hidden flex items-center justify-center">
                        {product.image_url ? (
                          <Image
                            src={product.image_url}
                            alt={product.name}
                            fill
                            className="object-cover"
                            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw"
                            onError={(e) => {
                              const target = e.target as HTMLImageElement;
                              target.style.display = 'none';
                              const parent = target.parentElement;
                              if (parent && !parent.querySelector('.fallback-icon')) {
                                const fallback = document.createElement('div');
                                fallback.className = 'fallback-icon flex items-center justify-center w-full h-full';
                                fallback.innerHTML = '<svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25L5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z"/></svg>';
                                parent.appendChild(fallback);
                              }
                            }}
                          />
                        ) : (
                          <ShoppingCart className="w-12 h-12 text-gray-400" />
                        )}
                      </div>

                      <div className="space-y-3">
                        <h3 className="font-bold text-gray-900 line-clamp-2 text-base leading-tight">
                          {product.name}
                        </h3>

                        <p className="text-sm text-gray-600 font-medium">
                          {/* {product.brand} • {product.size}{product.unit} */}
                          {product.brand} • {product.size}
                        </p>

                        <p className="text-xs text-gray-500 line-clamp-2 leading-relaxed">
                          {product.description}
                        </p>

                        <div className="flex items-center justify-between pt-2">
                          <span className="text-xs bg-blue-600 text-white px-3 py-1 rounded-full font-medium">
                            {product.category}
                          </span>
                          <span className="text-xs text-blue-600 font-semibold">
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
              <div className="flex items-center justify-center gap-2 bg-white p-6 rounded-xl shadow-sm">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handlePageChange(page - 1)}
                  disabled={page <= 1}
                  className="border-blue-200 text-blue-600 hover:bg-blue-50"
                >
                  <ChevronLeft className="w-4 h-4" />
                  Previous
                </Button>

                <div className="flex items-center gap-2">
                  {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                    let pageNum;
                    if (totalPages <= 5) {
                      pageNum = i + 1;
                    } else if (page <= 3) {
                      pageNum = i + 1;
                    } else if (page >= totalPages - 2) {
                      pageNum = totalPages - 4 + i;
                    } else {
                      pageNum = page - 2 + i;
                    }

                    return (
                      <Button
                        key={pageNum}
                        variant={page === pageNum ? "default" : "outline"}
                        size="sm"
                        onClick={() => handlePageChange(pageNum)}
                        className={`w-8 h-8 p-0 ${page === pageNum
                            ? "bg-blue-600 hover:bg-blue-700 border-blue-600"
                            : "border-blue-200 text-blue-600 hover:bg-blue-50"
                          }`}
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
                  className="border-blue-200 text-blue-600 hover:bg-blue-50"
                >
                  Next
                  <ChevronRight className="w-4 h-4" />
                </Button>
              </div>
            )}
          </>
        )}

        {!query.trim() && !loading && (
          <div className="flex flex-col items-center justify-center min-h-[60vh] px-4">
            <div className="max-w-2xl text-center">
              <div className="w-32 h-32 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-8">
                <div className="w-16 h-16 text-blue-600">
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <circle cx="12" cy="12" r="10" />
                    <circle cx="8" cy="10" r="1.5" fill="white" />
                    <circle cx="16" cy="10" r="1.5" fill="white" />
                    <path d="M8 16s1.5-2 4-2 4 2 4 2" stroke="white" strokeWidth="2" fill="none" strokeLinecap="round" />
                  </svg>
                </div>
              </div>
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                You searched nothing! 🤷‍♂️
              </h2>
              <p className="text-xl text-gray-600 mb-10 leading-relaxed">
                Looks like you forgot to tell us what you're looking for!
                <br />Don't worry, it happens to the best of us.
              </p>
              <div className="space-y-6">
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Link href="/">
                    <Button size="lg" className="bg-blue-600 hover:bg-blue-700 px-8 py-4 text-lg font-semibold">
                      Back to Home
                    </Button>
                  </Link>
                </div>
                <div className="bg-white rounded-xl p-6 border shadow-sm">
                  <p className="text-sm font-medium text-gray-700 mb-3">Try these popular searches:</p>
                  <div className="flex flex-wrap justify-center gap-2">
                    {['Bananas', 'Milk', 'Bread', 'Chicken', 'Rice', 'Eggs'].map((suggestion) => (
                      <button
                        key={suggestion}
                        onClick={() => router.push(`/search?q=${encodeURIComponent(suggestion)}`)}
                        className="px-4 py-2 text-sm bg-blue-50 text-blue-700 hover:bg-blue-100 rounded-full transition-colors border border-blue-200"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {searchResults && searchResults.results.length === 0 && !loading && query.trim() && (
          <div className="flex flex-col items-center justify-center min-h-[60vh] px-4">
            <div className="max-w-2xl text-center">
              <div className="w-32 h-32 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-8">
                <div className="w-16 h-16 text-blue-600">
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <circle cx="12" cy="12" r="10" />
                    <circle cx="8" cy="10" r="1.5" fill="white" />
                    <circle cx="16" cy="10" r="1.5" fill="white" />
                    <path d="M8 16s1.5-2 4-2 4 2 4 2" stroke="white" strokeWidth="2" fill="none" strokeLinecap="round" />
                  </svg>
                </div>
              </div>
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                No products found
              </h2>
              <p className="text-xl text-gray-600 mb-10 leading-relaxed">
                We couldn't find any products matching "<span className="font-bold text-gray-900 bg-gray-100 px-2 py-1 rounded">{query}</span>".
                <br />Try adjusting your search terms or browse our popular categories.
              </p>
              <div className="space-y-6">
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Link href="/">
                    <Button size="lg" className="bg-blue-600 hover:bg-blue-700 px-8 py-4 text-lg font-semibold">
                      Back to Home
                    </Button>
                  </Link>
                  <Button
                    size="lg"
                    variant="outline"
                    className="px-8 py-4 text-lg border-2 border-blue-600 text-blue-600 hover:bg-blue-50"
                    onClick={() => router.push('/search?q=')}
                  >
                    Browse All Products
                  </Button>
                </div>
                <div className="bg-white rounded-xl p-6 border shadow-sm">
                  <p className="text-sm font-medium text-gray-700 mb-3">Try these popular searches:</p>
                  <div className="flex flex-wrap justify-center gap-2">
                    {['Bananas', 'Milk', 'Bread', 'Chicken', 'Rice', 'Eggs'].map((suggestion) => (
                      <button
                        key={suggestion}
                        onClick={() => router.push(`/search?q=${encodeURIComponent(suggestion)}`)}
                        className="px-4 py-2 text-sm bg-blue-50 text-blue-700 hover:bg-blue-100 rounded-full transition-colors border border-blue-200"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
}
