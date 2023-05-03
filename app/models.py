from database import Base
from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "posts_table"
    id = Column(Integer, primary_key=True, nullable=False,index=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean, server_default='TRUE')
    created_by=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    # owner_id = Column(Integer, ForeignKey("users.id"))
    # owner = relationship("User", back_populates="posts")