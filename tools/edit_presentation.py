from pathlib import Path
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(r"C:\Users\zoras\Downloads\АнтиСхема_презентация_Посысаев_Иван.odp")
BUILD = Path(r"C:\Users\zoras\AppData\Local\Temp\opencode\odp_build")
OUT = ROOT / "АнтиСхема_презентация_Посысаев_Иван_Шульга_Георгий.odp"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 occurrence, found {count}")
    return text.replace(old, new, 1)


def get_page(text: str, name: str) -> str:
    match = re.search(
        r'<draw:page\s[^>]*draw:name="%s".*?</draw:page>' % re.escape(name),
        text,
        re.S,
    )
    if not match:
        raise SystemExit(f"page {name} not found")
    return match.group(0)


def main() -> None:
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)

    with zipfile.ZipFile(SRC) as archive:
        archive.extractall(BUILD)

    content_path = BUILD / "content.xml"
    content = content_path.read_text(encoding="utf-8")
    original_pages = len(re.findall(r"<draw:page\s", content))
    if original_pages != 10:
        raise SystemExit(f"expected 10 pages, found {original_pages}")

    # --- Title slide: add the second author ---
    page1_old = get_page(content, "page1")
    page1 = replace_once(
        page1_old,
        "Автор: Посысаев Иван Сергеевич, ученик 10 «И» класса",
        "Авторы: Посысаев Иван Сергеевич и Шульга Георгий, ученики 10 «И» класса",
        "page1 authors",
    )
    page1 = replace_once(
        page1,
        "Название школы, автор и руководители указаны по данным автора проекта.",
        "Название школы, авторы и руководители указаны по данным авторов проекта.",
        "page1 note",
    )
    content = content.replace(page1_old, page1, 1)

    # --- Split the old page 4 into audience + how it works ---
    page4_old = get_page(content, "page4")
    page4 = replace_once(
        page4_old,
        "Для кого и как это работает",
        "Целевая аудитория",
        "page4 title",
    )
    page4 = replace_once(page4, "Основная аудитория", "Кто участвует", "page4 left heading")
    page4 = replace_once(
        page4,
        "Игровой цикл",
        "Почему им это нужно",
        "page4 right heading",
    )
    page4 = replace_once(
        page4,
        "Ситуация → выбор ответа → объяснение → короткий вывод для жизни",
        "Подростки получают сообщения от незнакомцев, предложения «лёгкого заработка» и просьбы сообщить код.",
        "page4 right body",
    )
    page4 = replace_once(
        page4,
        "Можно пройти на телефоне за несколько минут. Регистрация для первого запуска не нужна.",
        "Возраст 14–17 лет · основной формат — телефон · первый запуск без регистрации.",
        "page4 footer",
    )

    page4b = page4.replace('draw:name="page4"', 'draw:name="page4b"', 1)
    page4b = replace_once(page4b, "Целевая аудитория", "Принцип работы", "page4b title")
    page4b = replace_once(page4b, "Кто участвует", "Игровой цикл", "page4b left heading")
    page4b = replace_once(
        page4b,
        "Школьники 8–11 классов, которые активно общаются онлайн и пользуются цифровыми сервисами.",
        "Ситуация → выбор ответа → объяснение → короткий вывод для жизни",
        "page4b left body",
    )
    page4b = replace_once(page4b, "Почему им это нужно", "Формат", "page4b right heading")
    page4b = replace_once(
        page4b,
        "Подростки получают сообщения от незнакомцев, предложения «лёгкого заработка» и просьбы сообщить код.",
        "Короткие задания по 1–2 минуты: диалог с выбором ответа и «распознай мошенничество».",
        "page4b right body",
    )
    page4b = replace_once(
        page4b,
        "Возраст 14–17 лет · основной формат — телефон · первый запуск без регистрации.",
        "Можно пройти на телефоне за несколько минут. Регистрация для первого запуска не нужна.",
        "page4b footer",
    )
    page4b = replace_once(page4b, ">04</text:span>", ">05</text:span>", "page4b number")

    content = content.replace(page4_old, page4 + page4b, 1)

    # --- Renumber the following slides ---
    page5 = get_page(content, "page5")
    page5 = replace_once(page5, ">05</text:span>", ">06</text:span>", "page5 number")
    content = content.replace(get_page(content, "page5"), page5, 1)

    page6 = get_page(content, "page6")
    page6 = replace_once(page6, ">06</text:span>", ">07</text:span>", "page6 number")
    page6 = replace_once(
        page6,
        "Сделать сайт и проверить понятность заданий на одноклассниках.",
        "Сделать сайт с понятными заданиями и разбором каждого ответа.",
        "page6 task 3",
    )
    content = content.replace(get_page(content, "page6"), page6, 1)

    page7 = get_page(content, "page7")
    page7 = replace_once(
        page7,
        "Изучил схемы, выбрал аудиторию и 5–7 ситуаций.",
        "Изучили схемы, выбрали аудиторию и 5–7 ситуаций.",
        "page7 stage 1 body",
    )
    page7 = replace_once(
        page7,
        "Написал диалоги, ответы и разбор ошибок.",
        "Написали диалоги, ответы и разбор ошибок.",
        "page7 stage 2 body",
    )
    page7 = replace_once(
        page7,
        "Собрал страницы и механику выбора на сайте.",
        "Собрали страницы и механику выбора на сайте.",
        "page7 stage 3 body",
    )
    page7 = replace_once(page7, "Этап 4 · Проверка", "Этап 4 · Демонстрация", "page7 stage 4")
    page7 = replace_once(
        page7,
        "Дал ученикам пройти задания и исправить непонятные места.",
        "Подготовили сайт к показу и защите проекта.",
        "page7 stage 4 body",
    )
    page7 = replace_once(
        page7,
        "Итог: рабочая демонстрационная версия и выводы по её проверке.",
        "Итог: рабочая демонстрационная версия сайта.",
        "page7 result",
    )
    content = content.replace(get_page(content, "page7"), page7, 1)

    page8 = get_page(content, "page8")
    page8 = replace_once(
        page8,
        "Веб-сайт с двумя типами заданиями: диалог и «распознай мошенничество».",
        "Веб-сайт с двумя типами заданий: диалог и «распознай мошенничество».",
        "page8 typo",
    )
    page8 = replace_once(page8, "Проверка", "Доступность", "page8 heading")
    page8 = replace_once(
        page8,
        "Тест с 10 учениками: понятность заданий и доля верных ответов до и после разбора.",
        "Сайт открывается на телефоне и компьютере, регистрация не нужна.",
        "page8 testing body",
    )
    page8 = replace_once(
        page8,
        "Все результаты запланированы, а не достигнуты. Число сценариев и участников — целевые показатели автора.",
        "Все результаты запланированы, а не достигнуты. Число сценариев — целевой показатель авторов.",
        "page8 note",
    )
    content = content.replace(get_page(content, "page8"), page8, 1)

    # --- Remove the "Следующие шаги" slide ---
    page10 = get_page(content, "page10")
    content = content.replace(page10, "", 1)

    # --- Keep the slide number fields in sync with the new order ---
    counter = [0]

    def renumber(match: re.Match) -> str:
        counter[0] += 1
        block = match.group(0)
        return re.sub(
            r'draw:page-number="\d+"',
            f'draw:page-number="{counter[0]}"',
            block,
        )

    content = re.sub(r"<draw:page\s.*?</draw:page>", renumber, content, flags=re.S)

    pages = len(re.findall(r"<draw:page\s", content))
    if pages != 10:
        raise SystemExit(f"expected 10 pages after edit, found {pages}")

    ET.fromstring(content)
    content_path.write_text(content, encoding="utf-8")

    # --- Rebuild the ODP: mimetype first and uncompressed ---
    if OUT.exists():
        OUT.unlink()

    with zipfile.ZipFile(OUT, "w") as archive:
        archive.write(
            BUILD / "mimetype",
            "mimetype",
            compress_type=zipfile.ZIP_STORED,
        )
        for path in sorted(BUILD.rglob("*")):
            if not path.is_file() or path.name == "mimetype":
                continue
            relative = path.relative_to(BUILD).as_posix()
            archive.write(path, relative, compress_type=zipfile.ZIP_DEFLATED)

    print(f"written: {OUT}")
    print(f"slides: {pages}")


if __name__ == "__main__":
    main()
