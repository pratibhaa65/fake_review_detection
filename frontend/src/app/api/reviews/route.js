import fs from "fs";
import path from "path";

export async function POST(req) {
    const body = await req.json();
    const { productId, reviewer, rating, comment } = body;

    const filePath = path.join(process.cwd(), "public/products.json");

    const data = JSON.parse(fs.readFileSync(filePath, "utf-8"));

    const product = data.products.find((p) => p.id === Number(productId));

    if (!product) {
        return Response.json({ message: "Product not found" }, { status: 404 });
    }

    product.reviews.push({ reviewer, rating: Number(rating), comment });

    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));

    return Response.json({ message: "Review added successfully" });
}


