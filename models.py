from database import base
from sqlalchemy import Column, ForeignKey,Integer,Boolean,String
from datetime import datetime
from sqlalchemy.orm import relationship
import passlib.hash as _hash

class User2(base):
    __tablename__ = "student2"
    id = Column (Integer,primary_key=True ,index=True)
    name = Column(String(50))
    email = Column(String(100),unique=True)
    password = Column (String(30))


class UserModel(base):
    __tablename__ = "users"
    id = Column (Integer,primary_key=True ,index=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String,unique=True,index=True)
    password_hash = Column (String)
    created_at = Column(datetime,default=datetime.utcnow())
    posts = relationship("post",back_populates='user')

    def password_verification(self,password:str):
        return _hash.bcrypt.verify(password,self.password_hash)

class PostModel(base):
     __tablename__ = "posts"
     id = Column (Integer,primary_key=True ,index=True)
     user_id = Column (Integer,ForeignKey("users.id")) # A foreign key is a relational database concept that establishes a relationship between two tables. It is a column or a set of columns in one table that refers to the primary key of another table.
     post_title = Column(String,index=True)
     post_description = Column(String,index=True)
     created_at = Column(datetime,default=datetime.utcnow())
     user = relationship("user",back_populates='posts')

    # user: This attribute represents the relationship from the "post" entity back to the "user" entity. It will be used to access the user associated with a particular post.
    # relationship("user"): This specifies the target entity or table with which the relationship is being established. In this case, it indicates that the relationship is with the "user" entity.
    # back_populates='posts': This parameter indicates that the "user" entity has a corresponding attribute named "posts" that establishes the reverse relationship with the "post" entity.
