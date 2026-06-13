from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

from calendar import monthrange
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

import os
import shutil

from database import engine
from models import Bitacora, Lluvia, Foto

app = FastAPI()

# =========================
# CARPETAS
# =========================
os.makedirs("static/fotos", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


# =========================
# MENÚ PRINCIPAL
# =========================
@app.get("/", response_class=HTMLResponse)
def inicio():

    return """
    <html>
    <body style="font-family:Arial; padding:20px;">

        <h1>🏗️ Residente360</h1>

        <hr>

        <h2>📝 Bitácora</h2>
        <a href="/bitacora"><button>➕ Nueva</button></a><br><br>
        <a href="/ver-bitacoras"><button>📋 Ver Bitácoras</button></a><br><br>

        <hr>

        <h2>🌧 Lluvia</h2>
        <a href="/lluvia"><button>Registrar</button></a><br><br>

        <hr>

        <h2>📷 Fotos</h2>
        <a href="/fotos"><button>Subir</button></a><br><br>
        <a href="/ver-fotos"><button>Ver</button></a><br><br>

        <hr>

        <h2>📅 Calendario</h2>
        <a href="/calendario"><button>Ver Calendario</button></a><br><br>

        <hr>

        <h2>📄 Informe</h2>

        <form action="/informe" method="get">

            📅 Día:<br>
            <input type="date" name="fecha_dia"><br><br>

            📆 Mes:<br>
            <input type="month" name="fecha_mes"><br><br>

            <button>Generar PDF</button>

        </form>

    </body>
    </html>
    """


# =========================
# BITÁCORA
# =========================
@app.get("/bitacora", response_class=HTMLResponse)
def bitacora():

    return """
    <h1>📝 Bitácora</h1>

    <form action="/guardar-bitacora" method="post">

        Fecha: <input type="date" name="fecha"><br><br>

        Clima:
        <select name="clima">
            <option>Soleado</option>
            <option>Nublado</option>
            <option>Lluvioso</option>
        </select><br><br>

        Actividad:<br>
        <textarea name="actividad"></textarea><br><br>

        Observación:<br>
        <textarea name="observacion"></textarea><br><br>

        <button>Guardar</button>

    </form>

    <a href="/">Volver</a>
    """


@app.post("/guardar-bitacora")
def guardar_bitacora(
    fecha: str = Form(...),
    clima: str = Form(...),
    actividad: str = Form(...),
    observacion: str = Form(...)
):

    with Session(engine) as session:
        session.add(Bitacora(
            fecha=fecha,
            clima=clima,
            actividad=actividad,
            observacion=observacion
        ))
        session.commit()

    return RedirectResponse(url="/", status_code=303)


@app.get("/ver-bitacoras", response_class=HTMLResponse)
def ver_bitacoras():

    with Session(engine) as session:
        bitacoras = session.query(Bitacora).order_by(Bitacora.id.desc()).all()

    html = ""

    for b in bitacoras:
        html += f"""
        <div style="border:1px solid #ccc; padding:10px; margin:10px;">
            <h3>📅 {b.fecha}</h3>
            <p><b>Clima:</b> {b.clima}</p>
            <p><b>Actividad:</b> {b.actividad}</p>
            <p><b>Observación:</b> {b.observacion}</p>
        </div>
        """

    return f"""
    <html>
    <body style="font-family:Arial; padding:20px;">
        <h1>📋 Bitácoras</h1>
        {html}
        <a href="/">Volver</a>
    </body>
    </html>
    """


# =========================
# LLUVIA
# =========================
@app.get("/lluvia", response_class=HTMLResponse)
def lluvia():

    return """
    <h1>🌧 Lluvia</h1>

    <form action="/guardar-lluvia" method="post">

        Fecha: <input type="date" name="fecha"><br><br>
        Inicio: <input type="time" name="inicio"><br><br>
        Fin: <input type="time" name="fin"><br><br>

        Intensidad:
        <select name="intensidad">
            <option>Leve</option>
            <option>Moderada</option>
            <option>Fuerte</option>
        </select><br><br>

        Observación:<br>
        <textarea name="observacion"></textarea><br><br>

        <button>Guardar</button>

    </form>

    <a href="/">Volver</a>
    """


@app.post("/guardar-lluvia")
def guardar_lluvia(
    fecha: str = Form(...),
    inicio: str = Form(...),
    fin: str = Form(...),
    intensidad: str = Form(...),
    observacion: str = Form(...)
):

    with Session(engine) as session:
        session.add(Lluvia(
            fecha=fecha,
            inicio=inicio,
            fin=fin,
            intensidad=intensidad,
            observacion=observacion
        ))
        session.commit()

    return RedirectResponse(url="/", status_code=303)


# =========================
# FOTOS
# =========================
@app.get("/fotos", response_class=HTMLResponse)
def fotos():

    return """
    <h1>📷 Fotos</h1>

    <form action="/guardar-foto" method="post" enctype="multipart/form-data">

        Fecha: <input type="date" name="fecha"><br><br>
        Descripción:<br>
        <input type="text" name="descripcion"><br><br>

        Archivo: <input type="file" name="archivo"><br><br>

        <button>Subir</button>

    </form>

    <a href="/">Volver</a>
    """


@app.post("/guardar-foto")
def guardar_foto(
    fecha: str = Form(...),
    descripcion: str = Form(...),
    archivo: UploadFile = File(...)
):

    ruta = f"static/fotos/{archivo.filename}"

    with open(ruta, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)

    with Session(engine) as session:
        session.add(Foto(
            fecha=fecha,
            descripcion=descripcion,
            archivo=archivo.filename
        ))
        session.commit()

    return RedirectResponse(url="/ver-fotos", status_code=303)


@app.get("/ver-fotos", response_class=HTMLResponse)
def ver_fotos():

    with Session(engine) as session:
        fotos = session.query(Foto).all()

    html = ""

    for f in fotos:
        html += f"""
        <div>
            <h3>{f.fecha}</h3>
            <p>{f.descripcion}</p>
            <img src="/static/fotos/{f.archivo}" width="250">
        </div>
        <hr>
        """

    return f"""
    <html>
    <body style="font-family:Arial; padding:20px;">
        <h1>📷 Fotos</h1>
        {html}
        <a href="/">Volver</a>
    </body>
    </html>
    """


# =========================
# CALENDARIO CLICABLE
# =========================
@app.get("/calendario", response_class=HTMLResponse)
def calendario(mes: str = None):

    if not mes:
        mes = datetime.now().strftime("%Y-%m")

    year, month = map(int, mes.split("-"))
    dias_mes = monthrange(year, month)[1]

    with Session(engine) as session:
        bitacoras = [b.fecha for b in session.query(Bitacora).all()]
        lluvias = [l.fecha for l in session.query(Lluvia).all()]
        fotos = [f.fecha for f in session.query(Foto).all()]

    html = ""

    for d in range(1, dias_mes + 1):

        fecha = f"{year}-{str(month).zfill(2)}-{str(d).zfill(2)}"

        clase = "dia"

        if fecha in bitacoras:
            clase += " bitacora"
        if fecha in lluvias:
            clase += " lluvia"
        if fecha in fotos:
            clase += " foto"

        html += f"""
        <a href="/dia/{fecha}" style="text-decoration:none;">
            <div class="{clase}">
                {d}
            </div>
        </a>
        """

    return f"""
    <html>
    <head>
        <style>
            .dia {{
                display:inline-block;
                width:80px;
                height:80px;
                margin:5px;
                text-align:center;
                line-height:80px;
                border:1px solid #ccc;
                font-family:Arial;
            }}

            .bitacora {{ background:#b6fcb6; }}
            .lluvia {{ background:#b6d7fc; }}
            .foto {{ background:#ffe0b3; }}
        </style>
    </head>

    <body>
        <h1>📅 Calendario {mes}</h1>
        {html}
        <br><br>
        <a href="/">Volver</a>
    </body>
    </html>
    """


@app.get("/dia/{fecha}", response_class=HTMLResponse)
def ver_dia(fecha: str):

    with Session(engine) as session:

        bitacoras = session.query(Bitacora).filter(Bitacora.fecha == fecha).all()
        lluvias = session.query(Lluvia).filter(Lluvia.fecha == fecha).all()
        fotos = session.query(Foto).filter(Foto.fecha == fecha).all()

    html = f"<h1>📅 {fecha}</h1>"

    html += "<h2>📝 Bitácora</h2>"
    for b in bitacoras:
        html += f"<p>{b.actividad} - {b.observacion}</p>"

    html += "<h2>🌧 Lluvia</h2>"
    for l in lluvias:
        html += f"<p>{l.inicio}-{l.fin} ({l.intensidad})</p>"

    html += "<h2>📷 Fotos</h2>"
    for f in fotos:
        html += f'<img src="/static/fotos/{f.archivo}" width="200">'

    return f"""
    <html>
    <body style="font-family:Arial; padding:20px;">
        {html}
        <a href="/calendario">Volver</a>
    </body>
    </html>
    """


# =========================
# INFORME PDF
# =========================
@app.get("/informe")
def informe(fecha_dia: str = None, fecha_mes: str = None):

    styles = getSampleStyleSheet()
    contenido = []

    with Session(engine) as session:

        if fecha_dia:

            bitacoras = session.query(Bitacora).filter(Bitacora.fecha == fecha_dia).all()
            lluvias = session.query(Lluvia).filter(Lluvia.fecha == fecha_dia).all()
            fotos = session.query(Foto).filter(Foto.fecha == fecha_dia).all()

            titulo = f"INFORME DIARIO {fecha_dia}"
            archivo = f"informe_{fecha_dia}.pdf"

        elif fecha_mes:

            bitacoras = session.query(Bitacora).filter(Bitacora.fecha.like(f"{fecha_mes}%")).all()
            lluvias = session.query(Lluvia).filter(Lluvia.fecha.like(f"{fecha_mes}%")).all()
            fotos = session.query(Foto).filter(Bitacora.fecha.like(f"{fecha_mes}%")).all()

            titulo = f"INFORME MENSUAL {fecha_mes}"
            archivo = f"informe_{fecha_mes}.pdf"

        else:
            return {"error": "Selecciona fecha o mes"}

    doc = SimpleDocTemplate(archivo)

    # TITULO
    contenido.append(Paragraph(titulo, styles["Title"]))
    contenido.append(Spacer(1, 12))

    # BITÁCORA
    contenido.append(Paragraph("BITÁCORA", styles["Heading2"]))
    if bitacoras:
        for b in bitacoras:
            texto = f"{b.fecha} - {b.clima} - {b.actividad} - {b.observacion}"
            contenido.append(Paragraph(texto, styles["Normal"]))
    else:
        contenido.append(Paragraph("Sin registros", styles["Normal"]))

    contenido.append(Spacer(1, 10))

    # LLUVIA
    contenido.append(Paragraph("LLUVIA", styles["Heading2"]))
    if lluvias:
        for l in lluvias:
            texto = f"{l.fecha} {l.inicio}-{l.fin} {l.intensidad} - {l.observacion}"
            contenido.append(Paragraph(texto, styles["Normal"]))
    else:
        contenido.append(Paragraph("Sin registros", styles["Normal"]))

    contenido.append(Spacer(1, 10))

    # FOTOS
    contenido.append(Paragraph("FOTOS", styles["Heading2"]))
    if fotos:
        for f in fotos:
            ruta = f"static/fotos/{f.archivo}"
            contenido.append(Paragraph(f"{f.fecha} - {f.descripcion}", styles["Normal"]))
            try:
                contenido.append(Image(ruta, width=250, height=180))
            except:
                pass
    else:
        contenido.append(Paragraph("Sin fotos", styles["Normal"]))

    doc.build(contenido)

    return FileResponse(archivo, media_type="application/pdf")
#internet main
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)