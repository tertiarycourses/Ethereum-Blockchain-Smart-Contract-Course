#!/usr/bin/env python3
"""Build aligned PPTX, Learner Guide, Lesson Plan and self-contained labs."""

from __future__ import annotations

import json
import os
import shutil
import sys
import textwrap
import zipfile
from pathlib import Path

from PIL import Image, ImageOps
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches as DInches, Pt as DPt, RGBColor as DRGBColor
from pptx import Presentation
from pptx.chart.data import ChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CW = REPO / "courseware"
ASSETS = CW / "assets"
LABS_DIR = REPO / "labs"
sys.path.insert(0, str(HERE))
import course_data as C

PRODOC_DIR = REPO / ".claude" / "skills" / "courseware-build" / "build"
sys.path.insert(0, str(PRODOC_DIR))
import prodoc

ORG_LOGO = REPO / ".claude" / "skills" / "courseware-build" / "assets" / "tertiary-infotech-logo.png"
HERO = ASSETS / "cover-hero-v8.png"
WORKFLOW_SCREENSHOTS = {
    1: ASSETS / "workflow-screenshots/lab-01-firefly-prompt.png",
    2: ASSETS / "workflow-screenshots/lab-02-canvas-dimensions.png",
    3: ASSETS / "workflow-screenshots/lab-03-reference-controls.png",
    4: ASSETS / "workflow-screenshots/lab-04-firefly-controls.png",
    5: ASSETS / "workflow-screenshots/lab-05-fill-variations.png",
    6: ASSETS / "workflow-screenshots/lab-06-background-controls.png",
    7: ASSETS / "workflow-screenshots/lab-07-expand.png",
    8: ASSETS / "workflow-screenshots/lab-08-prompt-selection.png",
    9: ASSETS / "workflow-screenshots/lab-09-neural-filter.png",
    10: ASSETS / "workflow-screenshots/lab-10-colour-balance.png",
}

ASSETS.mkdir(parents=True, exist_ok=True)
LABS_DIR.mkdir(parents=True, exist_ok=True)

# ---------- shared content helpers ----------

def lab_dir(lab):
    return LABS_DIR / f"lab-{lab['num']:02d}-{lab['slug']}"


def first_jpeg(lab):
    preferred = lab.get("slide_image")
    if preferred:
        p = REPO / preferred
        if p.exists():
            return p
    for src, _ in lab["assets"]:
        p = REPO / src
        if p.suffix.lower() in {".jpg", ".jpeg", ".png"} and p.exists():
            return p
    return None


def doc_preview(path, lab_num):
    """Create a print-clear, compact preview for the Learner Guide.

    Lab source images remain untouched; only the DOCX embedding copy is
    downsampled so the guide stays practical to download and publish.
    """
    cache = HERE / ".doc-previews"
    cache.mkdir(parents=True, exist_ok=True)
    out = cache / f"lab-{lab_num:02d}.jpg"
    if out.exists() and out.stat().st_size > 0:
        return out
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
        image.thumbnail((1400, 1050), Image.Resampling.LANCZOS)
        image.save(out, "JPEG", quality=84, optimize=True, progressive=True)
    return out


def materialise_labs():
    # Labs are generated artifacts. Remove only numbered lab directories so a
    # superseded sequence cannot survive beside the current build.
    for old_target in LABS_DIR.glob("lab-[0-9][0-9]-*"):
        if old_target.is_dir():
            shutil.rmtree(old_target)
    index = [
        f"# {C.TITLE} — Labs",
        "",
        f"**Course code:** {C.COURSE_CODE}",
        f"**Version:** {C.VERSION} · {C.VERSION_DATE}",
        "",
        "Each lab is self-contained. Open its folder, read the guide, and work only on the supplied PSD/JPEG assets. Save all outputs inside the same lab folder or your trainer-approved workspace.",
        "",
        "## Lab sequence",
        "",
    ]
    for lab in C.LABS:
        target = lab_dir(lab)
        target.mkdir(parents=True, exist_ok=True)
        for old in target.iterdir():
            if old.is_file() and old.name not in {"README.md", "README.pdf"}:
                old.unlink()
        copied = []
        for rel, out_name in lab["assets"]:
            src = REPO / rel
            if not src.exists():
                raise FileNotFoundError(src)
            shutil.copy2(src, target / out_name)
            copied.append(out_name)
            if src.name == "photoshop_PP.zip":
                with zipfile.ZipFile(src) as zf:
                    for member in zf.infolist():
                        if member.is_dir() or member.filename.startswith("__MACOSX/"):
                            continue
                        name = Path(member.filename).name
                        if Path(name).suffix.lower() in {".jpg", ".jpeg", ".psd", ".png"}:
                            with zf.open(member) as inp, open(target / name, "wb") as out:
                                shutil.copyfileobj(inp, out)
                            copied.append(name)
        md = [
            f"# Lab {lab['num']:02d} — {lab['title']}",
            "",
            f"**Course:** {C.TITLE} (`{C.COURSE_CODE}`)",
            f"**Version:** {C.VERSION} · {C.VERSION_DATE}",
            "",
            "## Scenario",
            "",
            lab["scenario"],
            "",
            "## Objective",
            "",
            lab["objective"],
            "",
            "## Supplied Photoshop/JPEG files",
            "",
        ]
        md.extend([f"- `{name}`" for name in sorted(set(copied), key=str.lower)])
        md += ["", "## Detailed procedure", ""]
        md.extend([f"{i}. {step}" for i, step in enumerate(lab["steps"], 1)])
        md += [
            "",
            "## Evidence to retain",
            "",
            lab["evidence"],
            "",
            "## Acceptance criteria",
            "",
        ]
        md.extend([f"- [ ] {item}" for item in lab["acceptance"]])
        md += [
            "", "## Reflection prompts", "",
            "- Which decision most improved the message or focal hierarchy?",
            "- How does the Layers panel prove that the workflow remains editable?",
            "- What rights or provenance evidence must accompany the finished image?", "",
        ]
        (target / "README.md").write_text("\n".join(md), encoding="utf-8")
        index.append(f"{lab['num']}. [Lab {lab['num']:02d} — {lab['title']}](lab-{lab['num']:02d}-{lab['slug']}/README.md) — {lab['objective']}")
    (LABS_DIR / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")


# ---------- PowerPoint ----------

BLUE = RGBColor(0x22, 0x4A, 0xF4)
CYAN = RGBColor(0x00, 0xB8, 0xD9)
MAGENTA = RGBColor(0xE1, 0x1D, 0x74)
VIOLET = RGBColor(0x7C, 0x3A, 0xED)
INK = RGBColor(0x16, 0x19, 0x20)
GREY = RGBColor(0x5B, 0x63, 0x72)
MID = RGBColor(0xDA, 0xDF, 0xE8)
LIGHT = RGBColor(0xF5, 0xF7, 0xFB)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREEN = RGBColor(0x00, 0x9A, 0x78)
AMBER = RGBColor(0xE9, 0x85, 0x00)
RED = RGBColor(0xC9, 0x28, 0x28)
PALETTE = [BLUE, CYAN, MAGENTA, VIOLET, GREEN, AMBER]

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SLIDE_MAP = {}


def _slide():
    return prs.slides.add_slide(BLANK)


def _shape(slide, x, y, w, h, fill, radius=True, line=None):
    kind = MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE if radius else MSO_AUTO_SHAPE_TYPE.RECTANGLE
    shp = slide.shapes.add_shape(kind, x, y, w, h)
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line:
        shp.line.color.rgb = line
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def _text(slide, x, y, w, h, text, size=18, color=INK, bold=False,
          align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP, margin=0.06, font="Arial"):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame; tf.clear(); tf.word_wrap = True; tf.vertical_anchor = valign
    tf.margin_left = tf.margin_right = Inches(margin)
    tf.margin_top = tf.margin_bottom = Inches(margin)
    p = tf.paragraphs[0]; p.alignment = align
    p.space_after = Pt(0)
    r = p.add_run(); r.text = text; r.font.name = font; r.font.size = Pt(size)
    r.font.bold = bold; r.font.color.rgb = color
    return box


def _rich_text(slide, x, y, w, h, lines, size=18, color=INK, gap=5):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame; tf.clear(); tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05)
    for i, item in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        if isinstance(item, tuple):
            head, body = item
            r = p.add_run(); r.text = head; r.font.bold = True; r.font.size = Pt(size); r.font.name = "Arial"; r.font.color.rgb = color
            r = p.add_run(); r.text = body; r.font.size = Pt(size); r.font.name = "Arial"; r.font.color.rgb = color
        else:
            r = p.add_run(); r.text = item; r.font.size = Pt(size); r.font.name = "Arial"; r.font.color.rgb = color
    return box


def _fit_picture(slide, path, x, y, w, h, crop=False):
    path = Path(path)
    if not path.exists():
        return None
    with Image.open(path) as im:
        iw, ih = im.size
    if crop:
        pic = slide.shapes.add_picture(str(path), x, y, w, h)
        frame = w / h; ratio = iw / ih
        if ratio > frame:
            shown = frame / ratio; pic.crop_left = pic.crop_right = (1 - shown) / 2
        elif ratio < frame:
            shown = ratio / frame; pic.crop_top = pic.crop_bottom = (1 - shown) / 2
        return pic
    scale = min(w / iw, h / ih)
    pw, ph = int(iw * scale), int(ih * scale)
    return slide.shapes.add_picture(str(path), x + (w - pw) / 2, y + (h - ph) / 2, pw, ph)


def _footer(slide, source=None, dark=False):
    n = len(prs.slides)
    colour = RGBColor(0xD7, 0xDE, 0xE9) if dark else GREY
    _text(slide, Inches(0.45), Inches(7.08), Inches(4.0), Inches(0.22),
          f"{C.SHORT_TITLE}  ·  {C.COURSE_CODE}", 8.5, colour)
    _text(slide, Inches(4.45), Inches(7.08), Inches(4.3), Inches(0.22),
          f"© 2026 {C.ORG}", 7.8, colour, align=PP_ALIGN.CENTER)
    if source:
        _text(slide, Inches(9.0), Inches(7.08), Inches(3.2), Inches(0.22), source, 7.2, colour, align=PP_ALIGN.RIGHT)
    _text(slide, Inches(12.55), Inches(7.08), Inches(0.35), Inches(0.22), str(n), 8.5, colour, align=PP_ALIGN.RIGHT)


def _header(slide, title, kicker, accent=BLUE, source=None):
    _shape(slide, 0, 0, prs.slide_width, prs.slide_height, WHITE, radius=False)
    _shape(slide, Inches(0), Inches(0), Inches(0.22), Inches(1.64), accent, radius=False)
    _text(slide, Inches(0.72), Inches(0.36), Inches(11.8), Inches(0.3), kicker.upper(), 11.5, accent, True)
    title_size = 23 if len(title) > 52 else 28
    _text(slide, Inches(0.72), Inches(0.76), Inches(11.85), Inches(0.75), title, title_size, INK, True)
    _shape(slide, Inches(0.72), Inches(1.55), Inches(11.9), Inches(0.02), MID, radius=False)
    _footer(slide, source)


def cover():
    s = _slide()
    _shape(s, 0, 0, prs.slide_width, prs.slide_height, WHITE, radius=False)
    if HERO.exists():
        _fit_picture(s, HERO, Inches(5.45), 0, Inches(7.88), Inches(7.5), crop=True)
        overlay = _shape(s, Inches(5.1), 0, Inches(1.2), Inches(7.5), WHITE, radius=False)
        overlay.fill.transparency = 18
    if ORG_LOGO.exists():
        _fit_picture(s, ORG_LOGO, Inches(0.75), Inches(0.55), Inches(2.15), Inches(0.85))
    _shape(s, Inches(3.35), Inches(0.58), Inches(1.45), Inches(0.68), INK)
    _text(s, Inches(3.35), Inches(0.71), Inches(1.45), Inches(0.22), "WSQ COURSE", 9.5, CYAN, True, PP_ALIGN.CENTER)
    _text(s, Inches(0.78), Inches(1.65), Inches(4.6), Inches(0.36), "COURSE SLIDES · WSQ", 12, MAGENTA, True)
    _text(s, Inches(0.78), Inches(2.15), Inches(4.85), Inches(2.3), C.TITLE, 33, INK, True)
    _shape(s, Inches(0.8), Inches(4.58), Inches(1.35), Inches(0.08), CYAN, radius=False)
    _rich_text(s, Inches(0.78), Inches(4.93), Inches(4.75), Inches(1.35), [
        ("WSQ Course Code  ", C.COURSE_CODE),
        ("TSC  ", f"{C.TSC_TITLE} · {C.TSC_CODE}"),
        ("Provider  ", f"{C.ORG} · {C.UEN}"),
    ], size=12.5, color=GREY, gap=4)
    _text(s, Inches(0.78), Inches(6.72), Inches(4.7), Inches(0.35), f"Version {C.VERSION} · {C.VERSION_DATE}", 11, MAGENTA, True)
    _text(s, Inches(6.15), Inches(7.08), Inches(6.6), Inches(0.2), f"© 2026 {C.ORG} · {C.COURSE_CODE}", 8, WHITE, False, PP_ALIGN.RIGHT)
    _text(s, Inches(12.55), Inches(7.08), Inches(.35), Inches(.2), "1", 8, WHITE, False, PP_ALIGN.RIGHT)


