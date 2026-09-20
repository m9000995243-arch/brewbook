# Как запустить BrewBook на компьютере и собрать APK для телефона

Инструкция с нуля. Выбирайте свой путь:

- **A. Запуск на компьютере** (Windows / macOS / Linux) — 5 минут.
- **B. Сборка APK через GitHub Actions** — телефон получает APK, на компьютере
  ничего собирать не нужно. **Самый простой способ для Windows.**
- **C. Сборка APK локально** (Linux или Windows+WSL) — 1–2 часа в первый раз.
- **D. Быстрая проверка на телефоне без сборки** (Kivy Launcher / Pydroid).
- **E. iOS** — отдельно, нужен Mac.

---

## 0. Что скачать и куда положить

1. Скачайте архив `brewbook.zip` и распакуйте.
2. Положите папку по пути **без пробелов, кириллицы и длинных имён**:
   - Windows: `C:\dev\brewbook`
   - macOS/Linux: `~/dev/brewbook`
3. Внутри должны лежать `main.py`, `buildozer.spec`, папка `app/`.
   Если вместо этого внутри ещё одна папка `brewbook` — поднимите содержимое
   на уровень выше. `main.py` обязан лежать рядом с `buildozer.spec`.

Проверка структуры:

```
C:\dev\brewbook\
    main.py
    buildozer.spec
    requirements.txt
    README.md
    app\...
```

---

## A. Запуск на компьютере

### A1. Установить Python

- **Windows:** скачайте Python **3.11** или **3.12** с python.org.
  При установке обязательно поставьте галочку **«Add python.exe to PATH»**.
- **macOS:** `brew install python@3.12`
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt update
  sudo apt install -y python3 python3-venv python3-pip
  ```

Проверка — откройте терминал (Windows: `Win+R` → `cmd` → Enter):

```bash
python --version        # Windows
python3 --version       # macOS/Linux
```

Должно показать 3.11.x или 3.12.x.

### A2. Перейти в папку проекта

```bash
cd C:\dev\brewbook          # Windows
cd ~/dev/brewbook           # macOS/Linux
```

### A3. Создать виртуальное окружение и поставить зависимости

**Windows:**
```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

После `activate` в начале строки терминала появится `(.venv)` — значит всё верно.

> На Linux для звука и окна может потребоваться:
> `sudo apt install -y libgl1 libmtdev1 libsdl2-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0`

### A4. Запустить

```bash
python main.py
```

Откроется окно 420×860 (вертикальный «телефонный» формат).
**Esc** работает как кнопка «Назад».

### A5. Если что-то не так

| Симптом | Что делать |
|---|---|
| `python: command not found` | Python не в PATH. Переустановите с галочкой «Add to PATH» или используйте `py -3.12` |
| `ModuleNotFoundError: kivy` | Не активировано окружение. Выполните `activate` ещё раз |
| Окно открылось и сразу закрылось | Запускайте из терминала, а не двойным кликом — увидите текст ошибки |
| Чёрное окно / артефакты | `set KIVY_GL_BACKEND=angle_sdl2` (Windows) перед запуском |
| Не видно рецептов | Проверьте, что существует `app/data/recipes.json` |

Файл базы (избранное, заметки, свои рецепты) создаётся автоматически:
- Windows: `C:\Users\<вы>\AppData\Roaming\brewbook\brewbook.db`
- macOS: `~/Library/Application Support/brewbook/`
- Linux: `~/.config/brewbook/`

Удалите этот файл, чтобы сбросить приложение к заводскому состоянию.

---

## B. Сборка APK через GitHub Actions (рекомендую для Windows)

Собирать APK можно только на Linux. GitHub бесплатно даёт вам Linux-машину:
вы загружаете код, через ~30–40 минут скачиваете готовый APK. На своём
компьютере ставить ничего не нужно.

### B1. Завести репозиторий

1. Зарегистрируйтесь на github.com.
2. Нажмите **New repository**, имя `brewbook`, тип **Private**, кнопка
   **Create repository**.

### B2. Загрузить файлы

Проще всего — через браузер:
на странице репозитория **Add file → Upload files**, перетащите содержимое
папки `brewbook` (именно содержимое: `main.py`, `buildozer.spec`, папка `app`,
папка `.github`), внизу нажмите **Commit changes**.

> Внимание: браузер иногда не грузит папки, начинающиеся с точки. Если папка
> `.github` не загрузилась — создайте файл вручную: **Add file → Create new
> file**, в имени введите `.github/workflows/build-apk.yml` и вставьте туда
> содержимое одноимённого файла из архива.

Через git (если установлен):
```bash
cd C:\dev\brewbook
git init
git add .
git commit -m "BrewBook"
git branch -M main
git remote add origin https://github.com/ВАШ_ЛОГИН/brewbook.git
git push -u origin main
```

### B3. Запустить сборку

1. Вкладка **Actions** в репозитории.
2. Если просит — нажмите **I understand my workflows, go ahead and enable them**.
3. Слева выберите **Build Android APK** → справа **Run workflow** → зелёная
   кнопка **Run workflow**.
4. Сборка идёт 25–45 минут (первый раз дольше: качается Android SDK/NDK).

