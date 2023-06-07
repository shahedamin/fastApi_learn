from database import engine,base,SessionLocal
import models,schemas
from sqlalchemy.orm import Session
from email_validator import validate_email,EmailNotValidError
import fastapi
import passlib.hash as _hash
import jwt as jwt
JWT_SECRET = "JJJJJJJJJJJJJJJJJJUEHEIUGHFFIURIUIUGRHRIURIUGHU"

def create_db():
    return base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create_db()

async def getUserByEmail(email:str,db:Session):
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()

async def create_user(user:schemas.UserRequest,db:Session):
    try:
        isValid = validate_email(email=user.email)
        email = isValid.email
    except EmailNotValidError:
        raise fastapi.HTTPException(status_code=400,detail="Provide valid email")
    
    
    hashed_password = _hash.bcrypt.hash(user.password)
    user_object = models.UserModel(
        name = user.name,
        email = email,
        phone = user.phone,
        password_hash = hashed_password

    )
    
    db.add(user_object)
    db.commit()
    db.refresh(user_object)
    return user_object


async def create_token(user:models.UserModel):
    #convert user model to user schema
    user_schema = schemas.UserResponse.from_orm(user)
    #convert object  to dictionary
    user_dict = user_schema.dict()
    del user_dict["created_at"]

    token =  jwt.encode(user_dict,JWT_SECRET)
    return dict(access_token=token,token_type = "bearer")

