from fastapi import APIRouter, status, Depends, HTTPException
from app import (schemas, models, auth, database, utils)
from typing import List
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(
    prefix="/users",
    tags=['User']
)


@router.post('/', response_model=schemas.UserRes, status_code=status.HTTP_201_CREATED)
async def create_user(new_user: schemas.UserReq, db: Session = Depends(database.get_db)):

    hashed_password = utils.hash(new_user.password)
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


# TODO implement superuser
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.UserRes])
async def get_all_users(limit: int = 25, skip: int = 0, search: Optional[str] = "", db: Session = Depends(database.get_db)):
    """Allows superuser to view all users. Currently, everyone can.
    """

    all_users = db.query(models.User).order_by(models.User.created_at.desc()).filter(
        models.User.full_name.contains(search.lower())).limit(limit=limit).offset(skip).all()
    if all_users:
        return all_users


@router.get('/detail', response_model=List[schemas.UserDetailRes], status_code=status.HTTP_200_OK)
async def get_user_details(limit: int = 25, skip: int = 0, search: Optional[str] = "", db: Session = Depends(database.get_db)):
    users = db.query(models.User).join(models.UserDetail).order_by(models.User.created_at.desc()).filter(
        models.User.full_name.contains(search.lower())).limit(limit=limit).offset(skip).all()
    return users


@router.get('/{id}', response_model=schemas.UserDetailRes, status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int, db: Session = Depends(database.get_db),
                         auth_user: models.User = Depends(auth.oauth2.get_current_user)):
    user_found: models.User = db.query(
        models.User).filter(models.User.id == id).first()
    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f' user with id {id} does not exist')
    if not user_found.id == auth_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Unauthorized')
    return user_found


@router.put('/{id}', response_model=schemas.UserRes, status_code=status.HTTP_200_OK)
async def update_user(userSchema: schemas.UserReq, id: int, db: Session = Depends(database.get_db),
                      auth_user: models.User = Depends(auth.oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f' user with id {id} does not exist')

    if not user_query.first().id == auth_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Unauthorized')
    try:
        hashed_password = utils.hash(userSchema.password)
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
    """
    Deletes the user.
    Removes the user's entire video directory ./storage/{user_id}
    """
    user_query = db.query(models.User).filter(models.User.id == id)

    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} does not exist')

    user_id = user_query.first().id
    if not user_id == auth_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Unauthorized')
    remove_vidoes_of_deleted_users(user_id, db)
    user_query.delete(synchronize_session=False)
    db.commit()

    return {"user": "deleted"}


def remove_vidoes_of_deleted_users(user_id, db):
    """
    Cascades the effect of user deletion. With the way the database is
    created, there is no association between User and Videos. Both have
    common reference Mapping that is used to remove Videos uploaded by User
    """
    mapping: models.Mapping = db.query(models.Mapping).filter(
        models.Mapping.u_id == user_id).all()
    vid_ids = [vids.v_id for vids in mapping]
    for id in vid_ids:
        video: models.Video = db.query(
            models.Video).filter(models.Video.id == id)
        utils.delete_entire_folder(user_id)
        video.delete(synchronize_session=False)
    db.commit()
