"use client";

import React, { useEffect, useState } from "react";

const CreateProduct = () => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");
  const [category, setCategory] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  // UI-only states
  const [categories, setCategories] = useState([]);
  const [useCustomCategory, setUseCustomCategory] = useState(false);
  const [customCategory, setCustomCategory] = useState("");

  /* ---------- FETCH CATEGORIES (UI only) ---------- */
  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/categories`)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setCategories(data);
        } else {
          setUseCustomCategory(true); // 🔥 IMPORTANT
        }
      })
      .catch(() => {
        setUseCustomCategory(true); // fallback
      });
  }, []);

  async function handleSubmit() {
    setIsSubmitting(true);

    const finalCategory = useCustomCategory
      ? customCategory.trim()
      : category.trim();
    if (!finalCategory) {
      alert("Category is required");
      setIsSubmitting(false);
      return;
    }
    const productData = {
      name,
      description,
      price,
      category: finalCategory,
    };

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/products`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(productData),
        },
      );

      if (response.ok) {
        alert("Product created successfully!");
        setName("");
        setDescription("");
        setPrice("");
        setCategory("");
        setCustomCategory("");
        setUseCustomCategory(false);
      } else {
        const data = await response.json();
        alert(data.message || "Failed to create product.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while creating the product.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center px-6">
      <div className="bg-white rounded-xl shadow-lg w-full max-w-xl p-8">
        <h1 className="text-3xl font-bold mb-6 text-center">
          Create New Product
        </h1>

        <div className="space-y-5">
          {/* Product Name */}
          <div>
            <label className="block text-sm font-medium mb-1">
              Product Name
            </label>
            <input
              type="text"
              value={name}
              required
              onChange={(e) => setName(e.target.value)}
              className="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500"
              placeholder="Enter product name"
            />
          </div>

          {/* Category */}
          <div>
            <label className="block text-sm font-medium mb-1">Category</label>

            {categories.length > 0 && !useCustomCategory ? (
              <select
                value={category}
                onChange={(e) => {
                  if (e.target.value === "__new__") {
                    setUseCustomCategory(true);
                    setCategory("");
                  } else {
                    setCategory(e.target.value);
                  }
                }}
                className="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500"
              >
                <option value="">Select category</option>
                {categories.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
                <option value="__new__">➕ Add new category</option>
              </select>
            ) : (
              <input
                type="text"
                value={customCategory}
                onChange={(e) => setCustomCategory(e.target.value)}
                className="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter new category"
              />
            )}
          </div>

          {/* Price */}
          <div>
            <label className="block text-sm font-medium mb-1">Price</label>
            <input
              type="number"
              value={price}
              required
              onChange={(e) => setPrice(e.target.value)}
              className="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500"
              placeholder="Enter price"
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium mb-1">
              Description
            </label>
            <textarea
              rows="4"
              value={description}
              required
              onChange={(e) => setDescription(e.target.value)}
              className="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500"
              placeholder="Short product description"
            />
          </div>

          <button
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="w-full bg-indigo-500 hover:bg-indigo-600 text-white py-3 rounded-lg font-semibold transition disabled:opacity-50"
          >
            {isSubmitting ? "Creating..." : "Create Product"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreateProduct;
