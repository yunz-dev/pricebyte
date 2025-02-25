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

    // Fetch from your external API
    const externalApiUrl = process.env.EXTERNAL_API_URL || 'http://localhost:8000';
    const apiUrl = `${externalApiUrl}/api/products/search?q=${encodeURIComponent(q)}&offset=${offset}&limit=${limit}`;
    
    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'accept': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: SearchResponse = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error('Error searching products:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}