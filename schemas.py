from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    email:str
    name:str
    phone:str
    
class UserRequest(UserBase):
    password:str
    
    class Config:
        orm_mode = True

class UserResponse(UserBase):
    id : int
    created_at: datetime

    class Config:
        orm_mode = True