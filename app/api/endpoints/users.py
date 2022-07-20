from fastapi import APIRouter, status, Depends, HTTPException
from app import (schemas, models, auth, database, utils)
from typing import List
from sqlalchemy import func, exc
from sqlalchemy.orm import Session
from typing import Optional
router = APIRouter(
    prefix="/users",
    tags=['User']
)


@router.post('/', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(new_user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    hashed_password = utils.password_encrypt.hash(new_user.password)
    new_user.password = hashed_password
    new_user = models.User(**new_user.dict())
    user_same_email = db.query(models.User).filter(
        models.User.email == new_user.email).first()
    if not user_same_email:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f'username with the email={new_user.email}  already exists')


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
async def get_all_users(limit:int = 25, skip: int = 0, search: Optional[str]="", db: Session = Depends(database.get_db)):
    all_users = db.query(models.User).order_by(models.User.created_at.desc()).filter(
                models.User.full_name.contains(search.lower())).limit(limit=limit).offset(skip).all()
    return all_users


@router.get('/{id}', response_model=schemas.UserDetailResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int, db: Session = Depends(database.get_db)):
    user_found = db.query(models.User).filter(models.User.u_id == id).first()
    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f' user with id {id} does not exist')
    return user_found


@router.put('/{id}', response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
async def update_user(userSchema: schemas.UserCreate, id: int, db: Session = Depends(database.get_db),
                        auth_user: models.User = Depends(auth.oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f' user with id {id} does not exist')

    if not user_query.first().id == auth_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Unauthorized')
    try:
        hashed_password = utils.password_encrypt.hash(userSchema.password)
        userSchema.password = hashed_password
        user_query.update(userSchema.dict(), synchronize_session=False)
        db.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="the email already exist. Add unique email")
    return user_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(database.get_db), 
                    auth_user: models.User = Depends(auth.oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == id)

    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} does not exist')

    if not user_query.first().id == auth_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Unauthorized')

    user_query.delete(synchronize_session=False)
    db.commit()
    return "deleted"
