from os import getenv
import dotenv

dotenv.load_dotenv(override=True)


TELEGRAM_BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')

CLIENT_SECRET_FILE_NAME = getenv('CLIENT_SECRET_FILE_NAME')