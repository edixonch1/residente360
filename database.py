from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔴 PEGA AQUÍ TU URL DE SUPABASE
DATABASE_URL = "postgresql://postgres:Chingate123#@db.xxx.supabase.co:5432/postgres"

# ⚙️ Motor de base de datos
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)

# 🧠 Sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🧱 Base para modelos
Base = declarative_base()
