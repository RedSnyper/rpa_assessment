from sqlalchemy.sql.expression import text
from ..database.db import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class UserDetail(Base):
    __tablename__ = "user_details"
    id = Column(Integer, primary_key=True, nullable=False)
    u_id = Column(Integer,ForeignKey("users.id", ondelete='CASCADE'))
    vid_count = Column(Integer, server_default=text('0'))
    total_spent = Column(Float, server_default=text('0'))


