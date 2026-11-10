"""Extraction de texte depuis un PDF : texte natif si présent, sinon OCR."""

import pymupdf
import pytesseract
from PIL import Image

MIN_CHARS = 30
OCR_DPI = 300


def _page_to_image(page, dpi: int) -> Image.Image:
    pix = page.get_pixmap(dpi=dpi)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def extract_pdf(path, dpi: int = OCR_DPI) -> tuple[str, str]:
    """Retourne (texte complet, méthode : natif, ocr, mixte ou vide)."""
    texts, methods = [], set()
    with pymupdf.open(path) as doc:
        for page in doc:
            text = page.get_text().strip()
            if len(text) >= MIN_CHARS:
                methods.add("natif")
            else:
                image = _page_to_image(page, dpi)
                text = pytesseract.image_to_string(image, lang="fra").strip()
                methods.add("ocr")
            texts.append(text)

    if not methods:
        method = "vide"
    elif len(methods) == 1:
        method = methods.pop()
    else:
        method = "mixte"
    return "\n\n".join(texts), method