"use client";

const ReviewModal = ({ review, onClose }) => {
  if (!review) return null;

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl max-w-lg w-full p-6 relative animate-fadeIn">

        {/* Close */}
        <button
          onClick={onClose}
          className="absolute top-3 right-4 text-gray-500 hover:text-black text-xl"
        >
          ✕
        </button>

        <h3 className="text-xl font-semibold mb-2">
          {review.reviewer}
        </h3>

        <span className="inline-block mb-4 text-sm bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full">
          ⭐ {review.rating}/5
        </span>

        <p className="text-gray-700 leading-relaxed">
          {review.review}
        </p>
      </div>
    </div>
  );
};

export default ReviewModal;
