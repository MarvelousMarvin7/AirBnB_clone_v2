#!/usr/bin/python3
"""Change over to database storage with sqlalchemy"""
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
from models.review import Review
from models.user import User
from models.place import Place
from models.amenity import Amenity


class DBStorage:
    """Database storge for HBNB"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        db = getenv('HBNB_MYSQL_DB')
        host = getenv('HBNB_MYSQL_HOST')
        env = getenv('HBNB_ENV')

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'
            .format(user, passwd, host, db),
            pool_pre_ping=True
        )

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects depending on the class name (cls)"""
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls).all()
        else:
            query = self.__session.query(User).all() + \
                    self.__session.query(State).all() + \
                    self.__session.query(City).all() + \
                    self.__session.query(Amenity).all() + \
                    self.__session.query(Place).all() + \
                    self.__session.query(Review).all()
        obj_dict = {}
        for obj in query:
            key = '{}.{}'.format(type(obj).__name__, obj.id)
            obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and
        the current database session"""
        Base.metadata.create_all(self.__engine)
        maker = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(maker)
        self.__session = Session()

    def close(self):
        """calls remove"""
        if self.__session:
            self.__session.remove()
