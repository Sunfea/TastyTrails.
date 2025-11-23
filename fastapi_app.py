import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TastyTrails FastAPI", version="1.0.0")

# Add CORS middleware
# In production, replace with specific origins
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware to track request processing time
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
        return response
    except Exception as e:
        logger.error(f"Error processing request {request.method} {request.url.path}: {str(e)}")
        raise e

@app.get("/")
async def root():
    return {"message": "Welcome to TastyTrails FastAPI Service"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "fastapi",
        "timestamp": time.time()
    }

# Search endpoints
@app.get("/api/search/restaurants")
async def search_restaurants(query: Optional[str] = None):
    # Placeholder for search functionality
    if query is None or query.strip() == "":
        raise HTTPException(status_code=400, detail="Query parameter is required")
    return {"message": f"Searching for restaurants with query: {query}", "results": []}

# Recommendation endpoints
@app.get("/api/recommendations")
async def get_recommendations(user_id: Optional[int] = None):
    # Placeholder for recommendation functionality
    return {"message": f"Getting recommendations for user: {user_id}", "recommendations": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)