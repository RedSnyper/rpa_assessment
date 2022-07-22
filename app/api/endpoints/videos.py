from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
    UploadFile
)
from app import (schemas, models, auth, database, utils)
from typing import List
from sqlalchemy import exc
from sqlalchemy.orm import Session
from typing import Optional
from dataclasses import dataclass
from .costs import calculate_cost
from .validate import validate_file
from .payment import payment_service

router = APIRouter(
    prefix="/videos",
    tags=['Videos']
)


@dataclass
class VideoInfo:
    title: str
    type: str
    size: int
    duration: int


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def upload_file(file: UploadFile, description: str,
                      db: Session = Depends(database.get_db),
                      auth_user: models.User = Depends(auth.oauth2.get_current_user)):
    """
    Upload file. The file gets validated on type, size, length. Cost is calculated
    on basis of size and length. Awaits a mimic payment service handler. On success
    uploads.

    User needs to be login.
    File upload dir = /storage/{user.id}/file  
    """
    vid_resp = validate_file(file)
    video: VideoInfo = VideoInfo(**vid_resp)
    cost = calculate_cost(vid_size=video.size,
                          vid_length=video.duration)
    payment_res: schemas.PaymentResponse = await payment_service(vid_title=video.title, cost=cost)
    if payment_res.payment == "success":
        try:
            file_path = utils.save_video_file(file, f"storage/{auth_user.id}")
            video_record = models.Video(
                title=video.title, desc=description, URI=str(file_path))
            db.add(video_record)
            db.commit()
            vid: models.Video = db.query(models.Video).filter(
                models.Video.title == video_record.title).first()
            db.add(models.Mapping(v_id=vid.id, u_id=auth_user.id))
            db.commit()
            return {"upload": "Success"}
        except exc.IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            detail=f'Integrity error. The video must have been already uploaded by you')
    raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED,
                        detail=f'payment needs to be done first')


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.VideoResponse])
async def get_all_videos(limit: int = 25, skip: int = 0, search: Optional[str] = "", db: Session = Depends(database.get_db)):
    all_vids = db.query(models.Video).order_by(models.Video.uploaded_at.desc()).filter(
        models.Video.title.contains(search.lower())).limit(limit=limit).offset(skip).all()
    if all_vids:
        return all_vids


@router.get('/detail', response_model=List[schemas.VideoDetailResponse])
async def get_video_details(limit: int = 25, skip: int = 0, search: Optional[str] = "", db: Session = Depends(database.get_db)):
    all_vids = db.query(models.Video).join(models.VideoDetail).order_by(models.Video.uploaded_at.desc()).filter(
        models.Video.title.contains(search.lower())).limit(limit=limit).offset(skip).all()
    if all_vids:
        return all_vids


@router.put("/{id}")
async def update_video(id: int, title: str, desc: str, file: Optional[UploadFile] = None,
                       db: Session = Depends(database.get_db),
                       auth_user: models.User = Depends(auth.oauth2.get_current_user)):
    """
    Updates the video details. Updating the entire video not yet implemented

    """
    mapping = models.Mapping =\
        db.query(models.Mapping).filter(models.Mapping.v_id == id)

    video = db.query(models.Video).filter(models.Video.id == id)
    user_query = db.query(models.User).filter(
        models.User.id == mapping.first().u_id)

    if not video.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} does not exist')
    user_id = user_query.first().id
    if not user_id == auth_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Unauthorized')
    try:

        video.first().title = title
        video.first().desc = desc
        video.update({"title": title, "desc": desc},
                     synchronize_session=False)
        if file:
            utils.update_video_file(1, "abc")  # Not Implemented Yet
        db.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="the email already exist. Add unique email")


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(id: int, db: Session = Depends(database.get_db),
                       auth_user: models.User = Depends(auth.oauth2.get_current_user)):
    '''
    Deletes based on the video ids
    '''
    mapping: models.Mapping =\
        db.query(models.Mapping).filter(models.Mapping.v_id == id)

    if not mapping.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'video id:{id} does not exist')
    video = db.query(models.Video).filter(models.Video.id == id)
    user_query = db.query(models.User).filter(
        models.User.id == mapping.first().u_id)

   
    user_id = user_query.first().id
    if not user_id == auth_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Unauthorized')

    video_loc = video.first().URI
    video.delete(synchronize_session=False)
    mapping.delete(synchronize_session=False)
    db.commit()
    utils.delete_video_file(video_loc)
    return {"success": "deleted"}
