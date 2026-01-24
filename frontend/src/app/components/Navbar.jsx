"use client";

import Link from "next/link";

const Navbar = () => {
  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-indigo-600">
          FakeReviewAI
        </Link>

        <div className="space-x-10 text-sm font-medium">
          <Link href="/" className="hover:text-indigo-600">
            HOME
          </Link>
          <Link href="/create" className="hover:text-indigo-600">
            NEW PRODUCT
          </Link>
          <Link href="/products" className="hover:text-indigo-600">
            ALL PRODUCTS
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
