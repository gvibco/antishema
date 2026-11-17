"""Собрать презентацию «АнтиСхема» с нуля.

Палитра: три цвета, один шрифт Arial.
Запуск: py tools/build_presentation.py
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "АнтиСхема_презентация_Посысаев_Иван_Шульга_Георгий.pptx"

BG = RGBColor(0xF7, 0xF3, 0xEA)
INK = RGBColor(0x12, 0x3B, 0x3A)
ACCENT = RGBColor(0xE4, 0x57, 0x2E)
FONT = "Arial"

W = 13.333
H = 7.5
MARGIN = 0.8


def set_run(run, size=16, color=INK, bold=False):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color


def text_box(
    slide,
    left,
    top,
    width,
    height,
    text,
    size=16,
    color=INK,
    bold=False,
    align=PP_ALIGN.LEFT,
    anchor=MSO_ANCHOR.TOP,
    line_spacing=1.08,
    space_after=0,
):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    frame = box.text_frame
    frame.word_wrap = True
    frame.auto_size = None
    frame.margin_left = 0
    frame.margin_right = 0
    frame.margin_top = 0
    frame.margin_bottom = 0
    frame.vertical_anchor = anchor

    for index, line in enumerate(str(text).split("\n")):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.alignment = align
        paragraph.line_spacing = line_spacing
        paragraph.space_after = Pt(space_after)
        run = paragraph.add_run()
        run.text = line
        set_run(run, size, color, bold)

    return box


def rect(
    slide,
    left,
    top,
    width,
    height,
    fill=None,
    line=None,
    line_width=1.0,
    rounded=False,
    radius=0.12,
):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(
        shape_type, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.shadow.inherit = False

    if rounded:
        try:
            shape.adjustments[0] = radius
        except (IndexError, ValueError):
            pass

    if fill is None:
        shape.fill.background()
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill

    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(line_width)

    return shape


def line(slide, x1, y1, x2, y2, color=INK, width=1.0):
    connector = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2)
    )
    connector.line.color.rgb = color
    connector.line.width = Pt(width)
    return connector


def circle(slide, left, top, size, fill, line_color=None):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(left), Inches(top), Inches(size), Inches(size)
    )
    shape.shadow.inherit = False
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line_color is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(1)
    return shape


def new_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide.background.fill
    background.solid()
    background.fore_color.rgb = BG
    return slide


def slide_title(slide, title, top=0.55, size=32):
    text_box(slide, MARGIN, top, 11.7, 0.7, title, size=size, bold=True)
    rect(slide, MARGIN, top + 0.78, 0.55, 0.06, fill=ACCENT)


def footer(slide, text):
    text_box(slide, MARGIN, 6.95, 11.7, 0.3, text, size=9.5, color=INK)


def build():
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    prs.core_properties.title = "АнтиСхема — интерактивный веб-тренажёр против интернет-мошенничества"
    prs.core_properties.author = "Посысаев Иван Сергеевич, Шульга Георгий"
    prs.core_properties.subject = "Учебный проект, 10 «И» класс, Школа № 2127"

    # ---------------------------------------------------------------- 1. Титул
    slide = new_slide(prs)
    rect(slide, 0.0, 0.0, 0.18, H, fill=ACCENT)
    text_box(
        slide,
        1.05,
        0.75,
        11.0,
        0.5,
        "Государственное бюджетное образовательное учреждение города Москвы «Школа № 2127»",
        size=12,
    )
    text_box(
        slide,
        1.05,
        2.05,
        10.8,
        2.2,
        "Интерактивный веб-тренажёр\nпротив интернет-мошенничества",
        size=44,
        bold=True,
        line_spacing=0.98,
    )
    rect(slide, 1.05, 4.35, 1.1, 0.08, fill=ACCENT)
    text_box(
        slide,
        1.05,
        4.62,
        8.5,
        0.5,
        "АнтиСхема · учебный проект 10 «И» класса",
        size=18,
        color=ACCENT,
        bold=True,
    )
    text_box(
        slide,
        1.05,
        5.55,
        11.0,
        0.5,
        "Авторы: Посысаев Иван Сергеевич и Шульга Георгий, ученики 10 «И» класса",
        size=13,
        bold=True,
    )
    text_box(
        slide,
        1.05,
        5.98,
        11.2,
        0.5,
        "Руководители: Пальчикова Ирина Анатольевна, Шишкова Ирина Борисовна, Чаплоуская Любовь Геннадьевна",
        size=11.5,
    )
    text_box(slide, 1.05, 6.55, 4.0, 0.4, "Москва · 2026", size=11.5)

    # ------------------------------------------------------------ 2. Актуальность
    slide = new_slide(prs)
    slide_title(slide, "Актуальность")
    text_box(
        slide,
        MARGIN,
        1.65,
        8.1,
        1.9,
        "Мошенник требует решить всё сразу: пугает потерей денег, обещает выгоду или просит код из СМС.",
        size=24,
        bold=True,
        line_spacing=1.08,
    )
    text_box(
        slide,
        MARGIN,
        3.72,
        7.5,
        1.25,
        "У подростков такие ситуации начинаются с обычного сообщения в мессенджере или предложения «лёгкого заработка».",
        size=16,
        line_spacing=1.2,
    )
    rect(slide, MARGIN, 5.18, 7.9, 1.18, fill=ACCENT)
    text_box(
        slide,
        MARGIN + 0.3,
        5.35,
        7.3,
        0.85,
        "Нужен способ потренироваться до реального столкновения с обманом.",
        size=19,
        color=BG,
        bold=True,
        line_spacing=1.05,
        anchor=MSO_ANCHOR.MIDDLE,
    )

    line(slide, 9.55, 1.6, 9.55, 5.95, color=INK, width=1.0)
    triggers = [
        ("01", "Страх", "потерять деньги или аккаунт"),
        ("02", "Выгода", "приз, подработка, «лёгкие» деньги"),
        ("03", "Спешка", "решение нужно принять прямо сейчас"),
    ]
    for index, (number, name, note) in enumerate(triggers):
        y = 1.7 + index * 1.45
        text_box(slide, 9.95, y, 0.7, 0.3, number, size=12, color=ACCENT, bold=True)
        text_box(slide, 9.95, y + 0.28, 2.6, 0.45, name, size=24, bold=True)
        text_box(slide, 9.95, y + 0.8, 2.6, 0.5, note, size=11.5, line_spacing=1.1)

    # ------------------------------------------- 3. Проблема и выводы анализа
    slide = new_slide(prs)
    slide_title(slide, "Проблема и выводы анализа")
    columns = [
        ("01", "Советы полезны, но их сложно применить под давлением и в спешке."),
        ("02", "Одна и та же уловка выглядит по-разному: «друг», «банк», «подработка»."),
        ("03", "На ошибках учатся лучше, если сразу получить понятное объяснение."),
    ]
    col_width = 3.68
    for index, (number, text) in enumerate(columns):
        x = MARGIN + index * (col_width + 0.33)
        rect(slide, x, 1.62, col_width, 0.05, fill=ACCENT)
        text_box(slide, x, 1.85, 1.0, 0.5, number, size=26, color=ACCENT, bold=True)
        text_box(slide, x, 2.5, col_width, 1.9, text, size=15.5, line_spacing=1.25)

    rect(slide, MARGIN, 5.12, 11.7, 1.35, fill=INK)
    text_box(
        slide,
        MARGIN + 0.32,
        5.28,
        11.1,
        1.05,
        "Проблема: школьнику не хватает безопасной практики принятия решений в подозрительном диалоге.",
        size=20,
        color=BG,
        bold=True,
        line_spacing=1.1,
        anchor=MSO_ANCHOR.MIDDLE,
    )

    # ------------------------------------- 4. Аудитория + психологическое обоснование
    slide = new_slide(prs)
    slide_title(slide, "Целевая аудитория")
    text_box(slide, MARGIN, 1.55, 5.0, 0.3, "КТО УЧАСТВУЕТ", size=12, color=ACCENT, bold=True)
    text_box(
        slide,
        MARGIN,
        1.95,
        5.0,
        1.35,
        "Школьники 8–11 классов, которые активно общаются онлайн и пользуются цифровыми сервисами.",
        size=16,
        line_spacing=1.2,
    )
    text_box(slide, 6.55, 1.55, 5.9, 0.3, "ПОЧЕМУ ИМ ЭТО НУЖНО", size=12, color=ACCENT, bold=True)
    text_box(
        slide,
        6.55,
        1.95,
        5.9,
        1.35,
        "Подростки получают сообщения от незнакомцев, предложения «лёгкого заработка» и просьбы сообщить код.",
        size=16,
        line_spacing=1.2,
    )

    rect(slide, MARGIN, 3.62, 11.7, 2.35, fill=INK)
    rect(slide, MARGIN + 0.32, 3.88, 0.12, 0.12, fill=ACCENT)
    text_box(
        slide,
        MARGIN + 0.55,
        3.82,
        11.0,
        0.3,
        "ПСИХОЛОГИЧЕСКОЕ ОБОСНОВАНИЕ",
        size=12,
        color=BG,
        bold=True,
    )
    text_box(
        slide,
        MARGIN + 0.32,
        4.22,
        11.0,
        1.15,
        "После неверного выбора возникает когнитивный диссонанс — расхождение между «со мной такое не случится» и «я попался». Мгновенный разбор снимает это напряжение и закрепляет безопасное действие.",
        size=15,
        color=BG,
        line_spacing=1.28,
    )
    text_box(
        slide,
        MARGIN + 0.32,
        5.42,
        11.0,
        0.4,
        "Поэтому разбор появляется сразу после выбора, а не в конце теста.",
        size=13,
        color=BG,
        bold=True,
    )
    text_box(
        slide,
        MARGIN,
        6.32,
        11.7,
        0.35,
        "14–17 лет · основной формат — телефон · первый запуск без регистрации",
        size=11,
    )

    # -------------------------------------------------------- 5. Принцип работы
    slide = new_slide(prs)
    slide_title(slide, "Принцип работы")
    steps = [
        ("1", "Ситуация", "Сообщение от «банка», «друга» или «работодателя»."),
        ("2", "Выбор", "Два варианта ответа — как в реальном чате."),
        ("3", "Разбор", "Сразу видно, где была ловушка."),
        ("4", "Правило", "Короткий вывод, который остаётся в памяти."),
    ]
    step_width = 2.7
    gap = 0.3
    line(slide, 1.3, 2.4, 12.0, 2.4, color=INK, width=1.0)
    for index, (number, name, note) in enumerate(steps):
        x = MARGIN + index * (step_width + gap)
        circle(slide, x + 0.5, 2.12, 0.56, ACCENT)
        text_box(
            slide,
            x + 0.5,
            2.19,
            0.56,
            0.35,
            number,
            size=14,
            color=BG,
            bold=True,
            align=PP_ALIGN.CENTER,
        )
        text_box(slide, x, 2.95, step_width, 0.45, name, size=19, bold=True)
        text_box(slide, x, 3.42, step_width, 1.0, note, size=12.5, line_spacing=1.2)

    text_box(slide, MARGIN, 4.75, 2.0, 0.3, "ФОРМАТ", size=12, color=ACCENT, bold=True)
    text_box(
        slide,
        MARGIN,
        5.1,
        11.4,
        0.85,
        "Короткие задания по 1–2 минуты: диалог с выбором ответа и «распознай мошенничество».",
        size=18,
        bold=True,
        line_spacing=1.1,
    )
    text_box(
        slide,
        MARGIN,
        6.15,
        11.4,
        0.4,
        "Можно пройти на телефоне за несколько минут. Регистрация для первого запуска не нужна.",
        size=11.5,
    )

    # ---------------------------------------------------------- 6. Пример задания
    slide = new_slide(prs)
    slide_title(slide, "Пример задания")
    text_box(slide, MARGIN, 1.55, 6.2, 0.3, "В ЧАТЕ ПИШЕТ НЕИЗВЕСТНЫЙ:", size=12, color=ACCENT, bold=True)
    rect(slide, MARGIN, 1.98, 6.4, 2.05, fill=INK, rounded=True, radius=0.06)
    text_box(
        slide,
        MARGIN + 0.33,
        2.22,
        5.75,
        1.6,
        "«Я из поддержки. Чтобы защитить аккаунт, срочно пришли код из СМС»",
        size=23,
        color=BG,
        bold=True,
        line_spacing=1.08,
    )
    text_box(
        slide,
        MARGIN,
        4.32,
        6.4,
        0.4,
        "Так выглядит типичная уловка: давление, страх и просьба о коде.",
        size=11.5,
    )

    text_box(slide, 7.75, 1.55, 4.7, 0.3, "ВАРИАНТЫ ОТВЕТА", size=12, color=ACCENT, bold=True)
    rect(slide, 7.75, 1.98, 4.75, 0.82, fill=None, line=INK, line_width=1.0, rounded=True, radius=0.1)
    text_box(
        slide,
        8.0,
        2.18,
        4.3,
        0.45,
        "А  Отправить код, чтобы аккаунт не заблокировали",
        size=12.5,
        line_spacing=1.1,
    )
    rect(slide, 7.75, 2.98, 4.75, 0.98, fill=ACCENT, rounded=True, radius=0.1)
    text_box(
        slide,
        8.0,
        3.15,
        4.3,
        0.65,
        "Б  Не отправлять код и открыть сервис самостоятельно",
        size=12.5,
        color=BG,
        bold=True,
        line_spacing=1.1,
    )
    text_box(slide, 7.75, 4.12, 4.75, 0.3, "Верный ответ", size=10.5, color=ACCENT, bold=True)
    text_box(
        slide,
        7.75,
        4.75,
        4.75,
        1.2,
        "После выбора: почему это безопасно или где была ошибка.",
        size=15,
        line_spacing=1.2,
    )

    # --------------------------------------------------------- 7. Цель и задачи
    slide = new_slide(prs)
    slide_title(slide, "Цель и задачи проекта")
    text_box(slide, MARGIN, 1.55, 2.0, 0.3, "ЦЕЛЬ", size=12, color=ACCENT, bold=True)
    text_box(
        slide,
        MARGIN,
        1.95,
        11.2,
        1.55,
        "Создать веб-тренажёр, который помогает школьникам распознавать признаки мошенничества и выбирать безопасное действие.",
        size=24,
        bold=True,
        line_spacing=1.08,
    )
    line(slide, MARGIN, 3.72, 12.5, 3.72, color=INK, width=0.75)
    text_box(slide, MARGIN, 3.95, 2.0, 0.3, "ЗАДАЧИ", size=12, color=ACCENT, bold=True)
    tasks = [
        ("1", "Собрать и проверить", "типичные схемы по надёжным источникам."),
        ("2", "Написать сценарии", "с вариантами ответа и объяснениями."),
        ("3", "Сделать сайт", "с понятными заданиями и разбором каждого ответа."),
    ]
    task_width = 3.68
    for index, (number, name, note) in enumerate(tasks):
        x = MARGIN + index * (task_width + 0.33)
        text_box(slide, x, 4.42, 0.5, 0.45, number, size=24, color=ACCENT, bold=True)
        text_box(slide, x + 0.52, 4.44, task_width - 0.52, 0.55, name, size=15, bold=True)
        text_box(slide, x + 0.52, 4.98, task_width - 0.52, 1.0, note, size=12.5, line_spacing=1.2)

    # ---------------------------------------------------- 8. Дорожная карта (Гантт)
    slide = new_slide(prs)
    slide_title(slide, "Дорожная карта")
    text_box(slide, MARGIN, 1.48, 5.0, 0.35, "Сентябрь — ноябрь 2026", size=13, color=ACCENT, bold=True)

    timeline_x = 3.7
    timeline_width = 8.8
    week_width = timeline_width / 12
    header_y = 1.95
    header_h = 0.46

    months = [("Сентябрь", 0, 4), ("Октябрь", 4, 8), ("Ноябрь", 8, 12)]
    for name, start, end in months:
        x = timeline_x + start * week_width
        width = (end - start) * week_width
        rect(slide, x, header_y, width, header_h, fill=INK)
        text_box(
            slide,
            x,
            header_y + 0.1,
            width,
            0.3,
            name,
            size=12,
            color=BG,
            bold=True,
            align=PP_ALIGN.CENTER,
        )

    for week in range(13):
        x = timeline_x + week * week_width
        line(slide, x, header_y + header_h, x, 6.05, color=INK, width=0.4)
    line(slide, timeline_x, header_y + header_h, timeline_x + timeline_width, header_y + header_h, color=INK, width=0.9)

    rows = [
        ("Исследование схем", 0, 3, "1–3 нед.", INK, INK),
        ("Сценарии и разбор", 2, 6, "3–6 нед.", INK, INK),
        ("Сайт и механика", 5, 10, "6–10 нед.", INK, INK),
        ("Подготовка к защите", 9, 12, "10–12 нед.", ACCENT, ACCENT),
    ]
    row_top = 2.78
    row_gap = 0.78
    for index, (name, start, end, label, bar_color, label_color) in enumerate(rows):
        y = row_top + index * row_gap
        text_box(slide, MARGIN, y + 0.02, 2.75, 0.4, name, size=13.5, bold=True, color=label_color)
        x = timeline_x + start * week_width
        width = (end - start) * week_width
        rect(slide, x, y + 0.02, width, 0.4, fill=bar_color, rounded=True, radius=0.18)
        text_box(
            slide,
            x,
            y + 0.08,
            width,
            0.26,
            label,
            size=9.5,
            color=BG,
            bold=True,
            align=PP_ALIGN.CENTER,
        )

    text_box(
        slide,
        MARGIN,
        6.22,
        11.5,
        0.4,
        "Итог: рабочая демонстрационная версия сайта.",
        size=14,
        bold=True,
    )

    # --------------------------------------------------- 9. Планируемые результаты
    slide = new_slide(prs)
    slide_title(slide, "Планируемые результаты")
    results = [
        ("Рабочий прототип", "Веб-сайт с двумя типами заданий: диалог и «распознай мошенничество»."),
        ("Содержание", "10 проверенных сценариев и 12 правил с объяснением каждого ответа."),
        ("Доступность", "Сайт открывается на телефоне и компьютере, регистрация не нужна."),
    ]
    for index, (name, text) in enumerate(results):
        y = 1.65 + index * 1.5
        text_box(slide, MARGIN, y, 2.9, 0.35, name.upper(), size=12, color=ACCENT, bold=True)
        text_box(slide, 3.85, y - 0.05, 8.5, 1.0, text, size=18, line_spacing=1.18)
        if index < len(results) - 1:
            line(slide, MARGIN, y + 1.18, 12.5, y + 1.18, color=INK, width=0.6)

    # ------------------------------------------------------ 10. Сравнение с аналогами
    slide = new_slide(prs)
    slide_title(slide, "Сравнение с аналогами")
    text_box(
        slide,
        MARGIN,
        1.45,
        11.4,
        0.75,
        "У существующих проектов можно взять проверенные темы. Наш акцент — короткий диалог и объяснение каждого выбора.",
        size=14.5,
        line_spacing=1.2,
    )

    columns = [
        ("Критерий", 2.2),
        ("Финкульт «Грабли»", 2.75),
        ("Финзачёт Банка России", 3.05),
        ("АнтиСхема", 3.7),
    ]
    table_left = MARGIN
    table_top = 2.35
    header_h = 0.55
    row_h = 0.82
    x = table_left
    for index, (name, width) in enumerate(columns):
        fill = ACCENT if index == len(columns) - 1 else INK
        rect(slide, x, table_top, width, header_h, fill=fill)
        text_box(
            slide,
            x + 0.12,
            table_top + 0.12,
            width - 0.24,
            0.35,
            name,
            size=11,
            color=BG,
            bold=True,
            line_spacing=1.0,
        )
        x += width

    body = [
        ["Основной формат", "Истории и советы", "Онлайн-задания", "Диалог с выбором ответа"],
        ["Тематика", "Разные схемы обмана", "Широкая финграмотность", "Мошенничество в общении"],
        ["Для школьника", "Материал для чтения", "Проверка знаний", "Короткая практика + разбор"],
    ]
    for row_index, values in enumerate(body):
        y = table_top + header_h + row_index * row_h
        x = table_left
        for col_index, (_, width) in enumerate(columns):
            rect(
                slide,
                x,
                y,
                width,
                row_h,
                fill=BG,
                line=INK,
                line_width=0.75,
            )
            text_box(
                slide,
                x + 0.12,
                y + 0.13,
                width - 0.24,
                row_h - 0.2,
                values[col_index],
                size=11.5,
                bold=col_index == 0 or col_index == 3,
                line_spacing=1.05,
            )
            x += width

    text_box(
        slide,
        MARGIN,
        5.55,
        11.4,
        0.55,
        "Сравнение показывает предполагаемую нишу проекта, а не превосходство над существующими ресурсами.",
        size=11,
        line_spacing=1.2,
    )

    # --------------------------------------------------------- 11. Итоговые выводы
    slide = new_slide(prs)
    slide_title(slide, "Итоговые выводы")
    conclusions = [
        ("1", "Проблема решена практически", "У школьника есть безопасная среда, где можно ошибиться и сразу понять, как действовать."),
        ("2", "Тренажёр учит действию", "Не пересказу правил, а выбору в конкретном диалоге — с разбором каждого ответа."),
        ("3", "Проект готов к использованию", "10 сценариев, два формата заданий и отдельная страница из 12 правил."),
    ]
    for index, (number, name, text) in enumerate(conclusions):
        y = 1.65 + index * 1.42
        text_box(slide, MARGIN, y - 0.05, 0.7, 0.6, number, size=30, color=ACCENT, bold=True)
        text_box(slide, 1.55, y, 10.8, 0.4, name, size=19, bold=True)
        text_box(slide, 1.55, y + 0.42, 10.8, 0.65, text, size=14, line_spacing=1.2)
        if index < len(conclusions) - 1:
            line(slide, MARGIN, y + 1.15, 12.5, y + 1.15, color=INK, width=0.6)

    text_box(slide, MARGIN, 6.25, 11.5, 0.5, "Спасибо за внимание", size=20, color=ACCENT, bold=True)

    # ---------------------------------------------------------------- save
    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"written: {OUT}")
    print(f"slides: {len(prs.slides)}")


if __name__ == "__main__":
    build()
