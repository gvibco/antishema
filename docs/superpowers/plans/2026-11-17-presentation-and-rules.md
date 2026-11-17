# АнтиСхема — презентация и страница правил: план

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.
> Steps use checkbox (`- [ ]`) syntax.

**Goal:** Пересобрать презентацию в 11 слайдов с палитрой из трёх цветов и
диаграммой Ганта, расширить сайт до 10 сценариев и добавить страницу правил.

**Architecture:** Презентация собирается скриптом `tools/build_presentation.py`
на python-pptx, конвертируется в ODP/PDF через LibreOffice, PNG-превью — через
PyMuPDF. Сайт остаётся статическим: сценарии в `js/scenarios.js`, новая
страница `rules.html`, стили в общем `css/styles.css`.

**Tech Stack:** Python 3.15, python-pptx, LibreOffice, PyMuPDF, Node.js test
runner, чистые HTML/CSS/JS.

## Global Constraints

- Один шрифт презентации: Arial.
- Три цвета презентации: `#F7F3EA`, `#123B3A`, `#E4572E`.
- Без номеров слайдов и без заметок докладчика.
- Сайт работает без сборки и внешних зависимостей.
- Все сценарии вымышленные, с одним правильным ответом.

---

### Task 1: Расширить набор сценариев до 10

**Files:**
- Modify: `js/scenarios.js`
- Modify: `tests/scenarios.test.js`

**Interfaces:**
- Produces: массив `SCENARIOS` из 10 объектов; типы `dialog` и `recognize`.
- `validateScenarios` продолжает возвращать пустой массив.

- [ ] **Step 1: Добавить тест на 10 сценариев**

В `tests/scenarios.test.js` заменить проверку «не меньше пяти» на:

```js
test('в наборе десять сценариев', () => {
  assert.equal(scenarios.length, 10);
});
```

- [ ] **Step 2: Запустить тест — должен упасть**

Run: `node --test tests/scenarios.test.js`
Expected: FAIL, `actual: 6, expected: 10`.

- [ ] **Step 3: Добавить четыре сценария**

В конец массива `SCENARIOS` в `js/scenarios.js` добавить:

