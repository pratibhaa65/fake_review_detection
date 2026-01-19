"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function ReviewForm({ productId }) {
  const [review, setReview] = useState({
    reviewer: "",
    rating: "",
    review: "",
  });

  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/reviews`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ id: productId, ...review }),
        },
      );

      if (res.ok) {
        alert("Review added");
        setReview({ reviewer: "", rating: "", review: "" });
        router.refresh();
      } else {
        const errorData = await res.json();
        alert(`Error: ${errorData.message}`);
      }
    } catch (error) {
      alert("An unexpected error occurred. Please try again later.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2 w-1/2">
      <input
        placeholder="Name"
        onChange={(e) => setReview({ ...review, reviewer: e.target.value })}
        value={review.reviewer}
        className="border border-gray-600 p-2 rounded-xl"
      />

      <input
        type="number"
        placeholder="Rating"
        onChange={(e) => setReview({ ...review, rating: e.target.value })}
        className="border border-gray-600 p-2 rounded-xl"
        value={review.rating}
      />

      <textarea
        placeholder="Review"
        onChange={(e) => setReview({ ...review, review: e.target.value })}
        className="border border-gray-600 p-2 rounded-xl"
        value={review.review}
      />

      <button
        type="submit"
        className="border text-left border-gray-600 p-2 rounded-xl"
      >
        Submit Review
      </button>
    </form>
  );
}
