import enum
from sqlalchemy.sql.expression import text
from ..database.db import Base
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from sqlalchemy import Integer, Enum

valid_len = 10 * 60 # 10min to seconds
valid_size = 1 * 1024 ** 3 #1GB to byte

class VideoType(enum.Enum):
    mkv = 1
    mp4 = 2

class Video(Base):
    __tablename__ = "videos"
    v_id = Column(Integer, primary_key=True, nullable=False)
    vid_title = Column(String, nullable=False)
    vid_desc = Column(String, nullable=True)
    vid_URI = Column(String, nullable=False, unique=True)
    vid_len = Column(Integer, CheckConstraint(f'vid_len<={valid_len}'), nullable=False,)
    vid_size = Column(Integer,CheckConstraint(f'vid_size<={valid_size}'), nullable=False)
    vid_type = Column(Enum(VideoType), nullable=False)
    upload_cost = Column(Float, nullable = False)
    uploaded_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    u_id = Column(Integer, ForeignKey('users.u_id', ondelete='CASCADE'))
    
    user = relationship("User", back_populates = "videos")


