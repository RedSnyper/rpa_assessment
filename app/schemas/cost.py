from pydantic import BaseModel

class CalculateCostOn(BaseModel):
    vid_size: int
    vid_length: int

class Cost(BaseModel):
    cost: float

    class Config: 
        orm_mode = True