```js
{
  id: 'delivery-code',
  type: 'dialog',
  tag: 'Доставка',
  difficulty: 'Средне',
  title: 'Код для посылки',
  subtitle: 'Сообщение от «службы доставки»',
  messages: [
    { from: 'them', name: 'Доставка', text: 'Ваша посылка ждёт на складе. Подтвердите новый адрес.' },
    { from: 'them', name: 'Доставка', text: 'Назовите код из СМС, иначе вернём посылку отправителю.' },
  ],
  choices: [
    { id: 'send-code', text: 'Назвать код из СМС', correct: false },
    { id: 'open-app', text: 'Открыть приложение доставки и проверить заказ', correct: true },
  ],
  explanation:
    'Код из СМС подтверждает вход или платёж, а не доставку. Настоящая служба не просит код в чате. Проверь заказ по трек-номеру в официальном приложении или на сайте.',
  redFlag: 'Просят код из СМС ради посылки',
  rule: 'Код из СМС не подтверждает доставку.',
},
{
  id: 'vote-link',
  type: 'dialog',
  tag: 'Мессенджер',
  difficulty: 'Средне',
  title: 'Проголосуй за меня',
  subtitle: 'Ссылка от знакомого аккаунта',
  messages: [
    { from: 'them', name: 'Лиза', text: 'Привет! Участвую в конкурсе, помоги набрать голоса.' },
    { from: 'them', name: 'Лиза', text: 'Перейди по ссылке и войди через свой аккаунт, иначе голос не засчитают.' },
  ],
  choices: [
    { id: 'open-link', text: 'Перейти и войти в аккаунт', correct: false },
    { id: 'check-friend', text: 'Не вводить пароль: позвонить Лизе и проверить', correct: true },
  ],
  explanation:
    'Голосование не требует пароля от аккаунта. Ссылка может вести на копию сайта, которая крадёт логин. Проверь конкурс на официальной странице и позвони знакомому.',
  redFlag: 'Просят войти по ссылке ради голоса',
  rule: 'Голосование не требует пароля от аккаунта.',
},
{
  id: 'game-skins',
  type: 'recognize',
  tag: 'Распознавание',
  difficulty: 'Легко',
  title: 'Бесплатные скины',
  subtitle: 'Сообщение от «поддержки игры»',
  sender: 'Поддержка игры',
  message:
    'Поздравляем! Вы выиграли набор скинов. Для выдачи напишите логин и пароль от аккаунта.',
  choices: [
    { id: 'safe', text: 'Безопасно', correct: false },
    { id: 'fraud', text: 'Похоже на мошенничество', correct: true },
  ],
  explanation:
    'Настоящая поддержка никогда не спрашивает пароль. Такой «приз» нужен только для угона аккаунта. Не отправляй данные и проверь акцию внутри игры.',
  redFlag: 'Просят пароль от игры',
  rule: 'Пароль и код не нужны даже «поддержке».',
},
{
  id: 'test-reminder',
  type: 'recognize',
  tag: 'Распознавание',
  difficulty: 'Легко',
  title: 'Напоминание о контрольной',
  subtitle: 'Сообщение из классного чата',
  sender: 'Классный руководитель',
  message:
    'Ребята, завтра контрольная по геометрии. Повторите формулы площади и возьмите линейки.',
  choices: [
    { id: 'safe', text: 'Безопасно', correct: true },
    { id: 'fraud', text: 'Похоже на мошенничество', correct: false },
  ],
  explanation:
    'В сообщении нет просьбы о деньгах, кодах или ссылке. Отправитель знаком, тема обычная. Это безопасное сообщение.',
  redFlag: 'Признаков обмана нет',
  rule: 'Нет просьбы о данных или деньгах — нет повода паниковать.',
},
```

- [ ] **Step 4: Запустить тесты**

Run: `node --test tests/engine.test.js tests/scenarios.test.js`
Expected: PASS, 0 failures.

- [ ] **Step 5: Commit**

```bash
git add js/scenarios.js tests/scenarios.test.js
git commit -m "feat: add four anti-fraud scenarios"
```

---

### Task 2: Страница правил и навигация

**Files:**
- Create: `rules.html`
- Modify: `css/styles.css`
- Modify: `index.html`
- Modify: `trainer.html`
- Modify: `js/trainer.js`
- Modify: `tests/scenarios.test.js` (проверка страницы правил)

**Interfaces:**
- Produces: `rules.html` с 12 элементами `.rule-card` и блоком
  `.emergency-panel`.
- Навигация на всех страницах содержит ссылку `rules.html`.

- [ ] **Step 1: Создать `rules.html`**

Структура: шапка как в `index.html`, hero «Правила защиты от мошенников»,
якорные ссылки на четыре категории, четыре секции по три правила, блок
«Красные флаги», блок «Если уже обманули», подвал. Каждое правило —
`<article class="rule-card">` с номером, заголовком и текстом.

- [ ] **Step 2: Добавить стили**

В `css/styles.css` добавить классы `.rules-hero`, `.rules-toc`, `.rule-grid`,
`.rule-card`, `.rule-number`, `.rules-note`, `.emergency-panel`,
`.emergency-steps`, `.flags-strip`. Сетка 3 колонки на компьютере, 2 на
планшете, 1 на телефоне.

- [ ] **Step 3: Обновить навигацию и счётчики**

- В `index.html` и `trainer.html` добавить `<a href="rules.html">Правила</a>`.
- Заменить «6 сценариев» на «10 сценариев», «6 коротких ситуаций» на
  «10 коротких ситуаций», «6 заданий» на «10 заданий».
- В `js/trainer.js` заменить `6 заданий · без регистрации` на
  `10 заданий · без регистрации`.
