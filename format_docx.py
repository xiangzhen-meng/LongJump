"""
Apply 稿件模板.docx formatting to main.docx:
- Replace Word built-in heading styles with custom template-compliant styles
- Format all tables as three-line tables (三线表)
- Set page margins, fonts, line spacing per template requirements
"""
import shutil, copy
from docx import Document
from docx.shared import Pt, Cm, Emu, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import parse_xml
from lxml import etree

WML = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

def q(tag):
    return f"{{{WML}}}{tag}"

MAIN = "/Users/mengxz/Developer/LongJump/main.docx"
OUT  = "/Users/mengxz/Developer/LongJump/main_formatted.docx"

shutil.copy2(MAIN, OUT)
doc = Document(OUT)

# ── Helper: remove element ──
def remove_elem(parent, tag):
    el = parent.find(q(tag))
    if el is not None:
        parent.remove(el)

# ── Helper: get or create element ──
def ensure_elem(parent, tag, **attrs):
    el = parent.find(q(tag))
    if el is None:
        el = etree.SubElement(parent, q(tag))
    for k, v in attrs.items():
        el.set(q(k), v)
    return el

###############################################################################
# Step 1: docDefaults
###############################################################################
styles_xml = doc.styles.element
for dd in styles_xml.findall(q("docDefaults")):
    styles_xml.remove(dd)

dd = etree.SubElement(styles_xml, q("docDefaults"))

rpr_def = etree.SubElement(dd, q("rPrDefault"))
rpr = etree.SubElement(rpr_def, q("rPr"))
etree.SubElement(rpr, q("rFonts"), {
    q("ascii"): "Times New Roman",
    q("eastAsia"): "宋体",
    q("hAnsi"): "Times New Roman",
    q("cs"): "Times New Roman",
})
etree.SubElement(rpr, q("sz"), {q("val"): "21"})
etree.SubElement(rpr, q("szCs"), {q("val"): "21"})
etree.SubElement(rpr, q("lang"), {
    q("val"): "en-US", q("eastAsia"): "zh-CN", q("bidi"): "ar-SA"
})

ppr_def = etree.SubElement(dd, q("pPrDefault"))
ppr = etree.SubElement(ppr_def, q("pPr"))
etree.SubElement(ppr, q("spacing"), {
    q("line"): "360", q("lineRule"): "auto", q("after"): "0"
})

###############################################################################
# Step 2: Create custom heading styles (not Word built-in)
###############################################################################
def create_custom_style(doc, style_id, name, base_on="Normal",
                         font_ascii="Times New Roman", font_east="黑体",
                         size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT,
                         space_before_pt=6, space_after_pt=6, line_spacing=1.5,
                         next_style="Normal"):
    """Create a custom paragraph style if it doesn't exist."""
    try:
        style = doc.styles[name]
    except KeyError:
        # Create style via XML to avoid naming issues
        style_elem = etree.SubElement(doc.styles.element, q("style"), {
            q("type"): "paragraph",
            q("styleId"): style_id,
        })
        etree.SubElement(style_elem, q("name"), {q("val"): name})
        etree.SubElement(style_elem, q("basedOn"), {q("val"): base_on})
        etree.SubElement(style_elem, q("next"), {q("val"): next_style})
        # pPr
        ppr = etree.SubElement(style_elem, q("pPr"))
        etree.SubElement(ppr, q("spacing"), {
            q("line"): str(int(line_spacing * 240)),
            q("lineRule"): "auto",
            q("before"): str(int(space_before_pt * 20)),
            q("after"): str(int(space_after_pt * 20)),
        })
        jc_map = {WD_ALIGN_PARAGRAPH.LEFT: "left", WD_ALIGN_PARAGRAPH.CENTER: "center",
                  WD_ALIGN_PARAGRAPH.RIGHT: "right", WD_ALIGN_PARAGRAPH.JUSTIFY: "both"}
        if align in jc_map:
            etree.SubElement(ppr, q("jc"), {q("val"): jc_map[align]})
        # rPr
        rpr = etree.SubElement(style_elem, q("rPr"))
        etree.SubElement(rpr, q("rFonts"), {
            q("ascii"): font_ascii, q("eastAsia"): font_east,
            q("hAnsi"): font_ascii, q("cs"): font_ascii,
        })
        sz_val = str(int(size_pt * 2))
        etree.SubElement(rpr, q("sz"), {q("val"): sz_val})
        etree.SubElement(rpr, q("szCs"), {q("val"): sz_val})
        if bold:
            etree.SubElement(rpr, q("b"))
        # Re-fetch style
        doc.styles  # force reload? python-docx caches
    return doc.styles[name]

