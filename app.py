from fastapi import Depends, FastAPI,HTTPException
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