- В блоке `#flags` на главной добавить ссылку «Все 12 правил →».

- [ ] **Step 4: Добавить тест страницы правил**

В `tests/scenarios.test.js`:

```js
const fs = require('node:fs');
const path = require('node:path');

test('страница правил содержит 12 правил', () => {
  const html = fs.readFileSync(path.join(__dirname, '..', 'rules.html'), 'utf8');
  assert.equal((html.match(/class="rule-card"/g) || []).length, 12);
  assert.ok(html.includes('Если уже обманули'));
});
```

- [ ] **Step 5: Запустить тесты**

Run: `node --test tests/engine.test.js tests/scenarios.test.js`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add rules.html css/styles.css index.html trainer.html js/trainer.js tests/scenarios.test.js
git commit -m "feat: add dedicated scam protection rules page"
```

---

### Task 3: Пересобрать презентацию

**Files:**
- Create: `tools/build_presentation.py`
- Delete: `tools/edit_presentation.py`
- Modify: `tools/verify_presentation.py`

**Interfaces:**
- Produces: `.pptx`, `.odp`, PDF и PNG-превью.
- `verify_presentation.py` проверяет 11 слайдов, отсутствие номеров и заметок,
  наличие «Итоговые выводы» и «Диаграмма Ганта».

- [ ] **Step 1: Написать сборщик**

`tools/build_presentation.py` создаёт 11 слайдов 13.333×7.5 дюйма:
титул, актуальность, проблема, аудитория + диссонанс, принцип, пример,
цель и задачи, Гантт, результаты, сравнение, итоговые выводы.
Все тексты — Arial, палитра из трёх цветов. Диаграмма Ганта — прямоугольники
по 12 неделям, подписи месяцев «Сентябрь», «Октябрь», «Ноябрь».

- [ ] **Step 2: Собрать PPTX, ODP, PDF**

```powershell
py tools/build_presentation.py
& "C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to odp --outdir . "АнтиСхема_презентация_Посысаев_Иван_Шульга_Георгий.pptx"
& "C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to pdf --outdir docs/presentation "АнтиСхема_презентация_Посысаев_Иван_Шульга_Георгий.pptx"
py tools/render_presentation.py
```

- [ ] **Step 3: Проверить презентацию**

```powershell
py tools/verify_presentation.py
```

Expected: `SLIDES: 11`, все проверки `ok`, нет `BAD FOUND`.

- [ ] **Step 4: Визуально проверить PNG**

Открыть `docs/presentation/slides/slide-01.png` … `slide-11.png`, убедиться,
что нет обрезанного текста, наложений и лишних цветов.

- [ ] **Step 5: Commit**

```bash
git add tools/build_presentation.py tools/verify_presentation.py docs/presentation
git add "АнтиСхема_презентация_Посысаев_Иван_Шульга_Георгий.pptx" "АнтиСхема_презентация_Посысаев_Иван_Шульга_Георгий.odp"
git commit -m "feat: rebuild presentation with gantt chart and final conclusions"
```

---

### Task 4: Документация и финальная проверка

**Files:**
- Modify: `README.md`
- Modify: `docs/superpowers/specs/2026-11-17-presentation-and-rules-design.md` (если нужно)

- [ ] **Step 1: Обновить README**

10 сценариев, страница `rules.html`, 12 правил, новый файл презентации,
палитра и состав слайдов.

- [ ] **Step 2: Финальные тесты**

```powershell
node --test tests/engine.test.js tests/scenarios.test.js
py tools/verify_presentation.py
```

Expected: все тесты PASS, презентация 11 слайдов.

- [ ] **Step 3: Скриншоты**

Открыть сайт через локальный сервер, сделать скриншоты главной, тренажёра и
страницы правил (компьютер и телефон).

- [ ] **Step 4: Commit**

```bash
git add README.md docs
git commit -m "docs: update project structure and presentation details"
```
