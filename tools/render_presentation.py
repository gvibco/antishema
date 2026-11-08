import pymupdf
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "docs" / "presentation" / "АнтиСхема_презентация_Посысаев_Иван_Шульга_Георгий.pdf"
OUT = ROOT / "docs" / "presentation" / "slides"
OUT.mkdir(parents=True, exist_ok=True)

document = pymupdf.open(PDF)
for index, page in enumerate(document, 1):
    pixmap = page.get_pixmap(dpi=140)
    path = OUT / f"slide-{index:02d}.png"
    pixmap.save(path)
    print(path)

print("pages:", document.page_count)
