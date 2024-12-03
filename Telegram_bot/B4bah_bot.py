import os
import logging
import json
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import ollama

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Путь к файлу для сохранения истории
HISTORY_FILE = "chat_history.json"

# Глобальная переменная для хранения сессий
user_sessions = {}

# Максимальная длина истории чата для каждого пользователя
MAX_HISTORY_LENGTH = 50


# Функция для загрузки токена из файла
def load_token_from_path():
    token_file_path = input("Введите путь к файлу с токеном:\n>>> ").strip()
    if not os.path.exists(token_file_path):
        logging.error(f"Файл с токеном по пути {token_file_path} не найден.")
        raise FileNotFoundError(f"Файл {token_file_path} не существует. Проверьте путь и повторите попытку.")
    with open(token_file_path, "r", encoding="utf-8") as f:
        token = f.read().strip()
    if not token:
        logging.error("Файл с токеном пуст.")
        raise ValueError("Файл с токеном пуст.")
    logging.info("Токен успешно загружен из файла.")
    return token


# Функция для загрузки истории из файла
def load_history():
    global user_sessions
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            user_sessions = json.load(f)
        logging.info("История чатов загружена.")
    else:
        logging.info("Файл истории не найден. Начало новой истории.")


# Функция для сохранения истории в файл
def save_history():
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(user_sessions, f, ensure_ascii=False, indent=4)
        logging.info("История чатов сохранена.")
    except Exception as e:
        logging.error(f"Ошибка при сохранении истории: {e}")


# Ограничение длины истории
def trim_history(user_id):
    if len(user_sessions[user_id]) > MAX_HISTORY_LENGTH:
        user_sessions[user_id] = user_sessions[user_id][-MAX_HISTORY_LENGTH:]
        logging.info(f"История пользователя {user_id} обрезана до последних {MAX_HISTORY_LENGTH} сообщений.")


# Функция для запуска Ollama
def start_ollama():
    try:
        # Проверяем, запущен ли процесс Ollama
        output = os.popen('tasklist').read()  # Получаем список процессов
        if "ollama.exe" in output:
            logging.info("Ollama уже запущена.")
            return True

        # Если процесс не найден, запускаем его
        logging.info("Запуск Ollama...")
        os.system('start /B ollama run llama3.2-vision:latest')  # Запуск команды
        time.sleep(5)  # Ждем 5 секунд, чтобы дать время на запуск
        logging.info("Ollama успешно запущена.")
        return True
    except Exception as e:
        logging.error(f"Ошибка при запуске Ollama: {e}")
        return False


# Функция для запроса к Ollama
def get_ollama_response(user_id):
    try:
        # Отправка всей истории в Ollama для генерации ответа
        response = ollama.chat(model="llama3.2-vision:latest", messages=user_sessions[user_id])
        response_content = response["message"]["content"]
        return response_content
    except Exception as e:
        logging.error(f"Ошибка при запросе к Ollama: {e}")
        return "Извините, произошла ошибка при обработке запроса."


# Обработка сообщений пользователей
async def handle_message(update: Update, context):
    user_id = str(update.effective_user.id)  # Преобразуем ID пользователя в строку для JSON

    # Инициализация сессии для нового пользователя
    if user_id not in user_sessions:
        user_sessions[user_id] = [
            {'role': 'system', 'content': 'Отвечай максимально кратко и по делу.'}
        ]

    # Добавление нового сообщения пользователя в историю
    user_sessions[user_id].append({'role': 'user', 'content': update.message.text})

    # Ограничение длины истории
    trim_history(user_id)

    # Получение ответа от Ollama
    response_content = get_ollama_response(user_id)

    # Добавление ответа от Ollama в историю
    user_sessions[user_id].append({'role': 'assistant', 'content': response_content})

    # Ограничение длины истории после добавления ответа
    trim_history(user_id)

    # Сохранение обновленной истории
    save_history()

    # Отправка ответа пользователю
    await update.message.reply_text(response_content)


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


# Главная функция
def main():
    # Загрузка токена
    token = load_token_from_path()

    # Загрузка истории перед запуском бота
    load_history()

    # Запуск Ollama перед запуском бота
    if not start_ollama():
        logging.error("Не удалось запустить Ollama. Завершение работы.")
        return

    # Создание приложения Telegram
    app = ApplicationBuilder().token(token).build()

    # Регистрация команд и обработчиков
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Запуск бота
    logging.info("Запуск Telegram-бота...")
    app.run_polling()


if __name__ == '__main__':
    main()
