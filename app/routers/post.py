from fastapi import FastAPI, Response, HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
#from app import models, schemas
import models
import schemas, oauth2
from database import get_db
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import joinedload

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)

#@router.get('/', response_model=List[schemas.Post])
@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit : int = 10, skip : int =0, search : Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    #print(limit)
    post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
    #         models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # print(post)
    # print(post.dict())
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,10000000)
    # my_posts.append(post_dict)
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # it reflects the changes in the database while creating or inserting data into teh database
    #conn.commit()
    #print(current_user.id)
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    # post = cursor.fetchone()
    # print(test_post)
    # post = find_post(id)

    # post = posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with the given id : {id} not found')

    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delet_post(id : int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #index = find_index_post(id)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    post = deleted_post.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with the given id : {id} doesnot exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    
    
    deleted_post.delete(synchronize_session = False)
    db.commit()

    #my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),  current_user : int = Depends(oauth2.get_current_user)):
    #index = find_index_post(id)
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    postt = updated_post.first()
    if postt == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with the given id : {id} doesnot exist")
    
    if postt.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
    
    updated_post.update(post.dict(), synchronize_session= False)
    db.commit()
    
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return updated_post.first()