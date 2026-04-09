from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import UserModel
from schemas.user import UserCreate, UserOut, UserLogin # Importamos UserLogin
import hashlib

router = APIRouter()

def hash_password(password: str):
    """Encriptación básica usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario o email ya existen
    db_user = db.query(UserModel).filter((UserModel.username == user.username) | (UserModel.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario o email ya está registrado en el sistema.")
    
    # Crear el nuevo usuario
    nuevo_usuario = UserModel(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# --- NUEVO: Endpoint de Login ---
@router.post("/login")
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Verifica las credenciales del usuario para darle acceso"""
    
    # 1. Buscamos si el email existe en MySQL
    db_user = db.query(UserModel).filter(UserModel.email == user_credentials.email).first()
    
    # Si no existe el usuario, lanzamos error 401 (No Autorizado)
    if not db_user:
        raise HTTPException(status_code=401, detail="Acceso denegado: Credenciales inválidas.")
    
    # 2. Encriptamos la clave recibida y la comparamos con la guardada
    if db_user.password_hash != hash_password(user_credentials.password):
        raise HTTPException(status_code=401, detail="Acceso denegado: Credenciales inválidas.")
        
    # 3. Si todo está correcto, devolvemos el acceso y el rol (admin/user)
    return {
        "message": "Auth Gateway Unlocked",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "role": db_user.role
        }
    }