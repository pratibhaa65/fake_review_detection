import fs from "fs";
import path from "path";

export async function POST(req) {
    const body = await req.json();
    const { name, description, price, category } = body;
    const reviews = [];

    const filePath = path.join(process.cwd(), "public/products.json");

    const data = JSON.parse(fs.readFileSync(filePath, "utf-8"));

    data.products.push({ id: data.products.length + 1, name, description, price, category, reviews });

    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));

    return Response.json({ message: "Product added successfully" });
}


