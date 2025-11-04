from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User
from passlib.context import CryptContext

router = APIRouter(prefix="/users",tags=["Users"])
# is for creating the foundation of routering systeme
# it groups all related endpoinds to make things more structured
pwd_context = CryptContext(schemes="sha256_crypt",deprecated="auto")
# we chose the crypting algorithm and recrypte the old passwords for more security
@router.post("/") #<- endpoint for creating a user // we user POST method -> CREATING NEW THING.
def create_user(name: str,email: str,password: str,db: Session = Depends(get_db)): # <- its function
    useremail = db.query(User).filter(User.email == email).first()
    if useremail:
        raise HTTPException(status_code=404, detail="Email already exists")
    password = password[:72]
    hashed_password = pwd_context.hash(password)
    user = User(name = name, email = email,hashed_password=hashed_password)
    db.add(user) # add the user on the database specialy into the User table
    db.commit() # save the transaction
    db.refresh(user) # refresh
    return {"id":user.id,"name":user.name,"email":user.email}

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all() # is equivalent to this sql: SELECT * FORM users
    return users

@router.get("/{user_id}")
def get_users(user_id: int,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first() # is like SELECT * FROM User WHERE User.id == user_id LIMIT 1
    if not user:
        raise HTTPException(status_code=404 ,detail="User not found")
    return user