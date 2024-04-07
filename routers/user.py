from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models, schema, utils
from typing import List
from database import get_db
from pytest import Session
 
router = APIRouter(
    prefix="/users"
)

 #function to create users 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):    

    print("creating user!")

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict()) #type: ignore | this is the better way of writing all columns once, than the one above. Imagine you have 50 columns: you would need to type all of them!!!
    db.add(new_user) #type: ignore
    db.commit() #type: ignore
    db.refresh(new_user) #type: ignore

    print("finish creating user!")

    return new_user

#get users based on the id
@router.get("/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first() #type: ignore

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with od: {id} does not exists")
    
    return user