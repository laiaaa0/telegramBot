import telepot
import time
from setup import token, admin_id, valid_ids
import functions.ip as ip
import functions.quotes as quotes
import functions.camera as camera
import functions.webstreaming as streaming
import sys
import logging
from datetime import datetime
import os
# following this tutorial
# https://www.instructables.com/id/Set-up-Telegram-Bot-on-Raspberry-Pi/


class Handler():
    def __init__(self):
        self.bot = telepot.Bot(token)
        self.cam = camera.CameraController()
        self.bot.message_loop(self.handle)
        self.stream = streaming.PiStreamer()

    def command_from_text(self, text):
        args_list = text.split()
        if len(args_list) < 1:
            return ""
        return args_list[0]

    def rest_of_message(self, text):
        args_list = text.split()
        if len(args_list) < 2:
            return ""
        return " ".join(args_list[1:])

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != 'text':
            self.bot.sendMessage(chat_id, "This is not a command!")
            return
        chat_id = msg['chat']['id']
        chat_text = msg['text']
        command = self.command_from_text(chat_text)
        print('Got command %s' % command)
        print('From ID ', chat_id)
        if command == '/ip':
            self.bot.sendMessage(chat_id, ip.get_ip_information())
        elif command == '/quote':
            self.bot.sendMessage(chat_id, quotes.get_random_quote())
        elif command == '/request':
            self.bot.sendMessage(
                chat_id,
                "Thanks for submitting a feature request. The admin has been notified")
            self.bot.sendMessage(
                admin_id,
                "New request submitted : " +
                self.rest_of_message(chat_text))
        elif command == '/on':
            if chat_id in valid_ids:
                self.stream.start()
                external_ip = ip.get_external_ip()
                response = f"Stream started in http://{external_ip}:8000/index.html"
                self.bot.sendMessage(chat_id, response)

        elif command == '/off':
            if chat_id in valid_ids:
                self.stream.stop()
                self.stream.join()

        elif command == '/camera':
            filename = "output" + datetime.now().strftime("%Y%m%d_%H%M%S")
            self.bot.sendMessage(chat_id, "Getting camera frames...")
            if self.cam.record_until_detect_movement(filename):
                if os.path.exists(filename + ".gif"):
                    self.bot.sendVideo(
                        admin_id, video=open(
                            filename + ".gif", 'rb'))
                    try:
                        os.remove(filename + ".gif")
                    except BaseException as e:
                        logging.error("Failed to remove file")
            else:
                self.bot.sendMessage(
                    chat_id, "Could not get frames from the camera")


if __name__ == "__main__":
    h = Handler()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("telegram_bot.log")
        ]
    )

    while True:
        time.sleep(10)