# Force reload styles cache by accessing _element
h1_style = create_custom_style(doc, "H1Custom", "一级标题 论文",
    font_east="黑体", size_pt=12, bold=True,
    align=WD_ALIGN_PARAGRAPH.LEFT,
    space_before_pt=6, space_after_pt=6,
    line_spacing=1.5)

h2_style = create_custom_style(doc, "H2Custom", "二级标题 论文",
    font_east="黑体", size_pt=10.5, bold=True,
    align=WD_ALIGN_PARAGRAPH.LEFT,
    space_before_pt=4, space_after_pt=4,
    line_spacing=1.5)

h3_style = create_custom_style(doc, "H3Custom", "三级标题 论文",
    font_east="黑体", size_pt=10.5, bold=True,
    align=WD_ALIGN_PARAGRAPH.LEFT,
    space_before_pt=2, space_after_pt=2,
    line_spacing=1.5)

body_style = create_custom_style(doc, "BodyCustom", "正文 论文",
    font_east="宋体", size_pt=10.5, bold=False,
    align=WD_ALIGN_PARAGRAPH.JUSTIFY,
    space_before_pt=0, space_after_pt=0,
    line_spacing=1.5)


###############################################################################
# Step 3: Replace heading styles on paragraphs
###############################################################################
# Map built-in style names → custom style names
HEADING_MAP = {
    "Heading 1": "H1Custom", "Heading1": "H1Custom",
    "heading 1": "H1Custom",
    "Heading 2": "H2Custom", "Heading2": "H2Custom",
    "heading 2": "H2Custom",
    "Heading 3": "H3Custom", "Heading3": "H3Custom",
    "heading 3": "H3Custom",
    "Heading 4": "H3Custom", "Heading4": "H3Custom",
    "Heading 5": "H3Custom", "Heading5": "H3Custom",
}

# Also fix body text styles: map Body Text / First Paragraph to our custom body style
BODY_STYLE_MAP = {
    "Body Text": "BodyCustom", "BodyText": "BodyCustom",
    "body text": "BodyCustom",
    "First Paragraph": "BodyCustom", "FirstParagraph": "BodyCustom",
    "first paragraph": "BodyCustom",
}

for para in doc.paragraphs:
    ppr = para._element.find(q("pPr"))
    if ppr is None:
        continue
    pstyle = ppr.find(q("pStyle"))
    if pstyle is None:
        continue
    style_val = pstyle.get(q("val"))

    if style_val in HEADING_MAP:
        pstyle.set(q("val"), HEADING_MAP[style_val])
        # Remove any direct spacing/jc that might override style
        for tag in ["spacing", "jc"]:
            el = ppr.find(q(tag))
            if el is not None:
                ppr.remove(el)

    elif style_val in BODY_STYLE_MAP:
        pstyle.set(q("val"), BODY_STYLE_MAP[style_val])
        for tag in ["spacing", "jc", "ind"]:
            el = ppr.find(q(tag))
            if el is not None:
                ppr.remove(el)

