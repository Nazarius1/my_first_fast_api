from fastapi import status, HTTPException, Response, Depends, APIRouter
import models, schema
from . import my_oauth2
from typing import List, Optional
from database import get_db
from pytest import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts"
)

#@router.get("/", response_model=List[schema.Post])
@router.get("/", response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db), current_user = Depends(my_oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # my_posts = cursor.fetchall()
    # my_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #type: ignore

    
    my_posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(      #type: ignore
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #print(my_posts) 
    
    return my_posts

#return a specific post
@router.get("/{id}", response_model=schema.PostOut)
def get_post(id:int, db: Session = Depends(get_db), current_user = Depends(my_oauth2.get_current_user)):
    
    
    #post = db.query(models.Post).filter(models.Post.id == id).first() #type: ignore

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(  #type: ignore
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()
    
    print("post query:")
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")

    return post


#this request cannot be send to browser using http. it will give us error 405 method is not allowed
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db), current_user = Depends(my_oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(current_user.id)
    new_post = models.Post(owner_id = current_user.id, **post.dict()) #type: ignore | this is the better way of writing all columns once, than the one above. Imagine you have 50 columns: you would need to type all of them!!!
    db.add(new_post) #type: ignore
    db.commit() #type: ignore
    db.refresh(new_post) #type: ignore
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(my_oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id) #type: ignore

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    #print("id found!")
    post_query.delete(synchronize_session=False)
    db.commit() #type: ignore
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db), current_user = Depends(my_oauth2.get_current_user)):

    print("executing update post!")
    post_query = db.query(models.Post).filter(models.Post.id == id) #type: ignore

    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    post_query.update(post.dict(),synchronize_session=False) #type: ignore
    db.commit() #type: ignore
    return post_query.first()