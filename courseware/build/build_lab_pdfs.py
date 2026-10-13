#!/usr/bin/env python3
"""Render each learner-facing lab Markdown guide to a matching PDF."""

from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
LABS = REPO / "labs"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=30, textColor=colors.HexColor("#161920"), alignment=TA_CENTER, spaceAfter=18))
styles.add(ParagraphStyle(name="H1Blue", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=colors.HexColor("#224AF4"), spaceBefore=12, spaceAfter=8))
styles.add(ParagraphStyle(name="H2Magenta", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=colors.HexColor("#E11D74"), spaceBefore=10, spaceAfter=5))
styles.add(ParagraphStyle(name="BodyA", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=13.2, textColor=colors.HexColor("#343A46"), spaceAfter=5))
styles.add(ParagraphStyle(name="BulletA", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=13.2, leftIndent=12, firstLineIndent=-8, bulletIndent=3, spaceAfter=4))
styles.add(ParagraphStyle(name="Meta", parent=styles["BodyText"], fontName="Helvetica", fontSize=8, leading=11, textColor=colors.HexColor("#5B6372"), alignment=TA_CENTER))

def clean(text):
    # Keep the PDF index presentation-ready instead of exposing raw Markdown
    # link syntax and repository-relative README paths.
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    return escape(text.replace("**", "").replace("`", ""))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#DADFE8")); canvas.line(18*mm, 14*mm, 192*mm, 14*mm)
    canvas.setFont("Helvetica", 7.5); canvas.setFillColor(colors.HexColor("#5B6372"))
    canvas.drawString(18*mm, 9*mm, "TGS-2024045220 · Generative AI Visuals in Photoshop and Firefly · v7")
    canvas.drawRightString(192*mm, 9*mm, str(doc.page))
    canvas.restoreState()

def render(md_path):
    lines = md_path.read_text(encoding="utf-8").splitlines()
    title = next((x[2:].strip() for x in lines if x.startswith("# ")), md_path.stem)
    out = md_path.with_suffix(".pdf")
    story = [Spacer(1, 24*mm), Paragraph(clean(title), styles["CoverTitle"]), Spacer(1, 4*mm), Paragraph("Generative AI (GenAI) Visuals in Photoshop and Firefly", styles["Meta"]), Paragraph("TGS-2024045220 · Version 7 · 21 August 2026", styles["Meta"]), PageBreak()]
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("# "):
            if not line: story.append(Spacer(1, 2.2*mm))
            continue
        if line.startswith("## "):
            story.append(Paragraph(clean(line[3:]), styles["H1Blue"]))
        elif line.startswith("### "):
            story.append(Paragraph(clean(line[4:]), styles["H2Magenta"]))
        elif line.startswith("- [ ] "):
            story.append(Paragraph("☐ " + clean(line[6:]), styles["BulletA"]))
        elif line.startswith("- "):
            story.append(Paragraph("• " + clean(line[2:]), styles["BulletA"]))
        elif len(line) > 3 and line[0].isdigit() and ". " in line[:4]:
            n, body = line.split(". ", 1)
            story.append(Paragraph(f"<b>{clean(n)}.</b> {clean(body)}", styles["BodyA"]))
        else:
            story.append(Paragraph(clean(line), styles["BodyA"]))
    SimpleDocTemplate(str(out), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=18*mm, bottomMargin=18*mm, title=title, author="Tertiary Infotech Academy Pte Ltd").build(story, onFirstPage=footer, onLaterPages=footer)
    return out

if __name__ == "__main__":
    targets = [LABS / "README.md"] + sorted(LABS.glob("lab-[0-9][0-9]-*/README.md"))
    for target in targets:
        print(render(target))
