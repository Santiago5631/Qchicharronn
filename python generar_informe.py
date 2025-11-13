import subprocess
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
import datetime

# ======== FUNCIONES AUXILIARES ========

def run_git_command(args):
    result = subprocess.run(["git"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Error ejecutando git {' '.join(args)}: {result.stderr}")
    return result.stdout.strip()

def get_last_commit_hash():
    return run_git_command(["rev-parse", "HEAD"])

def get_project_name():
    return run_git_command(["rev-parse", "--show-toplevel"]).split("\\")[-1].split("/")[-1]

def get_branch_name():
    return run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])

def get_commit_info(commit_hash):
    fmt = "%H%n%an%n%ae%n%aI%n%s"
    output = run_git_command(["show", "-s", f"--format={fmt}", commit_hash])
    lines = output.splitlines()
    return {
        "hash": lines[0],
        "author": lines[1],
        "email": lines[2],
        "date": lines[3],
        "message": lines[4],
    }

def get_commit_files(commit_hash):
    output = run_git_command(["show", "--numstat", "--pretty=format:", commit_hash])
    files = []
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) == 3:
            added, deleted, filename = parts
            files.append((filename, added, deleted))
    return files

def describe_django_change(file_path):
    if "models.py" in file_path:
        return "Cambios en modelos."
    elif "views.py" in file_path:
        return "Cambios en vistas."
    elif "urls.py" in file_path:
        return "Actualización de rutas."
    elif "forms.py" in file_path:
        return "Cambios en formularios."
    elif "templates" in file_path:
        return "Cambios en plantillas HTML."
    return "Cambios generales."

# ======== PDF ========

def generar_pdf(commit_info, commit_files, project_name, branch_name):

    doc = SimpleDocTemplate(
        "informe_ultimo_commit.pdf",
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Titulo",
        parent=styles["Title"],
        textColor=colors.darkgreen,
        alignment=1,
        fontSize=18
    )

    elements = []
    elements.append(Paragraph("Informe del Último Commit – Proyecto Django", title_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"<b>Proyecto:</b> {project_name}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Rama:</b> {branch_name}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Hash:</b> {commit_info['hash']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Autor:</b> {commit_info['author']} &lt;{commit_info['email']}&gt;", styles["Normal"]))
    elements.append(Paragraph(f"<b>Fecha:</b> {commit_info['date']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Mensaje:</b> {commit_info['message']}", styles["Normal"]))
    elements.append(Spacer(1, 15))

    # ------- TABLA ARREGLADA CON ANCHO FIJO EN MM -------
    data = [["Archivo", "Añadidas", "Eliminadas", "Descripción"]]

    for f, a, d in commit_files:
        desc = describe_django_change(f)
        data.append([
            Paragraph(f, styles["Normal"]),  # Permite saltos de línea
            str(a),
            str(d),
            Paragraph(desc, styles["Normal"])
        ])

    # Asignación exacta de anchos de columna en mm
    col_widths = [80*mm, 25*mm, 25*mm, 50*mm]

    table = Table(data, colWidths=col_widths)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2e7d32")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (1, 1), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)

    doc.build(elements)

    print("✅ PDF generado correctamente con tabla organizada: informe_ultimo_commit.pdf")


# ======== MAIN ========

if __name__ == "__main__":
    commit_hash = get_last_commit_hash()
    info = get_commit_info(commit_hash)
    files = get_commit_files(commit_hash)
    project = get_project_name()
    branch = get_branch_name()
    generar_pdf(info, files, project, branch)
