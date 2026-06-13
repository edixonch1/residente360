from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String


# =========================
# BASE
# =========================
class Base(DeclarativeBase):
    pass


# =========================
# BITÁCORA
# =========================
class Bitacora(Base):
    __tablename__ = "bitacoras"

    id = Column(Integer, primary_key=True)
    fecha = Column(String)
    clima = Column(String)
    actividad = Column(String)
    observacion = Column(String)


# =========================
# LLUVIA
# =========================
class Lluvia(Base):
    __tablename__ = "lluvias"

    id = Column(Integer, primary_key=True)
    fecha = Column(String)
    inicio = Column(String)
    fin = Column(String)
    intensidad = Column(String)
    observacion = Column(String)


# =========================
# FOTOS
# =========================
class Foto(Base):
    __tablename__ = "fotos"

    id = Column(Integer, primary_key=True)
    fecha = Column(String)
    descripcion = Column(String)

    # SOLO nombre del archivo
    archivo = Column(String)