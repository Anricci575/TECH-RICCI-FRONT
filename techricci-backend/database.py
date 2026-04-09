import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Obtenemos la URL desde Vercel (Variables de Entorno).
# Si no la encuentra (porque estás programando en tu PC local), usará tu conexión de siempre.
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:12345678@localhost:3306/techricci_db")

# 2. Parche de compatibilidad para la nube: 
# Las URLs de Railway empiezan con "mysql://", pero tu librería necesita "mysql+pymysql://"
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

# 3. Creación del motor con la URL final (sea local o nube)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para inyectar la sesión de la base de datos en cada ruta
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()