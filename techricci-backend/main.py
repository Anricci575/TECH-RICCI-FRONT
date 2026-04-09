import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # Importante para las imágenes
from database import engine, Base
from routers import products, users
# Importamos ambos modelos para que Base.metadata los reconozca al crear las tablas
from models.user import UserModel
from models.product import ProductModel 

# 1. SEGURIDAD: Crear carpetas para imágenes si no existen
UPLOAD_DIR = "static/uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Esto crea las tablas en MySQL (User y Product) si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TechRicci API",
    description="Core backend para la gestión de hardware y servicios IT.",
    version="1.0.0"
)

# Configuración de CORS robusta
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. MONTAR CARPETA ESTÁTICA 
# Esto permite que las imágenes sean accesibles vía URL
app.mount("/static", StaticFiles(directory="static"), name="static")

# Registro de Routers
app.include_router(users.router, prefix="/api/v1/users", tags=["Authentication"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Inventory"])

@app.get("/")
def root():
    return {"message": "TechRicci API SYSTEM_ONLINE - MySQL Connected and Static Files Mounted"}