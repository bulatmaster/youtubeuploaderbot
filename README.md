Установка и запуск:

ШАГ 1  ( эти шаги должны быть более жирным шрифтом, но я не знаю как его сделать )
установить необходимые библиотеки 
pip install -r requirements.txt


ШАГ 2
Получить файл авторизации в Гугл консоли:


1. Создание проекта в Google Cloud Console

    Перейдите на Google Cloud Console.
    Войдите с помощью учетной записи Google.
    Нажмите на значок меню в верхнем левом углу и выберите "Select a project" → "New Project".
    Укажите название проекта и выберите организацию (или оставьте поле пустым).
    Нажмите "Create".

2. Включение нужных API

    После создания проекта выберите его в верхнем меню.
    Перейдите в раздел "APIs & Services" → "Library".
    Найдите и включите API, которые вы хотите использовать, например:
        Google Drive API
        Google Sheets API

3. Создание учетных данных

    Перейдите в "APIs & Services" → "Credentials".
    Нажмите кнопку "Create Credentials" и выберите "OAuth client ID".
    Если появляется уведомление об отсутствии экрана согласия, выполните его настройку:
        Перейдите в "OAuth consent screen".
        Выберите External и нажмите "Create".
        Заполните обязательные поля, такие как название приложения.
        Нажмите "Save and Continue", оставив настройки по умолчанию.
    Вернитесь в раздел "Credentials", снова нажмите "Create Credentials", и выберите "OAuth client ID".
    Выберите тип приложения "Desktop app" и нажмите "Create".

4. Загрузка client_secret.json

    После создания OAuth client ID, появится окно с информацией о созданных учетных данных.
    Нажмите "Download JSON".
    Файл будет называться client_secret_<some_id>.json.

    Загрузите файл в корень проекта 


ШАГ 3 
Создайте файл .env , пропишите в него необходимые настройки согласно config.py файлу, например:

TELEGRAM_BOT_TOKEN='токен_телеграм_бота'

CLIENT_SECRET_FILE_NAME='client_secret_123456-abcdefg.json'


ШАГ 4
Запуск:
python main.py

