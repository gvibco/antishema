"""Проверить PPTX и ODP: 11 слайдов, один шрифт, три цвета, нужные тезисы."""

from pathlib import Path
import re
import zipfile
import xml.etree.ElementTree as ET

from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
PPTX = ROOT / "АнтиСхема_презентация_Посысаев_Иван_Шульга_Георгий.pptx"
ODP = ROOT / "АнтиСхема_презентация_Посысаев_Иван_Шульга_Георгий.odp"

PALETTE = {"123B3A", "E4572E", "F7F3EA"}
REQUIRED = [
    "Итоговые выводы",
    "Дорожная карта",
    "когнитивный диссонанс",
    "10 проверенных сценариев",
    "12 правил",
    "Сентябрь — ноябрь 2026",
    "Спасибо за внимание",
]
FORBIDDEN = [
    "Следующие шаги",
    "Источники",
    "Тест с 10 учениками",
    "Дал ученикам",
    "проверить понятность заданий на одноклассниках",
    "выводы по её проверке",
    "участников — целевые",
]

NS = {
    "draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
    "presentation": "urn:oasis:names:tc:opendocument:xmlns:presentation:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}


def check_pptx() -> None:
    prs = Presentation(PPTX)
    print("PPTX SLIDES:", len(prs.slides))

    fonts = set()
    colors = set()
    texts = []
    notes = 0

    for slide in prs.slides:
        if slide.has_notes_slide and "".join(slide.notes_slide.notes_text_frame.text.split()):
            notes += 1
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    if run.font.name:
                        fonts.add(run.font.name)
                    try:
                        colors.add(str(run.font.color.rgb))
                    except (AttributeError, ValueError):
                        pass
                    if run.text.strip():
                        texts.append(run.text.strip())

    joined = "\n".join(texts)
    print("PPTX FONTS:", sorted(fonts))
    print("PPTX COLORS:", sorted(colors))
    print("PPTX NOTES WITH TEXT:", notes)
    print("PPTX FONT OK:", fonts == {"Arial"})
    print("PPTX COLORS OK:", colors <= PALETTE)

    for phrase in REQUIRED:
        print(f"required: {phrase} -> {phrase in joined}")
    for phrase in FORBIDDEN:
        print(f"forbidden: {phrase} -> {phrase in joined}")


def check_odp() -> None:
    with zipfile.ZipFile(ODP) as archive:
        content = archive.read("content.xml").decode("utf-8")

    root = ET.fromstring(content)
    pages = root.findall(".//draw:page", NS)
    print("\nODP SLIDES:", len(pages))
    print("ODP FONTS:", sorted(set(re.findall(r'style:font-name="([^"]+)"', content))))
    print(
        "ODP COLORS:",
        sorted(set(re.findall(r'fo:color="(#[0-9A-Fa-f]+)"', content))),
    )

    note_text = []
    for notes in root.findall(".//presentation:notes", NS):
        value = "".join(notes.itertext()).strip()
        if value:
            note_text.append(value)

    visible_text = "\n".join("".join(page.itertext()) for page in pages)
    print("ODP NOTES WITH TEXT:", len(note_text))
    print("ODP PAGE-NUMBER FIELDS:", len(root.findall(".//text:page-number", NS)))
    print("ODP FONT OK:", "Calibri" not in content)
    print(
        "ODP COLORS OK:",
        set(re.findall(r'fo:color="(#[0-9A-Fa-f]+)"', content)) <= {"#123b3a", "#e4572e", "#f7f3ea"},
    )

    for phrase in REQUIRED:
        print(f"required: {phrase} -> {phrase in visible_text}")
    for phrase in FORBIDDEN:
        print(f"forbidden: {phrase} -> {phrase in visible_text}")


def main() -> None:
    check_pptx()
    check_odp()


if __name__ == "__main__":
    main()