# Also fix "Normal" style paragraphs that are body text 
# (apply the body text formatting directly)
try:
    normal_style = doc.styles["Normal"]
    n_ppr = normal_style.element.find(q("pPr"))
    if n_ppr is None:
        n_ppr = etree.SubElement(normal_style.element, q("pPr"))
    ensure_elem(n_ppr, "spacing", line="360", lineRule="auto", after="0")
    n_rpr = normal_style.element.find(q("rPr"))
    if n_rpr is None:
        n_rpr = etree.SubElement(normal_style.element, q("rPr"))
    ensure_elem(n_rpr, "rFonts",
                ascii="Times New Roman", eastAsia="宋体",
                hAnsi="Times New Roman", cs="Times New Roman")
    ensure_elem(n_rpr, "sz", val="21")
    ensure_elem(n_rpr, "szCs", val="21")
except:
    pass


###############################################################################
# Step 4: Title/Author/Abstract styles
###############################################################################
def set_style_font(doc, style_name, font_ascii="Times New Roman", font_east="宋体",
                   size_pt=10.5, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT,
                   space_before=0, space_after=0, line_spacing=1.5):
    try:
        s = doc.styles[style_name]
    except KeyError:
        return
    # rPr
    rpr = s.element.find(q("rPr"))
    if rpr is None:
        rpr = etree.SubElement(s.element, q("rPr"))
    ensure_elem(rpr, "rFonts", ascii=font_ascii, eastAsia=font_east,
                hAnsi=font_ascii, cs=font_ascii)
    sz_val = str(int(size_pt * 2))
    ensure_elem(rpr, "sz", val=sz_val)
    ensure_elem(rpr, "szCs", val=sz_val)
    # bold
    b = rpr.find(q("b"))
    if bold and b is None:
        etree.SubElement(rpr, q("b"))
    elif not bold and b is not None:
        rpr.remove(b)
    # pPr
    ppr = s.element.find(q("pPr"))
    if ppr is None:
        ppr = etree.SubElement(s.element, q("pPr"))
    ensure_elem(ppr, "spacing", line=str(int(line_spacing * 240)),
                lineRule="auto", before=str(space_before), after=str(space_after))
    jc_map = {
        WD_ALIGN_PARAGRAPH.LEFT: "left", WD_ALIGN_PARAGRAPH.CENTER: "center",
        WD_ALIGN_PARAGRAPH.RIGHT: "right", WD_ALIGN_PARAGRAPH.JUSTIFY: "both",
    }
    if align in jc_map:
        jce = ensure_elem(ppr, "jc", val=jc_map[align])
    else:
        jce = ppr.find(q("jc"))
        if jce is not None:
            ppr.remove(jce)

# Title: 小二黑体 (18pt), centered
set_style_font(doc, "Title", font_east="黑体", size_pt=18, bold=False,
               align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.5)
set_style_font(doc, "Title Char", font_east="黑体", size_pt=18, bold=False)

# Author: 小四仿宋 (12pt), centered
set_style_font(doc, "Author", font_east="仿宋", size_pt=12, bold=False,
               align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=0)
try:
    auth_style = doc.styles["Author"]
    auth_rpr = auth_style.element.find(q("rPr"))
    if auth_rpr is not None:
        ensure_elem(auth_rpr, "rFonts", ascii="Times New Roman", eastAsia="仿宋",
                    hAnsi="Times New Roman", cs="Times New Roman")
except:
    pass

# Date/Affiliation: 六号宋体 (7.5pt), centered
set_style_font(doc, "Date", font_east="宋体", size_pt=7.5, bold=False,
               align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=6)

# Abstract Title: 小五黑体 (9pt), bold, centered
set_style_font(doc, "Abstract Title", font_east="黑体", size_pt=9, bold=True,
               align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=0)

# Abstract body: 小五宋体 (9pt)
set_style_font(doc, "Abstract", font_east="宋体", size_pt=9, bold=False,
               align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=12)