def title_cards(title, kicker, cards, accent=BLUE, source=None, columns=3):
    s = _slide(); _header(s, title, kicker, accent, source)
    rows = (len(cards) + columns - 1) // columns
    gap = 0.22; total_w = 11.8; card_w = (total_w - gap * (columns - 1)) / columns
    top = 1.92; total_h = 4.86; card_h = (total_h - gap * (rows - 1)) / rows
    for i, (head, body) in enumerate(cards):
        r, c = divmod(i, columns); x = 0.75 + c * (card_w + gap); y = top + r * (card_h + gap)
        col = PALETTE[i % len(PALETTE)]
        _shape(s, Inches(x), Inches(y), Inches(card_w), Inches(card_h), LIGHT, line=MID)
        _shape(s, Inches(x), Inches(y), Inches(0.08), Inches(card_h), col, radius=False)
        _text(s, Inches(x + 0.24), Inches(y + 0.22), Inches(card_w - 0.44), Inches(0.42), head, 15, col, True)
        _text(s, Inches(x + 0.24), Inches(y + 0.72), Inches(card_w - 0.44), Inches(card_h - 0.92), body, 12.5, GREY)
    return s


def photo_points(title, kicker, image, points, accent=BLUE, source=None, image_right=False):
    s = _slide(); _header(s, title, kicker, accent, source)
    ix = 7.3 if image_right else 0.75; tx = 0.75 if image_right else 6.28
    _shape(s, Inches(ix), Inches(1.92), Inches(5.28), Inches(4.86), LIGHT, line=MID)
    _fit_picture(s, image, Inches(ix + 0.08), Inches(2.0), Inches(5.12), Inches(4.7), crop=True)
    y = 1.95
    for i, (head, body) in enumerate(points):
        col = PALETTE[i % len(PALETTE)]
        _shape(s, Inches(tx), Inches(y), Inches(5.3), Inches(1.02), LIGHT, line=MID)
        _shape(s, Inches(tx + 0.16), Inches(y + 0.19), Inches(0.52), Inches(0.52), col)
        _text(s, Inches(tx + 0.16), Inches(y + 0.25), Inches(0.52), Inches(0.25), str(i + 1), 11, WHITE, True, PP_ALIGN.CENTER)
        _text(s, Inches(tx + 0.84), Inches(y + 0.16), Inches(4.25), Inches(0.28), head, 14, INK, True)
        _text(s, Inches(tx + 0.84), Inches(y + 0.48), Inches(4.25), Inches(0.42), body, 11.3, GREY)
        y += 1.2
    return s


def process_slide(title, kicker, stages, outcome, accent=BLUE, source=None):
    s = _slide(); _header(s, title, kicker, accent, source)
    y = 2.05; gap = 0.22; w = (11.8 - gap * (len(stages) - 1)) / len(stages)
    for i, stage in enumerate(stages):
        x = 0.75 + i * (w + gap); col = PALETTE[i % len(PALETTE)]
        _shape(s, Inches(x), Inches(y), Inches(w), Inches(2.5), LIGHT, line=MID)
        _shape(s, Inches(x + 0.18), Inches(y + 0.18), Inches(0.6), Inches(0.6), col)
        _text(s, Inches(x + 0.18), Inches(y + 0.32), Inches(0.6), Inches(0.24), str(i + 1), 12, WHITE, True, PP_ALIGN.CENTER)
        _text(s, Inches(x + 0.18), Inches(y + 1.03), Inches(w - 0.36), Inches(0.65), stage, 15, INK, True, PP_ALIGN.CENTER)
        if i < len(stages) - 1:
            connector = s.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.CHEVRON, Inches(x + w + .035), Inches(y + 1.03), Inches(gap - .07), Inches(.5))
            connector.fill.solid(); connector.fill.fore_color.rgb = accent; connector.line.fill.background()
    _shape(s, Inches(0.75), Inches(5.05), Inches(11.8), Inches(1.24), accent)
    _text(s, Inches(1.0), Inches(5.3), Inches(1.65), Inches(0.25), "OUTCOME", 11, WHITE, True)
    _text(s, Inches(2.45), Inches(5.22), Inches(9.75), Inches(0.68), outcome, 16, WHITE, True)
    return s


def chart_slide(title, kicker, categories, series, chart_type, insight, accent=BLUE, source=None):
    s = _slide(); _header(s, title, kicker, accent, source)
    cd = ChartData(); cd.categories = categories
    for name, values in series:
        cd.add_series(name, values)
    frame = s.shapes.add_chart(chart_type, Inches(0.82), Inches(1.95), Inches(8.05), Inches(4.75), cd)
    chart = frame.chart; chart.has_title = False; chart.has_legend = len(series) > 1 or chart_type == XL_CHART_TYPE.DOUGHNUT
    if chart.has_legend:
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM; chart.legend.include_in_layout = False
    chart.chart_style = 10
    if chart_type == XL_CHART_TYPE.DOUGHNUT:
        plot = chart.plots[0]; plot.has_data_labels = True
        plot.data_labels.position = XL_LABEL_POSITION.BEST_FIT; plot.data_labels.show_percentage = True; plot.data_labels.show_category_name = False
    else:
        plot = chart.plots[0]; plot.has_data_labels = True; plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END; plot.data_labels.show_value = True
    _shape(s, Inches(9.18), Inches(2.05), Inches(3.25), Inches(3.95), LIGHT, line=MID)
    _text(s, Inches(9.48), Inches(2.35), Inches(2.65), Inches(0.45), "READ THE CHART", 12, accent, True)
    _text(s, Inches(9.48), Inches(3.03), Inches(2.65), Inches(2.25), insight, 15, INK, True)
    _text(s, Inches(9.48), Inches(5.55), Inches(2.65), Inches(0.28), "Editable native PowerPoint chart", 9, GREY)
    return s


def divider(topic):
    s = _slide(); SLIDE_MAP[f"topic_{topic['num']}"] = len(prs.slides)
    _shape(s, 0, 0, prs.slide_width, prs.slide_height, INK, radius=False)
    _shape(s, Inches(0.65), Inches(0.55), Inches(1.25), Inches(1.25), PALETTE[(topic['num'] - 1) % len(PALETTE)])
    _text(s, Inches(0.65), Inches(0.88), Inches(1.25), Inches(0.35), f"{topic['num']:02d}", 22, WHITE, True, PP_ALIGN.CENTER)
    _text(s, Inches(0.75), Inches(2.1), Inches(11.9), Inches(1.2), topic["title"], 38, WHITE, True)
    _text(s, Inches(0.78), Inches(3.55), Inches(11.2), Inches(0.85), topic["subtitle"], 18, RGBColor(0xC8, 0xCF, 0xDA))
    _text(s, Inches(0.78), Inches(5.85), Inches(6.5), Inches(0.35), topic["codes"], 14, CYAN, True)
    _footer(s, dark=True)


def lab_slide(lab, stages):
    SLIDE_MAP[f"lab_{lab['num']}"] = len(prs.slides) + 1
    img = first_jpeg(lab)
    s = _slide(); _header(s, f"Lab {lab['num']:02d} · {lab['title']}", f"HANDS-ON APPLICATION · TOPIC {lab['topic']}", MAGENTA)
    if img:
        _shape(s, Inches(0.75), Inches(1.92), Inches(4.1), Inches(4.88), LIGHT, line=MID)
        _fit_picture(s, img, Inches(0.83), Inches(2.0), Inches(3.94), Inches(3.1), crop=True)
        _text(s, Inches(1.0), Inches(5.35), Inches(3.55), Inches(1.12), lab["scenario"], 12.2, GREY)
    _text(s, Inches(5.15), Inches(1.95), Inches(7.15), Inches(0.72), lab["objective"], 15, INK, True)
    gap = 0.13; w = (7.12 - gap * 4) / 5
    for i, stage in enumerate(stages):
        x = 5.15 + i * (w + gap); col = PALETTE[i % len(PALETTE)]
        _shape(s, Inches(x), Inches(2.92), Inches(w), Inches(1.62), LIGHT, line=MID)
        _shape(s, Inches(x + 0.12), Inches(3.08), Inches(0.44), Inches(0.44), col)
        _text(s, Inches(x + 0.12), Inches(3.17), Inches(0.44), Inches(0.2), str(i + 1), 9.5, WHITE, True, PP_ALIGN.CENTER)
        _text(s, Inches(x + 0.1), Inches(3.75), Inches(w - 0.2), Inches(0.48), stage, 11.3, INK, True, PP_ALIGN.CENTER)
    _shape(s, Inches(5.15), Inches(4.86), Inches(7.12), Inches(1.33), MAGENTA)
    _text(s, Inches(5.4), Inches(5.07), Inches(1.45), Inches(0.28), "EVIDENCE", 10.5, WHITE, True)
    _text(s, Inches(6.72), Inches(5.0), Inches(5.28), Inches(0.8), lab["evidence"], 12.2, WHITE, True)
    _text(s, Inches(5.25), Inches(6.38), Inches(6.9), Inches(0.3), f"Full procedure · Learner Guide / Lab {lab['num']:02d}", 11, INK, True)
    return s


