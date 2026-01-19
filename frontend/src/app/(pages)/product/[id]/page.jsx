import ReviewForm from "../reviews";

const Page = async ({ params }) => {
  const { id } = await params;

  const res = await fetch(
    `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/products`,
    {
      cache: "no-store",
    },
  );
  const data = await res.json();

  const product = data.products.find((product) => product.id.toString() === id);

  if (!product) {
    return <p className="p-6 text-red-500">Product not found</p>;
  }

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      {/* Product Info */}
      <div className="space-y-2">
        <h1 className="text-2xl font-semibold">{product.name}</h1>
        <p className="text-gray-600">{product.description}</p>

        <div className="text-sm text-gray-700">
          <p>Price: Rs. {product.price}</p>
          <p>Category: {product.category}</p>
        </div>
      </div>

      <hr />

      {/* Reviews */}
      <div className="space-y-3">
        <h2 className="text-lg font-medium">Reviews</h2>

        {product.reviews && product.reviews.length > 0 ? (
          <ul className="space-y-2">
            {product.reviews.map((review, index) => (
              <li key={index} className="text-sm">
                <span className="font-medium">{review.reviewer}</span>{" "}
                <span className="text-gray-500">({review.rating}/5)⭐</span>
                <p className="text-gray-600">{review.review}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-gray-500">No reviews yet.</p>
        )}
      </div>

      <hr />

      {/* Review Form */}
      <div className="space-y-3">
        <h2 className="text-lg font-medium">Add a review</h2>
        <ReviewForm productId={product.id} />
      </div>
    </div>
  );
};

export default Page;
