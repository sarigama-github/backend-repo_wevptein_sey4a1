"""
Database Schemas for Naivedyam Restaurants

Each Pydantic model represents a MongoDB collection. The collection name
is the lowercase of the class name (e.g., Branch -> "branch").
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class Branch(BaseModel):
    name: str = Field(..., description="Branch name")
    address: str = Field(..., description="Full postal address")
    phone_primary: str = Field(..., description="Primary phone number")
    phone_secondary: Optional[str] = Field(None, description="Secondary phone number")
    latitude: Optional[float] = Field(None, description="Latitude for map")
    longitude: Optional[float] = Field(None, description="Longitude for map")
    hours: str = Field(..., description="Opening hours text")
    google_maps_url: Optional[str] = Field(None, description="Google Maps link")

class MenuItem(BaseModel):
    category: str = Field(..., description="Menu category (e.g., Dosas, Starters)")
    title: str = Field(..., description="Dish name")
    description: Optional[str] = Field(None, description="Short description")
    price: Optional[float] = Field(None, description="Optional price")
    image_url: Optional[str] = Field(None, description="Image URL for the dish")
    is_special: bool = Field(False, description="Whether this is a seasonal/special dish")

class Testimonial(BaseModel):
    name: str = Field(..., description="Customer name")
    message: str = Field(..., description="Testimonial text")
    rating: int = Field(5, ge=1, le=5, description="Rating out of 5")

class GalleryImage(BaseModel):
    title: str = Field(..., description="Image title")
    url: str = Field(..., description="Image URL")
    alt: str = Field(..., description="Alt text for accessibility")
    category: Optional[str] = Field(None, description="food | ambience | people")

class CateringRequest(BaseModel):
    name: str
    company: Optional[str] = None
    email: EmailStr
    phone: str
    event_date: Optional[str] = None
    guest_count: Optional[int] = None
    message: Optional[str] = None

class Inquiry(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: str
    branch: Optional[str] = None
