import Link from "next/link";

export default function ProductCard({ product }) {
  return (
    <Link href={`/product/${product.id}`}>
      <div className="h-full bg-white rounded-xl shadow hover:shadow-lg transition p-6 flex flex-col">

        {/* Product Name */}
        <h3 className="text-lg font-semibold mb-2 line-clamp-1">
          {product.name}
        </h3>

        {/* Description */}
        <p className="text-gray-600 text-sm line-clamp-3">
          {product.description}
        </p>

        {/* Spacer pushes price to bottom */}
        <div className="mt-auto pt-4">
          <p className="text-indigo-600 font-bold">
            Rs. {product.price}
          </p>
        </div>
      </div>
    </Link>
  );
}
