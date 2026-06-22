import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from scraper import scrape_trending_ebay
from seo_engine import seo_engine
from publisher import publisher
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SEO Blog Post Creation API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    title: str
    price: str
    url: str

class BlogRequest(BaseModel):
    product_title: str

class KeywordInfo(BaseModel):
    keyword: str
    intent: str
    competition: str
    strategy: str

class BlogResponse(BaseModel):
    title: str
    keywords: List[KeywordInfo]
    content: str

class PublishRequest(BaseModel):
    title: str
    content: str
    platform: str # "wordpress" or "medium"

@app.get("/trending", response_model=List[Product])
async def get_trending_products():
    try:
        products = await scrape_trending_ebay()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-blog", response_model=BlogResponse)
async def generate_blog(request: BlogRequest):
    try:
        keywords = await seo_engine.generate_keywords(request.product_title)
        content = await seo_engine.generate_blog_post(request.product_title, keywords)
        return BlogResponse(
            title=request.product_title,
            keywords=keywords,
            content=content
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/publish")
async def publish_blog(request: PublishRequest):
    try:
        if request.platform == "wordpress":
            result = await publisher.publish_to_wordpress(request.title, request.content)
        elif request.platform == "medium":
            result = await publisher.publish_to_medium(request.title, request.content)
        else:
            raise HTTPException(status_code=400, detail="Invalid platform")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
