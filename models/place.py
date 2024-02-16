#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from sqlalchemy import Table, Column, String, ForeignKey


class Place(BaseModel, Base):
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    amenities = relationship(
        "Amenity",
        secondary="place_amenity",
        backref="places",
        viewonly=False
    )

    @property
    def amenities(self):
        """ Getter attribute for FileStorage """
        from models import storage
        amenities_list = []
        for amenity_id in self.amenity_ids:
            amenity = storage.get("Amenity", amenity_id)
            if amenity:
                amenities_list.append(amenity)
        return amenities_list

    @amenities.setter
    def amenities(self, obj):
        """ Setter attribute for FileStorage """
        if isinstance(obj, Amenity):
            if not hasattr(self, 'amenity_ids'):
                setattr(self, 'amenity_ids', [])
            if obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)


metadata = Base.metadata

place_amenity = Table(
    'place_amenity', metadata,
    Column("place_id", String(60), ForeignKey("places.id"),
           primary_key=True, nullable=False),
    Column("amenity_id", String(60), ForeignKey("amenities.id"),
           primary_key=True, nullable=False)
)
