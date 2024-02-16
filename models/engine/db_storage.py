#!/usr/bin/python3
"""This module defines a class to manage DB storage for hbnb clone"""
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Initializes DBStorage instance."""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            os.getenv('HBNB_MYSQL_USER'), os.getenv('HBNB_MYSQL_PWD'),
            os.getenv('HBNB_MYSQL_HOST', 'localhost'),
            os.getenv('HBNB_MYSQL_DB')), pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects depending on the class name."""
        cls_dict = {
            "User": User, "Place": Place, "State": State,
            "City": City, "Amenity": Amenity, "Review": Review
        }

        obj_dict = {}
        if cls:
            # If cls is provided, query only objects of that class
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                obj_dict[key] = obj
        else:
            # If cls is None, query all types of objects
            for class_name in cls_dict:
                objs = self.__session.query(cls_dict[class_name]).all()
                for obj in objs:
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    obj_dict[key] = obj

            return obj_dict

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads all tables and creates the database session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        call remove() method on the private session attribute
        """
        self.__session.close()

# Rest of the class definition
