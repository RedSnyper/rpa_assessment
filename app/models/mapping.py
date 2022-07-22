from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer

class Mapping(Base):
    __tablename__ = "mappings"
    id = Column(Integer, primary_key=True, nullable=False)
    u_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    v_id = Column(Integer, ForeignKey("videos.id", ondelete='CASCADE'))
    