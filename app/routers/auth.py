from django.db import router
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentications']
)



@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            details=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            details=f"Invalid Credentials")

    # cretae JWT tocken here !
    access_token = oauth2.created_access_token(date = {"user_id": user.id})
    return {"access_token" : access_token, "token_type": "bearer"}
    
    # return {"token": "Example Token"}
