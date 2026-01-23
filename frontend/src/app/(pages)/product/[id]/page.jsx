import ProductClient from "./ProductClient";

const Page = async ({ params }) => {
  const { id } = await params;

  const res = await fetch(
    `${process.env.NEXT_PUBLIC_BACKEND_URL}/products/${id}`,
    { cache: "no-store" }
  );

  if (!res.ok) {
    return <p className="p-6 text-red-500">Failed to load product</p>;
  }
  const data = await res.json();

  const product = data.find((product) => product.id.toString() === id);

  return <ProductClient product={product} />;
};

export default Page;
