from database import base
from sqlalchemy import Column,Integer,Boolean,String

class User2(base):
    __tablename__ = "student2"
    id = Column (Integer,primary_key=True ,index=True)
    name = Column(String(50))
    email = Column(String(100),unique=True)
    password = Column (String(30))


