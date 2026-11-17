"""Привести ODP к одному шрифту и трём цветам после конвертации LibreOffice."""

from pathlib import Path
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ODP = ROOT / "АнтиСхема_презентация_Посысаев_Иван_Шульга_Георгий.odp"
BUILD = Path(r"C:\Users\zoras\AppData\Local\Temp\opencode\odp_normalize")


def normalize_xml(text: str) -> str:
    text = text.replace("Calibri", "Arial")
    text = re.sub(r"#ffffff", "#f7f3ea", text, flags=re.IGNORECASE)
    return text


def main() -> None:
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)

    with zipfile.ZipFile(ODP) as archive:
        archive.extractall(BUILD)

    for name in ("content.xml", "styles.xml"):
        path = BUILD / name
        if not path.exists():
            continue
        path.write_text(normalize_xml(path.read_text(encoding="utf-8")), encoding="utf-8")

    ODP.unlink()
    with zipfile.ZipFile(ODP, "w") as archive:
        archive.write(BUILD / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for path in sorted(BUILD.rglob("*")):
            if not path.is_file() or path.name == "mimetype":
                continue
            archive.write(
                path,
                path.relative_to(BUILD).as_posix(),
                compress_type=zipfile.ZIP_DEFLATED,
            )

    print(f"normalized: {ODP}")


if __name__ == "__main__":
    main()
