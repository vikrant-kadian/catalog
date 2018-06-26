from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import UniqueConstraint
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)

    @property
    def serialize(self):
        return {
            'Id': self.id,
            'Username': self.username,
            'Email': self.email
        }


class Manufacturer(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    manufacturer = Column(String(160), nullable=False, unique=True)

    @property
    def serialize(self):
        return {
            'Id': self.id,
            'Manufacturer': self.manufacturer
        }


class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    name = Column(String(180), nullable=False)
    description = Column(String, nullable=False)
    manufacturer = Column(String, ForeignKey('companies.manufacturer'))
    companies = relationship(Manufacturer)

    @property
    def serialize(self):
        return {
            'Id': self.id,
            'Car': self.name,
            'Description': self.description,
            'Manufacturer': self.manufacturer
        }

engine = create_engine('postgresql://grader:grader@localhost/catalog')
Base.metadata.create_all(engine)
