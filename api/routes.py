from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.db import get_db
from database.models import Listing
from scraper.zillow_api import run_scraper

router = APIRouter()

@router.get("/listings")
def get_listings(
    db: Session = Depends(get_db),
    city: str = Query(None),
    state: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    bedrooms: int = Query(None),
    limit: int = Query(50),
    offset: int = Query(0)
):
    query = db.query(Listing)

    if city:
        query = query.filter(Listing.city.ilike(f"%{city}%"))
    if state:
        query = query.filter(Listing.state.ilike(f"%{state}%"))
    if min_price:
        query = query.filter(Listing.price >= min_price)
    if max_price:
        query = query.filter(Listing.price <= max_price)
    if bedrooms:
        query = query.filter(Listing.bedrooms == bedrooms)

    total = query.count()
    listings = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "listings": listings
    }

@router.get("/listings/{listing_id}")
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        return {"error": "Not found"}
    return listing

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    stats = db.query(
        Listing.city,
        Listing.state,
        func.count(Listing.id).label("count"),
        func.avg(Listing.price).label("avg_price"),
        func.min(Listing.price).label("min_price"),
        func.max(Listing.price).label("max_price"),
        func.avg(Listing.living_area).label("avg_area")
    ).group_by(Listing.city, Listing.state).all()

    return [
        {
            "city": s.city,
            "state": s.state,
            "count": s.count,
            "avg_price": round(s.avg_price or 0, 2),
            "min_price": s.min_price,
            "max_price": s.max_price,
            "avg_area": round(s.avg_area or 0, 2)
        }
        for s in stats
    ]

@router.post("/scrape")
def scrape():
    run_scraper()
    return {"message": "✅ Scraping completed"}