### B4. Скачать APK

Откройте завершившийся запуск → внизу блок **Artifacts** → **brewbook-apk** →
скачается zip, внутри файл вида `brewbook-1.0.0-arm64-v8a_armeabi-v7a-debug.apk`.

### B5. Установить на телефон

1. Перекиньте APK на телефон (кабель, Telegram «Избранное», Google Drive).
2. Откройте файл в проводнике телефона.
3. Android спросит про «Установка неизвестных приложений» — разрешите для
   проводника/браузера, через который открываете.
4. Установить → Открыть.

Если Play Protect ругается — «Всё равно установить»: приложение просто не
подписано сертификатом из магазина.

---

## C. Сборка APK локально

### C1. Windows: сначала поставить WSL

Buildozer под Windows напрямую не работает. Нужен Linux внутри Windows:

1. Откройте **PowerShell от имени администратора**.
2. ```powershell
   wsl --install -d Ubuntu
   ```
3. Перезагрузите компьютер, дождитесь окна Ubuntu, придумайте логин и пароль.
4. Дальше все команды выполняйте **в окне Ubuntu**, а не в PowerShell.
5. Скопируйте проект внутрь Linux-файловой системы (не оставляйте в `/mnt/c` —
   сборка там медленная и ломается на правах доступа):
   ```bash
   mkdir -p ~/dev && cp -r /mnt/c/dev/brewbook ~/dev/ && cd ~/dev/brewbook
   ```

### C2. Системные зависимости (Ubuntu / WSL)

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-venv \
    autoconf automake libtool libtool-bin pkg-config zlib1g-dev \
    libncurses-dev libffi-dev libssl-dev cmake ccache ant
```

### C3. Установить Buildozer

```bash
cd ~/dev/brewbook
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install buildozer==1.5.0 cython==0.29.36
```

### C4. Собрать

```bash
buildozer android debug
```

Первый запуск скачивает ~3–4 ГБ (Android SDK, NDK, исходники Python) и идёт
40–90 минут. На вопрос о лицензии Android SDK отвечайте `y`.

Готовый файл: `bin/brewbook-1.0.0-arm64-v8a_armeabi-v7a-debug.apk`.

### C5. Поставить на телефон по кабелю

1. На телефоне: **Настройки → О телефоне** → 7 раз нажать «Номер сборки» →
   появится «Для разработчиков» → включить **Отладка по USB**.
2. Подключите кабелем, на телефоне разрешите отладку.
3. ```bash
   buildozer android debug deploy run logcat
   ```
   Приложение установится, запустится, и в терминал пойдут логи — по ним видно
   любую ошибку.

### C6. Типичные проблемы

| Ошибка | Решение |
|---|---|
| `Aidl not found` / SDK не качается | `buildozer android clean`, затем снова `buildozer android debug` |
| `libtinfo5` не ставится (Ubuntu 24.04) | Пакет больше не нужен, просто пропустите его |
| `JAVA_HOME is not set` | `export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64` |
| Сборка падает на `Cython` | Строго `cython==0.29.36`, новее ломает python-for-android |
| Приложение ставится, но сразу закрывается | `buildozer android debug deploy run logcat \| grep python` — увидите traceback |
| Очень долго / ошибки прав в WSL | Проект должен лежать в `~/dev/...`, а не в `/mnt/c/...` |

### C7. Релизная сборка (для раздачи другим)

```bash
buildozer android release
# подпись
keytool -genkey -v -keystore ~/brewbook.keystore -alias brewbook \
        -keyalg RSA -keysize 2048 -validity 10000
~/.buildozer/android/platform/android-sdk/build-tools/34.0.0/apksigner sign \
        --ks ~/brewbook.keystore bin/brewbook-1.0.0-release-unsigned.apk
```

---

## D. Быстрая проверка на телефоне без сборки

Если хочется просто посмотреть, как выглядит, не дожидаясь APK:

1. Установите **Pydroid 3** из Google Play.
2. В Pydroid: меню → **Pip** → установить `kivy`.
3. Скопируйте папку `brewbook` в память телефона, откройте `main.py`, запустите.

Это способ «посмотреть», а не полноценное приложение: не будет иконки на
рабочем столе, вибрации и системного «Поделиться».

---

## E. iOS

Нужен Mac с Xcode:

```bash
pip install kivy-ios
toolchain build python3 kivy
toolchain create BrewBook /путь/к/brewbook
open BrewBook-ios/BrewBook.xcodeproj
```

Дальше сборка и запуск из Xcode. Для установки на свой iPhone хватит
бесплатного Apple ID (приложение будет жить 7 дней), для App Store нужен
платный аккаунт разработчика.

---

## Что менять дальше

- **Добавить рецепт** — дописать объект в `app/data/recipes.json` (формат описан
  в README). На телефоне после этого нужна пересборка APK.
- **Версия приложения** — строка `version = 1.0.0` в `buildozer.spec`.
- **Иконка и заставка** — положите PNG в `assets/` и раскомментируйте строки
  `icon.filename` / `presplash.filename` в `buildozer.spec`.
- **Название на телефоне** — строка `title` в `buildozer.spec`.
