"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export default function ReviewForm({ productId }) {
  const [review, setReview] = useState({
    reviewer: "",
    rating: "",
    review: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/products/${productId}/reviews`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(review),
        },
      );

      const data = await res.json();

      if (!res.ok) {
        if (res.status === 403) {
          setError(data.message || "Review detected as fake.");
        } else if (res.status === 429) {
          setError(data.message || "You already submitted this review recently. Please wait.");
        } else {
          setError(data.message || "Failed to submit review.");
        }
        return;
      }

      // ✅ Success
      setReview({ reviewer: "", rating: "", review: "" });
      router.refresh();
    } catch (err) {
      setError("Server not reachable. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-md space-y-4">
      {/* Name */}
      <div>
        <label className="block text-sm font-medium mb-1">Your Name</label>
        <input
          type="text"
          required
          value={review.reviewer}
          onChange={(e) => setReview({ ...review, reviewer: e.target.value })}
          className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500"
          placeholder="John Doe"
        />
      </div>

      {/* Rating */}
      <div>
        <label className="block text-sm font-medium mb-1">Rating</label>
        <select
          required
          value={review.rating}
          onChange={(e) => setReview({ ...review, rating: e.target.value })}
          className="w-full border rounded-lg px-3 py-2"
        >
          <option value="">Select rating</option>
          {[1, 2, 3, 4, 5].map((r) => (
            <option key={r} value={r}>
              {r} ⭐
            </option>
          ))}
        </select>
      </div>

      {/* Review */}
      <div>
        <label className="block text-sm font-medium mb-1">Review</label>
        <textarea
          rows="4"
          required
          value={review.review}
          onChange={(e) => setReview({ ...review, review: e.target.value })}
          className="w-full border rounded-lg px-3 py-2"
          placeholder="Write your experience..."
        />
      </div>

      {error && (
        <div className="text-sm text-red-600 bg-red-50 border border-red-200 p-3 rounded-lg">
          ⚠️ {error}
        </div>
      )}

      {/* Submit */}
      <button
        type="submit"
        disabled={loading}
        className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50"
      >
        {loading ? "Submitting..." : "Submit Review"}
      </button>
    </form>
  );
}
