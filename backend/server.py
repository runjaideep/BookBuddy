from fastapi import FastAPI, HTTPException
from datetime import date
import db_helper
import requests
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

class Library(BaseModel):
    title: str
    total_pages: int
    author: str
    genre: str
    progress: Optional[str]

class DateRange(BaseModel):
    start_date: date
    end_date: date

class GenreRequest(BaseModel):
    name: str

@app.get("/bookbuddy/library", response_model=List[Library])
def get_library():
    library = db_helper.fetch_books()
    return library

@app.post("/bookbuddy/genres")
def add_genre(genre: GenreRequest):
    db_helper.insert_genre(genre.name)
    return {"message": "Genre inserted successfully"}

@app.get("/bookbuddy/recommendations")
def fetch_recommendations(title: str, author: str = None):
    recommendations = db_helper.fetch_recommendations(title=title,author=author)
    return recommendations

# Example usage:

