"use client";

import { useState } from "react";
import ReviewForm from "../reviews";
import ReviewModal from "@/app/components/ReviewModal";

export default function ProductClient({ product }) {
  const [selectedReview, setSelectedReview] = useState(null);

  return (
    <div className="bg-gray-50 min-h-screen">
      <div className="max-w-4xl mx-auto px-6 py-16 space-y-14">

        {/* ================= PRODUCT HEADER ================= */}
        <div className="bg-white rounded-2xl shadow-md p-10 space-y-6">
          <div className="flex items-center gap-6">
            <div className="w-20 h-20 rounded-xl bg-indigo-600 text-white flex items-center justify-center text-3xl font-bold">
              {product.name?.charAt(0)}
            </div>

            <div>
              <h1 className="text-4xl font-bold">{product.name}</h1>
              <p className="text-gray-600 mt-1">
                Category:{" "}
                <span className="text-indigo-600 font-medium">
                  {product.category}
                </span>
              </p>
            </div>
          </div>

          <p className="text-gray-700 leading-relaxed">
            {product.description}
          </p>

          <span className="text-3xl font-bold text-indigo-600">
            Rs. {product.price}
          </span>
        </div>

        {/* ================= REVIEWS GRID ================= */}
        <div className="bg-white rounded-2xl shadow-md p-10 space-y-6">
          <h2 className="text-2xl font-semibold">Customer Reviews</h2>

          {product.reviews?.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {product.reviews.map((review) => (
                <div
                  key={review.review_id}
                  onClick={() => setSelectedReview(review)}
                  className="border rounded-xl p-5 cursor-pointer hover:shadow transition"
                >
                  <div className="flex justify-between mb-2">
                    <span className="font-semibold">{review.reviewer}</span>
                    <span className="text-sm text-indigo-600">
                      ⭐ {review.rating}/5
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm line-clamp-3">
                    {review.review}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">No reviews yet.</p>
          )}
        </div>

        {/* ================= REVIEW FORM ================= */}
        <div className="bg-white rounded-2xl shadow-md p-10">
          <h2 className="text-2xl font-semibold mb-4">Add a Review</h2>
          <ReviewForm productId={product.id} />
        </div>

        {/* ================= REVIEW MODAL ================= */}
        {selectedReview && (
          <ReviewModal
            review={selectedReview}
            onClose={() => setSelectedReview(null)}
          />
        )}
      </div>
    </div>
  );
}
