import fs from "fs";
// import { get } from "http";
import crypto from "crypto";
import path from "path";


const requestStore = new Map();

const LIMIT = 4;          // max same payload
const WINDOW = 60 * 1000; // 60 seconds


function hashPayload(payload) {
    return crypto
        .createHash("sha256")
        .update(JSON.stringify(payload))
        .digest("hex");
}

function getClientIP(req) {
    return (
        req.headers.get("x-forwarded-for")?.split(",")[0] ||
        req.headers.get("x-real-ip") ||
        "unknown"
    );
}


export async function POST(req) {
    const body = await req.json();
    const { productId, reviewer, rating, comment } = body;

    const ip = getClientIP(req);
    console.log(ip)
    const payloadHash = hashPayload({
        reviewer,
        rating,
        comment,
    });

    const key = `${ip}:${payloadHash}`;
    const now = Date.now();

    if (!requestStore.has(key)) {
        requestStore.set(key, []);
    }

    const timestamps = requestStore
        .get(key)
        .filter((t) => now - t < WINDOW);

    if (timestamps.length >= LIMIT) {
        return Response.json(
            { message: "Duplicate review detected from same IP" },
            { status: 429 }
        );
    }


    timestamps.push(now);
    requestStore.set(key, timestamps);



    try {
        const filePath = path.join(process.cwd(), "public/products.json");

        const data = JSON.parse(fs.readFileSync(filePath, "utf-8"));

        const product = data.products.find((p) => p.id === Number(productId));

        if (!product) {
            return Response.json({ message: "Product not found" }, { status: 404 });
        }

        product.reviews.push({ reviewer, rating: Number(rating), comment });

        fs.writeFileSync(filePath, JSON.stringify(data, null, 2));

        return Response.json({ message: "Review added successfully" });
    } catch (error) {
        return Response.json({ message: "Internal server error" }, { status: 500 });
    }
}


