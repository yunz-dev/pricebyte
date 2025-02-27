
import Link from 'next/link';
import { ShoppingCart, Mail, Phone, MapPin, Github, Heart } from 'lucide-react';

export default function Footer() {
    return (
      <footer className="bg-blue-900 text-white mt-16">
        {/* Open Source Support Banner */}
        <div className="bg-gradient-to-r from-blue-800 to-blue-600 py-6">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <div className="flex items-center justify-center gap-3 mb-3">
              <Github className="w-6 h-6" />
              <h3 className="text-xl font-bold">Free & Open Source</h3>
              <Heart className="w-5 h-5 text-red-400" />
            </div>
            <p className="text-blue-100 mb-4">
              PriceByte is completely free to use and open source. Help us improve by contributing to the project on GitHub!
            </p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <a 
                href="https://github.com/yunz-dev/pricebyte" 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-white text-blue-600 px-6 py-3 rounded-full font-semibold hover:bg-gray-100 transition-colors"
              >
                <Github className="w-5 h-5" />
                Star on GitHub
              </a>
              <a 
                href="https://github.com/yunz-dev/pricebyte/issues" 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-blue-700 text-white px-6 py-3 rounded-full font-semibold hover:bg-blue-800 transition-colors border border-blue-500"
              >
                Report Issues
              </a>
            </div>
          </div>
        </div>
        
        <div className="max-w-7xl mx-auto px-4 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Brand Section */}
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
                  <ShoppingCart className="w-4 h-4 text-blue-600" />
                </div>
                <span className="text-xl font-bold">PriceByte</span>
              </div>
              <p className="text-blue-200 text-sm leading-relaxed">
                Australia's favourite way to compare grocery prices and save money on your weekly shop.
              </p>
              <div className="flex gap-4">
                <div className="w-8 h-8 bg-blue-800 rounded-full flex items-center justify-center hover:bg-blue-700 cursor-pointer transition-colors">
                  <span className="text-xs font-bold">f</span>
                </div>
                <div className="w-8 h-8 bg-blue-800 rounded-full flex items-center justify-center hover:bg-blue-700 cursor-pointer transition-colors">
                  <span className="text-xs font-bold">t</span>
                </div>
                <div className="w-8 h-8 bg-blue-800 rounded-full flex items-center justify-center hover:bg-blue-700 cursor-pointer transition-colors">
                  <span className="text-xs font-bold">in</span>
                </div>
              </div>
            </div>

            {/* Quick Links */}
            <div className="space-y-4">
              <h3 className="font-semibold text-lg">Quick Links</h3>
              <div className="space-y-2">
                <Link href="/" className="block text-blue-200 hover:text-white transition-colors text-sm">
                  Browse Products
                </Link>
                <Link href="/" className="block text-blue-200 hover:text-white transition-colors text-sm">
                  Specials & Offers
                </Link>
                <Link href="/" className="block text-blue-200 hover:text-white transition-colors text-sm">
                  Price Alerts
                </Link>
                <Link href="/" className="block text-blue-200 hover:text-white transition-colors text-sm">
                  Shopping Lists
                </Link>
              </div>
            </div>

            {/* Customer Service */}
            <div className="space-y-4">
              <h3 className="font-semibold text-lg">Customer Service</h3>
              <div className="space-y-2">
                <Link href="/" className="block text-blue-200 hover:text-white transition-colors text-sm">
                  Help & Support
                </Link>
                <Link href="/" className="block text-blue-200 hover:text-white transition-colors text-sm">
                  Contact Us
                </Link>
                <Link href="/" className="block text-blue-200 hover:text-white transition-colors text-sm">
                  Privacy Policy
                </Link>
                <Link href="/" className="block text-blue-200 hover:text-white transition-colors text-sm">
                  Terms & Conditions
                </Link>
              </div>
            </div>

            {/* Contact Info */}
            <div className="space-y-4">
              <h3 className="font-semibold text-lg">Get in Touch</h3>
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-blue-200 text-sm">
                  <Phone className="w-4 h-4" />
                  <span>1800 PRICEBYTE</span>
                </div>
                <div className="flex items-center gap-2 text-blue-200 text-sm">
                  <Mail className="w-4 h-4" />
                  <span>help@pricebyte.com.au</span>
                </div>
                <div className="flex items-start gap-2 text-blue-200 text-sm">
                  <MapPin className="w-4 h-4 mt-0.5" />
                  <span>Sydney, NSW<br />Australia</span>
                </div>
              </div>
            </div>
          </div>

          {/* Bottom Section */}
          <div className="border-t border-blue-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
            <div className="text-blue-200 text-sm mb-4 md:mb-0">
              © 2025 PriceByte. All rights reserved.
            </div>
            <div className="flex gap-6 text-blue-200 text-sm">
              <Link href="/" className="hover:text-white transition-colors">
                Privacy
              </Link>
              <Link href="/" className="hover:text-white transition-colors">
                Terms
              </Link>
              <Link href="/" className="hover:text-white transition-colors">
                Accessibility
              </Link>
            </div>
          </div>
        </div>
      </footer>
    );
}