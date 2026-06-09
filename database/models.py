from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    zpid = Column(String, unique=True, nullable=False)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(String)
    price = Column(Float)
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    living_area = Column(Float)
    home_type = Column(String)
    home_status = Column(String)
    zestimate = Column(Float)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)