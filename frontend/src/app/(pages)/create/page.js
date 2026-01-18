"use client"

import React, { useState } from 'react'

const CreateProduct = () => {
    const [name, setName] = useState('')
    const [description, setDescription] = useState('')
    const [price, setPrice] = useState('')
    const [category, setCategory] = useState('')
    const [isSubmitting, setIsSubmitting] = useState(false)

    async function handleSubmit() {
        setIsSubmitting(true)
        const productData = { name, description, price, category }

        try {
            const response = await fetch('api/products', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData),
            })

            if (response.ok) {
                alert('Product created successfully!')
                setName('')
                setDescription('')
                setPrice('')
                setCategory('')
            } else {
                alert('Failed to create product.')
            }
        } catch (error) {
            console.error('Error:', error)
            alert('An error occurred while creating the product.')
        } finally {
            setIsSubmitting(false)
        }
    }

    return (
        <div className="max-w-2xl mx-auto p-6">
            <h1 className="text-3xl font-bold mb-6">Create New Product</h1>

            <div className="bg-white rounded-lg shadow p-6 space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1" htmlFor="name">
                        Product Name
                    </label>
                    <input
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        type="text"
                        id="name"
                        value={name}
                        required
                        onChange={(e) => setName(e.target.value)}
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1" htmlFor="description">
                        Description
                    </label>
                    <textarea
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        id="description"
                        rows="3"
                        value={description}
                        required
                        onChange={(e) => setDescription(e.target.value)}
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1" htmlFor="price">
                        Price
                    </label>
                    <input
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        type="number"
                        id="price"
                        value={price}
                        required
                        onChange={(e) => setPrice(e.target.value)}
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1" htmlFor="category">
                        Category
                    </label>
                    <input
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        type="text"
                        id="category"
                        value={category}
                        required
                        onChange={(e) => setCategory(e.target.value)}
                    />
                </div>

                <button
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-md transition-colors disabled:bg-gray-400"
                    onClick={handleSubmit}
                    disabled={isSubmitting}
                >
                    {isSubmitting ? 'Creating...' : 'Create Product'}
                </button>
            </div>
        </div>
    )
}

export default CreateProduct