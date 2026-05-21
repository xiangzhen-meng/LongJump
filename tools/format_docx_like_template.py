#!/usr/bin/env python3
import copy
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "main_crossref.docx"
OUT = ROOT / "main_formatted.docx"

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
WURI = NS["w"]
W = f"{{{WURI}}}"
ET.register_namespace("w", WURI)


def q(name: str) -> str:
    return W + name


def child(parent, tag):
    el = parent.find(f"w:{tag}", NS)
    if el is None:
        el = ET.SubElement(parent, q(tag))
    return el


def ppr(p):
    return child(p, "pPr")


def rpr(r):
    return child(r, "rPr")


def set_attr(el, **attrs):
    for k, v in attrs.items():
        el.set(q(k), str(v))


def remove_children(parent, tag):
    for el in list(parent.findall(f"w:{tag}", NS)):
        parent.remove(el)


def remove_font_theme_attrs(fonts):
    for attr in ["asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"]:
        fonts.attrib.pop(q(attr), None)


def get_text(p):
    return "".join(t.text or "" for t in p.findall(".//w:t", NS))


def ensure_p_style(p, style_id):
    pp = ppr(p)
    pstyle = pp.find("w:pStyle", NS)
    if pstyle is None:
        pstyle = ET.Element(q("pStyle"))
        pp.insert(0, pstyle)
    pstyle.set(q("val"), style_id)


def clear_p_style(p):
    pp = ppr(p)
    for el in list(pp.findall("w:pStyle", NS)):
        pp.remove(el)


def set_para(p, *, jc=None, before=None, after=None, line=None, line_rule="auto", first_line=None, keep_next=False):
    pp = ppr(p)
    if jc:
        set_attr(child(pp, "jc"), val=jc)
    if before is not None or after is not None or line is not None:
        sp = child(pp, "spacing")
        if before is not None:
            sp.set(q("before"), str(before))
        if after is not None:
            sp.set(q("after"), str(after))
        if line is not None:
            sp.set(q("line"), str(line))
            sp.set(q("lineRule"), line_rule)
    if first_line is not None:
        set_attr(child(pp, "ind"), firstLine=str(first_line))
    remove_children(pp, "pageBreakBefore")
    remove_children(pp, "keepNext")
    if keep_next:
        child(pp, "keepNext")


def set_run_font_size(r, *, east_asia="宋体", ascii_font="Times New Roman", size="21", bold=None):
    rp = rpr(r)
    fonts = child(rp, "rFonts")
    remove_font_theme_attrs(fonts)
    set_attr(fonts, ascii=ascii_font, hAnsi=ascii_font, eastAsia=east_asia, cs=ascii_font)
    set_attr(child(rp, "sz"), val=size)
    set_attr(child(rp, "szCs"), val=size)
    if bold is True:
        child(rp, "b")
        child(rp, "bCs")
    elif bold is False:
        remove_children(rp, "b")
        remove_children(rp, "bCs")


def clear_italic(p):
    for r in p.findall(".//w:r", NS):
        rp = r.find("w:rPr", NS)
        if rp is None:
            continue
        remove_children(rp, "i")
        remove_children(rp, "iCs")


def remove_rendered_page_breaks(root):
    for parent in root.iter():
        for el in list(parent):
            if el.tag == q("lastRenderedPageBreak"):
                parent.remove(el)


def set_para_runs(p, *, east_asia="宋体", ascii_font="Times New Roman", size="21", bold=None):
    for r in p.findall(".//w:r", NS):
        set_run_font_size(r, east_asia=east_asia, ascii_font=ascii_font, size=size, bold=bold)


def replace_exact_text(p, text):
    runs = p.findall("w:r", NS)
    for r in runs:
        p.remove(r)
    r = ET.SubElement(p, q("r"))
    t = ET.SubElement(r, q("t"))
    t.text = text
    return r


