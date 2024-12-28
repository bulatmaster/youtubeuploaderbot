import logging
import os
import pickle

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

import config 


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def authenticate():
    # Задаем область доступа (Scope) для YouTube Data API
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    creds = None

    # Проверяем, существует ли уже сохраненный токен
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Если токен отсутствует или недействителен, запускаем процесс авторизации
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Настраиваем процесс авторизации
            flow = InstalledAppFlow.from_client_secrets_file(
                config.CLIENT_SECRET_FILE_NAME, SCOPES)
            creds = flow.run_local_server(port=0)  # Открывает браузер для авторизации

        # Сохраняем токен в файл для будущего использования
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


# Загрузка видео на YouTube
def upload_to_youtube(file_path, title="Uploaded by Telegram Bot", description=""):
    creds = None

    # Загружаем токен, если он есть
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Проверяем, что токен валиден, и обновляем его при необходимости
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("Не удалось загрузить учетные данные. Проверьте файл токена.")

    # Создаем сервис YouTube API
    youtube = build('youtube', 'v3', credentials=creds)

    # Подготовка данных для загрузки
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['Telegram', 'Bot'],
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'public'  # Можно выбрать: 'private', 'unlisted', 'public'
        }
    }

    # Загружаем видео
    media = MediaFileUpload(file_path, mimetype='video/*', resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()

    return f"https://youtu.be/{response['id']}"


# Команда старт с кнопкой "Поехали!"
async def start_with_button(update: Update, context):
    keyboard = [[InlineKeyboardButton("Поехали!", callback_data='go')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Готов загрузить видео?", reply_markup=reply_markup)


# Обработка нажатия кнопки "Поехали!"
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()  # Подтверждаем обработку

    if query.data == 'go':
        await query.edit_message_text("Отлично! Пришли мне видео, и я загружу его на YouTube.")


# Обработка видео
async def handle_video(update: Update, context):
    file = await update.message.video.get_file()
    file_path = f"video_{update.message.video.file_id}.mp4"
    await file.download_to_drive(file_path)

    try:
        await update.message.reply_text("Загружаю видео на YouTube...")
        youtube_link = upload_to_youtube(file_path, title="Видео от Telegram бота")
        await update.message.reply_text(f"Видео загружено! Вот ссылка: {youtube_link}")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")
    finally:
        os.remove(file_path)


# Основной код
def main():
    TOKEN = config.TELEGRAM_BOT_TOKEN

    # Создание приложения
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start_with_button))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    authenticate()
    print("Авторизация успешна! Токен сохранен.")
    main()
