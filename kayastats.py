# -*- coding: utf-8 -*-
# KayaAI
import socketserver
from http.server import BaseHTTPRequestHandler
import time
from telegram import Bot
from telegram.error import TelegramError
# KayaAI
# Get Telegram Bot API token, chat ID and server information from the usertelegram_token = input("Enter the Telegram Bot API Token: ")
telegram_token = input("Enter the Telegram Bot API Token: ")
chat_id = input("Enter the Telegram Chat ID: ")
host = input("Enter the server address (for example, localhost): ")
port = int(input("Enter the server port (for example, 8000): "))

# Get the DDoS attack detection threshold from the user (for example, 160 MB, 2 GB, 1024 KB, 8192 bytes) 
ddos_threshold_input = input("Enter the DDoS attack detection threshold (for example, 160MB, 2GB, 1024KB, 8192 bytes, etc.): ")
ddos_threshold_input = ddos_threshold_input.strip().lower()

ddos_threshold = 0  # DDoS threshold is initially set to 0 in bytes 

# Convert threshold value in bytes correctly
if ddos_threshold_input.endswith("bytes"):
    ddos_threshold = int(ddos_threshold_input.replace("bytes", "").strip())
elif ddos_threshold_input.endswith("kb"):
    ddos_threshold = int(ddos_threshold_input.replace("kb", "").strip()) * 1024  # Convert KB to byte
elif ddos_threshold_input.endswith("mb"):
    ddos_threshold = float(ddos_threshold_input.replace("mb", "").strip()) * 1024 * 1024  # Convert MB to bytes
elif ddos_threshold_input.endswith("gb"):
    ddos_threshold = float(ddos_threshold_input.replace("gb", "").strip()) * 1024 * 1024 * 1024  # Converting GB to bytes
else:
    print("Invalid DDoS attack detection threshold. Please enter in bytes, KB, MB, or GB.")
    exit(1)
# KayaAI
class MyRequestHandler(BaseHTTPRequestHandler):
    total_bytes = 0  # Total bytes

    def do_GET(self):
        content_length = int(self.headers.get('Content-Length', 0))
        request_ip = self.client_address[0]
        
        print(f"Incoming Request {self.path}")
        print(f"Sender IP: {request_ip}")
        print(f"Request Size: {content_length} bytes")
        print("-" * 30)

        # DDoS attack detection
        if content_length > ddos_threshold:
            message = f"DDoS attack detected!\nSender IP: {request_ip}\nRequest Size: {content_length} bytes"
            send_notification(message)

def send_notification(message):
    try:
        bot = Bot(token=telegram_token)
        bot.send_message(chat_id=chat_id, text=message)
        print("Telegram notification sent.")
    except TelegramError as e:
        print(f"Telegram notification sending error: {e}")
        print("The process is being halted.")
        exit(1)

# Server initialization
with socketserver.TCPServer((host, port), MyRequestHandler) as httpd:
    print(f"The server is running at {host}:{port}")

    # Listening for requests to the server in an infinite loop
    # KayaAI
    while True:
        try:
            httpd.handle_request()
        except KeyboardInterrupt:
            print("The server has been shut down.")
            break