def section_properties(cols=1, continuous=False):
    sect = ET.Element(q("sectPr"))
    if continuous:
        set_attr(ET.SubElement(sect, q("type")), val="continuous")
    pg_sz = ET.SubElement(sect, q("pgSz"))
    set_attr(pg_sz, w="11900", h="16840")
    mar = ET.SubElement(sect, q("pgMar"))
    set_attr(mar, top="1247", right="1134", bottom="1247", left="1134", header="851", footer="992", gutter="0")
    col = ET.SubElement(sect, q("cols"))
    if cols == 2:
        set_attr(col, num="2", space="392")
    else:
        set_attr(col, space="720")
    return sect


def insert_section_after(paras, idx, cols):
    pp = ppr(paras[idx])
    old = pp.find("w:sectPr", NS)
    if old is not None:
        pp.remove(old)
    pp.append(section_properties(cols, continuous=True))


def clear_para_numbering_and_indent(p):
    pp = ppr(p)
    remove_children(pp, "numPr")
    ind = pp.find("w:ind", NS)
    if ind is not None:
        pp.remove(ind)


def clear_para_formatting_for_direct_style(p):
    clear_p_style(p)
    clear_para_numbering_and_indent(p)


def normalize_heading_text(text):
    text = text.strip()
    text = re.sub(r"^[\u00b7\u2022\s]+", "", text)
    text = re.sub(r"^(\d+)\s*\.\s*(\d+)\s*", r"\1.\2 ", text)
    text = re.sub(r"^(\d+)\s+\.\s*(\d+)\s*", r"\1.\2 ", text)
    text = re.sub(r"^(\d+)\s*([^\d.\s].*)$", r"\1 \2", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def update_styles(styles_path):
    tree = ET.parse(styles_path)
    root = tree.getroot()
    style_fonts = {
        "Normal": ("宋体", "Times New Roman", "21", False),
        "BodyText": ("宋体", "Times New Roman", "21", False),
        "FirstParagraph": ("宋体", "Times New Roman", "21", False),
        "Title": ("黑体", "Times New Roman", "32", True),
        "Author": ("仿宋", "Times New Roman", "24", False),
        "Date": ("仿宋", "Times New Roman", "24", False),
        "Abstract": ("宋体", "Times New Roman", "18", False),
        "AbstractTitle": ("黑体", "Times New Roman", "18", True),
        "Heading1": ("黑体", "Times New Roman", "24", True),
        "Heading2": ("黑体", "Times New Roman", "21", True),
        "Caption": ("黑体", "Times New Roman", "18", True),
        "TableCaption": ("黑体", "Times New Roman", "18", True),
        "ImageCaption": ("黑体", "Times New Roman", "18", True),
    }
    for st in root.findall("w:style", NS):
        sid = st.get(q("styleId"))
        if sid not in style_fonts:
            continue
        east_asia, ascii_font, size, bold = style_fonts[sid]
        rp = child(st, "rPr")
        fonts = child(rp, "rFonts")
        remove_font_theme_attrs(fonts)
        set_attr(fonts, ascii=ascii_font, hAnsi=ascii_font, eastAsia=east_asia, cs=ascii_font)
        set_attr(child(rp, "sz"), val=size)
        set_attr(child(rp, "szCs"), val=size)
        if bold:
            child(rp, "b")
            child(rp, "bCs")
        else:
            remove_children(rp, "b")
            remove_children(rp, "bCs")
    tree.write(styles_path, encoding="utf-8", xml_declaration=True)


def format_table(tbl):
    tbl_pr = child(tbl, "tblPr")
    jc = child(tbl_pr, "jc")
    set_attr(jc, val="center")
    for p in tbl.findall(".//w:p", NS):
        set_para(p, jc="center", before=0, after=0, line=300)
        set_para_runs(p, east_asia="宋体", ascii_font="Times New Roman", size="18")


def main():
    if not SRC.exists():
        raise SystemExit(f"missing {SRC}")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        with zipfile.ZipFile(SRC) as z:
            z.extractall(tmp)

        doc_path = tmp / "word" / "document.xml"
        styles_path = tmp / "word" / "styles.xml"
        update_styles(styles_path)
        root = ET.parse(doc_path)
        body = root.getroot().find("w:body", NS)
        paras = body.findall("w:p", NS)
        remove_rendered_page_breaks(root.getroot())

        # Keep title and abstract one-column, then immediately switch the
        # article body (including introduction) to two columns. The section is
        # continuous so Word can start the two-column body on the same page.
        abstract_label = next((i for i, p in enumerate(paras) if get_text(p).strip() in {"Abstract", "摘要"}), None)
        abstract_body_idx = abstract_label + 1 if abstract_label is not None and abstract_label + 1 < len(paras) else None
        if abstract_body_idx is not None:
            insert_section_after(paras, abstract_body_idx, 1)

        body_sect = body.find("w:sectPr", NS)
        if body_sect is not None:
            body.remove(body_sect)
        body.append(section_properties(2))

        for i, p in enumerate(paras):
            text = get_text(p).strip()
            style = p.find("w:pPr/w:pStyle", NS)
            style_id = style.get(q("val")) if style is not None else ""

            if i == 0:
                clear_para_formatting_for_direct_style(p)
                set_para(p, jc="center", before=0, after=40, line=300, keep_next=False)
                set_para_runs(p, east_asia="黑体", ascii_font="Times New Roman", size="32", bold=False)
            elif i in (1, 2):
                clear_para_formatting_for_direct_style(p)
                set_para(p, jc="center", before=0, after=20, line=220)
                set_para_runs(p, east_asia="仿宋", ascii_font="Times New Roman", size="21")
            elif text == "Abstract":
                clear_para_formatting_for_direct_style(p)
                replace_exact_text(p, "摘要")
                set_para(p, jc="left", before=40, after=0, line=220)
                set_para_runs(p, east_asia="黑体", ascii_font="Times New Roman", size="18", bold=False)
            elif abstract_body_idx is not None and i == abstract_body_idx:
                clear_p_style(p)
                set_para(p, jc="both", before=0, after=40, line=220, first_line=0)
                set_para_runs(p, east_asia="宋体", ascii_font="Times New Roman", size="18")
            elif text.startswith("表 "):
                set_para(p, jc="center", before=120, after=60, line=240, keep_next=True)
                set_para_runs(p, east_asia="黑体", ascii_font="Times New Roman", size="18", bold=True)
                clear_italic(p)
            elif text.startswith("Figure ") or text.startswith("图 "):
                set_para(p, jc="center", before=60, after=120, line=240)
                set_para_runs(p, east_asia="黑体", ascii_font="Times New Roman", size="18", bold=True)
                clear_italic(p)
            elif style_id == "Heading2" or re.match(r"^\d+\.\d+", text):
                clear_para_formatting_for_direct_style(p)
                normalized = normalize_heading_text(text)
                if normalized != text:
                    replace_exact_text(p, normalized)
                set_para(p, jc="left", before=0, after=0, line=360, keep_next=False)
                set_para_runs(p, east_asia="黑体", ascii_font="Times New Roman", size="21", bold=True)
            elif style_id == "Heading1" or re.match(r"^\d+[^\d.]", text):
                clear_para_formatting_for_direct_style(p)
                # Pandoc's section number and title are adjacent in docx text; add a space.
                normalized = normalize_heading_text(text)
                if normalized != text:
                    replace_exact_text(p, normalized)
                set_para(p, jc="left", before=72, after=72, line=360, keep_next=False)
                set_para_runs(p, east_asia="黑体", ascii_font="Times New Roman", size="24", bold=True)
            elif text:
                set_para(p, jc="both", before=0, after=0, line=360, first_line=420)
                set_para_runs(p, east_asia="宋体", ascii_font="Times New Roman", size="21")

        for tbl in body.findall("w:tbl", NS):
            format_table(tbl)

        root.write(doc_path, encoding="utf-8", xml_declaration=True)

        if OUT.exists():
            OUT.unlink()
        shutil.make_archive(str(OUT.with_suffix("")), "zip", tmp)
        OUT.with_suffix(".zip").rename(OUT)


if __name__ == "__main__":
    main()
