from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user" # Por defecto es usuario normal

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True

# --- NUEVO: Esquema para validar el inicio de sesión ---
class UserLogin(BaseModel):
    email: str
    password: str