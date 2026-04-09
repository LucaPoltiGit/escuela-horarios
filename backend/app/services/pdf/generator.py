from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from typing import List
from app.schemas.horario import SlotAsignado
from app.models.models import Modulo

DIAS = ["lunes", "martes", "miercoles", "jueves", "viernes"]

COLORES = {
    "header_dia": colors.HexColor("#2563EB"),
    "header_modulo": colors.HexColor("#1E40AF"),
    "recreo": colors.HexColor("#FEF3C7"),
    "comedor": colors.HexColor("#FEE2E2"),
    "clase": colors.white,
    "maestra": colors.HexColor("#DCFCE7"),
    "vacio": colors.white,
    "titulo": colors.HexColor("#1E3A5F"),
}

def _build_grilla_grado(
    grado_nombre: str,
    maestra_nombre: str,
    modulos: List[Modulo],
    asignaciones: List[SlotAsignado],
    escuela_nombre: str
) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=1*cm, bottomMargin=1*cm)
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle("titulo", fontSize=14, textColor=COLORES["titulo"],
                                   alignment=TA_CENTER, spaceAfter=6, fontName="Helvetica-Bold")
    sub_style = ParagraphStyle("sub", fontSize=10, alignment=TA_CENTER, spaceAfter=12)

    # Índice de asignaciones por (dia, modulo)
    asig_map = {}
    for a in asignaciones:
        asig_map[(a.dia, a.modulo_numero)] = a

    # Encabezado
    header = ["Módulo / Horario"] + DIAS

    rows = [header]
    row_colors = [[(0, 0), COLORES["header_dia"]]] 

    for i, modulo in enumerate(modulos, start=1):
        hora = f"Mód {modulo.numero}\n{modulo.hora_inicio.strftime('%H:%M')}-{modulo.hora_fin.strftime('%H:%M')}"

        if modulo.tipo.value in ("recreo", "comedor"):
            label = "RECREO" if modulo.tipo.value == "recreo" else "COMEDOR"
            fila = [hora] + [label] * 5
            rows.append(fila)
            for col in range(6):
                row_colors.append([(i, col), COLORES[modulo.tipo.value]])
        else:
            fila = [hora]
            for dia in DIAS:
                asig = asig_map.get((dia, modulo.numero))
                if asig:
                    fila.append(f"{asig.materia}\n{asig.profesor_nombre}")
                else:
                    fila.append(f"Seño\n{maestra_nombre}")
            rows.append(fila)
            for col in range(1, 6):
                celda = fila[col]
                color = COLORES["maestra"] if celda.startswith("Seño") else COLORES["clase"]
                row_colors.append([(i, col), color])

    col_widths = [3.5*cm] + [4.5*cm]*5
    table = Table(rows, colWidths=col_widths, rowHeights=1.5*cm)

    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), COLORES["header_dia"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (0, -1), COLORES["header_modulo"]),
        ("TEXTCOLOR", (0, 1), (0, -1), colors.white),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
    ]

    for entry in row_colors:
        if len(entry) == 2 and isinstance(entry[0], tuple):
            (r, c), color = entry
            if r > 0:
                style_cmds.append(("BACKGROUND", (c, r), (c, r), color))

    table.setStyle(TableStyle(style_cmds))

    elementos = [
        Paragraph(f"{escuela_nombre}", titulo_style),
        Paragraph(f"Horario — {grado_nombre} | Maestra: {maestra_nombre}", sub_style),
        table
    ]
    doc.build(elementos)
    return buffer.getvalue()


def _build_grilla_curricular(
    profesor_nombre: str,
    materia: str,
    modulos: List[Modulo],
    asignaciones: List[SlotAsignado],
    escuela_nombre: str
) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), topMargin=1*cm, bottomMargin=1*cm)
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle("titulo", fontSize=14, textColor=COLORES["titulo"],
                                   alignment=TA_CENTER, spaceAfter=6, fontName="Helvetica-Bold")
    sub_style = ParagraphStyle("sub", fontSize=10, alignment=TA_CENTER, spaceAfter=12)

    asig_map = {}
    for a in asignaciones:
        asig_map[(a.dia, a.modulo_numero)] = a

    header = ["Módulo / Horario"] + DIAS
    rows = [header]

    for i, modulo in enumerate(modulos, start=1):
        hora = f"Mód {modulo.numero}\n{modulo.hora_inicio.strftime('%H:%M')}-{modulo.hora_fin.strftime('%H:%M')}"

        if modulo.tipo.value in ("recreo", "comedor"):
            label = "RECREO" if modulo.tipo.value == "recreo" else "COMEDOR"
            rows.append([hora] + [label] * 5)
        else:
            fila = [hora]
            for dia in DIAS:
                asig = asig_map.get((dia, modulo.numero))
                fila.append(asig.grado_nombre if asig else "—")
            rows.append(fila)

    col_widths = [3.5*cm] + [4.5*cm]*5
    table = Table(rows, colWidths=col_widths, rowHeights=1.5*cm)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLORES["header_dia"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (0, -1), COLORES["header_modulo"]),
        ("TEXTCOLOR", (0, 1), (0, -1), colors.white),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
    ]))

    elementos = [
        Paragraph(f"{escuela_nombre}", titulo_style),
        Paragraph(f"Horario Curricular — {profesor_nombre} | {materia}", sub_style),
        table
    ]
    doc.build(elementos)
    return buffer.getvalue()


def generar_pdfs_horario(
    escuela_nombre: str,
    asignaciones: List[SlotAsignado],
    modulos: List[Modulo],
    grados_map: dict,
    profesores_map: dict
) -> bytes:
    """Genera un PDF con todas las grillas — una por grado y una por curricular"""
    from reportlab.platypus import SimpleDocTemplate
    from pypdf import PdfWriter, PdfReader

    writer = PdfWriter()

    # Grilla por grado
    for grado_id, grado_info in grados_map.items():
        asig_grado = [a for a in asignaciones if a.grado_id == grado_id]
        pdf_bytes = _build_grilla_grado(
            grado_nombre=grado_info["nombre"],
            maestra_nombre=grado_info["maestra"],
            modulos=modulos,
            asignaciones=asig_grado,
            escuela_nombre=escuela_nombre
        )
        reader = PdfReader(BytesIO(pdf_bytes))
        for page in reader.pages:
            writer.add_page(page)

    # Grilla por curricular
    for prof_id, prof_info in profesores_map.items():
        asig_prof = [a for a in asignaciones if a.profesor_id == prof_id]
        pdf_bytes = _build_grilla_curricular(
            profesor_nombre=prof_info["nombre"],
            materia=prof_info["materia"],
            modulos=modulos,
            asignaciones=asig_prof,
            escuela_nombre=escuela_nombre
        )
        reader = PdfReader(BytesIO(pdf_bytes))
        for page in reader.pages:
            writer.add_page(page)

    output = BytesIO()
    writer.write(output)
    return output.getvalue()