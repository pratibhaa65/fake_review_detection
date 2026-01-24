"use client";

import { useEffect, useState } from "react";
import ProductCard from "../components/ProductCard";
import SectionTitle from "../components/SectionTitle";

const ProductsPage = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState(["All"]);
  const [selectedCategory, setSelectedCategory] = useState("All");

  /* ---------------- FETCH PRODUCTS ---------------- */
  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/products`)
      .then((res) => res.json())
      .then(setProducts)
      .catch(() => {});
  }, []);

  /* ---------------- FETCH CATEGORIES ---------------- */
  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/categories`)
      .then((res) => res.json())
      .then((data) => setCategories(["All", ...data]))
      .catch(() => {});
  }, []);

  /* ---------------- FILTER PRODUCTS ---------------- */
  const filteredProducts =
    selectedCategory === "All"
      ? products
      : products.filter((p) => p.category === selectedCategory);

  return (
    <div className="max-w-7xl mx-auto px-6 py-16">
      <SectionTitle
        title="All Products"
        subtitle="Browse products by category"
      />

      {/* ================= CATEGORY FILTER ================= */}
      <div className="flex flex-wrap gap-3 mb-10 justify-center">
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => setSelectedCategory(category)}
            className={`px-4 py-2 rounded-full text-sm font-medium border transition
              ${
                selectedCategory === category
                  ? "bg-indigo-600 text-white border-indigo-600"
                  : "bg-white text-gray-700 border-gray-300 hover:bg-gray-100"
              }
            `}
          >
            {category}
          </button>
        ))}
      </div>

      {/* ================= PRODUCT GRID ================= */}
      {filteredProducts.length === 0 ? (
        <p className="text-center text-gray-500 mt-20">
          No products found in this category.
        </p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 auto-rows-fr">

          {filteredProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </div>
  );
};

export default ProductsPage;