# Table Caption: centered above table, 小五黑体 (9pt)
set_style_font(doc, "Table Caption", font_east="黑体", size_pt=9, bold=False,
               align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=2)

# Image Caption: centered below figure, 小五宋体 (9pt)
set_style_font(doc, "Image Caption", font_east="宋体", size_pt=9, bold=False,
               align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=6)

# Fix captioned figure style
set_style_font(doc, "Captioned Figure", font_east="宋体", size_pt=9, bold=False,
               align=WD_ALIGN_PARAGRAPH.CENTER)


###############################################################################
# Step 5: Page margins
###############################################################################
for section in doc.sections:
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.2)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(2.0)


###############################################################################
# Step 6: Format all tables as three-line tables (三线表)
###############################################################################
def set_cell_border(cell, position, sz="4", val="single", color="000000"):
    """Set border on a cell. position: top, bottom, left, right"""
    tc = cell._tc
    tc_pr = tc.find(q("tcPr"))
    if tc_pr is None:
        tc_pr = etree.SubElement(tc, q("tcPr"))
    borders = tc_pr.find(q("tcBorders"))
    if borders is None:
        borders = etree.SubElement(tc_pr, q("tcBorders"))
    tag = q(position)
    el = borders.find(tag)
    if el is None:
        el = etree.SubElement(borders, tag)
    el.set(q("val"), val)
    el.set(q("sz"), sz)
    el.set(q("color"), color)
    el.set(q("space"), "0")

def format_three_line_table(table):
    """Apply three-line table formatting:
    - Top of header row: thick line (1.5pt = sz=12)
    - Bottom of header row: thin line (0.75pt = sz=6)  
    - Bottom of last row: thick line (1.5pt = sz=12)
    - No vertical borders, no interior horizontal borders
    """
    nrows = len(table.rows)
    if nrows == 0:
        return

    # Remove all existing borders first, then set three-line
    for row in table.rows:
        for cell in row.cells:
            tc = cell._tc
            tc_pr = tc.find(q("tcPr"))
            if tc_pr is not None:
                borders = tc_pr.find(q("tcBorders"))
                if borders is not None:
                    tc_pr.remove(borders)

    # Header row
    header_row = table.rows[0]
    for cell in header_row.cells:
        set_cell_border(cell, "top", sz="12", val="single")     # thick top
        set_cell_border(cell, "bottom", sz="6", val="single")   # thin bottom

    # Data rows - remove any top border, set thin bottom
    for i, row in enumerate(table.rows):
        if i == 0:
            continue  # header done
        for cell in row.cells:
            set_cell_border(cell, "top", sz="0", val="none")
            set_cell_border(cell, "bottom", sz="0", val="none")

    # Last row: thick bottom border
    last_row = table.rows[-1]
    for cell in last_row.cells:
        set_cell_border(cell, "bottom", sz="12", val="single")

    # Remove left/right borders from all cells
    for row in table.rows:
        for cell in row.cells:
            set_cell_border(cell, "left", sz="0", val="none")
            set_cell_border(cell, "right", sz="0", val="none")

    # Format cell text: 小五 (9pt), 宋体, centered for header
    for ri, row in enumerate(table.rows):
        for cell in row.cells:
            for para in cell.paragraphs:
                # Set paragraph spacing
                ppr = para._element.find(q("pPr"))
                if ppr is None:
                    ppr = etree.SubElement(para._element, q("pPr"))
                spacing = ppr.find(q("spacing"))
                if spacing is None:
                    spacing = etree.SubElement(ppr, q("spacing"))
                spacing.set(q("line"), "260")
                spacing.set(q("lineRule"), "auto")
                spacing.set(q("before"), "0")
                spacing.set(q("after"), "0")
                # No first-line indent in tables
                ind = ppr.find(q("ind"))
                if ind is not None:
                    ppr.remove(ind)
                # Center text in header, left-align data
                jc = ppr.find(q("jc"))
                if jc is None:
                    jc = etree.SubElement(ppr, q("jc"))
                if ri == 0:
                    jc.set(q("val"), "center")
                else:
                    jc.set(q("val"), "center")  # Center all cells for clean look

            for run in cell.paragraphs[0].runs:
                rpr_elem = run._element.find(q("rPr"))
                if rpr_elem is None:
                    rpr_elem = etree.SubElement(run._element, q("rPr"))
                # Set font
                rfonts = rpr_elem.find(q("rFonts"))
                if rfonts is None:
                    rfonts = etree.SubElement(rpr_elem, q("rFonts"))
                rfonts.set(q("ascii"), "Times New Roman")
                rfonts.set(q("eastAsia"), "宋体")
                rfonts.set(q("hAnsi"), "Times New Roman")
                rfonts.set(q("cs"), "Times New Roman")
                # Remove theme attributes
                for attr in ["w:asciiTheme", "w:eastAsiaTheme", "w:hAnsiTheme", "w:cstheme"]:
                    if qn(attr) in rfonts.attrib:
                        del rfonts.attrib[qn(attr)]
                # Size: header 9pt bold, data 9pt
                sz = rpr_elem.find(q("sz"))
                if sz is None:
                    sz = etree.SubElement(rpr_elem, q("sz"))
                sz.set(q("val"), "18")  # 9pt
                szCs = rpr_elem.find(q("szCs"))
                if szCs is None:
                    szCs = etree.SubElement(rpr_elem, q("szCs"))
                szCs.set(q("val"), "18")
                if ri == 0:
                    b = rpr_elem.find(q("b"))
                    if b is None:
                        etree.SubElement(rpr_elem, q("b"))

    # Set table width to 100% and alignment center
    tbl = table._tbl
    tbl_pr = tbl.find(q("tblPr"))
    if tbl_pr is None:
        tbl_pr = etree.SubElement(tbl, q("tblPr"))
    ensure_elem(tbl_pr, "jc", val="center")
    # Set table width to auto/fit
    tbl_w = tbl_pr.find(q("tblW"))
    if tbl_w is not None:
        tbl_pr.remove(tbl_w)
    ensure_elem(tbl_pr, "tblW", w="5000", type="pct")


