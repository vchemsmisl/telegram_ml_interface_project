import telebot
from src.constants import (
	BOT_TOKEN,
    DATA_PATH,
    SUPPORTED_DATASET_TYPES,
    AVAILABLE_MODELS,
    AVAILABLE_TASK_TYPES
)
from telebot import types
import requests
import wget
import re

#эти переменные будут в конфиге, который мы будем создавать в поле класса бота
task_type = None
test_proportion = None
models = None
timeout = None

bot = telebot.TeleBot(BOT_TOKEN)

# @bot.message_handler(content_types=['text'])
# def start_working_poll(message):
#     chat_id = message.chat.id
#
#     if message.text in ['/start', '/help']:
#         keyboard = types.InlineKeyboardMarkup()
#         key = types.InlineKeyboardButton(text='Start working', callback_data='any')
#         keyboard.add(key)
#
#         bot.send_message(chat_id, text=messages.STARTING_MESSAGE_TRUE, reply_markup=keyboard)
#     else:
#         bot.send_message(chat_id, messages.STARTING_MESSAGE_FALSE)
#
#
# @bot.callback_query_handler(func=lambda call: call.data == 'any')
# def ask_for_dataset_poll(call):
#     bot.send_message(call.message.chat.id, messages.ASKING_FOR_DATASET_MESSAGE)
#
# @bot.message_handler(content_types=['document'])
# def get_dataset_and_ask_for_task_type_poll(message):
#
#     while True:
#         doc_type = message.document.file_name.split('.')[-1]
#
#         if doc_type in SUPPORTED_DATASET_TYPES:
#             break
#         else:
#             bot.send_message(message.chat.id, messages.WRONG_FILE_TYPE_MESSAGE)
#             bot.register_next_step_handler(message, get_dataset_and_ask_for_task_type_poll)
#             break
#
#     file_info = bot.get_file(message.document.file_id)
#     file_url = requests.get(
#         f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}'
#     ).url
#
#     if not DATA_PATH.exists():
#         DATA_PATH.mkdir(parents=True)
#     wget.download(file_url, out=DATA_PATH.absolute().as_posix() + f'/data_for_training.{doc_type}')
#
#     keyboard = types.InlineKeyboardMarkup()
#     key_reg = types.InlineKeyboardButton(text='Regression', callback_data='reg')
#     key_bin_classif = types.InlineKeyboardButton(text='Binary classification', callback_data='binary')
#     key_multiclass_classif = types.InlineKeyboardButton(text='Multiclass classification', callback_data='multiclass')
#     key_multiple_reg = types.InlineKeyboardButton(text='Multiple regression', callback_data='multi:reg')
#     key_multilable_classif = types.InlineKeyboardButton(text='Multiclass classification', callback_data='multilabel')
#
#     keyboard.add(key_reg)
#     keyboard.add(key_bin_classif)
#     keyboard.add(key_multiclass_classif)
#     keyboard.add(key_multiple_reg)
#     keyboard.add(key_multilable_classif)
#
#     bot.send_message(message.chat.id, text=messages.ASKING_FOR_TASK_TYPE_MESSAGE, reply_markup=keyboard)
#
# @bot.callback_query_handler(func=lambda call: call.data in AVAILABLE_TASK_TYPES)
# def ask_for_test_set_proportion_poll(call):
#     global task_type # убрать при реализации в классе
#     task_type = call.data
#     bot.send_message(call.message.chat.id, messages.ASKING_FOR_TEST_PROPORTION_MESSAGE)
#
#     bot.register_next_step_handler(call.message, get_test_proportion_and_ask_for_models_list_poll)
#
# def get_test_proportion_and_ask_for_models_list_poll(message):
#
#     while True:
#         test_proportion_input = message.text
#
#         if re.fullmatch(r'\d+\.\d+', test_proportion_input) and 0 <= float(test_proportion_input) <= 1:
#             break
#         else:
#             bot.send_message(message.chat.id, messages.WRONG_TEST_PROPORTION_MESSAGE)
#             bot.register_next_step_handler(message, get_test_proportion_and_ask_for_models_list_poll)
#             return
#
#     global test_proportion # убрать при реализации в классе
#     test_proportion = float(test_proportion_input)
#
#     bot.send_message(message.chat.id, messages.ASKING_FOR_MODELS_MESSAGE)
#
#     bot.register_next_step_handler(message, get_models_names_and_ask_for_timeout_poll)
#
# def get_models_names_and_ask_for_timeout_poll(message):
#     models_input = message.text.split(', ')
#
#     while True:
#         for model_name in models_input:
#             if model_name in AVAILABLE_MODELS:
#                 continue
#             else:
#                 bot.send_message(message.chat.id, messages.WRONG_MODEL_NAME_MESSAGE)
#                 bot.register_next_step_handler(message, get_models_names_and_ask_for_timeout_poll)
#                 return
#         break
#
#     global models # убрать при реализации в классе
#     models = models_input
#
#     bot.send_message(message.chat.id, messages.ASKING_FOR_TIMEOUT_MESSAGE)
#
#     bot.register_next_step_handler(message, get_timeout_and_start_training_poll)
#
# def get_timeout_and_start_training_poll(message):
#
#     while True:
#         timeout_input = message.text
#
#         if timeout_input.isnumeric() and 0 < int(timeout_input):
#             break
#         else:
#             bot.send_message(message.chat.id, messages.WRONG_TIMEOUT_MESSAGE)
#             bot.register_next_step_handler(message, get_timeout_and_start_training_poll)
#             return
#
#     global timeout
#     timeout = float(timeout_input)
#
#     bot.send_message(message.chat.id, messages.MODEL_TRAINING_START_MESSAGE)

chat_id = None

def send_random_message(bot):

    @bot.message_handler(func=lambda message: message == '/stop')
    def random_message(message):
        bot.send_message(message.from_user.id, 'test message')
        global chat_id
        chat_id = message.from_user.id
        bot.polling()
        bot.stop_polling()

        # send(bot, chat_id)

def send(bot, chat_id):
    bot.polling()
    pdf_doc = open('Исаков Данила Андреевич_резюме.pdf', 'rb')
    bot.send_document(chat_id, pdf_doc)


send_random_message(bot)
send(bot, chat_id)