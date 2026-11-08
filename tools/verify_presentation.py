import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ODP = ROOT / "АнтиСхема_презентация_Посысаев_Иван_Шульга_Георгий.odp"
NS = {
    "draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
}

with zipfile.ZipFile(ODP) as archive:
    content = archive.read("content.xml").decode("utf-8")

root = ET.fromstring(content)
pages = root.findall(".//draw:page", NS)
all_text = "\n".join("".join(page.itertext()) for page in pages)

print("SLIDES:", len(pages))
for index, page in enumerate(pages, 1):
    texts = []
    for element in page.iter():
        if element.tag.split("}")[1] in ("p", "h"):
            value = "".join(element.itertext()).strip()
            if value:
                texts.append(value)
    print(f"\n--- SLIDE {index} ---")
    print(" | ".join(texts[:5]))

print("\nCHECKS")
for bad in (
    "Тест с 10 учениками",
    "Следующие шаги",
    "Дал ученикам пройти",
    "проверить понятность заданий на одноклассниках",
    "выводы по её проверке",
    "участников — целевые",
):
    print(("BAD FOUND: " if bad in all_text else "ok absent: ") + bad)

for label, needle in (
    ("author", "Шульга Георгий"),
    ("audience", "Целевая аудитория"),
    ("principle", "Принцип работы"),
    ("availability", "Доступность"),
):
    print(f"{label}: {needle in all_text}")
