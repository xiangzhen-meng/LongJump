"""Verify formatting of original vs formatted docx"""
import xml.etree.ElementTree as ET
import subprocess, os

NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

os.makedirs('/tmp/docx_inspect/formatted', exist_ok=True)
subprocess.run(['rm', '-rf', '/tmp/docx_inspect/formatted/word'])
subprocess.run(['unzip', '-o', '/Users/mengxz/Developer/LongJump/main_formatted.docx',
                '-d', '/tmp/docx_inspect/formatted'], capture_output=True)

for label, path in [('原始 main.docx', '/tmp/docx_inspect/main/word'),
                     ('格式化后 main_formatted.docx', '/tmp/docx_inspect/formatted/word')]:
    print(f'\n===== {label} =====')

    tree = ET.parse(f'{path}/styles.xml')
    root = tree.getroot()

    dd = root.find(f'{{{NS}}}docDefaults')
    if dd is not None:
        rpr = dd.find('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPrDefault/{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr')
        if rpr is not None:
            fonts = rpr.find(f'{{{NS}}}rFonts')
            sz = rpr.find(f'{{{NS}}}sz')
            print(f'  默认字体: {fonts.attrib if fonts is not None else "无"}')
            print(f'  默认字号: {sz.attrib if sz is not None else "无"}')
        ppr = dd.find(f'{{{NS}}}pPrDefault/{{{NS}}}pPr')
        if ppr is not None:
            spacing = ppr.find(f'{{{NS}}}spacing')
            print(f'  默认段间距: {spacing.attrib if spacing is not None else "无"}')

    # Check key styles
    for sid in ['Title', 'Author', 'AbstractTitle', 'Abstract', 'Heading1', 'Heading2', 'BodyText']:
        for s in root.findall(f'{{{NS}}}style'):
            if s.get(f'{{{NS}}}styleId') == sid:
                rpr = s.find(f'{{{NS}}}rPr')
                if rpr is not None:
                    fonts = rpr.find(f'{{{NS}}}rFonts')
                    sz = rpr.find(f'{{{NS}}}sz')
                    b = rpr.find(f'{{{NS}}}b')
                    font_str = ''
                    if fonts is not None:
                        ea = fonts.get(f'{{{NS}}}eastAsia', '')
                        asc = fonts.get(f'{{{NS}}}ascii', '')
                        font_str = f'{asc}/{ea}'
                    sz_str = sz.get(f'{{{NS}}}val') if sz is not None else '-'
                    bold_str = 'B' if b is not None else ''
                    print(f'  {sid:20s}: font={font_str:30s} sz={sz_str:4s} {bold_str}')

    # Document section
    doc_tree = ET.parse(f'{path}/document.xml')
    doc_root = doc_tree.getroot()
    body = doc_root.find(f'{{{NS}}}body')
    sectPr = body.find(f'{{{NS}}}sectPr')
    if sectPr is not None:
        pgMar = sectPr.find(f'{{{NS}}}pgMar')
        if pgMar is not None:
            t = pgMar.get(f'{{{NS}}}top', '-')
            b = pgMar.get(f'{{{NS}}}bottom', '-')
            l = pgMar.get(f'{{{NS}}}left', '-')
            r = pgMar.get(f'{{{NS}}}right', '-')
            print(f'  页边距: top={t} bottom={b} left={l} right={r} (twips)')
