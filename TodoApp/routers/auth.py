from fastapi import APIRouter , Depends, status ,HTTPException
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm ,OAuth2PasswordBearer 
from jose import jwt, JWTError
from datetime import timedelta
import datetime 

router = APIRouter(
    prefix = "/auth",
    tags = ["authentication"]
)

SECRET_KEY = '06e27fc5fc4f87baee250ac1398e6a80c5a379de70466b4c5d98586390057515'
ALGORITHM = 'HS256'


#dont know the meaning of this line entirely
bcrypt_context = CryptContext(schemes=['bcrypt'] , deprecated = 'auto')
oauth2bearer = OAuth2PasswordBearer(tokenUrl = "auth/token")

#what is bearer token and how it is used ?


class CreateUserRequest(BaseModel):

    user_name :str
    email:str
    first_name: str
    last_name: str
    password :str
    role : str

class Token(BaseModel):

    access_token :str 
    token_type : str 



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session , Depends(get_db)]


def authenticate_user(username : str ,password :str, db:db_dependency):
    user = db.query(Users).filter(Users.user_name == username).first()
    if not user:
        return False
    if bcrypt_context.verify(password , user.hashed_password):
        return user
    else:
        return False

async def get_current_user(token : Annotated[str, Depends(oauth2bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms= [ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get('id')
        if username is None  or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return username , user_id 
    except JWTError:                                                        #what is JWT Error ? why it is used ? 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

def create_access_token(username :str , user_id : int , expires_delta : timedelta):
    encode = {'sub' : username , 'id' : user_id }
    expires = datetime.datetime.now() + expires_delta              #didnt understood this line 
    encode.update({'exp': expires})
    return jwt.encode(encode , SECRET_KEY , algorithm=ALGORITHM)


@router.post("/" , status_code = status.HTTP_201_CREATED)
async def get_user(db: db_dependency, create_user_request: CreateUserRequest):
     create_user_model = Users(
        email=create_user_request.email,
        user_name=create_user_request.user_name,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role = create_user_request.role,
        hashed_password =bcrypt_context.hash( create_user_request.password),
        is_active=True
     )
    
     db.add(create_user_model)
     db.commit()


@router.post("/token", response_model = Token)
async def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()],db : db_dependency):
    user = authenticate_user(form_data.username ,form_data.password, db )

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) 
    token = create_access_token(user.user_name, user.id, timedelta(minutes = 20))
    return {'access_token' : token , 'token_type' : 'bearer'}