def build_slides():
    cover()
    title_cards("Digital Attendance", "MANDATORY WSQ ADMIN", [("Attendance event", "Complete the trainer-displayed electronic attendance for every required session."), ("Identity", "Use your own authorised Singpass identity and never submit on another learner's behalf."), ("Verification", "Remain until the trainer confirms that your attendance has been recorded correctly.")], CYAN, columns=3)
    title_cards("Dr Alfred Ang", "NAMED TRAINER PROFILE", [("Role", "Principal Trainer · Tertiary Infotech Academy Pte Ltd"), ("Expertise", "Applied AI, digital transformation, courseware development and adult learning."), ("Facilitation", "Concept-first explanation followed by coached practice and evidence review."), ("Quality focus", "Source alignment, reproducible workflows and clear acceptance criteria."), ("Learning culture", "Ask questions early; explain the reason behind every editing choice."), ("Contact", "enquiry@tertiaryinfotech.com · +65 6100 0613")], BLUE)
    title_cards("Let’s Know Each Other", "OPENING ACTIVITY", [("Your role", "What kind of images do you create or manage?"), ("Your channel", "Web, social, print, e-commerce, photography or internal communication?"), ("Your friction", "Which Photoshop task currently costs you the most time?"), ("Your goal", "What visible improvement would make this course worthwhile?"), ("Your experience", "Name one tool or workflow you already use."), ("Your evidence", "What finished artifact will show that you improved?")], CYAN)
    title_cards("Working Agreements", "GROUND RULES", [("Be present", "Return from breaks on time and complete mandatory attendance."), ("Participate", "Try the tools, explain choices and ask questions."), ("Respect", "One conversation at a time; critique the work, not the person."), ("Protect assets", "Use supplied or licensed materials and retain rights evidence."), ("Save versions", "Preserve originals and use clear file/layer naming."), ("Share safely", "Do not post learner work, assessment content or personal data without permission.")], MAGENTA)
    title_cards("Course Materials", "LMS-TMS", [("Portal", "Use https://lms-tms.tertiaryinfotech.com/ for the current learner materials."), ("Courseware", "Obtain the slides, Learner Guide and the ten self-contained lab folders."), ("Outcome", "Confirm every lab folder contains its guide and supplied PSD/JPEG assets before class work begins.")], BLUE, columns=3)
    process_slide("Two-Day Learning Journey", "COURSE FLOW", ["Explore", "Construct", "Experiment", "Evaluate", "Demonstrate"], "Day 1 builds foundations and controlled experimentation; Day 2 integrates, evaluates and assesses a complete workflow.", VIOLET)
    title_cards("Skills Framework Alignment", "VISUAL COMMUNICATION", [("TSC title", C.TSC_TITLE), ("TSC code", C.TSC_CODE), ("Course code", C.COURSE_CODE), ("Duration", C.DURATION), ("Assessment", "WA 60 min · PP 60 min"), ("Competency", "Every applicable K and A criterion must be Competent.")], BLUE)
    title_cards("Knowledge Criteria", "K1–K5", C.TSC_KNOWLEDGE, MAGENTA, columns=3)
    title_cards("Ability Criteria", "A1–A7", C.TSC_ABILITIES, CYAN, columns=3)
    title_cards("Learning Outcomes", "WHAT YOU WILL BE ABLE TO DO", [(f"LO{i}", lo.split(":", 1)[1].strip()) for i, lo in enumerate(C.LEARNING_OUTCOMES, 1)], VIOLET, columns=3)
    title_cards("Course Outline", "FOUR CONNECTED TOPICS", [(f"Topic {t['num']}", f"{t['title']}\n{t['subtitle']}\n{t['codes']}") for t in C.TOPICS], BLUE, columns=2)
    process_slide("Assessment Design", "SUMMATIVE EVIDENCE", ["WA · K1–K5", "PP · A1/A2", "PP · A3/A4", "PP · A5/A6", "PP · A7"], "Open-book assessment: 5 written questions in 60 minutes and 4 practical tasks in 60 minutes.", MAGENTA)
    title_cards("Briefing for Assessment", "BEFORE THE PAPERS BEGIN", [("Individual work", "No discussion, photography or recording of assessment scripts."), ("Approved references", "Use course slides, Learner Guide and materials allowed by the assessor."), ("Phones/materials", "Place unapproved items under the table or as directed."), ("Writing", "Use black/blue pen for hard copy; no correction fluid or tape."), ("Time", "WA 60 minutes; PP 60 minutes; submit when time is called."), ("Outcome", "Competent or Not Yet Competent, with reassessment and appeal rights explained.")], RED)
    title_cards("Tools, Materials and Workspace", "K2 · K3", [("Hardware", "Laptop, calibrated display where available, mouse or graphics tablet, reliable storage."), ("Software", "Current Adobe Photoshop desktop release and supported operating system."), ("Workspace", "Panels arranged for task focus, sufficient scratch disk, colour-managed viewing conditions."), ("Input assets", "High-resolution PSD/JPEG/TIFF/RAW files with known source and usage rights."), ("Output", "Channel specifications for pixel size, colour space, transparency and compression."), ("Safety", "Versioned backups, non-destructive editing and verified exports before delivery.")], GREEN)
    title_cards("Photoshop Scope and Disclaimer", "TOOL CONTEXT", [("Industry tool", "Photoshop supports photo editing, compositing, design, retouching and output preparation."), ("Not an Adobe certification", "This WSQ course does not certify an Adobe credential."), ("Interface changes", "Commands may move between releases; use the current Help search when labels differ."), ("Decision over clicks", "Understand selection, layering, masking, colour and output principles that survive UI changes."), ("Responsible AI", "Review generated results, respect third-party rights and retain provenance evidence."), ("Rights", "Adobe and Photoshop are trademarks of Adobe; the provider is not affiliated with Adobe.")], MAGENTA)

    divider(C.TOPICS[0])
    photo_points("Raster and Vector Images", "DIGITAL IMAGE ESSENTIALS", REPO / "reference/Exercise Files/19 Shape Layers/Sunset.jpg", [("Raster", "Pixels capture continuous-tone detail but depend on resolution."), ("Vector", "Paths and shapes scale cleanly and suit defined edges."), ("Hybrid", "Photoshop documents can combine raster layers, vector masks, type and Smart Objects."), ("Decision", "Choose the structure that preserves the edit you may need later.")], BLUE, "Adobe Photoshop Help")
    chart_slide("Pixel Width by Deliverable", "EDITABLE OUTPUT-PLANNING CHART", ["Social square", "Presentation HD", "4K display", "A4 print @300 ppi"], [("Pixel width", [1080, 1920, 3840, 3508])], XL_CHART_TYPE.COLUMN_CLUSTERED, "Plan the working document from the output requirement. More pixels increase available detail and file size; they do not rescue a low-quality source.", CYAN, "Adobe: Image file size factors")
    title_cards("Resolution, Bit Depth and File Size", "FOUNDATION DECISIONS", [("Pixel dimensions", "The count of pixels defines how much raster detail is available."), ("Resolution metadata", "Ppi links pixels to physical print size; screen delivery is governed by pixel dimensions."), ("Bit depth", "Higher bit depth supports more tonal values but increases storage and processing demand."), ("Layers/channels", "More layers, masks and channels make the file larger but preserve editability."), ("Compression", "JPEG is lossy; PNG is lossless for transparency; TIFF/PSD preserve production data."), ("Resampling", "Adding pixels estimates new values—it cannot recreate detail that was never captured.")], BLUE)
    title_cards("Colour Modes and Channels", "RGB · CMYK · GRAYSCALE", [("RGB", "Additive light model for screens and most editing workflows."), ("CMYK", "Subtractive process model used for many print-production workflows."), ("Grayscale", "One luminance channel; colour information is removed."), ("Profiles", "Describe how numeric colour values should appear on a device or in a working space."), ("Soft proof", "Preview a target output condition while keeping the master editable."), ("Convert deliberately", "Confirm printer/profile requirements before converting a finished copy.")], MAGENTA)
    title_cards("Composition Principles", "K5 · DESIGN WITH PURPOSE", [("Balance", "Distribute visual weight intentionally; symmetry is only one option."), ("Contrast", "Separate the focal message through tone, colour, scale, texture or shape."), ("Hierarchy", "Make the intended reading order obvious before the viewer studies detail."), ("Alignment", "Use shared edges and baselines to create order."), ("Proximity", "Group related elements and separate unrelated information."), ("Negative space", "Give the subject and message room to breathe.")], VIOLET)
    photo_points("Layers as a Reversible Stack", "CONSTRUCTION MODEL", REPO / "reference/Exercise Files/07 Layers/Peppers.jpg", [("Content layers", "Separate major image components and name them by role."), ("Groups", "Organise related layers for navigation and shared masks."), ("Opacity and blend", "Control interaction without merging source pixels."), ("Auditability", "A reviewer should be able to understand how the result was built.")], GREEN, "Adobe: Select layers")
    title_cards("Layer Mask vs Vector Mask", "NON-DESTRUCTIVE VISIBILITY", [("Layer mask", "Resolution-dependent grayscale mask edited with selections and painting tools."), ("Vector mask", "Resolution-independent path that creates a crisp geometric clipping edge."), ("Black", "Hides the corresponding portion of the layer."), ("White", "Reveals the corresponding portion of the layer."), ("Gray", "Produces partial visibility."), ("Choose by edge", "Soft organic transitions favour layer masks; precise shapes favour vector masks.")], MAGENTA, "Adobe: Add and edit layer masks")
    title_cards("Choose the Selection Tool", "EDGE-BASED DECISION", [("Marquee", "Geometric rectangles and ellipses."), ("Lasso", "Freehand or polygonal boundaries."), ("Object/Quick Selection", "Distinct subjects with recognisable contrast."), ("Colour Range", "Repeated or similar hues across an image."), ("Pen tool", "Precise, controllable hard edges and product cut-outs."), ("Select and Mask", "Refinement workspace for hair, fur, soft edges and output as a mask.")], CYAN, "Adobe: Get started with selections")
    for lab, stages in zip(C.LABS[:4], [
        ["Inspect", "Plan output", "Crop", "Frame", "Export"],
        ["Place", "Organise", "Align", "Brand", "Export"],
        ["Add mask", "Paint", "Restore", "Refine", "Verify"],
        ["Select", "Refine", "Mask", "Match", "Review"],
    ]):
        lab_slide(lab, stages)
    title_cards("Topic 1 Checkpoint", "EXPLAIN YOUR DECISIONS", [("K1", "Which techniques and materials produce the intended effect without sacrificing editability?"), ("K2", "Which tools, equipment and source files are appropriate for the output?"), ("A1", "How did stakeholder purpose influence the option you explored?"), ("Evidence", "Can another person verify dimensions, layers, masks and output settings?"), ("Risk", "Where could resolution, colour or edge quality fail?"), ("Next", "Which controlled experiment will improve the work?")], BLUE)

    divider(C.TOPICS[1])
    chart_slide("Reversibility by Editing Technique", "EDITABLE DECISION CHART", ["Direct pixel edit", "Duplicate layer", "Separate retouch layer", "Adjustment layer", "Smart Object + mask"], [("Reversibility score", [1, 2, 4, 5, 5])], XL_CHART_TYPE.BAR_CLUSTERED, "Scale: 1 = low, 5 = high. Use the highest-reversibility technique that still achieves the intended effect so the file supports comparison, feedback and change requests.", MAGENTA, "Adobe: Nondestructive editing")
    title_cards("Retouching Tool Decision", "MATCH TOOL TO DEFECT", [("Spot Healing", "Small isolated blemishes with suitable surrounding texture."), ("Healing Brush", "Controlled source texture blended with destination tone."), ("Clone Stamp", "Exact pixel copying for structure, edges or repeating patterns."), ("Patch", "Larger selected areas replaced from a chosen source region."), ("Content-Aware", "Contextual fill or movement that still requires visual review."), ("Retouch layer", "Keep repairs separate and sample all layers where the tool supports it.")], CYAN)
    photo_points("Retouching: Texture Before Speed", "LOCAL PIXEL EDITING", REPO / "reference/Exercise Files/11 Retouching/Portrait.jpg", [("Match scale", "Brush size should follow the defect and surrounding texture."), ("Match direction", "Light, grain and structure must flow consistently through the repair."), ("Avoid repetition", "Obvious cloned patterns expose the intervention."), ("Review twice", "Inspect at 100% for pixels and Fit view for overall plausibility.")], MAGENTA)
    title_cards("Blend Modes as Colour Relationships", "BASE · BLEND · RESULT", [("Darken group", "Keeps darker relationships; useful for line art, shadows and density."), ("Lighten group", "Keeps lighter relationships; useful for highlights and removing dark backgrounds."), ("Contrast group", "Combines lightening and darkening around a neutral point."), ("Comparative modes", "Expose differences between layers and support technical checks."), ("Colour components", "Hue, Saturation, Colour and Luminosity separate aspects of colour."), ("Control", "Opacity, Fill and masks determine where and how strongly the mode appears.")], VIOLET)
    photo_points("Smart Objects Preserve Options", "EDIT ONCE · UPDATE MANY", REPO / "reference/Exercise Files/14 Blend Modes/Big Sky.jpg", [("Transform", "Scale, rotate, skew and warp without repeatedly resampling source pixels."), ("Smart Filters", "Reopen settings, reorder effects and mask the filter stack."), ("Embedded", "Keeps source content inside the PSD for portable handoff."), ("Linked", "References an external source that can update across documents.")], BLUE, "Adobe: Smart Objects overview")
    title_cards("Experiment Without Losing the Baseline", "A2 · CONTROLLED COMPARISON", [("Duplicate", "Create a named baseline or version before testing."), ("Change one factor", "Vary the blend mode, adjustment, filter or mask—not everything at once."), ("Hold the view", "Compare at the same zoom, background and output profile."), ("Record", "Name the treatment and note the exact variable changed."), ("Evaluate", "Judge the treatment against purpose and acceptance criteria."), ("Recommend", "Select one option and explain the evidence behind the choice.")], GREEN)
    for lab, stages in zip(C.LABS[4:6], [
        ["Diagnose", "Choose tool", "Repair", "Inspect", "Compare"],
        ["Baseline", "Vary mode", "Smart place", "Compare", "Recommend"],
    ]):
        lab_slide(lab, stages)
    title_cards("Topic 2 Checkpoint", "FROM PRACTICE TO IMPROVEMENT", [("K3", "How does workspace setup affect speed, consistency and output reliability?"), ("K4", "Which theoretical context or visual language guides the treatment?"), ("A2", "What did you vary, what did you hold constant, and what improved?"), ("Quality", "Can you prove texture, edges and transitions remain credible?"), ("Editability", "Which decisions can still be changed without rebuilding?"), ("Stakeholder", "Which option best meets the audience and channel need?")], MAGENTA)

    divider(C.TOPICS[2])
    photo_points("Transform for Believable Space", "PERSPECTIVE AND ADAPTATION", REPO / "reference/Exercise Files/16 Transformations/Window.jpg", [("Scale and proportion", "Match the physical size relationship implied by the scene."), ("Perspective", "Align receding edges and vanishing directions."), ("Warp", "Use only where a surface bends or perspective requires local control."), ("Integration", "Match sharpness, contrast, colour and shadow after geometry is correct.")], BLUE)
    title_cards("Correction Before Creative Grading", "COLOUR WORKFLOW", [("Diagnose", "Read the histogram and identify clipping, cast and exposure imbalance."), ("Correct", "Neutralise technical problems while protecting important detail."), ("Grade", "Create a deliberate mood or campaign palette after the correction is stable."), ("Localise", "Use masks or clipping to protect skin, product colour or focal areas."), ("Compare", "Toggle original, corrected and graded states at the same view."), ("Export", "Use the requested profile and check the exported file—not only the canvas.")], CYAN)
    chart_slide("Image Evaluation Rubric", "EDITABLE QUALITY-WEIGHTING CHART", ["Composition", "Edge quality", "Tone and colour", "Technical output", "Rights evidence"], [("Weight", [25, 25, 20, 15, 15])], XL_CHART_TYPE.DOUGHNUT, "A strong result is not only attractive. It communicates clearly, survives close inspection, meets output specifications and carries usable rights/provenance evidence.", VIOLET)
    title_cards("Smart Filters: Editable Effects", "FILTER WITH CONTROL", [("Convert first", "A supported filter becomes a Smart Filter when applied to a Smart Object."), ("Revisit", "Reopen filter settings whenever the treatment needs revision."), ("Reorder", "Change the stack order to test how effects interact."), ("Blend", "Adjust a Smart Filter's blending options separately."), ("Mask", "Use the filter mask to hide, reveal or soften the total filter effect."), ("Review", "Some filters have mode/depth limits; verify the intended output.")], MAGENTA, "Adobe: Apply Smart Filters")
    title_cards("Choose the Output Format", "DELIVERY DECISION", [("PSD", "Layered master for continued editing and handoff."), ("TIFF", "High-quality print/archive exchange with optional layers and lossless compression."), ("JPEG", "Compact photographic delivery; no transparency; lossy compression."), ("PNG", "Lossless screen graphic with alpha transparency; not a layered master."), ("Profile", "Embed or convert to the agreed colour profile."), ("Verification", "Open the exported file and confirm dimensions, profile, edges and compression.")], GREEN)
    title_cards("Copyright and Asset Permission", "K6 · SINGAPORE CONTEXT", [("Protected expression", "Original photographs, artworks and other creative expressions may be protected automatically."), ("Permission", "An online image is not automatically free to reuse; identify the owner and applicable licence."), ("Scope", "Check whether modification, commercial use, redistribution and sublicensing are permitted."), ("People and privacy", "Obtain appropriate consent for identifiable people and intended publication context."), ("Attribution", "Credit exactly as the licence or agreement requires; attribution does not replace permission."), ("Record", "Keep the source URL/file, owner, licence, consent, date and intended use with the project.")], RED, "IPOS Copyright Resources · not legal advice")
    title_cards("Responsible Generative AI in Photoshop", "CURRENT WORKFLOW", [("Rights-aware inputs", "Do not upload or reference third-party content without the required rights."), ("Prompt and variation log", "Record what was requested and which variation was selected."), ("Human review", "Check factual/visual plausibility, bias, artefacts and suitability for the audience."), ("Commercial terms", "Confirm the current model/feature terms, especially for beta or partner models."), ("Content Credentials", "Use provenance features where appropriate to communicate how the asset was created."), ("Final responsibility", "The editor remains responsible for the output, rights and publication decision.")], MAGENTA, "Adobe Generative AI User Guidelines")
    for lab, stages in zip(C.LABS[6:], [
        ["Read plane", "Place", "Transform", "Integrate", "Inspect"],
        ["Diagnose", "Correct", "Grade", "Mask", "Compare"],
        ["Smart convert", "Filter", "Mask", "Revise", "Export"],
        ["Explore", "Improve", "Evaluate", "Peer review", "Deliver"],
    ]):
        lab_slide(lab, stages)
    title_cards("Peer Review That Improves the Work", "A4 · DISCUSS THE PROCESS", [("Describe", "State the purpose, audience, output and key editing decisions."), ("Show evidence", "Reveal the layer structure, masks, adjustments and before/after view."), ("Ask", "Request feedback against one or two explicit acceptance criteria."), ("Observe", "Record what the reviewer noticed—not only what you intended."), ("Decide", "Accept, adapt or reject feedback with a reason."), ("Revise", "Make one traceable change and document its effect.")], CYAN)
    title_cards("Topic 3 Checkpoint", "EVALUATE AND DISCUSS", [("K5", "Which design principles make the message easier to understand?"), ("K6", "Can you prove permission, licence, consent and attribution?"), ("A3", "Which technique best meets purpose, quality and editability criteria?"), ("A4", "How did peer discussion change or confirm the workflow?"), ("Output", "Does the exported file meet the agreed channel specification?"), ("Reflection", "What would you repeat, adapt or stop next time?")], VIOLET)
    title_cards("Course Synthesis", "A PROFESSIONAL EDITING LOOP", [("Brief", "Clarify purpose, audience, channel and constraints."), ("Source", "Choose suitable, high-quality and rights-cleared assets."), ("Construct", "Build with layers, groups, masks and Smart Objects."), ("Experiment", "Vary one factor and compare controlled alternatives."), ("Evaluate", "Use visible quality, technical and rights criteria."), ("Deliver", "Export, verify and retain the editable master plus evidence.")], BLUE)
    process_slide("Final Assessment", "WA + PP", ["Briefing", "WA · 60 min", "Transition", "PP · 90 min", "Submit"], "Question papers are open book. Complete your own work and retain the evidence requested by the assessor.", RED)
    process_slide("Assessment Flow", "COMPETENCY SIGN-OFF", ["WA · K1–K5", "PP · A1–A7", "Assessor reviews", "C / NYC decision", "Feedback & sign-off"], "If gaps remain, the assessor explains reassessment and appeal arrangements.", MAGENTA)
    title_cards("Assessment Attendance", "MANDATORY CLOSING ADMIN", [("Complete", "Submit the official assessment attendance event before leaving."), ("Confirm", "Remain until the trainer confirms the attendance record."), ("Exceptions", "Report an unsuccessful or incorrect submission immediately for authorised follow-up.")], CYAN, columns=3)
    title_cards("Course Feedback and TRAQOM", "HELP IMPROVE DELIVERY", [("Complete", "Use the official LMS-TMS/TRAQOM route provided by the trainer."), ("Be specific", "Name the activity, explanation or resource that helped or blocked you."), ("Rate fairly", "Separate course content, facilitation, venue and administration."), ("Suggest", "Describe one practical improvement."), ("Support", "Post-course subject consultation is available through the provider."), ("Contact", "enquiry@tertiaryinfotech.com · +65 6100 0613")], GREEN)
    title_cards("Recommended Courses", "CONTINUE THE CREATIVE WORKFLOW", [("Illustrator", "Create scalable vector graphics and brand assets."), ("InDesign", "Build professional print and digital publications."), ("After Effects", "Composite motion graphics and visual effects."), ("Premiere Pro", "Edit video stories and campaign content."), ("UI Design", "Apply visual hierarchy and interaction principles to digital interfaces."), ("Portfolio", "Combine edited imagery with a documented design process.")], VIOLET)
    title_cards("Support", "AFTER THE COURSE", [("Subject questions", "Email enquiry@tertiaryinfotech.com for post-course consultation."), ("Course portal", "https://lms-tms.tertiaryinfotech.com/"), ("Provider", "Tertiary Infotech Academy Pte Ltd"), ("Telephone", "+65 6100 0613"), ("Website", "www.tertiarycourses.com.sg"), ("Reminder", "Do not send confidential assessment content over public channels.")], BLUE)
    s = _slide(); _shape(s, 0, 0, prs.slide_width, prs.slide_height, INK, radius=False)
    _text(s, Inches(0.9), Inches(2.1), Inches(11.6), Inches(1.1), "Thank You", 48, WHITE, True, PP_ALIGN.CENTER)
    _text(s, Inches(1.7), Inches(3.55), Inches(9.9), Inches(0.65), "Create with intent · preserve options · verify the output", 20, CYAN, True, PP_ALIGN.CENTER)
    _text(s, Inches(2.6), Inches(5.25), Inches(8.2), Inches(0.42), f"{C.COURSE_CODE} · {C.TITLE}", 13, RGBColor(0xC8, 0xCF, 0xDA), False, PP_ALIGN.CENTER)
    _footer(s, dark=True)
    out = CW / f"{C.SHORT_TITLE}-{C.VERSION}.pptx"
    prs.save(out)
    (HERE / "slide_map.json").write_text(json.dumps(SLIDE_MAP, indent=2), encoding="utf-8")
    return out


