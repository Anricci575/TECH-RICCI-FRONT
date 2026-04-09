from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    nombre: str
    # Cambiamos precio a float para que coincida con el modelo de la DB
    precio: float 
    # Renombrado de 'specs' a 'descripcion' para coincidir con el Frontend
    descripcion: str 
    # --- NUEVOS CAMPOS DEL INVENTARIO ---
    categoria: str
    stock: int
    
    # --- NUEVO CAMPO DE IMAGEN ---
    # Usamos Optional porque algunos equipos pueden no tener foto al registrarlos
    imagen: Optional[str] = None 

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    status: str # Añadimos status para que Vue.js sepa si pintar ONLINE o SOLD_OUT

    class Config:
        from_attributes = True