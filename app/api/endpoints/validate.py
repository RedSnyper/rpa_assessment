import os
from fastapi import APIRouter, UploadFile, Depends
from fastapi import File, HTTPException, status
from pymediainfo import MediaInfo
from app.schemas import ValidatedFileResponse

vid_type = [".mp4", ".mkv"]
max_size = 1024 ** 3


router = APIRouter(
    prefix="/validate",
    tags=['Validate']
)


def validate_file(file) -> dict:
    file_name, file_type = os.path.splitext(file.filename)
    if file_type not in vid_type:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail=f'file type {file_type} not supported')
    file.file.seek(0, 2)
    file_size = file.file.tell()
    if not file_size <= max_size:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f'file size {round(file_size/max_size,2)}GB exceeds the limit of 1GB')
    media = MediaInfo.parse(file.file)
    file_duration = media.tracks[0].duration  # returns in millisec
    file_duration /= 1000
    mins, sec = divmod(file_duration, 60)
    if not file_duration <= 600:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f'file duration {mins}:{sec} mins exceeds time of 10mins')

    return {
        "title": file_name,
        "type": file_type,
        "size": file_size,
        "duration": file_duration
    }


@router.post("/", response_model=ValidatedFileResponse, status_code=status.HTTP_200_OK)
async def validate_upload(file: UploadFile):
    """
        Endpoint exposed for users to check if the video can be uploaded or not.
    """
    response = await validate_file(file)
    return response
