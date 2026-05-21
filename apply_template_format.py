"""
Apply formatting from 稿件模板.docx to main.docx.
Modifies styles, docDefaults, section properties, and removes direct formatting.
Content is preserved.
"""

from docx import Document
from docx.shared import Pt, Cm, Emu, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from lxml import etree
import copy
import shutil
import os

TEMPLATE_PATH = "/Users/mengxz/Developer/LongJump/稿件模板.docx"
MAIN_PATH = "/Users/mengxz/Developer/LongJump/main.docx"
OUTPUT_PATH = "/Users/mengxz/Developer/LongJump/main_formatted.docx"

WML_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

def qn_tag(tag):
    return f"{{{WML_NS}}}{tag}"


def apply_formatting():
    shutil.copy2(MAIN_PATH, OUTPUT_PATH)
    doc = Document(OUTPUT_PATH)

    # ── Step 1: Update docDefaults (default font, size, paragraph spacing) ──
    styles_xml = doc.styles.element
    doc_defaults = styles_xml.find(qn_tag("docDefaults"))
    if doc_defaults is not None:
        styles_xml.remove(doc_defaults)

    # Create new docDefaults with template formatting
    # Default font: Times New Roman (ASCII) + 宋体 (East Asia), size 10.5pt (五号)
    # Default paragraph: 1.5x line spacing, no after spacing
    new_defaults = etree.SubElement(styles_xml, qn_tag("docDefaults"))
    rpr_default = etree.SubElement(new_defaults, qn_tag("rPrDefault"))
    rpr = etree.SubElement(rpr_default, qn_tag("rPr"))
    etree.SubElement(rpr, qn_tag("rFonts"),
                     {qn_tag("ascii"): "Times New Roman",
                      qn_tag("eastAsia"): "宋体",
                      qn_tag("hAnsi"): "Times New Roman",
                      qn_tag("cs"): "Times New Roman"})
    etree.SubElement(rpr, qn_tag("sz"), {qn_tag("val"): "21"})
    etree.SubElement(rpr, qn_tag("szCs"), {qn_tag("val"): "21"})
    etree.SubElement(rpr, qn_tag("lang"),
                     {qn_tag("val"): "en-US",
                      qn_tag("eastAsia"): "zh-CN",
                      qn_tag("bidi"): "ar-SA"})

    ppr_default = etree.SubElement(new_defaults, qn_tag("pPrDefault"))
    ppr = etree.SubElement(ppr_default, qn_tag("pPr"))
    etree.SubElement(ppr, qn_tag("spacing"),
                     {qn_tag("line"): "360",
                      qn_tag("lineRule"): "auto",
                      qn_tag("after"): "0"})

    # ── Step 2: Update existing styles ──

    # Helper: get or update a style
    _STYLE_NAME_MAP = {
        "Heading1": "heading 1", "Heading2": "heading 2", "Heading3": "heading 3",
        "Heading4": "heading 4", "Heading5": "heading 5", "Heading6": "heading 6",
        "Heading7": "heading 7", "Heading8": "heading 8", "Heading9": "heading 9",
        "BodyText": "Body Text", "BodyTextChar": "Body Text Char",
        "FirstParagraph": "First Paragraph",
        "AbstractTitle": "Abstract Title",
        "TitleChar": "Title Char",
        "Heading1Char": "Heading 1 Char", "Heading2Char": "Heading 2 Char",
        "Heading3Char": "Heading 3 Char", "Heading4Char": "Heading 4 Char",
        "Heading5Char": "Heading 5 Char", "Heading6Char": "Heading 6 Char",
        "Heading7Char": "Heading 7 Char", "Heading8Char": "Heading 8 Char",
        "Heading9Char": "Heading 9 Char",
        "TableCaption": "Table Caption", "ImageCaption": "Image Caption",
        "DefinitionTerm": "Definition Term",
        "BlockText": "Block Text",
        "FootnoteText": "Footnote Text",
    }
    def get_style(style_id):
        name = _STYLE_NAME_MAP.get(style_id, style_id)
        try:
            return doc.styles[name]
        except KeyError:
            try:
                return doc.styles[style_id]
            except KeyError:
                return None

    def set_font_xml(style, font_ascii="Times New Roman", font_east="宋体",
                     size_pt=None, bold=False, italic=False, color=None):
        """Configure font properties on a style's rPr XML element"""
        if style is None:
            return
        rpr = style.element.find(qn_tag("rPr"))
        if rpr is None:
            rpr = etree.SubElement(style.element, qn_tag("rPr"))

        if size_pt is not None:
            sz_val = str(int(size_pt * 2))
            sz = rpr.find(qn_tag("sz"))
            if sz is None:
                sz = etree.SubElement(rpr, qn_tag("sz"))
            sz.set(qn_tag("val"), sz_val)
            szCs = rpr.find(qn_tag("szCs"))
            if szCs is None:
                szCs = etree.SubElement(rpr, qn_tag("szCs"))
            szCs.set(qn_tag("val"), sz_val)

        rfonts = rpr.find(qn_tag("rFonts"))
        if rfonts is None:
            rfonts = etree.SubElement(rpr, qn_tag("rFonts"))
        rfonts.set(qn_tag("ascii"), font_ascii)
        rfonts.set(qn_tag("eastAsia"), font_east)
        rfonts.set(qn_tag("hAnsi"), font_ascii)
        rfonts.set(qn_tag("cs"), font_ascii)
        for attr in ["w:asciiTheme", "w:eastAsiaTheme", "w:hAnsiTheme", "w:cstheme"]:
            if qn(attr) in rfonts.attrib:
                del rfonts.attrib[qn(attr)]

        if bold:
            b = rpr.find(qn_tag("b"))
            if b is None:
                b = etree.SubElement(rpr, qn_tag("b"))
        else:
            b = rpr.find(qn_tag("b"))
            if b is not None:
                rpr.remove(b)

        if italic:
            i = rpr.find(qn_tag("i"))
            if i is None:
                i = etree.SubElement(rpr, qn_tag("i"))
        else:
            i = rpr.find(qn_tag("i"))
            if i is not None:
                rpr.remove(i)

        if color is not None:
            color_el = rpr.find(qn_tag("color"))
            if color_el is None:
                color_el = etree.SubElement(rpr, qn_tag("color"))
            color_el.set(qn_tag("val"), color)
            for attr in ["w:themeColor", "w:themeShade", "w:themeTint"]:
                if qn(attr) in color_el.attrib:
                    del color_el.attrib[qn(attr)]

    def set_paragraph_style(style, font_ascii="Times New Roman", font_east="宋体",
                            size_pt=None, bold=False, italic=False,
                            align=None, space_before=None, space_after=None,
                            line_spacing=None, first_line_indent=None,
                            color=None, outline_level=None):
        """Configure a paragraph style"""
        if style is None:
            return
        pf = style.paragraph_format

        if align is not None:
            pf.alignment = align
        if space_before is not None:
            pf.space_before = Pt(space_before)
        if space_after is not None:
            pf.space_after = Pt(space_after)
        if line_spacing is not None:
            pf.line_spacing = line_spacing
        if first_line_indent is not None:
            pf.first_line_indent = Cm(first_line_indent)

        set_font_xml(style, font_ascii, font_east, size_pt, bold, italic, color)

        # Fonts via XML
        rpr = style.element.find(qn_tag("rPr"))
        if rpr is None:
            rpr = etree.SubElement(style.element, qn_tag("rPr"))
        rfonts = rpr.find(qn_tag("rFonts"))
        if rfonts is None:
            rfonts = etree.SubElement(rpr, qn_tag("rFonts"))
        rfonts.set(qn_tag("ascii"), font_ascii)
        rfonts.set(qn_tag("eastAsia"), font_east)
        rfonts.set(qn_tag("hAnsi"), font_ascii)
        rfonts.set(qn_tag("cs"), font_ascii)

        if color is not None:
            color_el = rpr.find(qn_tag("color"))
            if color_el is None:
                color_el = etree.SubElement(rpr, qn_tag("color"))
            color_el.set(qn_tag("val"), color)
            # Remove theme color attributes if set
            for attr in ["w:themeColor", "w:themeShade", "w:themeTint"]:
                if qn(attr) in color_el.attrib:
                    del color_el.attrib[qn(attr)]

        # Remove theme font references (force explicit fonts)
        for attr in ["w:asciiTheme", "w:eastAsiaTheme", "w:hAnsiTheme", "w:cstheme"]:
            if qn(attr) in rfonts.attrib:
                del rfonts.attrib[qn(attr)]

        # Outline level
        if outline_level is not None:
            ppr = style.element.find(qn_tag("pPr"))
            if ppr is None:
                ppr = etree.SubElement(style.element, qn_tag("pPr"))
            ol = ppr.find(qn_tag("outlineLvl"))
            if ol is None:
                ol = etree.SubElement(ppr, qn_tag("outlineLvl"))
            ol.set(qn_tag("val"), str(outline_level))

    # ── Normal style (body text base) ──
    normal = get_style("Normal")
    set_paragraph_style(normal,
                        font_ascii="Times New Roman", font_east="宋体",
                        size_pt=10.5,
                        line_spacing=1.5,
                        space_after=0)

    # ── Title (title of paper) ──
    title = get_style("Title")
    set_paragraph_style(title,
                        font_ascii="Times New Roman", font_east="黑体",
                        size_pt=18,
                        bold=False,
                        align=WD_ALIGN_PARAGRAPH.CENTER,
                        line_spacing=1.5,
                        space_after=0)
    # Title Char style
    title_char = get_style("TitleChar")
    set_font_xml(title_char, font_ascii="Times New Roman", font_east="黑体",
                 size_pt=18, bold=False)

    # ── Author ──
    author = get_style("Author")
    set_paragraph_style(author,
                        font_ascii="Times New Roman", font_east="仿宋",
                        size_pt=12,
                        align=WD_ALIGN_PARAGRAPH.CENTER,
                        line_spacing=1.5,
                        space_before=6,
                        space_after=0)

    # ── Date (treat as affiliation line) ──
    date = get_style("Date")
    set_paragraph_style(date,
                        font_ascii="Times New Roman", font_east="宋体",
                        size_pt=7.5,
                        align=WD_ALIGN_PARAGRAPH.CENTER,
                        line_spacing=1.5,
                        space_before=0,
                        space_after=6)

    # ── Abstract Title ──
    abstract_title = get_style("AbstractTitle")
    set_paragraph_style(abstract_title,
                        font_ascii="Times New Roman", font_east="黑体",
                        size_pt=9,
                        bold=True,
                        align=WD_ALIGN_PARAGRAPH.CENTER,
                        line_spacing=1.5,
                        space_before=12,
                        space_after=0)

    # ── Abstract ──
    abstract = get_style("Abstract")
    set_paragraph_style(abstract,
                        font_ascii="Times New Roman", font_east="宋体",
                        size_pt=9,
                        line_spacing=1.5,
                        space_before=4,
                        space_after=12)

    # ── Heading 1 (first-level section title) ──
    h1 = get_style("Heading1")
    set_paragraph_style(h1,
                        font_ascii="Times New Roman", font_east="黑体",
                        size_pt=12,
                        bold=True,
                        line_spacing=1.5,
                        space_before=6,
                        space_after=6,
                        outline_level=0)
    h1_char = get_style("Heading1Char")
    set_font_xml(h1_char, font_ascii="Times New Roman", font_east="黑体",
                 size_pt=12, bold=True)

    # ── Heading 2 ──
    h2 = get_style("Heading2")
    set_paragraph_style(h2,
                        font_ascii="Times New Roman", font_east="黑体",
                        size_pt=10.5,
                        bold=True,
                        line_spacing=1.5,
                        space_before=4,
                        space_after=4,
                        outline_level=1)
    h2_char = get_style("Heading2Char")
    set_font_xml(h2_char, font_ascii="Times New Roman", font_east="黑体",
                 size_pt=10.5, bold=True)

    # ── Heading 3 ──
    h3 = get_style("Heading3")
    set_paragraph_style(h3,
                        font_ascii="Times New Roman", font_east="黑体",
                        size_pt=10.5,
                        bold=True,
                        line_spacing=1.5,
                        space_before=4,
                        space_after=4,
                        outline_level=2)
    h3_char = get_style("Heading3Char")
    set_font_xml(h3_char, font_ascii="Times New Roman", font_east="黑体",
                 size_pt=10.5, bold=True)

    # ── Heading 4-9, keep same but with correct fonts ──
    for hid, hlevel in [("Heading4", 3), ("Heading5", 4), ("Heading6", 5),
                         ("Heading7", 6), ("Heading8", 7), ("Heading9", 8)]:
        hs = get_style(hid)
        if hs:
            set_paragraph_style(hs,
                                font_ascii="Times New Roman", font_east="黑体",
                                size_pt=10.5,
                                bold=True,
                                line_spacing=1.5,
                                space_before=2,
                                space_after=2,
                                outline_level=hlevel)
        hs_char = get_style(hid + "Char")
        if hs_char:
            set_font_xml(hs_char, font_ascii="Times New Roman", font_east="黑体",
                         size_pt=10.5, bold=True)

    # ── Body Text ──
    body_text = get_style("BodyText")
    set_paragraph_style(body_text,
                        font_ascii="Times New Roman", font_east="宋体",
                        size_pt=10.5,
                        line_spacing=1.5,
                        space_before=0,
                        space_after=0,
                        first_line_indent=0.74)
    body_text_char = get_style("BodyTextChar")
    set_font_xml(body_text_char, font_ascii="Times New Roman", font_east="宋体",
                 size_pt=10.5)

    # ── First Paragraph ──
    first_para = get_style("FirstParagraph")
    set_paragraph_style(first_para,
                        font_ascii="Times New Roman", font_east="宋体",
                        size_pt=10.5,
                        line_spacing=1.5,
                        space_before=0,
                        space_after=0,
                        first_line_indent=0.74)

    # ── Compact ──
    compact = get_style("Compact")
    set_paragraph_style(compact,
                        font_ascii="Times New Roman", font_east="宋体",
                        size_pt=10.5,
                        line_spacing=1.5,
                        space_before=0,
                        space_after=0)

    # ── Caption, Table, etc ──
    caption = get_style("Caption")
    set_paragraph_style(caption,
                        font_ascii="Times New Roman", font_east="黑体",
                        size_pt=9,
                        bold=False,
                        italic=False,
                        line_spacing=1.5,
                        space_after=4)
    # Remove italic from Caption's rPr
    if caption:
        caption_rpr = caption.element.find(qn_tag("rPr"))
        if caption_rpr is not None:
            for tag in [qn_tag("i"), qn_tag("iCs")]:
                el = caption_rpr.find(tag)
                if el is not None:
                    caption_rpr.remove(el)

    # ── Step 3: Section properties (page margins) ──
    for section in doc.sections:
        section.top_margin = Cm(2.2)
        section.bottom_margin = Cm(2.2)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)
        section.header_distance = Cm(1.5)
        section.footer_distance = Cm(1.75)

    # ── Step 4: Remove direct formatting from runs (let styles inherit) ──
    # For paragraphs that use styles, remove direct run formatting
    styled_paragraph_names = {
        "Title", "Author", "Date",
        "AbstractTitle", "Abstract",
        "Heading1", "Heading2", "Heading3", "Heading4", "Heading5",
        "Heading6", "Heading7", "Heading8", "Heading9",
        "BodyText", "Body Text", "FirstParagraph", "First Paragraph",
        "Compact", "Normal", "Caption", "TableCaption", "ImageCaption",
        "BlockText", "FootnoteText", "Figure", "CaptionedFigure"
    }

    for para in doc.paragraphs:
        ppr = para._element.find(qn_tag("pPr"))
        style_id = None
        if ppr is not None:
            pstyle = ppr.find(qn_tag("pStyle"))
            if pstyle is not None:
                style_id = pstyle.get(qn_tag("val"))

        if style_id in styled_paragraph_names:
            # Remove direct spacing overrides (let style handle it)
            if ppr is not None:
                spacing = ppr.find(qn_tag("spacing"))
                if spacing is not None:
                    ppr.remove(spacing)
                jc = ppr.find(qn_tag("jc"))
                if jc is not None:
                    ppr.remove(jc)

            # Remove direct run formatting for every run in this paragraph
            for run in para.runs:
                rpr_elem = run._element.find(qn_tag("rPr"))
                if rpr_elem is not None:
                    # Remove font overrides
                    for tag_name in [qn_tag("rFonts"), qn_tag("sz"), qn_tag("szCs"),
                                     qn_tag("b"), qn_tag("bCs"),
                                     qn_tag("i"), qn_tag("iCs"),
                                     qn_tag("color"), qn_tag("spacing")]:
                        for el in rpr_elem.findall(tag_name):
                            rpr_elem.remove(el)
                    # If rPr is now empty, remove it
                    if len(rpr_elem) == 0 and len(rpr_elem.attrib) == 0:
                        run._element.remove(rpr_elem)

    # ── Step 5: Fix table formatting ──
    for table in doc.tables:
        # Set table style
        try:
            tbl_pr = table._tbl.find(qn_tag("tblPr"))
        except AttributeError:
            tbl_pr = table._element.find(qn_tag("tblPr"))

        if tbl_pr is not None:
            tbl_style = tbl_pr.find(qn_tag("tblStyle"))
            # Remove existing table style reference so we can apply direct formatting
            # or set to a simple style

        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    # Apply body text formatting to cell content
                    ppr = para._element.find(qn_tag("pPr"))
                    if ppr is not None:
                        spacing = ppr.find(qn_tag("spacing"))
                        if spacing is not None:
                            ppr.remove(spacing)
                    for run in para.runs:
                        rpr_elem = run._element.find(qn_tag("rPr"))
                        if rpr_elem is not None:
                            rfonts = rpr_elem.find(qn_tag("rFonts"))
                            if rfonts is None:
                                rfonts = etree.SubElement(rpr_elem, qn_tag("rFonts"))
                            rfonts.set(qn_tag("ascii"), "Times New Roman")
                            rfonts.set(qn_tag("eastAsia"), "宋体")
                            rfonts.set(qn_tag("hAnsi"), "Times New Roman")
                            rfonts.set(qn_tag("cs"), "Times New Roman")
                            for attr in ["w:asciiTheme", "w:eastAsiaTheme",
                                         "w:hAnsiTheme", "w:cstheme"]:
                                if qn(attr) in rfonts.attrib:
                                    del rfonts.attrib[qn(attr)]
                            sz = rpr_elem.find(qn_tag("sz"))
                            if sz is None:
                                sz = etree.SubElement(rpr_elem, qn_tag("sz"))
                            sz.set(qn_tag("val"), "18")  # 9pt = 五号 for tables
                            szcs = rpr_elem.find(qn_tag("szCs"))
                            if szcs is None:
                                szcs = etree.SubElement(rpr_elem, qn_tag("szCs"))
                            szcs.set(qn_tag("val"), "18")

    # ── Step 6: Save ──
    doc.save(OUTPUT_PATH)
    print(f"✓ Saved formatted document to: {OUTPUT_PATH}")


if __name__ == "__main__":
    apply_formatting()
