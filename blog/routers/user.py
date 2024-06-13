from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, schemas, models
from sqlalchemy.orm import Session
from ..services import user

router = APIRouter(
    tags=['Users'],
    prefix='/user'
)
get_db = database.get_db


# Endpoint for user creation
@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


# Endpoint to show user
@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)
