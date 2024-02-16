#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.city import City
import os
from os import environ


class State(BaseModel, Base):
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state",
                          cascade="all, delete, delete-orphan")
    @property
    def cities(self):
        "Return list of City objects"
        dict_all_cities = models.storage.all(City)
        list_cities = []
        for city in dict_all_cities.values():
            if city.state_id == self.id:
                list_cities.append(city)
        return list_cities
