from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import models, schemas, crud, auth, config_gen
from .database import engine, get_db, Base
from .auth import get_current_user

# ایجاد جدول‌ها
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Myapp Panel",
    description="پنل مدیریت VPN ساده",
    version="1.0.0"
)


# -------------------- Auth --------------------

@app.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user(db, email=user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="این ایمیل قبلاً ثبت شده است")
    user = crud.create_user(db, user_in)
    return user


@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user(db, email=form_data.username)
    if not user or not auth.verify_pwd(form_data.password, user.hashed_pwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ایمیل یا رمز عبور اشتباه است",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# -------------------- Keys --------------------

@app.post("/keys", response_model=schemas.KeyCreatedResponse, status_code=status.HTTP_201_CREATED)
def create_key(
    key_in: schemas.KeyCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    key, secret = crud.create_key(db, owner_id=current_user.id, key_in=key_in)
    config_data = config_gen.generate_config(key.protocol, secret, key.ip)

    return {
        "key": key,
        "secret": secret,
        "config": config_data
    }


@app.get("/keys", response_model=list[schemas.KeyOut])
def list_keys(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_keys_by_user(db, owner_id=current_user.id)


@app.delete("/keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    success = crud.delete_key(db, key_id=key_id, owner_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="کلید یافت نشد")
    return None


@app.get("/")
def root():
    return {"message": "Myapp Panel is running"}
