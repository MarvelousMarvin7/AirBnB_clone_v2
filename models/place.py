#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
import models
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from models.associations import place_amenity



class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    review = relationship('Review', cascade='all, delete, delete-orphan',
                          backref='place')
    amenities = relationship('Amenity', secondary=place_amenity,
                             viewonly=False,
                             back_populates='places')

    @property
    def reviews(self):
        """Returns the lisst of Review instances"""
        review_list = []
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            return self.reviews
        else:
            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

    @property
    def amenities(self):
        """Getter attribute amenities that returns the list of Amenity"""
        if getenv("HBNB_TYPE_STORAGE") == "db":
            return self.amenities
        else:
            amenity_list = []
            for amenity in models.storage.all(Amenity).values():
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

    @amenities.setter
    def amenities(self, obj):
        """Setter attribute amenities that handles
        append method for adding an Amenity.id"""
        if getenv("HBNB_TYPE_STORAGE") != "db" and isinstance(obj, Amenity):
            if 'amenity_ids' not in self.__dict__:
                self.amenity_ids = []
            if obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
