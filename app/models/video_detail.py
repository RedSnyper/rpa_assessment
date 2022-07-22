from ..database.db import Base
from sqlalchemy import Column, Integer, Float, ForeignKey, CheckConstraint
from sqlalchemy.types import Enum
import enum

valid_len = 10 * 60 # 10min to seconds
valid_size = 1 * 1024 ** 3 #1GB to byte

class VideoType(enum.Enum):
    mkv = 'mkv'
    mp4 = 'mp4'

class VideoDetail(Base):
    __tablename__ = "video_details"
    id = Column(Integer, primary_key=True, nullable=False)
    v_id = Column(Integer,ForeignKey("videos.id", ondelete='CASCADE'))
    len = Column(Integer, CheckConstraint(f'len<={valid_len}'), nullable=False,)
    size = Column(Integer,CheckConstraint(f'size<={valid_size}'), nullable=False)
    type = Column(Enum(VideoType), nullable=False)
    upload_cost = Column(Float, nullable = False)

    