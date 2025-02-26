export function ProductCardSkeleton() {
  return (
    <div className="h-full border-0 shadow-md rounded-2xl overflow-hidden">
      <div className="p-5 animate-pulse">
        <div className="aspect-square bg-gray-200 rounded-xl mb-4"></div>
        <div className="space-y-3">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-3 bg-gray-200 rounded w-1/2"></div>
          <div className="h-3 bg-gray-200 rounded w-full"></div>
          <div className="flex items-center justify-between pt-2">
            <div className="h-6 bg-gray-200 rounded-full w-16"></div>
            <div className="h-3 bg-gray-200 rounded w-12"></div>
          </div>
        </div>
      </div>
    </div>
  );
}

export function SearchResultsSkeleton() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
      {Array.from({ length: 12 }, (_, i) => (
        <ProductCardSkeleton key={i} />
      ))}
    </div>
  );
}

export function ProductPageSkeleton() {
  return (
    <div className="container mx-auto px-4 py-6 max-w-7xl">
      <div className="grid lg:grid-cols-12 gap-6">
        
        {/* Left Column */}
        <div className="lg:col-span-7">
          <div className="sticky top-24 space-y-6">
            {/* Product Image Skeleton */}
            <div className="bg-white rounded-2xl p-8 shadow-sm border">
              <div className="aspect-square bg-gray-200 rounded-xl animate-pulse"></div>
            </div>

            {/* Price History Skeleton */}
            <div className="p-6 shadow-sm bg-white rounded-2xl border">
              <div className="animate-pulse">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-9 h-9 bg-gray-200 rounded-lg"></div>
                  <div className="h-6 bg-gray-200 rounded w-32"></div>
                </div>
                <div className="h-3 bg-gray-200 rounded w-3/4 mb-6"></div>
                <div className="h-64 bg-gray-200 rounded-lg mb-6"></div>
                
                {/* AI Insights Skeleton */}
                <div className="p-4 bg-gray-100 rounded-xl">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-8 h-8 bg-gray-200 rounded-lg"></div>
                    <div className="h-4 bg-gray-200 rounded w-20"></div>
                  </div>
                  <div className="space-y-2">
                    <div className="h-3 bg-gray-200 rounded w-full"></div>
                    <div className="h-3 bg-gray-200 rounded w-4/5"></div>
                    <div className="h-3 bg-gray-200 rounded w-full"></div>
                    <div className="h-3 bg-gray-200 rounded w-3/4"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="lg:col-span-5">
          <div className="bg-white rounded-2xl p-6 shadow-sm border mb-4">
            <div className="animate-pulse">
              {/* Product Header Skeleton */}
              <div className="mb-5">
                <div className="flex items-center gap-2 mb-3">
                  <div className="h-6 bg-gray-200 rounded-full w-16"></div>
                  <div className="h-6 bg-gray-200 rounded-full w-12"></div>
                </div>
                <div className="h-8 bg-gray-200 rounded w-3/4 mb-3"></div>
                <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-2/3"></div>
              </div>

              {/* Price Skeleton */}
              <div className="mb-6 p-4 bg-gray-100 rounded-xl">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="h-10 bg-gray-200 rounded w-24 mb-1"></div>
                    <div className="h-3 bg-gray-200 rounded w-32"></div>
                  </div>
                  <div className="text-right">
                    <div className="h-3 bg-gray-200 rounded w-16 mb-1"></div>
                    <div className="h-4 bg-gray-200 rounded w-20"></div>
                  </div>
                </div>
              </div>

              {/* Store Selection Skeleton */}
              <div className="mb-6">
                <div className="h-5 bg-gray-200 rounded w-32 mb-3"></div>
                <div className="space-y-3">
                  <div className="p-3 bg-gray-100 rounded-lg">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="h-4 bg-gray-200 rounded w-16 mb-1"></div>
                        <div className="h-3 bg-gray-200 rounded w-24"></div>
                      </div>
                      <div className="text-right">
                        <div className="h-5 bg-gray-200 rounded w-12 mb-1"></div>
                        <div className="h-3 bg-gray-200 rounded w-16"></div>
                      </div>
                    </div>
                  </div>
                  <div className="p-3 bg-gray-100 rounded-lg">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="h-4 bg-gray-200 rounded w-20 mb-1"></div>
                        <div className="h-3 bg-gray-200 rounded w-24"></div>
                      </div>
                      <div className="text-right">
                        <div className="h-5 bg-gray-200 rounded w-12 mb-1"></div>
                        <div className="h-3 bg-gray-200 rounded w-16"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Nutrition Facts Skeleton */}
          <div className="p-4 shadow-sm bg-white rounded-2xl border">
            <div className="animate-pulse">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 bg-gray-200 rounded-lg"></div>
                <div className="h-5 bg-gray-200 rounded w-28"></div>
              </div>
              <div className="h-3 bg-gray-200 rounded w-3/4 mb-4"></div>
              
              <div className="space-y-3">
                {Array.from({ length: 12 }, (_, i) => (
                  <div key={i} className="flex justify-between">
                    <div className="h-3 bg-gray-200 rounded w-20"></div>
                    <div className="h-3 bg-gray-200 rounded w-12"></div>
                    <div className="h-3 bg-gray-200 rounded w-12"></div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export function BreadcrumbSkeleton() {
  return (
    <div className="bg-white border-b">
      <div className="container mx-auto px-4 py-3 max-w-7xl">
        <div className="flex items-center space-x-2 animate-pulse">
          <div className="h-3 bg-gray-200 rounded w-12"></div>
          <div className="h-3 bg-gray-200 rounded w-1"></div>
          <div className="h-3 bg-gray-200 rounded w-16"></div>
          <div className="h-3 bg-gray-200 rounded w-1"></div>
          <div className="h-3 bg-gray-200 rounded w-32"></div>
        </div>
      </div>
    </div>
  );
}