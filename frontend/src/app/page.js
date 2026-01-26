"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import ProductCard from "./components/ProductCard";
import SectionTitle from "./components/SectionTitle";

export default function Home() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/products`)
      .then((res) => res.json())
      .then((data) => {
        setProducts(data.slice(0, 6));
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800 text-white">

      {/* ================= HERO SECTION ================= */}
      <section className="max-w-6xl mx-auto px-6 py-24 text-center">
        <h1 className="text-5xl font-extrabold leading-tight mb-6">
          Detect Fake Reviews <br />
          <span className="text-indigo-400">
            Before They Mislead Customers
          </span>
        </h1>

        <p className="text-gray-300 text-lg max-w-3xl mx-auto mb-10">
          An AI-powered Fake Review Detection System that analyzes product reviews, ratings, and behavior
          patterns to ensure trust and authenticity.
        </p>

        <div className="flex justify-center gap-6">
          <Link
            href="/create"
            className="bg-indigo-500 hover:bg-indigo-600 text-white px-8 py-3 rounded-lg font-semibold transition"
          >
            ➕ Create Product
          </Link>

          <Link
            href="/products"
            className="bg-white text-indigo-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100"
          >
            Browse Products
          </Link>
        </div>
      </section>

      {/* ================= FEATURED PRODUCTS ================= */}
      <section className="bg-gray-100 py-20 text-gray-800">
        <div className="max-w-6xl mx-auto px-6">

          <SectionTitle
            title="Featured Products"
          />

          {loading && (
            <p className="text-center text-gray-500 mt-10">
              Loading products...
            </p>
          )}

          {!loading && products.length === 0 && (
            <p className="text-center text-gray-500 mt-10">
              No products available
            </p>
          )}

          {/* <div className="grid md:grid-cols-3 gap-8 mt-10"> */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 auto-rows-fr">

            {products.slice(0,4).map((product) => (
              <ProductCard
                key={product.id}
                product={product}
              />
            ))}
          </div>

          <div className="text-center mt-12">
            <Link
              href="/products"
              className="bg-indigo-500 hover:bg-indigo-600 text-white px-8 py-3 rounded-lg font-semibold transition"
            >
              View All Products →
            </Link>
          </div>
        </div>
      </section>

      {/* ================= FEATURES ================= */}
      <section className="bg-white text-gray-800 py-20">
        <div className="max-w-6xl mx-auto px-6">
          <SectionTitle
            title="Why Use Our System?"
          />

          <div className="grid md:grid-cols-3 gap-10">
            {[
              {
                title: "🔍 Smart Review Analysis",
                text: "Analyze reviews using AI techniques to detect fake or suspicious review behavior."
              },
              {
                title: "⭐ Rating Validation",
                text: "Strict 1–5 rating enforcement to prevent manipulation."
              },
              {
                title: "🛡️ Secure & Reliable",
                text: "Built with clean backend validation and a structured database for data integrity."
              }
            ].map((feature, idx) => (
              <div
                key={idx}
                className="bg-gray-50 p-8 rounded-xl shadow hover:shadow-lg transition"
              >
                <h3 className="text-xl font-semibold mb-4">
                  {feature.title}
                </h3>
                <p className="text-gray-600">{feature.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ================= CALL TO ACTION ================= */}
      <section className="py-24 text-center bg-slate-900">
        <h2 className="text-4xl font-bold mb-6">
          Start Building Trust Today
        </h2>

        <p className="text-gray-300 mb-8">
          Add products, collect reviews, and analyze authenticity with ease.
        </p>

        <Link
          href="/create"
          className="bg-indigo-500 hover:bg-indigo-600 text-white px-10 py-4 rounded-lg font-semibold transition"
        >
          Get Started 🚀
        </Link>
      </section>
    </main>
  );
}
