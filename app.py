from fastapi import Depends, FastAPI,HTTPException,security
import schemas,services
from sqlalchemy.orm import Session

app = FastAPI()

@app.post("/api/v1/users")
async def register_user(user:schemas.UserRequest,db:Session=Depends(services.get_db)):
    db_user = await services.getUserByEmail(email=user.email,db=db)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already exist')
    
    # Create the user and return a token 
    db_user = await services.create_user(user=user , db=db)
    return await services.create_token(user=db_user)

@app.post("/api/v1/login")
async def login_user(
    form_data:security.OAuth2PasswordRequestForm = Depends(),
    db:Session=Depends(services.get_db)):

    db_user=await services.login(email=form_data.username, password=form_data.password, db=db)
    # If invalid login then throw exception
    if not db_user:
        raise HTTPException(status_code=401, detail="wrong login credentials")
    return await services.create_token(db_user)


@app.get("/api/users/current-user",response_model=schemas.UserResponse)
async def current_user(user:schemas.UserResponse=Depends(services.current_user)):
    return user