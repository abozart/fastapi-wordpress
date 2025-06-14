from sqlalchemy import text
from passlib.hash import phpass
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from .database import get_db

security = HTTPBasic()


def verify_wp_user(db, username: str, password: str) -> bool:
    result = db.execute(text("SELECT user_pass FROM wp_users WHERE user_login=:login"), {"login": username}).fetchone()
    if result:
        return phpass.verify(password, result[0])
    return False


def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db=Depends(get_db)):
    if verify_wp_user(db, credentials.username, credentials.password):
        return credentials.username
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
