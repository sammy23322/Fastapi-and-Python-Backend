from fastapi import APIRouter, Depends, HTTPException , status, Path
from models import Users
from pydantic import BaseModel, Field
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos, Users
from routers.auth import get_current_user
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm ,OAuth2PasswordBearer 

router = APIRouter(
    prefix = "/user",
    tags = ["user"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# why a class is made and what is the possible solution without classes
class Usererfication(BaseModel):         
    password:str
    new_password:str = Field(min_length= 6)


#dont know the meaning of this line entirely
bcrypt_context = CryptContext(schemes=['bcrypt'] , deprecated = 'auto')
oauth2bearer = OAuth2PasswordBearer(tokenUrl = "auth/token")
db_dependency = Annotated[Session , Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/",  status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401 , detail='Authentication Failed')
    
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency, db:db_dependency,
                          user_verification:Usererfication):
    if user is None:
        raise HTTPException(status_code=401, detail = "authentication failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):           #doubt in this line 
        raise HTTPException(status_code = 401 , detail = "error on password change")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()