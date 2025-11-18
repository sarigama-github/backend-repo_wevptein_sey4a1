import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import Branch, MenuItem, Testimonial, GalleryImage, CateringRequest, Inquiry

app = FastAPI(title="Naivedyam Restaurants API", description="Backend for Naivedyam website", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "name": "Naivedyam API"}

@app.get("/schema")
def get_schema_names():
    # Allow Flames viewer to introspect
    return {
        "collections": ["branch", "menuitem", "testimonial", "galleryimage", "cateringrequest", "inquiry"]
    }

# Branches
@app.get("/branches", response_model=List[Branch])
def list_branches():
    docs = get_documents("branch")
    return [Branch(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.post("/branches", status_code=201)
def create_branch(branch: Branch):
    try:
        _id = create_document("branch", branch)
        return {"id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Menu
@app.get("/menu", response_model=List[MenuItem])
def list_menu():
    docs = get_documents("menuitem")
    return [MenuItem(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.post("/menu", status_code=201)
def create_menu_item(item: MenuItem):
    try:
        _id = create_document("menuitem", item)
        return {"id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Testimonials
@app.get("/testimonials", response_model=List[Testimonial])
def list_testimonials():
    docs = get_documents("testimonial")
    return [Testimonial(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.post("/testimonials", status_code=201)
def create_testimonial(item: Testimonial):
    try:
        _id = create_document("testimonial", item)
        return {"id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Gallery
@app.get("/gallery", response_model=List[GalleryImage])
def list_gallery():
    docs = get_documents("galleryimage")
    return [GalleryImage(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.post("/gallery", status_code=201)
def create_gallery_image(item: GalleryImage):
    try:
        _id = create_document("galleryimage", item)
        return {"id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Forms
@app.post("/catering", status_code=201)
def submit_catering(form: CateringRequest):
    try:
        _id = create_document("cateringrequest", form)
        return {"id": _id, "message": "Thank you. We will contact you shortly."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/inquiry", status_code=201)
def submit_inquiry(form: Inquiry):
    try:
        _id = create_document("inquiry", form)
        return {"id": _id, "message": "Thanks for reaching out. We will get back soon."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health + DB test
@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