CONCEPT_IMAGES = {
    "Human-led GenAI Creative Loop": "courseware/assets/cover-hero-v7.png",
    "GenAI Image Use Cases and Boundaries": "reference/lab reference 1/02 Turning descriptions into images/02-03-Understanding Firefly models/model4.jpg",
    "Prompt Anatomy": "reference/lab reference 1/02 Turning descriptions into images/02-02-Creating your first prompt/Firefly_a dog reading a book while sitting at a desk by candle light, while wearing glasses,  120801.jpg",
    "Prompt Iteration and Variation": "reference/lab reference 1/02 Turning descriptions into images/02-08-Reusing prompts/Firefly a raccoon sitting on a crescent  176327 zF4.jpg",
    "Visual Hierarchy and Emphasis": "reference/lab reference 1/03 Using advanced settings/03-01-Color-lighting-composition/Firefly_photography, dynamic portrait of a japanese woman, New York street behind background, 589911.jpg",
    "Scale, Balance and Alignment": "reference/lab reference 1/03 Using advanced settings/03-02-Using a Structure reference/Firefly_a library of books 578606.jpg",
    "Contrast, Repetition and Negative Space": "reference/lab reference 1/03 Using advanced settings/03-05-Combining settings/Firefly_A marble statue of a bird, on a pink background, surrounded by foliage 53233.jpg",
    "Audience, Story and Responsible Provenance": "reference/lab reference 1/10 Ethical Generative AI/10-02-Downloading images with credentials/adventure.jpg",
    "Choosing a Firefly Image Model": "reference/lab reference 1/02 Turning descriptions into images/02-03-Understanding Firefly models/model4ultra.jpg",
    "Content Type and Visual Intensity": "reference/lab reference 1/02 Turning descriptions into images/02-06-Using content types and styles/Firefly_a robot dancing at a party 830052.jpg",
    "Colour, Lighting and Camera Controls": "reference/lab reference 1/03 Using advanced settings/03-01-Color-lighting-composition/Firefly_a butterfly resting on a flower 480324.jpg",
    "Composition Reference": "reference/lab reference 1/03 Using advanced settings/03-03-Creating your own Structure reference/reference.jpg",
    "Style Reference": "reference/lab reference 1/03 Using advanced settings/03-04-Using a Style reference/hummingbird.jpg",
    "Storyboard Architecture": "reference/lab reference 1/10 Ethical Generative AI/10-02-Downloading images with credentials/adventure.jpg",
    "Task Flow for Team Collaboration": "courseware/assets/cover-hero-v7.png",
    "Photoshop Generative AI Feature Map": "reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-03-Generating backgrounds/park bench.jpg",
    "Selection as a Generative Instruction": "reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-06-Using reference/reference.jpeg",
    "Generative Fill": "reference/lab reference 1/04 Image magic with generative fill/04-02-Inserting objects and subjects/breakfast.jpeg",
    "Generative Expand": "reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-04-Generative expand/landscape-start.jpeg",
    "Generate Background and Harmonize": "reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-03-Generating backgrounds/park bench.jpg",
    "Reference Image in Generative Fill": "reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-06-Using reference/reference.jpeg",
    "Inpainting and Outpainting": "reference/lab reference 1/04 Image magic with generative fill/04-07-Challenge/exotic.jpeg",
    "Aesthetic Critique and Golden-ratio Heuristics": "reference/lab reference 1/03 Using advanced settings/03-01-Color-lighting-composition/Firefly_photography, dynamic portrait of a japanese woman, New York street behind background, 774439.jpg",
    "Hue, Saturation, Brightness and Value": "reference/lab reference 1/03 Using advanced settings/03-01-Color-lighting-composition/Firefly_a butterfly resting on a flower 900942.jpg",
    "Adjustment Layers and Masks": "reference/lab reference 1/05 Using Firefly in Adobe Photoshop/05-03-Generating backgrounds/park bench.jpg",
    "Histogram and Levels": "reference/lab reference 1/03 Using advanced settings/03-02-Using a Structure reference/model.jpeg",
    "Curves": "reference/lab reference 1/03 Using advanced settings/03-01-Color-lighting-composition/Firefly_photography, dynamic portrait of a japanese woman, New York street behind background, 774439.jpg",
    "Colour Balance and Hue/Saturation": "reference/lab reference 1/03 Using advanced settings/03-01-Color-lighting-composition/Firefly_photography, dynamic portrait of a japanese woman, New York street behind background, 589911.jpg",
    "Neural Filters and Restoration": "reference/lab reference 1/09 Adobe Firefly for enterprise/09-03-Style kits/model.jpeg",
    "Campaign Colour Consistency": "reference/lab reference 1/09 Adobe Firefly for enterprise/09-04-Creative production/01.jpeg",
    "Output Verification and Content Credentials": "reference/lab reference 1/10 Ethical Generative AI/10-02-Downloading images with credentials/adventure.jpg",
}


