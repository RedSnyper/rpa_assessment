from typing import Optional
from fastapi import APIRouter, Depends
from app.schemas import PaymentResponse, PaymentInfo

router = APIRouter(
    prefix="/payment",
    tags=['Payment']
)


async def payment_service_factory(service=None):
    """
        initialize some payment service here 
    """
    return {"payment": "success"}


async def payment_service(vid_title: str, cost: int, *args) -> PaymentResponse:
    """
        process some payment thingy here 
    """
    response = await payment_service_factory()
    return PaymentResponse(**response)
