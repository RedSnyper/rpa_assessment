from sqlalchemy.sql.expression import text
from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    desc = Column(String, nullable=True)
    URI = Column(String, nullable=False, unique=True)
    uploaded_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    detail = relationship("VideoDetail", backref="videos") 