def concept_overview_slide(item, index):
    # Reuse the rights-cleared, self-contained lab evidence set as authentic visual
    # exhibits. Editable annotations and decision prompts remain native shapes.
    visual_pool = [p for p in (first_jpeg(lab) for lab in C.LABS) if p is not None]
    img = visual_pool[(index - 1) % len(visual_pool)] if index <= 20 and visual_pool else None
    points = [
        ("How it works", item["mechanism"]),
        ("Best used for", item["best_for"]),
        ("Professional decision", "Choose this method when its content model and edge behaviour fit the brief."),
        ("Quality signal", item["evidence"]),
    ]
    if img and img.exists():
        return photo_points(item["title"], f"CONCEPT {index:02d} · AUTHENTIC ASSET + EDITABLE ANNOTATIONS", img,
                            points, PALETTE[index % len(PALETTE)], item["source"], image_right=index % 2 == 0)
    return title_cards(item["title"], f"CONCEPT {index:02d} · HOW IT WORKS", points,
                       PALETTE[index % len(PALETTE)], item["source"], columns=2)


def concept_controls_slide(item, index):
    s = _slide(); accent = PALETTE[(index + 2) % len(PALETTE)]
    _header(s, f"{item['title']} · control and judgement", "KEY CONTROLS · FAILURE MODE · PROOF", accent, item["source"])
    blocks = [
        ("CONTROL MAP", item["controls"], BLUE),
        ("WATCH FOR", item["watch"], MAGENTA),
        ("QUALITY PROOF", item["evidence"], GREEN),
    ]
    for i, (head, body, col) in enumerate(blocks):
        x = 0.75 + i * 4.0
        _shape(s, Inches(x), Inches(2.0), Inches(3.78), Inches(3.55), LIGHT, line=MID)
        _shape(s, Inches(x), Inches(2.0), Inches(3.78), Inches(0.12), col, radius=False)
        _text(s, Inches(x + 0.26), Inches(2.35), Inches(3.22), Inches(0.35), head, 12, col, True)
        _text(s, Inches(x + 0.26), Inches(2.95), Inches(3.22), Inches(2.15), body, 16, INK, True)
    _shape(s, Inches(0.75), Inches(5.85), Inches(11.78), Inches(0.72), accent)
    _text(s, Inches(1.0), Inches(6.04), Inches(11.25), Inches(0.3),
          "Decision rule · preserve a baseline, isolate the intended change, then inspect at the delivery size.", 14, WHITE, True, PP_ALIGN.CENTER)
    return s


def concept_artifact_slide(item, index):
    s = _slide(); accent = PALETTE[index % len(PALETTE)]
    _header(s, f"Worked Artifact · {item['title']}", "INPUT → DECISION → OUTPUT", accent, item["source"])
    stages = [("01 · INTENT", item["best_for"]), ("02 · CONTROL SET", item["controls"]),
              ("03 · REVIEW GATE", item["watch"]), ("04 · RETAINED EVIDENCE", item["evidence"])]
    for j, (head, body) in enumerate(stages):
        x = .72 + j * 3.0; col = PALETTE[(index + j) % len(PALETTE)]
        _shape(s, Inches(x), Inches(2.0), Inches(2.82), Inches(3.85), LIGHT, line=MID)
        _shape(s, Inches(x), Inches(2.0), Inches(2.82), Inches(.12), col, radius=False)
        _text(s, Inches(x+.2), Inches(2.32), Inches(2.42), Inches(.45), head, 12, col, True)
        _text(s, Inches(x+.2), Inches(2.94), Inches(2.42), Inches(2.25), body, 14, INK)
        if j < 3: _text(s, Inches(x+2.83), Inches(3.5), Inches(.16), Inches(.4), "›", 26, GREY, True, PP_ALIGN.CENTER)
    _shape(s, Inches(.88), Inches(6.05), Inches(11.55), Inches(.58), WHITE, line=accent)
    _text(s, Inches(1.05), Inches(6.18), Inches(11.2), Inches(.27), "Acceptance trace: explain the final visual from intent, through named controls, to retained evidence.", 12.5, accent, True, PP_ALIGN.CENTER)
    return s


