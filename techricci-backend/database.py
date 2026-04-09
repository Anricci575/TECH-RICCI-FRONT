from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Formato: mysql+pymysql://usuario:contraseña@servidor:puerto/nombre_bd
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:12345678@localhost:3306/techricci_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para inyectar la sesión de la base de datos en cada ruta
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()