"""Teste la robustesse de l'OCR sur des scans dégradés."""

import re
import sys
from difflib import SequenceMatcher

import frontmatter
import numpy as np
import pymupdf
import pytesseract
from PIL import Image, ImageFilter

from scripts.make_test_scan import markdown_to_plain

CODE = "DC-4095"
DPI = 200


def load_page_image(pdf_path: str) -> Image.Image:
    with pymupdf.open(pdf_path) as doc:
        pix = doc[0].get_pixmap(dpi=DPI)
        return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def resize(img: Image.Image, factor: float) -> Image.Image:
    width, height = img.size
    return img.resize((int(width * factor), int(height * factor)), Image.LANCZOS)


def rotate(img: Image.Image, angle: float) -> Image.Image:
    return img.rotate(angle, expand=True, fillcolor="white")


def blur(img: Image.Image, radius: float) -> Image.Image:
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def noise(img: Image.Image, sigma: float) -> Image.Image:
    rng = np.random.default_rng(0)
    gray = np.array(img.convert("L"), dtype=float)
    gray += rng.normal(0, sigma, gray.shape)
    return Image.fromarray(np.clip(gray, 0, 255).astype("uint8"))


# (défaut, niveau, fonction de dégradation)
CASES = (
    [("rotation", f"{a}°", lambda img, a=a: rotate(img, a)) for a in (5, 10, 15)]
    + [("flou", f"rayon {r}", lambda img, r=r: blur(img, r)) for r in (1.5, 3, 5)]
    + [("bruit", f"écart {s}", lambda img, s=s: noise(img, s)) for s in (40, 80, 120)]
    + [("résolution", f"{int(f * 100)} %", lambda img, f=f: resize(img, f))
       for f in (0.4, 0.3, 0.2)]
)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def read(img: Image.Image) -> str:
    return normalize(pytesseract.image_to_string(img, lang="fra"))


def report(label: str, text: str, reference: str) -> None:
    ratio = SequenceMatcher(None, reference, text, autojunk=False).ratio()
    print(
        f"{label:26s} similarité={ratio:6.2%}  "
        f"{CODE} lu {text.count(CODE)}/{reference.count(CODE)}"
    )


if __name__ == "__main__":
    pdf_path, md_path = sys.argv[1], sys.argv[2]
    reference = normalize(markdown_to_plain(frontmatter.load(md_path).content))
    base = load_page_image(pdf_path)

    report("propre", read(base), reference)
    for defect, level, degrade in CASES:
        report(f"{defect} {level}", read(degrade(base)), reference)

    print("\nBasse résolution, puis agrandissement avant l'OCR :")
    for f in (0.4, 0.3, 0.2):
        agrandi = resize(resize(base, f), 1 / f)
        report(f"{int(f * 100)} % puis agrandi", read(agrandi), reference)