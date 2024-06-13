from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, database, models
from ..services import blog

router = APIRouter(
    tags=['Blogs'],
    prefix='/blog'
)
get_db = database.get_db


# Endpoint for get all blogs
@router.get('/', response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db)):
    return blog.get_all(db)


# Endpoint to create blogs
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request, db)


# Endpoint to delete blogs
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy_blog(id: int, db: Session = Depends(get_db)):
    return blog.destroy(id, db)


# Endpoint to update blogs
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update_blog(id, request, db)


# Endpoint to get blogs with specific id
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show_blogs(id: int, db: Session = Depends(get_db)):
    return blog.show(id, db)
