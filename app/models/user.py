from sqlalchemy import Column, Integer, String,DateTime,Date,SmallInteger,ForeignKey
from db.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Gender():
    FEMALE  = 0
    MALE    = 1
    UNKNOWN = 2


class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name            = Column(String, index=True,nullable=True)
    email           = Column(String, unique=True, index=True)
    password        = Column(String)
    phone_number    = Column(String, index=True,nullable=True)
    date_joined     = Column(DateTime,insert_default=datetime.now())
    dob             = Column(Date,nullable=True) 
    gender          = Column(SmallInteger,insert_default=Gender.UNKNOWN)            
    identity_number = Column(String,index=True)
    invited         = Column(Integer,insert_default=0)


    ### others columns
    introducer = Column(Integer, ForeignKey("users.id"), nullable=True)
    # introducer = relationship("User", remote_side=[id]) ##second way to declare foreign key

    last_modifier = Column(Integer, ForeignKey("users.id"), nullable=True)
    last_modified = Column(DateTime,insert_default=datetime.now())