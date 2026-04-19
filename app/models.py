from sqlalchemy import Column, Integer, Float, String, DateTime, Time, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class WindDirection(enum.Enum):
    N = "N"
    S = "S"
    E = "E"
    W = "W"
    NW = "NW"
    SW = "SW"
    NE = "NE"
    SE = "SE"

class Weather(Base):
    __tablename__ = 'weather'
    
    id = Column(Integer, primary_key=True)
    
    country = Column(String)              
    last_updated = Column(DateTime)      
    wind_degree = Column(Integer)        
    wind_kph = Column(Float)             
    wind_direction = Column(Enum(WindDirection))
    
    celestial_id = Column(Integer, ForeignKey('celestial_events.id'))

    celestial = relationship("CelestialEvents", back_populates="weather_entry")

class CelestialEvents(Base):
    __tablename__ = 'celestial_events'
    
    id = Column(Integer, primary_key=True)
    
    sunrise = Column(Time)               
    sunset = Column(Time)
    moonrise = Column(Time)
    moonset = Column(Time)
    moon_phase = Column(String)
    moon_illumination = Column(Integer)

    should_go_outside = Column(Boolean, default=True)
    
    weather_entry = relationship("Weather", back_populates="celestial")