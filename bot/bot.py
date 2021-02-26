"""file for control bot and his specification"""
from telebot import TeleBot
from time import sleep
from y_parser.parser import Parser
from bot.token import API_token, password


class Bot:
    """control bot"""

    SUCCESS_USERS_ID = []

    def __init__(self):
        self.__bot = TeleBot(API_token)
        self.__parser = Parser()

        @self.__bot.message_handler(commands=["help"])
        def __show_help(message):
            """show info about bot through /help command"""
            if message.from_user.id in self.SUCCESS_USERS_ID:
                self.__bot.send_message(
                    message.chat.id,
                    "Bot for getting info about science videos on Youtube. For start work write /parse.",
                )
            else:
                self.__bot.send_message(
                    message.chat.id,
                    "Bot for getting info about science videos on Youtube. For more info, auth through /start.",
                )

        @self.__bot.message_handler(commands=["start"])
        def __start_work(message):
            """start interaction with user and check his status"""
            if message.from_user.id in self.SUCCESS_USERS_ID:
                self.__bot.send_message(message.chat.id, "Access is allowed!")
            else:
                message_from_user = self.__bot.reply_to(message, """Entry password: """)
                self.__bot.register_next_step_handler(message_from_user, __auth_to_bot)

        def __auth_to_bot(message):
            """checks the password for correctness"""
            if message.text == password:
                self.__bot.send_message(
                    message.chat.id, "Access is allowed! Choose command."
                )
                self.SUCCESS_USERS_ID.append(message.from_user.id)
            else:
                self.__bot.send_message(
                    message.chat.id, "Access denied! Try again /start."
                )

        @self.__bot.message_handler(commands=["parse"])
        def __parsing(message):
            """start parsing and show result"""
            if message.from_user.id in self.SUCCESS_USERS_ID:
                self.__bot.send_message(
                    message.chat.id, "Parsing start. Please, await!"
                )

                info_about_videos = self.__get_info_about_videos()

                for info_about_video in info_about_videos:
                    self.__bot.send_message(
                        message.chat.id, f"Title: {info_about_video['title']}"
                    )
                    self.__bot.send_message(
                        message.chat.id, f"Views: {info_about_video['views']}"
                    )
                    self.__bot.send_message(
                        message.chat.id, f"Date: {info_about_video['date']}"
                    )
                    self.__bot.send_message(
                        message.chat.id, f"Like_bar: {info_about_video['like_bar']}"
                    )
                    self.__bot.send_message(
                        message.chat.id, f"Channel: {info_about_video['channel']}"
                    )
                    self.__bot.send_message(
                        message.chat.id, f"Link: {info_about_video['link']}"
                    )
                    self.__bot.send_message(message.chat.id, "-" * 10)
                    sleep(3)

            else:
                self.__bot.send_message(
                    message.chat.id, "Access denied! Try again /start."
                )

    def __get_info_about_videos(self):
        """return parsing result"""
        return self.__parser.start_parse()

    def start_bot(self):
        """start bot working"""
        self.__bot.polling()
