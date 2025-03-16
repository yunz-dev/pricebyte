import { NextRequest, NextResponse } from 'next/server';

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

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const q = searchParams.get('q') || '';
    const offset = parseInt(searchParams.get('offset') || '0');
    const limit = parseInt(searchParams.get('limit') || '10');

    if (!q.trim()) {
      return NextResponse.json({
        results: [],
        total_count: 0,
        offset,
        limit,
        has_next: false
      });
    }

    // Fetch from your external API with timeout
    const externalApiUrl = process.env.EXTERNAL_API_URL || 'http://localhost:8080';
    const apiUrl = `${externalApiUrl}/api/products/search?q=${encodeURIComponent(q)}&offset=${offset}&limit=${limit}`;
    
    // Create timeout controller
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
    
    try {
      const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json',
        },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`External API error: ${response.status} ${response.statusText}`);
      }

      const data: SearchResponse = await response.json();
      return NextResponse.json(data);
    } catch (fetchError) {
      clearTimeout(timeoutId);
      
      if (fetchError instanceof Error && fetchError.name === 'AbortError') {
        console.error('Search request timed out');
        return NextResponse.json(
          { error: 'Search request timed out. Please try again.' },
          { status: 504 }
        );
      }
      throw fetchError;
    }

  } catch (error) {
    console.error('Error searching products:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}