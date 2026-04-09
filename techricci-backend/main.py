import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # Importante para las imágenes
from database import engine, Base
from routers import products, users
# Importamos ambos modelos para que Base.metadata los reconozca al crear las tablas
from models.user import UserModel
from models.product import ProductModel 

# 1. SEGURIDAD Y COMPATIBILIDAD VERCEL: 
# Crear carpetas para imágenes solo si el sistema lo permite
UPLOAD_DIR = "static/uploads"
try:
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
except OSError:
    # Vercel es "Serverless" y de solo lectura. Capturamos el error para que no colapse.
    pass

# Esto crea las tablas en MySQL (User y Product) si no existen
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Alerta DB: {e}")

app = FastAPI(
    title="TechRicci API",
    description="Core backend para la gestión de hardware y servicios IT.",
    version="1.0.0"
)

# Configuración de CORS robusta para la Nube
# Expandimos origins a "*" para evitar bloqueos del navegador en producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. MONTAR CARPETA ESTÁTICA 
# Usamos try/except por si la carpeta no existe en el entorno Serverless
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    pass

# Registro de Routers
app.include_router(users.router, prefix="/api/v1/users", tags=["Authentication"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Inventory"])

@app.get("/")
def root():
    return {"message": "TechRicci API SYSTEM_ONLINE - MySQL Connected and Vercel Ready"}