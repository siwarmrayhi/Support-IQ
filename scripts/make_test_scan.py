"""Fabrique un faux scan (PDF image) à partir d'un document Markdown."""

import re
import sys
from pathlib import Path

import frontmatter
import pymupdf

DPI = 200
MARGIN = 40


def reflow(text: str) -> str:
    """Recolle les lignes coupées à la main, en gardant paragraphes et puces."""
    out = []
    for paragraph in re.split(r"\n\s*\n", text):
        items = []
        for line in paragraph.splitlines():
            line = line.strip()
            if re.match(r"(\d+\.|-)\s", line) or not items:
                items.append(line)
            else:
                items[-1] += " " + line
        out.append("\n".join(items))
    return "\n\n".join(out)


def markdown_to_plain(text: str) -> str:
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    return reflow(text.replace("**", "").replace("→", ">"))


def make_native_pdf(text: str) -> pymupdf.Document:
    for fontsize in (10, 9, 8, 7):
        doc = pymupdf.open()
        page = doc.new_page()
        rect = pymupdf.Rect(
            MARGIN, MARGIN, page.rect.width - MARGIN, page.rect.height - MARGIN
        )
        if page.insert_textbox(rect, text, fontsize=fontsize, fontname="helv") >= 0:
            return doc
    raise ValueError("Le texte ne tient pas sur une page, même à 7 points")


def make_scan(native: pymupdf.Document) -> pymupdf.Document:
    scan = pymupdf.open()
    for page in native:
        pix = page.get_pixmap(dpi=DPI)
        new_page = scan.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_image(new_page.rect, pixmap=pix)
    return scan


if __name__ == "__main__":
    source, output = Path(sys.argv[1]), Path(sys.argv[2])
    text = markdown_to_plain(frontmatter.load(source).content)
    make_scan(make_native_pdf(text)).save(output)
    print(f"Faux scan écrit : {output}")