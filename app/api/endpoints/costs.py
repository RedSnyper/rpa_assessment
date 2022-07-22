from fastapi import APIRouter, Depends, status
from app.schemas import CalculateCostOn, Cost

router = APIRouter(
    prefix="/cost",
    tags=['Cost']
)
# 5$ for video below 500MB and 12.5$ above 500MB.
# Additional 12.5$ if the video is under 6 minutes 18 second and
# 20$ if above.


def calculate_cost(vid_size: int = 0, vid_length: int = 0) -> float:
    base_cost = 5 if vid_size < (500 * 1024**2) else 12.5
    additional_cost = 12.5 if vid_length < (6*60 + 18) else 20
    return round(base_cost + additional_cost, 2)


@router.get("/", response_model=Cost, status_code=status.HTTP_200_OK)
def get_cost(fields: CalculateCostOn = Depends()):
    return {"cost": calculate_cost(fields.vid_size, fields.vid_length)}
