from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update
from typing import List
from .. import schemas, database, models

router = APIRouter(
    tags=['Blogs'],
    prefix='/blog'
)
get_db = database.get_db

# Endpoint for get all blogs
@router.get('/', response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

# Endpoint to create blogs
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Endpoint to delete blogs
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return f'Blog with id {id} deleted sucessfully'

# Endpoint to update blogs
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} not found')

    db.execute(
        update(models.Blog)
        .where(models.Blog.id == id)
        .values(request.dict())
    )
    db.commit()
    return 'Blog has been updated sucessfully'

# Endpoint to get blogs with specific id
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show_blogs(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} is not found')
    return blog
