from sqlalchemy.orm import Session
import secrets

from . import models, schemas
from .auth import hash_pwd
from .settings import settings


def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed = hash_pwd(user.password)
    db_user = models.User(email=user.email, hashed_pwd=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_key(db: Session, owner_id: int, key_in: schemas.KeyCreate):
    # انتخاب IP
    ip = key_in.ip or secrets.choice(settings.IP_POOL)

    # ساخت secret واقعی (فقط یک بار به کاربر نشان داده می‌شود)
    secret = secrets.token_urlsafe(32)

    key = models.APIKey(
        name=key_in.name,
        protocol=key_in.protocol,
        ip=ip,
        key_hash=hash_pwd(secret),
        owner_id=owner_id,
    )
    db.add(key)
    db.commit()
    db.refresh(key)
    return key, secret


def get_keys_by_user(db: Session, owner_id: int):
    return db.query(models.APIKey).filter(models.APIKey.owner_id == owner_id).all()


def get_key(db: Session, key_id: int, owner_id: int):
    return (
        db.query(models.APIKey)
        .filter(models.APIKey.id == key_id, models.APIKey.owner_id == owner_id)
        .first()
    )


def delete_key(db: Session, key_id: int, owner_id: int) -> bool:
    key = get_key(db, key_id, owner_id)
    if not key:
        return False
    db.delete(key)
    db.commit()
    return True
