import datetime
from unittest.mock import Base
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import Optional

from pydantic.types import conint


# class implemented using Pydantic model, to ensure the "post" request is always following the same requirements
# class Post(BaseModel): 
#     title: str
#     content: str
#     published: Optional[bool] = True


#Orders matter! if user schema is defined later, it would not be able to be used for other schema. In this case, the class Post which grab the "owner" value from class OwnerOut

class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr #build-in package from pydantic that could be used to validate email input
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    #below class is need to convert the values based on the regular pydantic model. Otherwise the process would be failing!
    class Config:
        orm_mode = True 

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Post(PostBase): # this would inherit the structure of class PostBase 
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    #below class is need to convert the values based on the regular pydantic model. Otherwise the process would be failing!
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #type: ignore  -- dir stands for direction. 0 means downvote and 1 means upvote. 
                      # here we use Confidence Interval method of pydantic to make sure the input never be higher than 1  



