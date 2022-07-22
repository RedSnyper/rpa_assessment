from pydantic import BaseModel

class PaymentInfo(BaseModel):
    vid_title: str
    cost: int

class PaymentResponse(BaseModel):
    payment: str
    class Config: 
        orm_mode = True