for table in doc.tables:
    format_three_line_table(table)


###############################################################################
# Step 7: Remove direct formatting from styled paragraphs
###############################################################################
STYLED_NAMES = {
    "H1Custom", "H2Custom", "H3Custom", "BodyCustom",
    "Title", "Author", "Date",
    "Abstract Title", "Abstract",
    "Table Caption", "Image Caption", "Captioned Figure",
    "Normal", "Compact",
}

for para in doc.paragraphs:
    ppr = para._element.find(q("pPr"))
    style_name = None
    if ppr is not None:
        ps = ppr.find(q("pStyle"))
        if ps is not None:
            style_name = ps.get(q("val"))

    if style_name in STYLED_NAMES:
        # Remove direct spacing/jc overrides
        if ppr is not None:
            for tag in ["spacing", "jc", "ind"]:
                el = ppr.find(q(tag))
                if el is not None:
                    ppr.remove(el)

        for run in para.runs:
            rpr_elem = run._element.find(q("rPr"))
            if rpr_elem is not None:
                for tag_name in [q("rFonts"), q("sz"), q("szCs"),
                                 q("b"), q("bCs"), q("i"), q("iCs"),
                                 q("color"), q("spacing"), q("lang")]:
                    for el in rpr_elem.findall(tag_name):
                        rpr_elem.remove(el)
                if len(rpr_elem) == 0 and len(rpr_elem.attrib) == 0:
                    run._element.remove(rpr_elem)


###############################################################################
# Step 8: Save
###############################################################################
doc.save(OUT)
print(f"Saved formatted document to: {OUT}")
print("Done! Tables are now three-line tables, headings use custom styles.")
