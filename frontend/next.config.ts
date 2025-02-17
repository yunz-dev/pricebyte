import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'shop.coles.com.au',
        pathname: '**',
      },
    ],
  },
};

export default nextConfig;
