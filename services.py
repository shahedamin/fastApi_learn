from database import engine,base,SessionLocal
import models,schemas
from sqlalchemy.orm import Session
from email_validator import validate_email,EmailNotValidError
import fastapi
import fastapi.security as _security
import passlib.hash as _hash
import jwt as jwt
JWT_SECRET = "JJJJJJJJJJJJJJJJJJUEHEIUGHFFIURIUIUGRHRIURIUGHU"
oauth2schema = _security.OAuth2PasswordBearer("/api/v1/login")

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


async def login(email:str, password:str, db:Session):
    db_user = await getUserByEmail(email=email, db=db)
    if not db_user:
        return False
    if not db_user.password_verification(password=password):
        return False
    
    return db_user


async def current_user(db:Session=fastapi.Depends(get_db), token:str=fastapi.Depends(oauth2schema)):
    try :
        payload=jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        # Get user by id and id is already available in the decoded user payload along with email,phone and name
        db_user = db.query(models.UserModel).get(payload['id'])
    except:
        raise fastapi.HTTPException(status_code=401, detail="wrong credentials")
    

    # if all ok then return the DTO//Schema version user
    return schemas.UserResponse.from_orm(db_user)