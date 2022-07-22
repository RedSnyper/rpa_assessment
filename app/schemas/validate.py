from pydantic import BaseModel


class FileInput(BaseModel):
    """
    File inputs are sent as form-data but pydantic validates
    json only. 
    TODO: find a way to make this work
    """
    pass

class ValidatedFileResponse(BaseModel):
    video_name: str
    video_type: str
    video_size: int
    video_duration: int

    class Config:
        orm_mode = True
