from sqlalchemy.sql.expression import text
from ..database.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
class Video(Base):
    __tablename__ = "videos"
    v_id = Column(Integer, primary_key=True, nullable=False)
    vid_title = Column(String, nullable=False)
    vid_desc = Column(String, nullable=True)
    vid_URI = Column(String, nullable=False, unique=True)
    vid_len = Column(Integer, nullable=False)
    vid_size = Column(Integer, nullable=False)
    vid_type = Column(String, nullable=False)
    upload_cost = Column(Float, nullable = False) #associated costs to each video for the user
    uploaded_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    u_id = Column(Integer, ForeignKey('users.u_id', ondelete='CASCADE'))
    


    user = relationship("User", back_populates = "videos")


