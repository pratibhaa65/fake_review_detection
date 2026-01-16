import React from "react";

const page = async ({ params }) => {
  const { id } = await params;
  const res = await fetch("/products.json");
  const products = await res.json();

  console.log(products);
  console.log(id);
  return <div>Hello</div>;
};

export default page;
