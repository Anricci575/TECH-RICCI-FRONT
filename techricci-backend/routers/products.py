import os
import shutil
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from database import get_db
from models.product import ProductModel
from schemas.product import Product  # Quitamos ProductCreate porque ahora usamos Form

router = APIRouter()

@router.get("/", response_model=list[Product])
def get_all_products(db: Session = Depends(get_db)):
    """Obtiene todo el inventario de la base de datos MySQL"""
    productos = db.query(ProductModel).all()
    return productos

@router.post("/", response_model=Product)
async def create_product(
    # Recibimos los datos individualmente como Form para permitir la imagen
    nombre: str = Form(...),
    precio: float = Form(...),
    descripcion: str = Form(...),
    categoria: str = Form(...),
    stock: int = Form(...),
    file: Optional[UploadFile] = File(None), # Archivo de imagen (Opcional)
    db: Session = Depends(get_db)
):
    """Añade un nuevo equipo e imagen a la base de datos"""
    
    file_path = None
    
    # 1. Si viene una imagen desde el Frontend, la guardamos físicamente
    if file:
        upload_dir = "static/uploads"
        # Creamos la carpeta si no existe
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        # Reemplazamos espacios en el nombre del archivo para evitar errores web
        safe_filename = file.filename.replace(" ", "_")
        file_path = f"{upload_dir}/{safe_filename}"
        
        # Guardamos el archivo binario en el disco duro
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    # 2. Construimos el modelo para MySQL
    nuevo_producto = ProductModel(
        nombre=nombre,
        precio=precio,
        descripcion=descripcion, 
        categoria=categoria,     
        stock=stock,             
        imagen=file_path         # <--- Guardamos la ruta de la imagen en la BD
    )
    
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto