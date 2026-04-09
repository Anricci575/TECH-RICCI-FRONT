from sqlalchemy import Column, Integer, String, Float
from database import Base

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), index=True, nullable=False)
    # Usamos Float para que MySQL maneje decimales de moneda correctamente
    precio = Column(Float, nullable=False) 
    
    # Este campo debe llamarse 'descripcion' para que el JSON de Vue.js encaje perfecto
    descripcion = Column(String(500), nullable=False) 
    
    # --- CAMPOS DE GESTIÓN DE INVENTARIO ---
    categoria = Column(String(50), nullable=False)
    stock = Column(Integer, default=1)
    status = Column(String(20), default="ONLINE")
    
    # --- NUEVA COLUMNA PARA IDENTIDAD VISUAL (IMAGEN) ---
    # nullable=True porque no todos los productos/reparaciones tendrán foto obligatoria
    imagen = Column(String(255), nullable=True)