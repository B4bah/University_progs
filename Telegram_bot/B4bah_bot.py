import os
import logging
import json
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import ollama

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Path to the file for saving chat history
HISTORY_FILE = "chat_history.json"

# Global variable for storing user sessions
user_sessions = {}

# Maximum length of chat history for each user
MAX_HISTORY_LENGTH = 50


# Function to load the token from a file
def load_token_from_path():
    token_file_path = input("Enter the path to the token file: ").strip()
    if not os.path.exists(token_file_path):
        logging.error(f"Token file not found at {token_file_path}.")
        raise FileNotFoundError(f"The file {token_file_path} does not exist. Please check the path and try again.")
    with open(token_file_path, "r", encoding="utf-8") as f:
        token = f.read().strip()
    if not token:
        logging.error("Token file is empty.")
        raise ValueError("The token file is empty.")
    logging.info("Token successfully loaded from the file.")
    return token


# Function to load chat history from a file
def load_history():
    global user_sessions
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            user_sessions = json.load(f)
        logging.info("Chat history loaded.")
    else:
        logging.info("History file not found. Starting a new history.")


# Function to save chat history to a file
def save_history():
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(user_sessions, f, ensure_ascii=False, indent=4)
        logging.info("Chat history saved.")
    except Exception as e:
        logging.error(f"Error saving chat history: {e}")


# Limit the length of chat history
def trim_history(user_id):
    if len(user_sessions[user_id]) > MAX_HISTORY_LENGTH:
        user_sessions[user_id] = user_sessions[user_id][-MAX_HISTORY_LENGTH:]
        logging.info(f"User {user_id}'s history trimmed to the last {MAX_HISTORY_LENGTH} messages.")


# Function to start Ollama
def start_ollama():
    try:
        # Check if the Ollama process is already running
        output = os.popen('tasklist').read()  # Get a list of processes
        if "ollama.exe" in output:
            logging.info("Ollama is already running.")
            return True

        # If the process is not found, start it
        logging.info("Starting Ollama...")
        os.system('start /B ollama run llama3.2-vision:latest')  # Run the command
        time.sleep(5)  # Wait for 5 seconds to allow it to start
        logging.info("Ollama successfully started.")
        return True
    except Exception as e:
        logging.error(f"Error starting Ollama: {e}")
        return False


# Function to query Ollama for a response
def get_ollama_response(user_id):
    try:
        # Send the entire chat history to Ollama to generate a response
        response = ollama.chat(model="llama3.2-vision:latest", messages=user_sessions[user_id])
        response_content = response["message"]["content"]
        return response_content
    except Exception as e:
        logging.error(f"Error querying Ollama: {e}")
        return "Sorry, an error occurred while processing your request."


# Handle user messages
async def handle_message(update: Update, context):
    user_id = str(update.effective_user.id)  # Convert user ID to a string for JSON

    # Initialize session for a new user
    if user_id not in user_sessions:
        user_sessions[user_id] = [
            {'role': 'system', 'content': 'Respond as briefly and to the point as possible.'}
        ]

    # Add the user's new message to the history
    user_sessions[user_id].append({'role': 'user', 'content': update.message.text})

    # Limit the history length
    trim_history(user_id)

    # Get a response from Ollama
    response_content = get_ollama_response(user_id)

    # Add Ollama's response to the history
    user_sessions[user_id].append({'role': 'assistant', 'content': response_content})

    # Limit the history length after adding the response
    trim_history(user_id)

    # Save the updated history
    save_history()

    # Send the response back to the user
    await update.message.reply_text(response_content)


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


# Main function
def main():
    # Load the token
    token = load_token_from_path()

    # Load history before starting the bot
    load_history()

    # Start Ollama before starting the bot
    if not start_ollama():
        logging.error("Failed to start Ollama. Exiting.")
        return

    # Create the Telegram bot application
    app = ApplicationBuilder().token(token).build()

    # Register commands and handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Start the bot
    logging.info("Starting Telegram bot...")
    app.run_polling()


if __name__ == '__main__':
    main()