def concept_annotation_slide(item, index):
    s = _slide(); accent = PALETTE[(index + 1) % len(PALETTE)]
    _header(s, f"Annotated Decision Model · {item['title']}", "CONTROL SURFACE + CANVAS + PROOF", accent, item["source"])
    _shape(s, Inches(.72), Inches(1.95), Inches(3.0), Inches(4.62), INK)
    _text(s, Inches(.96), Inches(2.16), Inches(2.52), Inches(.34), "CONTROL SURFACE", 13, WHITE, True)
    for j, ctl in enumerate([x.strip() for x in item["controls"].split("·")][:5]):
        y = 2.75 + j * .64
        _shape(s, Inches(.98), Inches(y), Inches(.42), Inches(.42), PALETTE[(index+j)%len(PALETTE)])
        _text(s, Inches(.98), Inches(y+.07), Inches(.42), Inches(.2), str(j+1), 9, WHITE, True, PP_ALIGN.CENTER)
        _text(s, Inches(1.54), Inches(y+.02), Inches(1.86), Inches(.34), ctl, 11.5, WHITE, True)
    _shape(s, Inches(4.08), Inches(1.95), Inches(5.08), Inches(4.62), WHITE, line=MID)
    _shape(s, Inches(4.33), Inches(2.2), Inches(4.58), Inches(3.05), LIGHT, line=MID)
    _text(s, Inches(4.62), Inches(2.52), Inches(4.0), Inches(.46), "EDITABLE CANVAS / OUTPUT STATE", 14, accent, True, PP_ALIGN.CENTER)
    _text(s, Inches(4.66), Inches(3.22), Inches(3.92), Inches(1.2), item["mechanism"], 14, INK, False, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    _shape(s, Inches(4.33), Inches(5.46), Inches(4.58), Inches(.78), RGBColor(0xE9,0xF8,0xF3), line=GREEN)
    _text(s, Inches(4.55), Inches(5.66), Inches(4.14), Inches(.32), "Inspect at working view and delivery view", 11.5, GREEN, True, PP_ALIGN.CENTER)
    _shape(s, Inches(9.52), Inches(1.95), Inches(2.82), Inches(4.62), LIGHT, line=MID)
    _text(s, Inches(9.78), Inches(2.18), Inches(2.3), Inches(.34), "PROOF PANEL", 13, accent, True)
    _text(s, Inches(9.78), Inches(2.78), Inches(2.3), Inches(2.15), item["evidence"], 13, INK)
    _text(s, Inches(9.78), Inches(5.35), Inches(2.3), Inches(.66), "Keep source, selected state and export together.", 11.5, GREY, True)
    return s


def concept_diagnostic_slide(item, index):
    s = _slide(); accent = PALETTE[(index + 2) % len(PALETTE)]
    _header(s, f"Diagnostic · {item['title']}", "SYMPTOM → CAUSE → CORRECTION → VERIFY", accent, item["source"])
    rows = [("OBSERVE", item["watch"], RED),
            ("ISOLATE", f"Hold the brief and baseline constant; inspect: {item['controls']}.", AMBER),
            ("CORRECT", "Change one control, preserve the editable source, and revise only the affected state.", BLUE),
            ("VERIFY", item["evidence"], GREEN)]
    for j, (head, body, col) in enumerate(rows):
        y = 1.9 + j * 1.17
        _shape(s, Inches(.78), Inches(y), Inches(1.55), Inches(.82), col)
        _text(s, Inches(.84), Inches(y+.25), Inches(1.43), Inches(.28), head, 12, WHITE, True, PP_ALIGN.CENTER)
        _shape(s, Inches(2.52), Inches(y), Inches(9.82), Inches(.82), LIGHT, line=MID)
        _text(s, Inches(2.77), Inches(y+.15), Inches(9.3), Inches(.52), body, 12.5, INK, j == 3)
    _text(s, Inches(.9), Inches(6.69), Inches(11.3), Inches(.25), "Accept only when the defect is reduced and protected content remains intact.", 11.5, accent, True, PP_ALIGN.CENTER)
    return s


def general_trainer_profile_slide():
    s = _slide(); _header(s, "General Trainer Profile", "FACILITATOR TEMPLATE", BLUE)
    _shape(s, Inches(0.85), Inches(1.92), Inches(3.15), Inches(4.75), LIGHT, line=MID)
    _shape(s, Inches(1.55), Inches(2.35), Inches(1.75), Inches(1.75), BLUE)
    _text(s, Inches(1.55), Inches(2.78), Inches(1.75), Inches(0.62), "?", 34, WHITE, True, PP_ALIGN.CENTER)
    _text(s, Inches(1.1), Inches(4.45), Inches(2.65), Inches(0.4), "TRAINER NAME", 15, INK, True, PP_ALIGN.CENTER)
    _text(s, Inches(1.1), Inches(5.0), Inches(2.65), Inches(0.8), "Insert approved profile photo and professional designation before delivery.", 11.5, GREY, False, PP_ALIGN.CENTER)
    title_cards_data = [("Name", "________________________________"), ("Title / Designation", "________________________________"), ("Qualifications", "________________________________"), ("Areas of expertise", "________________________________"), ("Training & industry experience", "________________________________"), ("Contact", "________________________________")]
    for i, (head, body) in enumerate(title_cards_data):
        x = 4.35 + (i % 2) * 4.05; y = 1.95 + (i // 2) * 1.48
        _shape(s, Inches(x), Inches(y), Inches(3.78), Inches(1.22), LIGHT, line=MID)
        _text(s, Inches(x + 0.25), Inches(y + 0.25), Inches(3.25), Inches(0.35), head, 14, PALETTE[i], True)
        _text(s, Inches(x + 0.25), Inches(y + 0.72), Inches(3.25), Inches(0.3), body, 12.5, GREY)
    return s


def named_trainer_profile_slide():
    s = _slide(); _header(s, "About the Trainer", "NAMED FACILITATOR", BLUE)
    _shape(s, Inches(.85), Inches(1.92), Inches(3.15), Inches(4.75), LIGHT, line=MID)
    _shape(s, Inches(1.55), Inches(2.35), Inches(1.75), Inches(1.75), BLUE)
    _text(s, Inches(1.55), Inches(2.82), Inches(1.75), Inches(.55), "AA", 28, WHITE, True, PP_ALIGN.CENTER)
    _text(s, Inches(1.1), Inches(4.45), Inches(2.65), Inches(.4), "DR ALFRED ANG", 15, INK, True, PP_ALIGN.CENTER)
    _text(s, Inches(1.1), Inches(5.0), Inches(2.65), Inches(.8), "Principal Trainer\nTertiary Infotech Academy", 11.5, GREY, False, PP_ALIGN.CENTER)
    data = [("Role", "Principal Trainer"), ("Expertise", "Digital transformation · GenAI visuals"),
            ("Facilitation", "Concepts · coached practice · evidence review"), ("Quality", "Reversible workflows · acceptance criteria"),
            ("Learning culture", "Explain the reason behind every edit"), ("Contact", "enquiry@tertiaryinfotech.com · +65 6100 0613")]
    for i, (head, body) in enumerate(data):
        x = 4.35 + (i % 2) * 4.05; y = 1.95 + (i // 2) * 1.48
        _shape(s, Inches(x), Inches(y), Inches(3.78), Inches(1.22), LIGHT, line=MID)
        _text(s, Inches(x+.25), Inches(y+.18), Inches(3.25), Inches(.3), head, 12.5, PALETTE[i], True)
        _text(s, Inches(x+.25), Inches(y+.58), Inches(3.25), Inches(.48), body, 11.5, INK)
    return s


def portal_visual_slide():
    s = _slide(); _header(s, "Download Course Materials", "LMS-TMS · LEARNER PACKAGE", CYAN)
    _shape(s, Inches(0.85), Inches(1.9), Inches(11.6), Inches(4.85), WHITE, line=MID)
    _shape(s, Inches(0.85), Inches(1.9), Inches(11.6), Inches(0.55), INK, radius=False)
    for i, col in enumerate([RED, AMBER, GREEN]): _shape(s, Inches(1.12 + i*0.27), Inches(2.08), Inches(0.12), Inches(0.12), col)
    _shape(s, Inches(2.2), Inches(2.02), Inches(8.7), Inches(0.28), RGBColor(0x32,0x38,0x44))
    _text(s, Inches(2.35), Inches(2.07), Inches(8.35), Inches(0.16), "lms-tms.tertiaryinfotech.com", 8.5, WHITE, False, PP_ALIGN.CENTER)
    _text(s, Inches(1.2), Inches(2.82), Inches(7.4), Inches(0.55), "GenAI Visuals · Photoshop + Firefly", 21, INK, True)
    _text(s, Inches(1.2), Inches(3.35), Inches(5.2), Inches(0.35), f"Courseware · {C.VERSION}", 12, MAGENTA, True)
    items = [("PPTX", "Trainer deck", BLUE), ("PDF", "Learner slides", CYAN), ("LG", "Detailed guide", MAGENTA), ("LP", "Delivery plan", VIOLET), ("10", "Lab folders", GREEN)]
    for i, (code, label, col) in enumerate(items):
        x = 1.2 + i * 2.18
        _shape(s, Inches(x), Inches(4.12), Inches(1.82), Inches(1.65), LIGHT, line=MID)
        _shape(s, Inches(x+0.5), Inches(4.36), Inches(0.82), Inches(0.62), col)
        _text(s, Inches(x+0.5), Inches(4.52), Inches(0.82), Inches(0.22), code, 12, WHITE, True, PP_ALIGN.CENTER)
        _text(s, Inches(x+0.15), Inches(5.18), Inches(1.52), Inches(0.3), label, 10.5, INK, True, PP_ALIGN.CENTER)
    _text(s, Inches(1.2), Inches(6.05), Inches(10.8), Inches(0.3), "Outcome · the complete package is available in one authenticated course record.", 13, GREY, True, PP_ALIGN.CENTER)
    return s


def access_labs_slide():
    s = _slide(); _header(s, "Access the Ten Lab Folders", "LEARNER-FACING GITHUB COURSEWARE", GREEN)
    url = "https://github.com/tertiarycourses/TGS-2024045220-Generative-AI-GenAI-Visuals-in-Photoshop-and-Firefly/tree/master/labs"
    _shape(s, Inches(0.95), Inches(2.0), Inches(11.35), Inches(3.95), LIGHT, line=MID)
    _text(s, Inches(1.3), Inches(2.38), Inches(10.65), Inches(0.55), "Open the course repository, select labs/, then open the numbered folder assigned by your trainer.", 20, INK, True, PP_ALIGN.CENTER)
    box = _text(s, Inches(2.65), Inches(3.35), Inches(7.95), Inches(0.78), "Open the learner lab folders", 22, BLUE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    box.text_frame.paragraphs[0].runs[0].hyperlink.address = url
    _text(s, Inches(1.55), Inches(4.78), Inches(10.2), Inches(0.6), "Every folder contains a detailed guide plus supplied PSD/JPEG assets. Keep your outputs inside that folder or the trainer-approved workspace.", 14, GREY, False, PP_ALIGN.CENTER)
    return s


def apply_fade_transitions(pptx_path):
    """Add a restrained native Fade transition to every slide via OOXML."""
    pptx_path = Path(pptx_path)
    tmp = pptx_path.with_suffix(".transition-tmp.pptx")
    p_ns = "http://schemas.openxmlformats.org/presentationml/2006/main"
    from lxml import etree
    with zipfile.ZipFile(pptx_path, "r") as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename.startswith("ppt/slides/slide") and info.filename.endswith(".xml"):
                root = etree.fromstring(data)
                for old in root.findall(f"{{{p_ns}}}transition"):
                    root.remove(old)
                transition = etree.Element(f"{{{p_ns}}}transition", spd="med", advClick="1")
                etree.SubElement(transition, f"{{{p_ns}}}fade")
                cSld = root.find(f"{{{p_ns}}}cSld")
                pos = root.index(cSld) + 1 if cSld is not None else 0
                root.insert(pos, transition)
                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
            zout.writestr(info, data)
    os.replace(tmp, pptx_path)


def build_slides_current():
    cover()
    title_cards("TRAQOM · SSG Digital Attendance", "MANDATORY WSQ ADMIN", [("TRAQOM", "Scan the QR code provided through the LMS for each required attendance event."), ("Identity", "Use only your authorised identity."), ("Verification", "Remain until the trainer confirms the SSG digital-attendance record.")], CYAN, columns=3)
    general_trainer_profile_slide()
    named_trainer_profile_slide()
    title_cards("Your GenAI Visual Context", "OPENING DISCUSSION", [("Role", "What visuals do you create or manage?"), ("Channel", "Social, web, presentation, print or campaign?"), ("Friction", "Which ideation or Photoshop task costs the most time?"), ("Quality", "Which visual defect is most visible today?"), ("Experience", "Which Firefly or Photoshop feature is familiar?"), ("Evidence", "What finished artifact will prove improvement?")], CYAN)
    title_cards("Working Agreements", "GROUND RULES", [("Participate", "Try the tools and explain choices."), ("Respect", "Critique work, not people."), ("Protect assets", "Use permitted sources and retain rights evidence."), ("Save versions", "Preserve originals and name layers/files."), ("Share safely", "Protect learner work and assessment content."), ("Verify", "Reopen exports before delivery.")], MAGENTA)
    portal_visual_slide()
    access_labs_slide()
    process_slide("Two-Day Learning Journey", "COURSE FLOW", ["Explore", "Reference", "Compose", "Critique", "Deliver"], "The workflow moves from audience-led exploration to Firefly control, editable Photoshop integration, critique and verified delivery.", VIOLET)
    title_cards("Skills Framework Alignment", "VISUAL COMMUNICATION", [("TSC", f"{C.TSC_TITLE} · {C.TSC_CODE}"), ("Course", C.COURSE_CODE), ("Duration", C.DURATION), ("Knowledge", "K1–K5"), ("Abilities", "A1–A7"), ("Assessment", "WA 60 min · PP 60 min")], BLUE)
    title_cards("Knowledge Criteria", "K1–K5", C.TSC_KNOWLEDGE, MAGENTA, columns=3)
    title_cards("Ability Criteria", "A1–A7", C.TSC_ABILITIES, CYAN, columns=3)
    title_cards("Learning Outcomes", "WHAT YOU WILL BE ABLE TO DO", [(f"LO{i}", lo.split(":",1)[1].strip()) for i, lo in enumerate(C.LEARNING_OUTCOMES,1)], VIOLET, columns=2)
    title_cards("Course Outline", "FOUR CONNECTED TOPICS", [(f"Topic {t['num']}", f"{t['title']}\n{t['subtitle']}\n{t['codes']}") for t in C.TOPICS], BLUE, columns=2)
    title_cards("Assessment Briefing", "BEFORE THE PAPERS BEGIN", [("Individual work", "No discussion, photography or recording of assessment scripts."), ("Approved references", "Use course materials allowed by the assessor."), ("Phones/materials", "Place unapproved items under the table or as directed."), ("Writing", "Use black/blue pen for hard copy; no correction fluid or tape."), ("Time", "WA 60 minutes; PP 60 minutes; submit when time is called."), ("Outcome", "Competent or Not Yet Competent, with reassessment and appeal rights explained.")], RED)
    process_slide("Assessment Design", "SUMMATIVE EVIDENCE", ["WA · K1–K5", "PP · A1/A2", "PP · A3/A4", "PP · A5/A6", "PP · A7"], "Five written questions and four connected practical tasks; each instrument is 60 minutes and open book.", MAGENTA)
    title_cards("Tools, Materials and Workspace", "K2 · K3", [("Hardware", "Laptop, suitable display, mouse/tablet and reliable storage."), ("Software", "Current supported Photoshop desktop release and Adobe Firefly access."), ("Workspace", "Panels arranged for task focus and sufficient scratch disk."), ("Sources", "Supplied rights-aware PSD/JPEG assets and approved references."), ("Output brief", "Audience, channel, pixel size, colour space and copy-safe areas."), ("Safety", "Backups, reversible editing and verified exports.")], GREEN)
    title_cards("Adobe Tool Scope", "TOOL CONTEXT", [("Firefly", "Prompt-led image exploration, reference controls and storyboard ideation."), ("Photoshop", "Selections, generative edits, compositing, colour and output."), ("Not Adobe certification", "This WSQ course does not certify an Adobe credential."), ("Interface drift", "Models and labels change; decisions and evidence remain durable."), ("Responsible AI", "Review outputs, respect rights and retain provenance."), ("Trademark", "Adobe, Firefly and Photoshop are Adobe trademarks.")], MAGENTA)

    concept_number = 0
    for topic in C.TOPICS:
        divider(topic)
        if topic["num"] == 1:
            chart_slide("Prompt Quality Is a System", "EDITABLE PROMPT-QUALITY CHART", ["Clear subject","Audience fit","Composition","Lighting/style","Constraints","Provenance"], [("Review score",[5,4,4,3,4,5])], XL_CHART_TYPE.BAR_CLUSTERED, "Illustrative review scores show that a vivid subject alone is insufficient; channel fit, composition, constraints and provenance complete the visual brief.", CYAN, "Adobe Firefly Help")
        elif topic["num"] == 2:
            chart_slide("Reference-control Decision", "ILLUSTRATIVE DECISION RATINGS · 1–5", ["Prompt only","Composition ref","Style ref","Both refs"], [("Structure control",[2,5,2,5]),("Style control",[2,2,5,5])], XL_CHART_TYPE.COLUMN_CLUSTERED, "Illustrative decision ratings (1–5): composition and style references solve different control problems. Combine them only after isolating each influence.", MAGENTA, "Adobe Firefly Help")
        elif topic["num"] == 3:
            chart_slide("Reversibility by Technique", "EDITABLE DECISION CHART", ["Flattened pixels","Duplicate layer","Generated layer","Adjustment layer","Smart Object + mask"], [("Score",[1,2,4,5,5])], XL_CHART_TYPE.BAR_CLUSTERED, "Scale: 1 = low, 5 = high. Prefer an editable generated layer, mask or Smart Object so critique can lead to a traceable revision.", VIOLET, "Adobe Photoshop Help")
        else:
            chart_slide("Campaign Colour Roles", "EDITABLE PALETTE-WEIGHTING CHART", ["Primary","Secondary","Accent","Neutral"], [("Visual share",[55,25,10,10])], XL_CHART_TYPE.DOUGHNUT, "Illustrative shares keep the primary colour dominant while secondary, accent and neutral roles support hierarchy rather than compete with it.", VIOLET)
            chart_slide("Output Verification Priority", "EDITABLE QA CHART", ["Dimensions","Colour/profile","Edges","Compression","Provenance"], [("Priority",[5,5,4,3,5])], XL_CHART_TYPE.COLUMN_CLUSTERED, "A professional hand-off verifies the exported file and its provenance—not only the layered working canvas.", GREEN)
        for item in [x for x in C.CONCEPTS if x["topic"] == topic["num"]]:
            concept_number += 1
            concept_overview_slide(item, concept_number)
            concept_controls_slide(item, concept_number)
            concept_artifact_slide(item, concept_number)
            concept_annotation_slide(item, concept_number)
            concept_diagnostic_slide(item, concept_number)
        for lab in [x for x in C.LABS if x["topic"] == topic["num"]]:
            lab_slide(lab, ["Analyse", "Choose", "Apply", "Inspect", "Evidence"])
        title_cards(f"Topic {topic['num']} Checkpoint", "EXPLAIN THE DECISION", [("Purpose", "What does the audience need to notice?"), ("Method", "Why does this technique fit the content and edge?"), ("Control", "Which setting most changes the outcome?"), ("Failure", "What defect would make the result unacceptable?"), ("Proof", "Which view and evidence demonstrate quality?"), ("Next", "What controlled variation would improve the result?")], PALETTE[topic["num"]], columns=3)

    title_cards("Professional Editing Loop", "COURSE SYNTHESIS", [("Brief", "Clarify purpose, audience, channel and constraints."), ("Source", "Choose sufficient, rights-cleared assets."), ("Construct", "Use layers, masks and Smart Objects."), ("Experiment", "Vary one factor against a baseline."), ("Evaluate", "Inspect visual, technical and rights criteria."), ("Deliver", "Export, reopen and retain the master.")], BLUE)
    title_cards("Copyright and Asset Permission", "RESPONSIBLE VISUAL PRACTICE", [("Ownership", "Identify the creator/owner."), ("Permission", "Public visibility does not grant reuse."), ("Scope", "Check modification, commercial and redistribution rights."), ("People", "Confirm consent and privacy context."), ("Attribution", "Credit as the licence requires."), ("Record", "Retain source, licence, consent, date and use.")], RED, "Adobe Firefly Terms · not legal advice")
    title_cards("Responsible Generative AI", "PROVENANCE AND REVIEW", [("Inputs", "Use only material you may provide."), ("Log", "Record prompt and selected variation."), ("Review", "Check plausibility, bias and artefacts."), ("Terms", "Confirm current feature terms."), ("Credentials", "Retain provenance where appropriate."), ("Responsibility", "The editor owns the publication decision.")], MAGENTA)
    title_cards("Peer Review", "A4 · DISCUSS THE PROCESS", [("Describe", "State purpose and key decisions."), ("Show", "Reveal layers, masks and before/after."), ("Ask", "Use explicit criteria."), ("Record", "Capture what the reviewer noticed."), ("Decide", "Accept, adapt or reject with reason."), ("Revise", "Make one traceable improvement.")], CYAN)
    title_cards("Support", "AFTER THE COURSE", [("Email", "enquiry@tertiaryinfotech.com"), ("Telephone", "+65 6100 0613"), ("Portal", "https://lms-tms.tertiaryinfotech.com/"), ("Provider", C.ORG), ("Website", "www.tertiarycourses.com.sg"), ("Privacy", "Do not send assessment content publicly.")], BLUE)
    process_slide("Final Assessment", "WA + PP", ["Briefing", "WA · 60 min", "Transition", "PP · 60 min", "Submit"], "Complete your own open-book evidence and submit when time is called.", RED)
    process_slide("Assessment Flow", "COMPETENCY SIGN-OFF", ["TRAQOM", "Assessment digital attendance", "WA then PP", "Submit on LMS", "Sign summary record"], "Complete the official sequence: TRAQOM → assessment digital attendance → WA then PP → LMS submission → Assessment Summary Record.", MAGENTA)
    title_cards("TRAQOM · SSG Digital Attendance", "DIGITAL ATTENDANCE · MANDATORY", [("TRAQOM", "Scan the QR code provided through the LMS."), ("Assessment attendance", "Complete the official digital-attendance event before assessment."), ("Verification", "Remain until the trainer confirms the SSG record.")], CYAN, columns=3)
    s = _slide(); _shape(s, 0, 0, prs.slide_width, prs.slide_height, WHITE, radius=False)
    _shape(s, Inches(0), Inches(0), Inches(0.22), Inches(7.5), BLUE, radius=False)
    _text(s, Inches(0.9), Inches(2.1), Inches(11.6), Inches(1.1), "Thank You", 48, INK, True, PP_ALIGN.CENTER)
    _text(s, Inches(1.5), Inches(3.55), Inches(10.3), Inches(0.65), "Create with intent · preserve options · verify the output", 20, BLUE, True, PP_ALIGN.CENTER)
    _footer(s)
    out = CW / f"{C.SHORT_TITLE}-{C.VERSION}.pptx"
    prs.save(out)
    apply_fade_transitions(out)
    (HERE / "slide_map.json").write_text(json.dumps(SLIDE_MAP, indent=2), encoding="utf-8")
    return out


# ---------- Learner Guide ----------

def _doc_setup():
    doc = Document(); doc.styles["Normal"].font.name = "Arial"; doc.styles["Normal"].font.size = DPt(11)
    prodoc.style_headings(doc); return doc


def _doc_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet"); p.add_run(item)


def _doc_table(doc, headers, rows, widths=None, font_size=9.5):
    t = doc.add_table(rows=1, cols=len(headers)); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    if widths:
        t.autofit = False
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = h; prodoc._shade_cell(c, "224AF4")
        for r in c.paragraphs[0].runs:
            r.bold = True; r.font.color.rgb = DRGBColor(255, 255, 255); r.font.size = DPt(font_size)
    header_pr = t.rows[0]._tr.get_or_add_trPr()
    repeat = OxmlElement("w:tblHeader"); repeat.set(qn("w:val"), "true"); header_pr.append(repeat)
    if widths:
        for i, width in enumerate(widths):
            t.rows[0].cells[i].width = DInches(width)
    for row in rows:
        cells = t.add_row().cells
        row_pr = t.rows[-1]._tr.get_or_add_trPr(); row_pr.append(OxmlElement("w:cantSplit"))
        for i, val in enumerate(row):
            cells[i].text = str(val); cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if widths:
                cells[i].width = DInches(widths[i])
            for r in cells[i].paragraphs[0].runs:
                r.font.size = DPt(font_size)
    return t


def _static_toc(doc, rows):
    """Keep an editable Word TOC field and add deterministic PDF-ready cached entries."""
    prodoc.add_toc(doc)
    for node in doc.element.body.iter(qn("w:t")):
        if node.text and "Right-click and choose" in node.text:
            node.text = "Current verified contents are listed below. Update this editable TOC field in Word to refresh page references."
    table = _doc_table(doc, ["Section", "Page"], rows, [5.9, .7], font_size=10)
    # prodoc.add_toc ends with a page-break paragraph; move cached entries before it.
    body = doc.element.body
    for el in reversed(list(body)):
        if el.tag == qn("w:p") and el.xpath('.//w:br[@w:type="page"]'):
            el.addprevious(table._tbl)
            break


def build_lg():
    md = [f"# {C.TITLE} — Learner Guide", "", f"**Course code:** {C.COURSE_CODE}", f"**Version:** {C.VERSION} · {C.VERSION_DATE}", "", "## Purpose", "", "This guide contains the detailed Photoshop procedures, evidence requirements and acceptance criteria that accompany the visual course slides. Preserve the supplied originals, work non-destructively, and keep the PSD plus verified export for every lab.", "", "## Learning outcomes", ""]
    md.extend([f"- {lo}" for lo in C.LEARNING_OUTCOMES])
    md += ["", "## TSC alignment", "", "| Code | Knowledge / Ability |", "|---|---|"]
    md.extend([f"| {code} | {text} |" for code, text in C.TSC_KNOWLEDGE + C.TSC_ABILITIES])
    md += ["", "## Core professional workflow", "", "1. Clarify purpose, audience, output channel and constraints.", "2. Verify source quality, ownership, licence, consent and permitted use.", "3. Set pixel dimensions, colour mode, bit depth and profile for the deliverable.", "4. Build with named layers, groups, masks, adjustment layers and Smart Objects.", "5. Experiment by changing one factor at a time and retaining a baseline.", "6. Evaluate at Fit and 100% views using composition, edge, tone, output and rights criteria.", "7. Export, reopen and verify the delivery file; retain the editable master and evidence.", ""]
    for topic in C.TOPICS:
        md += [f"## Topic {topic['num']} — {topic['title']}", "", topic["subtitle"], "", f"**Alignment:** {topic['codes']}", ""]
        for item in [x for x in C.CONCEPTS if x["topic"] == topic["num"]]:
            md += [f"### {item['title']}", "", item["mechanism"], "", f"**Best used for:** {item['best_for']}", "", f"**Key controls:** {item['controls']}", "", f"**Watch for:** {item['watch']}", "", f"**Quality evidence:** {item['evidence']}", ""]
        for lab in [x for x in C.LABS if x["topic"] == topic["num"]]:
            md += [f"### Lab {lab['num']:02d} — {lab['title']}", "", f"**Scenario:** {lab['scenario']}", "", f"**Objective:** {lab['objective']}", "", "#### Detailed procedure", ""]
            md.extend([f"{i}. {st}" for i, st in enumerate(lab["steps"], 1)])
            md += ["", "#### Evidence", "", lab["evidence"], "", "#### Acceptance criteria", ""]
            md.extend([f"- {a}" for a in lab["acceptance"]])
            md += ["", f"Self-contained lab folder: `labs/lab-{lab['num']:02d}-{lab['slug']}/`", ""]
    md += ["## Intellectual property and responsible AI", "", "Use only assets you created or are permitted to use. Record the source, owner, licence or consent, date, allowed modifications, commercial/redistribution scope and attribution requirement. An image being publicly viewable does not itself grant reuse permission. Review current Adobe generative-AI terms before commercial work; do not use third-party content in prompts or reference images without the required rights, and retain provenance information such as Content Credentials where appropriate. This guide is educational information, not legal advice.", "", "## Source register", ""]
    md.extend([f"- **{name}:** {value}" for name, value in C.SOURCES])
    (REPO / "LEARNER-GUIDE.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    doc = _doc_setup()
    prodoc.add_cover_page(doc, "LEARNER GUIDE", C.TITLE, C.VERSION.lstrip("v"), org_logo=str(ORG_LOGO), course_logo=None, course_code=C.COURSE_CODE)
    prodoc.add_version_control(doc, [("6.0", "Legacy release", "Original trainer slides and lab-reference set.", "Tertiary Infotech Academy"), (C.VERSION.lstrip("v"), C.VERSION_DATE, f"Expanded visual rebuild with {len(C.CONCEPTS)} retained concepts and ten self-contained Photoshop/Firefly labs.", C.TRAINER)])
    _static_toc(doc, [("Purpose and Use", 4), ("Learning Outcomes and TSC Alignment", 4),
                      ("Topic 1 — GenAI for Visual Communication", 5),
                      ("Topic 2 — Firefly Storyboards and Reference Control", 10),
                      ("Topic 3 — Photoshop Generative Editing and Critique", 15),
                      ("Topic 4 — Colour Strategy, Enhancement and Delivery", 23),
                      ("Intellectual Property, Responsible AI and Sources", 28)])
    doc.add_heading("Purpose and Use", 1); doc.add_paragraph("This Learner Guide carries the detailed procedures intentionally omitted from the visual course slides. Work from the supplied PSD/JPEG files, preserve originals, keep the layered master, and verify every export.")
    doc.add_heading("Learning Outcomes", 1); _doc_bullets(doc, C.LEARNING_OUTCOMES)
    doc.add_heading("TSC Alignment", 1)
    _doc_table(doc, ["Code", "Knowledge / Ability"], C.TSC_KNOWLEDGE + C.TSC_ABILITIES)
    doc.add_heading("Core Professional Workflow", 1)
    for i, text in enumerate(["Clarify purpose, audience, output channel and constraints.", "Verify source quality, ownership, licence, consent and permitted use.", "Set pixel dimensions, colour mode, bit depth and profile for the deliverable.", "Build with named layers, groups, masks, adjustment layers and Smart Objects.", "Experiment by changing one factor at a time and retaining a baseline.", "Evaluate at Fit and 100% views using composition, edge, tone, output and rights criteria.", "Export, reopen and verify the delivery file; retain the editable master and evidence."], 1):
        doc.add_paragraph(f"{i}. {text}")
    for topic in C.TOPICS:
        doc.add_heading(f"Topic {topic['num']} — {topic['title']}", 1)
        doc.add_paragraph(topic["subtitle"]); doc.add_paragraph(f"Alignment: {topic['codes']}")
        for item in [x for x in C.CONCEPTS if x["topic"] == topic["num"]]:
            doc.add_heading(item["title"], 2)
            doc.add_paragraph(item["mechanism"])
            for label, value in [("Best used for", item["best_for"]), ("Key controls", item["controls"]), ("Watch for", item["watch"]), ("Quality evidence", item["evidence"])]:
                p = doc.add_paragraph(); p.add_run(label + ": ").bold = True; p.add_run(value)
        for lab in [x for x in C.LABS if x["topic"] == topic["num"]]:
            doc.add_heading(f"Lab {lab['num']:02d} — {lab['title']}", 2)
            p = doc.add_paragraph(); p.add_run("Scenario: ").bold = True; p.add_run(lab["scenario"])
            p = doc.add_paragraph(); p.add_run("Goal: ").bold = True; p.add_run(lab["objective"])
            jpg = first_jpeg(lab)
            workflow_shot = WORKFLOW_SCREENSHOTS.get(lab["num"])
            if jpg and workflow_shot and workflow_shot.exists():
                try:
                    doc.add_heading("Workflow Evidence Preview", 3)
                    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.add_run().add_picture(str(workflow_shot), width=DInches(5.4))
                    doc.add_paragraph("Authentic workflow screenshot from the supplied v6 trainer reference. Interface labels and positions may differ in the current Adobe release. The workflow-state schematic below is an editable evidence model.")
                    asset_name = Path(jpg).name
                    control_state = lab["steps"][2] if len(lab["steps"]) > 2 else lab["steps"][0]
                    editable_proof = lab["evidence"].split(".")[0]
                    export_test = lab["acceptance"][-1]
                    _doc_table(doc, ["Input asset", "Named control state", "Editable proof", "Verification"],
                               [(asset_name, control_state, editable_proof, export_test)],
                               [1.25, 1.85, 1.75, 1.75], font_size=8.2)
                except Exception:
                    pass
            doc.add_heading("Detailed Procedure", 3)
            for i, step in enumerate(lab["steps"], 1):
                doc.add_paragraph(f"{i}. {step}")
            doc.add_heading("Evidence to Retain", 3); doc.add_paragraph(lab["evidence"])
            doc.add_heading("Test It", 3)
            test_box = doc.add_table(rows=1, cols=1); test_box.style = "Table Grid"
            prodoc._shade_cell(test_box.cell(0, 0), "E9F8F3")
            test_box.cell(0, 0).text = "PASS when:\n" + "\n".join(f"• {a}" for a in lab["acceptance"])
            p = doc.add_paragraph(); p.add_run("Lab folder: ").bold = True; p.add_run(f"labs/lab-{lab['num']:02d}-{lab['slug']}/")
    doc.add_heading("Intellectual Property and Responsible AI", 1)
    doc.add_paragraph("Use only assets you created or are permitted to use. Record the source, owner, licence or consent, date, allowed modifications, commercial or redistribution scope and attribution requirement. Public visibility does not itself grant reuse permission. Review current Adobe generative-AI terms before commercial work, respect third-party rights in prompts and reference images, and retain provenance information where appropriate. This guide is educational information, not legal advice.")
    doc.add_heading("Source Register", 1); _doc_table(doc, ["Authority", "Location"], C.SOURCES)
    prodoc.add_page_numbers(doc); prodoc.enable_update_fields(doc)
    out = CW / f"LG-{C.SHORT_TITLE}.docx"; doc.save(out); return out


def lesson_schedule_current(slide_map):
    lab_refs = lambda numbers: ", ".join(str(slide_map[f"lab_{n}"]) for n in numbers)
    return {
        1: [
            ("09:00–09:30", "30 min", "Admin", "Attendance, introductions, ground rules and material access", "Opening slides"),
            ("09:30–10:30", "60 min", "Topic 1", "Human-led GenAI workflow, boundaries, prompts and visual hierarchy", f"Topic 1: slide {slide_map['topic_1']}"),
            ("10:30–10:45", "15 min", "Break", "Tea break", "—"),
            ("10:45–12:00", "75 min", "Topic 1 + Labs", "Labs 1–2 and Topic 1 evidence checkpoint", f"Lab slides: {lab_refs([1,2])}"),
            ("12:00–13:00", "60 min", "Topic 2", "Firefly models, content controls, composition and style references", f"Topic 2: slide {slide_map['topic_2']}"),
            ("13:00–14:00", "60 min", "Lunch", "Lunch break", "—"),
            ("14:00–15:30", "90 min", "Topic 2 + Labs", "Labs 3–4: reference-controlled storyboard and task flow", f"Lab slides: {lab_refs([3,4])}"),
            ("15:30–15:45", "15 min", "Break", "Tea break", "—"),
            ("15:45–16:00", "15 min", "Topic 2", "Peer review and Topic 2 checkpoint", f"Labs: {lab_refs([3,4])}"),
            ("16:00–17:15", "75 min", "Topic 3", "Photoshop generative feature map, selections and Generative Fill", f"Topic 3: slide {slide_map['topic_3']}"),
            ("17:15–17:45", "30 min", "Topic 3 + Lab", "Begin Lab 5: Generative Fill", f"Lab slide: {lab_refs([5])}"),
            ("17:45–18:00", "15 min", "Admin", "Reflection, evidence save and PM attendance", "Day 1 close"),
        ],
        2: [
            ("09:00–09:15", "15 min", "Admin", "AM attendance and Day 1 recap", "Admin / recap"),
            ("09:15–10:30", "75 min", "Topic 3 + Labs", "Complete Labs 5–8: Fill, background, expand and reference control", f"Labs: {lab_refs([5,6,7,8])}"),
            ("10:30–10:45", "15 min", "Break", "Tea break", "—"),
            ("10:45–11:00", "15 min", "Topic 3", "Aesthetic critique and Topic 3 checkpoint", f"Labs: {lab_refs([5,6,7,8])}"),
            ("11:00–12:30", "90 min", "Topic 4", "Colour fundamentals, adjustment layers, restoration and delivery", f"Topic 4: slide {slide_map['topic_4']}"),
            ("12:30–13:30", "60 min", "Lunch", "Lunch break", "—"),
            ("13:30–14:30", "60 min", "Topic 4 + Lab", "Lab 9: restoration, critique and colour", f"Lab slide: {lab_refs([9])}"),
            ("14:30–14:45", "15 min", "Break", "Tea break", "—"),
            ("14:45–15:45", "60 min", "Topic 4 + Lab", "Lab 10 capstone and Topic 4 checkpoint", f"Lab slide: {lab_refs([10])}"),
            ("15:45–16:00", "15 min", "Synthesis", "Course synthesis, assessment briefing and administration", "Closing assessment slides"),
            ("16:00–17:00", "60 min", "Assessment", "Written Assessment (WA/SAQ), open book", "5 questions · K1–K5"),
            ("17:00–18:00", "60 min", "Assessment", "Practical Performance (PP), open book", "4 tasks · A1–A7"),
        ],
    }


def build_lp():
    slide_map = json.loads((HERE / "slide_map.json").read_text(encoding="utf-8"))
    doc = _doc_setup()
    prodoc.add_cover_page(doc, "LESSON PLAN", C.TITLE, C.VERSION.lstrip("v"), org_logo=str(ORG_LOGO), course_logo=None, course_code=C.COURSE_CODE)
    prodoc.add_version_control(doc, [("6.0", "Legacy release", "Original trainer slides and delivery plan.", "Tertiary Infotech Academy"), (C.VERSION.lstrip("v"), C.VERSION_DATE, "Aligned two-day plan for four topics, ten labs and two hours of approved assessment.", C.TRAINER)])
    _static_toc(doc, [("Course Information", 4), ("Learning Outcomes and Assessment", 4),
                      ("Two-Day Schedule", 4), ("Lab Alignment", 6)])
    doc.add_heading("Course Information", 1)
    _doc_table(doc, ["Item", "Information"], [("Course title", C.TITLE), ("Course code", C.COURSE_CODE), ("TSC", f"{C.TSC_TITLE} · {C.TSC_CODE}"), ("Duration", C.DURATION), ("Delivery", "Facilitated concepts, coached Photoshop/Firefly labs, critique and 2 hours of assessment"), ("Provider", f"{C.ORG} · {C.UEN}"), ("Version", f"{C.VERSION} · {C.VERSION_DATE}")])
    doc.add_heading("Learning Outcomes", 1); _doc_bullets(doc, C.LEARNING_OUTCOMES)
    doc.add_heading("Assessment", 1); _doc_bullets(doc, [C.ASSESSMENT["written"], C.ASSESSMENT["practical"], C.ASSESSMENT["note"]])
    schedules = lesson_schedule_current(slide_map)
    doc.add_heading("Two-Day Schedule", 1)
    doc.add_paragraph("The schedule comprises 14 hours of facilitated training/contact time, inclusive of attendance, tea breaks and assessment briefing, plus 2 hours of summative assessment. Learning-unit allocation is LU1 3 hours, LU2 3 hours, LU3 4 hours and LU4 4 hours.")
    for day, rows in schedules.items():
        doc.add_heading(f"Day {day}", 2); _doc_table(doc, ["Time", "Duration", "Mode", "Topic / Activity", "Slide / Evidence Reference"], rows, [0.72, 0.62, 0.72, 2.85, 1.45], font_size=8.2)
    doc.add_page_break(); doc.add_heading("Lab Alignment", 1)
    _doc_table(doc, ["Lab", "Topic / Outcome", "Slide", "Key acceptance evidence"], [(f"Lab {lab['num']:02d}: {lab['title']}", f"Topic {lab['topic']} · {C.TOPICS[lab['topic']-1]['codes']}", slide_map[f"lab_{lab['num']}"], "; ".join(lab["acceptance"][:2])) for lab in C.LABS], [1.55, 1.35, 0.5, 3.0], font_size=8.2)
    prodoc.add_page_numbers(doc); prodoc.enable_update_fields(doc)
    out = CW / f"LP-{C.SHORT_TITLE}.docx"; doc.save(out); return out


def write_support_files(pptx_path):
    slide_count = len(prs.slides)
    (REPO / "CHANGELOG.md").write_text(f"# Changelog\n\n## {C.VERSION} — {C.VERSION_DATE}\n\n- Expanded the trainer deck to {slide_count} substantive slides for the two-day course.\n- Removed only the requested Adobe Express text-effects and Text to Template subtopics.\n- Retained creative text treatment through a current workflow: generated texture plus editable Photoshop type, clipping mask, colour, fitting and legibility controls.\n- Added editable worked-artifact flows, annotated control/canvas/proof models and diagnostic panels for every retained concept.\n- Added a new original cover hero and preserved all ten lab folders and supplied assets.\n- Regenerated the Learner Guide and Lesson Plan from the same source; detailed procedures remain outside the PPT.\n- Kept the approved WA/PP timing and competency structure; no practice exam was added.\n\n## v7 — 21 August 2026\n\n- Source-aligned 114-slide visual rebuild with 32 concepts and ten self-contained labs.\n\n## v6 — Legacy\n\n- Original trainer-slide and lab-reference release.\n", encoding="utf-8")
    coverage = [f"# Source Coverage — {C.VERSION}", "", f"Course: {C.TITLE} ({C.COURSE_CODE})", "", "| Source authority | Used for |", "|---|---|"]
    uses = {
        "Official course page": "Current course identity, duration, outcomes, topics and assessment modes",
        "Legacy trainer slides v6": "Useful legacy topic coverage, TSC criteria and admin sequence",
        "Original practical lab references": "Authentic learner Photoshop/JPEG source assets",
        "Live LMS-TMS assessment papers": "Approved K/A instrument structure and timing",
    }
    for name, src in C.SOURCES:
        use = uses.get(name, "Current feature behaviour, control guidance or provenance requirements")
        coverage.append(f"| {name} — `{src}` | {use} |")
    coverage += ["", "## Output map", "", f"- Slides: `{pptx_path.name}` ({slide_count} slides)", f"- Learner Guide: `courseware/LG-{C.SHORT_TITLE}.docx` and `LEARNER-GUIDE.md`", f"- Lesson Plan: `courseware/LP-{C.SHORT_TITLE}.docx`", "- Labs: `labs/lab-01-*` through `labs/lab-10-*`; every folder includes Photoshop and/or JPEG assets.", "- Assessment: five-question WA (K1–K5) and four-task PP (A1–A7), 60 minutes each.", "", "## Explicit exclusions", "", "- No practice exam is included.", "- Click-by-click procedures are intentionally excluded from the PPT and retained in the Learner Guide and lab guides.", ""]
    (CW / f"SOURCE-COVERAGE-{C.VERSION}.md").write_text("\n".join(coverage), encoding="utf-8")


if __name__ == "__main__":
    if not HERO.exists():
        raise SystemExit(f"Missing required cover hero: {HERO}")
    # Preserve the existing ten self-contained labs and supplied assets in place.
    ppt = build_slides_current()
    lg = build_lg()
    lp = build_lp()
    write_support_files(ppt)
    print(f"Built {len(prs.slides)} slides")
    print(ppt)
    print(lg)
    print(lp)
