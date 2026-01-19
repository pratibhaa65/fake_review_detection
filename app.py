from fastapi import FastAPI
# from src.predict import predict_review
# from src.train import trainModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fake Review Detection API")

# 1. Define the origins that are allowed to talk to your API
origins = [
    "http://localhost:3000",      # React/Next.js default
    "http://127.0.0.1:3000",
    "https://your-frontend-domain.com",
]

# 2. Add the middleware to your FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Allows specific origins
    allow_credentials=True,            # Allows cookies/auth headers
    allow_methods=["*"],               # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],               # Allows all headers
)

@app.get("/")
def root():
    return {"message": "Welcome to Fake Review Detection API"}

@app.get("/predict")
def predict():
    result = predict_review()
    return {"prediction": result}


# @app.get("/train")
# def train():
#     result = trainModel()
#     return {"training_status": result}
