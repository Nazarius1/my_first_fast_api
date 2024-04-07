from datetime import datetime, timedelta
from pkgutil import get_data
from venv import create
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
import schema,database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM =  os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# it is also possible to get the environment values from your system!
# try:
# path =  os.getenv("PATH")
# print(path)



def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)) #type: ignore
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=str(ALGORITHM))

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:

        payload = jwt.decode(token, str(SECRET_KEY), algorithms=str([ALGORITHM]))

        id = payload.get("user_id") 

        if id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials", 
                                          headers={"WWW-Authenticate":"Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id==token.id).first()
    return user
