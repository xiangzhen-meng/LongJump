#!/usr/bin/env python3
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "main_pandoc_raw.md"
OUT = ROOT / "main_pandoc.md"


def convert_eq_refs(text: str) -> str:
    pattern = re.compile(
        r"\[\\\[(eq:[^\]\\]+)\\\]\]\(#\1\)\{reference-type=\"eqref\"\s+reference=\"\1\"\}",
        re.MULTILINE,
    )
    return pattern.sub(lambda m: f"[@{m.group(1)}]", text)


def convert_normal_refs(text: str) -> str:
    pattern = re.compile(
        r"\[([^\]]+)\]\(#(tab:[^\)]+|fig:[^\)]+)\)\{reference-type=\"ref\"\s+reference=\"\2\"\}",
        re.MULTILINE,
    )
    # Keep table/figure references as the visible number emitted by Pandoc's
    # LaTeX reader. The equation references are handled by pandoc-crossref.
    return pattern.sub(lambda m: m.group(1), text)


def convert_html_figures(text: str) -> str:
    pattern = re.compile(
        r'<figure id="(fig:[^"]+)"[^>]*>\s*'
        r'<embed src="([^"]+)" style="width:([0-9.]+)%"\s*/>\s*'
        r'<figcaption>(.*?)</figcaption>\s*'
        r'</figure>',
        re.DOTALL,
    )

    def repl(match: re.Match) -> str:
        fig_id, src, width, caption = match.groups()
        caption = re.sub(r"<[^>]+>", "", caption)
        caption = re.sub(r"\s+", " ", caption).strip()
        return f"![{caption}]({src}){{#{fig_id} width={width}%}}"

    return pattern.sub(repl, text)


def number_table_captions(text: str) -> str:
    table = re.compile(r"(:::\s*\{#tab:[^}]+\}\n)(.*?)(\n:::)" , re.DOTALL)
    counter = 0

    def repl(match: re.Match) -> str:
        nonlocal counter
        counter += 1
        start, body, end = match.groups()
        body = re.sub(
            r"(^\s*:\s*)(.*)$",
            lambda m: f"{m.group(1)}表 {counter} {m.group(2)}",
            body,
            count=1,
            flags=re.MULTILINE,
        )
        return start + body + end

    return table.sub(repl, text)


def move_equation_labels(text: str) -> str:
    # Move \label{eq:...} from inside display-math blocks to the Pandoc
    # attribute position so pandoc-crossref can number equations. Pandoc
    # crossref supports one identifier per display block, so multi-label align
    # blocks are split into one displayed equation per labelled row.
    block = re.compile(r"\$\$(.*?)\$\$", re.DOTALL)

    def repl(match: re.Match) -> str:
        body = match.group(1)
        labels = re.findall(r"\\label\{(eq:[^}]+)\}", body)
        if not labels:
            return match.group(0)
        if len(labels) > 1:
            body_no_env = re.sub(r"\\begin\{align\*?\}|\\end\{align\*?\}", "", body)
            pieces = []
            for line in body_no_env.splitlines():
                found = re.search(r"\\label\{(eq:[^}]+)\}", line)
                if not found:
                    continue
                label = found.group(1)
                cleaned = re.sub(r"\\label\{eq:[^}]+\}", "", line)
                cleaned = re.sub(r"\\\\\s*$", "", cleaned).strip()
                cleaned = cleaned.replace("&", "")
                if cleaned:
                    pieces.append(f"$$\n{cleaned}\n$$ {{#{label}}}")
            if pieces:
                return "\n\n".join(pieces) + "\n"
        label = labels[-1]
        cleaned = re.sub(r"\s*\\label\{eq:[^}]+\}", "", body)
        cleaned = cleaned.strip()
        return f"$$\n{cleaned}\n$$ {{#{label}}}\n"

    return block.sub(repl, text)


def main() -> None:
    text = RAW.read_text(encoding="utf-8")
    text = convert_eq_refs(text)
    text = convert_normal_refs(text)
    text = convert_html_figures(text)
    text = number_table_captions(text)
    text = move_equation_labels(text)
    OUT.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
