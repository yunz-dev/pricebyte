import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "PriceByte - Australia's Grocery Price Comparison",
    template: "%s | PriceByte"
  },
  description: "Australia's favourite way to compare grocery prices and save money on your weekly shop. Compare prices across Coles, Woolworths, ALDI, and more stores to find the best deals.",
  keywords: [
    "grocery prices",
    "price comparison", 
    "australia groceries",
    "coles prices",
    "woolworths prices", 
    "aldi prices",
    "supermarket deals",
    "grocery shopping",
    "price tracker",
    "food prices australia"
  ],
  authors: [{ name: "PriceByte Team" }],
  creator: "PriceByte",
  publisher: "PriceByte",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL("https://pricebyte.com.au"),
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "PriceByte - Australia's Grocery Price Comparison",
    description: "Compare grocery prices across Australia's major supermarkets and save money on your weekly shop. Free and open source.",
    url: "https://pricebyte.com.au",
    siteName: "PriceByte",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "PriceByte - Compare grocery prices across Australian supermarkets",
      },
    ],
    locale: "en_AU",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "PriceByte - Australia's Grocery Price Comparison",
    description: "Compare grocery prices across Australia's major supermarkets and save money on your weekly shop.",
    images: ["/og-image.png"],
    creator: "@pricebyte_au",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  icons: {
    icon: [
      { url: "/favicon.svg", type: "image/svg+xml" },
      { url: "/favicon.ico", sizes: "any" }
    ],
    shortcut: "/favicon.ico",
    apple: [
      { url: "/apple-icon-180.png", sizes: "180x180", type: "image/png" }
    ],
  },
  manifest: "/manifest.json",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
