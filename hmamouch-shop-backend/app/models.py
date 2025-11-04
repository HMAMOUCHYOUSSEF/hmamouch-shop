from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base() # the wight board in which we write on


# the User Model

class User(Base): #User is inheritance class the User class git all capabilites of the base class plus his own.

    __tablename__ = "users" # the Class attribute shared by all

    #these are instance attributes that are inheritant by the Base Class
    #every object has its unique instance attributes

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True,nullable=False)
    hashed_password = Column(String(255), nullable=False)

# the Product Model

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User")