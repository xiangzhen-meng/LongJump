#!/usr/bin/env python3
import shutil
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / "main_formatted.docx"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
}
WURI = NS["w"]
W = f"{{{WURI}}}"
ET.register_namespace("w", WURI)


def text(el):
    return "".join(t.text or "" for t in el.findall(".//w:t", NS)).strip()


def has_math(el):
    return el.find(".//m:oMath", NS) is not None or el.find(".//m:oMathPara", NS) is not None


def is_p(el):
    return el.tag == W + "p"


def is_tbl(el):
    return el.tag == W + "tbl"


def main():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        with zipfile.ZipFile(DOCX) as z:
            z.extractall(tmp)

        doc_path = tmp / "word" / "document.xml"
        tree = ET.parse(doc_path)
        body = tree.getroot().find("w:body", NS)
        items = list(body)

        remove_indices = set()
        replace_text = {}

        # Delete low-level two-body kinematics expansion and cross-product detail.
        remove_indices.update([20, 21, 23, 24, 25, 27])

        # Delete duplicate/auxiliary equations in landing displacement derivation.
        remove_indices.update([44, 45, 46])

        # Delete numerical initial/final evaluation equations; keep the surrounding discussion.
        remove_indices.update([64, 65, 66, 67])

        # Delete verbose three-body geometry/velocity expansion and coefficient expansion.
        remove_indices.update([
            85, 87, 89, 90, 92, 95, 98,
            99, 101, 103, 105, 107, 108,
            113, 115, 117, 119,
            120, 121, 122, 123,
            124, 125, 126,
            129, 131, 133, 135,
            136, 137, 139, 141, 143,
            144, 146, 147, 149, 150, 152,
            155, 160, 162,
            167, 168,
            170, 171, 173,
        ])

        # Keep the core model equations and adjust text that referenced deleted equations.
        replace_text[20] = "由质心位置和速度关系代入角动量守恒式，可得到二刚体模型的运动方程。"
        replace_text[85] = "取髋关节 O 为参考点，可写出各刚体质心位置以及总质心位置，并据此建立角动量守恒方程。"
        replace_text[99] = "速度关系由各刚体绕其连接点转动得到，代入角动量守恒式后可整理为三刚体模型的角动量分配关系。"
        replace_text[113] = "将各刚体相对总质心的位置和速度代入角动量守恒式，并按角速度合并同类项，可得："
        replace_text[129] = "其中系数函数 A_T、A_A、A_L 仅依赖当前姿态角度，具体展开式较长，本文不再逐项列出。"
        replace_text[170] = "三刚体模型中，脚的位置和总质心位置可由各刚体几何关系确定，因此落地前伸量可写为："

        for idx, new_text in replace_text.items():
            if idx < len(items) and is_p(items[idx]):
                p = items[idx]
                for r in list(p.findall("w:r", NS)):
                    p.remove(r)
                r = ET.SubElement(p, W + "r")
                t = ET.SubElement(r, W + "t")
                t.text = new_text

        for idx in sorted(remove_indices, reverse=True):
            if idx < len(items) and items[idx] in list(body):
                body.remove(items[idx])

        # Clean textual references to equations removed above.
        post_replacements = {
            "将式\xa023改写为：": "由上述角动量分配关系可改写为：",
            "将 、 代入式\xa023，整理得：": "将手臂和腿相对于躯干的角速度代入上述角动量分配关系，整理得：",
            "由式\xa010，总质心水平坐标：": "总质心水平坐标可由三刚体几何关系直接得到。",
            "记 、、。对每个刚体展开 ，得到  项线性表达式。按 、、 合并同类项，最终将式\xa016化为：": "将角动量守恒式按各刚体角速度合并同类项，可整理为：",
            "当手臂相对于躯干固定（），即JRA情形，式\xa036简化为": "当手臂相对于躯干固定时，即 JRA 情形，上式简化为：",
        }
        for p in body.findall("w:p", NS):
            current = text(p)
            if current not in post_replacements:
                continue
            for r in list(p.findall("w:r", NS)):
                p.remove(r)
            r = ET.SubElement(p, W + "r")
            t = ET.SubElement(r, W + "t")
            t.text = post_replacements[current]

        # Further prune long coefficient details from the already-pruned document.
        items2 = list(body)
        second_pass_remove = set()
        for idx, el in enumerate(items2):
            current = text(el) if is_p(el) else ""
            if current in {
                "为简洁，定义系数：",
                "速度关系：",
                "同理计算相对速度 ：",
                "其中系数函数  仅依赖当前姿态角度：",
                "这里  为常数项（与角度无关）， 为  的系数，其完整表达式如下：",
                "常数项：",
                "的系数：",
                "三刚体模型中，脚的位置（刚体  末端）：",
            }:
                second_pass_remove.add(idx)
            if is_p(el) and el.find("m:oMathPara", NS) is not None and 87 <= idx <= 113:
                # Keep the total centroid expression and final angular momentum
                # distribution, but drop intermediate coefficients.
                if idx not in {90, 97}:
                    second_pass_remove.add(idx)
            if is_p(el) and el.find("m:oMathPara", NS) is not None and idx in {121, 126, 128}:
                second_pass_remove.add(idx)
        for idx in sorted(second_pass_remove, reverse=True):
            if idx < len(items2) and items2[idx] in list(body):
                body.remove(items2[idx])

        tree.write(doc_path, encoding="utf-8", xml_declaration=True)

        tmp_zip = DOCX.with_suffix(".zip")
        if tmp_zip.exists():
            tmp_zip.unlink()
        shutil.make_archive(str(DOCX.with_suffix("")), "zip", tmp)
        tmp_zip.rename(DOCX)


if __name__ == "__main__":
    main()
