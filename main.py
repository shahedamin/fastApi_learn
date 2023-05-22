

# @app.get('/home/{name}')
# def root(name:str):
#     return {
#         'message':f'my name is {name} and I am very lazy'
#     }


# @app.get('/')
# def root2(name:str):
#     return {
#         'message':f'my name is {name} and I am very lazy'
#     }



###########################################################################################
from enum import Enum
from fastapi import Depends, FastAPI, HTTPException, Request, WebSocket
from pydantic import BaseModel
from database import engine,base,SessionLocal
from sqlalchemy import Column,Integer,Boolean,String
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from models import User2
from fastapi.responses import JSONResponse
# Why use ORM(sqlalchemy)- It handles tasks like data validation, serialization, and querying the database using an object-oriented API.
#  In synchronous programming, tasks are executed one after another in a sequential manner. In asynchronous programming, tasks can start executing without waiting for the completion of previous tasks

app=FastAPI()

# Create model
class Userss(base):
    __tablename__='student'
    id=Column(Integer,primary_key=True,index= True)
    email= Column (String,unique=True,index=True)
    is_active = Column (Boolean,default=True) 
    
# Connect model to database
base.metadata.create_all(bind=engine)


# This function will be used for CRUD operation
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


# This is schema.
# A schema refers to a formal definition or specification of the structure, data types, and constraints of a dataset. 
# It outlines the expected format, organization, and rules that the data should adhere to.A schema provides a blueprint or contract that defines the valid structure and properties of data. It acts as a guide for data validation, ensuring that the incoming data meets the defined criteria. By enforcing a schema, you can validate the integrity and quality of data and prevent errors or inconsistencies.
class Student_schema(BaseModel):
    id:int
    email:str
    is_active:bool

    class Config:
        orm_mode=True
    
@app.post('/users',response_model=Student_schema)
# As we are using post method,so we need to do CRUD with (Session) function
# Here we use depends function, so that we can use get_db function in multiple endpoints.
def index(user:Student_schema,db:Session=Depends(get_db)):
    s=Userss(id=user.id,email=user.email,is_active=user.is_active)
    db.add(s)
    db.commit() # Here we commit, because in database.py autocommit was false.
    return s

@app.get('/users',response_model=list[Student_schema])
def index(db:Session=Depends(get_db)):
    return db.query(Userss).all()

#-------------------------------------------------------------------------------------------

class Student_schema2(BaseModel):
    name:str
    email:str
    
    class Config:
        orm_mode = True

# As we don't need password in get method,so we create another schema with password for post method.
class Student_create_schema2(Student_schema2):
    password:str

@app.get('/users2',response_model=list[Student_schema2])
def get_users2(db:Session=Depends(get_db)):
    return db.query(User2).all()

@app.post('/users2',response_model=Student_schema2) # Here we only use Student_schema2,so that in response we get only name and email,not password.If we use Student_create_schema2,then password will also be shown in response.
def get_users2(user:Student_create_schema2,db:Session=Depends(get_db)):
    ss = User2(name=user.name,email=user.email,password=user.password)
    db.add(ss)
    db.commit()
    return ss

@app.put('/users2/{user_id}',response_model=Student_schema2) # path parameter
# put method will take 2 arguments.which id will change and schema class for that id
def update_users2(user_id:int,user:Student_schema2,db:Session=Depends(get_db)): # user:Student_schema2,we use Student_schema2 not Student_create_schema2, cause we will use another function for update password.
    try:
        u=db.query(User2).filter(User2.id==user_id).first() # Check whether this user id exists or not
        u.name= user.name
        u.email= user.email
        db.add(u)
        db.commit()
        return u
    except:
        return HTTPException(status_code=404,detail="User not found")
    
@app.delete('/users2/{user_id}',response_class=JSONResponse) # which type of response you want to return
def delete_users2(user_id:int,db:Session=Depends(get_db)): 
    try:
        u=db.query(User2).filter(User2.id==user_id).first() # Check whether this user id exists or not
        db.delete(u)
        db.commit()
        return {f"{user_id} this user has been deleted ":True}
    except:
        return HTTPException(status_code=404,detail="User not found")
    

# --------------------------------------------------------------------------------------------

templates=Jinja2Templates(directory="templates")

@app.get ('/home')
async def home(request:Request):
    return templates.TemplateResponse("homepage.html",{"request":request}) # In the provided code snippet, the ,{"request": request} part is used to pass additional data to the template when rendering the "homepage.html" template using templates.TemplateResponse.


webSocket_list=[]
@app.websocket("/ws") # WebSockets are used to enable real-time, bidirectional communication between a client and a server
# With async def, Python knows that, inside that function, it has to be aware of await expressions, and that it can "pause" ⏸ the execution of that function and go do something else 🔀 before coming back.
async def websocket_endpoint(websocket:WebSocket):
    await websocket.accept()
    if websocket not in webSocket_list:
        webSocket_list.append(websocket)
    while True:
        data=await websocket.receive_text()
        for i in webSocket_list:
            if i != websocket: # prevent to send back the same message to the sender
                await i.send_text(f'{data}') # Send the message to the receiver

# -------------------------------------------------------------------

# path parameter with fixed value
class Path_parameter_with_pre(str,Enum):
    s1="shahed"
    s2= "abid"
    s3="joy"
@app.get('/path_para/{roll}')
def pre_path(roll:Path_parameter_with_pre):
    if roll is Path_parameter_with_pre.s1:
        return{Path_parameter_with_pre.s1}
    else:
        return{Path_parameter_with_pre.s2,Path_parameter_with_pre.s3}

# "/files/home/johndoe/myfile.txt." here myfile.txt is also a path.So we should handle it like this
@app.get('/johndoe/{file_path:path }')
def read_file(file_path:str):
    return{file_path}

# When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.
@app.get("/query_para_test")
async def read_item(skip: int = 0, limit: int = 10):
    fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
    return fake_items_db[skip : skip + limit]