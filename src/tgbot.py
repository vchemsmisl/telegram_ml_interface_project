import telebot

import messages
from src.facade import ModelTrainingFacade
from constants import (
	BOT_TOKEN,
    DATA_PATH,
    SUPPORTED_DATASET_TYPES,
    AVAILABLE_MODELS,
    AVAILABLE_TASK_TYPES,
)
from telebot import types
import requests
import wget
import re
import shutil

def singleton_class(cls):

	class_objects = {}
	def wrapper(*args, **kwargs):

		if cls not in class_objects:
			class_objects[cls] = cls(*args, **kwargs)
		return class_objects[cls]

	return wrapper


@singleton_class
class TgBot:

	def __init__(self, model_config):
		self.bot = telebot.TeleBot(BOT_TOKEN)
		self.model_config = model_config
		self.name = 'vchemsmisl_bot'
		self.chat_id = None

	def start_infinity_polling(self):
		self.bot.infinity_polling(skip_pending=True)

	def execute_model_training_bot_interface(self):

		@self.bot.message_handler(content_types=['text'])
		def start_working_poll(message):
			self.chat_id = message.chat.id

			if message.text in ['/start', '/help']:
				keyboard = types.InlineKeyboardMarkup()
				key = types.InlineKeyboardButton(text='Start working', callback_data='any')
				keyboard.add(key)

				self.bot.send_message(self.chat_id, text=messages.STARTING_MESSAGE_TRUE, reply_markup=keyboard)
			else:
				self.bot.send_message(self.chat_id, messages.STARTING_MESSAGE_FALSE)

		@self.bot.callback_query_handler(func=lambda call: call.data == 'any')
		def ask_for_dataset_poll(call):
			self.bot.send_message(self.chat_id, messages.ASKING_FOR_DATASET_MESSAGE)

		@self.bot.message_handler(content_types=['document'])
		def get_dataset_and_ask_for_task_type_poll(message):

			while True:
				doc_type = message.document.file_name.split('.')[-1]

				if doc_type in SUPPORTED_DATASET_TYPES:
					break
				else:
					self.bot.send_message(self.chat_id, messages.WRONG_FILE_TYPE_MESSAGE)
					self.bot.register_next_step_handler(message, get_dataset_and_ask_for_task_type_poll)
					return

			self.model_config.fill_doc_type(doc_type)

			file_info = self.bot.get_file(message.document.file_id)
			file_url = requests.get(
				f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}'
			).url

			if DATA_PATH.exists():
				shutil.rmtree(DATA_PATH)
			DATA_PATH.mkdir(parents=True)
			wget.download(file_url, out=DATA_PATH.absolute().as_posix() + f'/data_for_training.{doc_type}')

			keyboard = types.InlineKeyboardMarkup()
			key_reg = types.InlineKeyboardButton(text='Regression', callback_data='reg')
			key_bin_classif = types.InlineKeyboardButton(text='Binary classification', callback_data='binary')
			key_multiclass_classif = types.InlineKeyboardButton(text='Multiclass classification',
																callback_data='multiclass')
			key_multiple_reg = types.InlineKeyboardButton(text='Multiple regression', callback_data='multi:reg')
			key_multilable_classif = types.InlineKeyboardButton(text='Multiclass classification',
																callback_data='multilabel')

			keyboard.add(key_reg)
			keyboard.add(key_bin_classif)
			keyboard.add(key_multiclass_classif)
			keyboard.add(key_multiple_reg)
			keyboard.add(key_multilable_classif)

			self.bot.send_message(self.chat_id, text=messages.ASKING_FOR_TASK_TYPE_MESSAGE, reply_markup=keyboard)

		@self.bot.callback_query_handler(func=lambda call: call.data in AVAILABLE_TASK_TYPES)
		def ask_for_test_set_proportion_poll(call):

			self.model_config.fill_task_type(call.data)

			self.bot.send_message(self.chat_id, messages.ASKING_FOR_TEST_PROPORTION_MESSAGE)
			self.bot.register_next_step_handler(call.message, get_test_proportion_and_ask_for_models_list_poll)

		def get_test_proportion_and_ask_for_models_list_poll(message):

			while True:
				test_proportion_input = message.text

				if re.fullmatch(r'\d+\.\d+', test_proportion_input) and 0 <= float(test_proportion_input) <= 1:
					break
				else:
					self.bot.send_message(self.chat_id, messages.WRONG_TEST_PROPORTION_MESSAGE)
					self.bot.register_next_step_handler(message, get_test_proportion_and_ask_for_models_list_poll)
					return

			self.model_config.fill_test_proportion(float(test_proportion_input))

			self.bot.send_message(self.chat_id, messages.ASKING_FOR_MODELS_MESSAGE)
			self.bot.register_next_step_handler(message, get_models_names_and_ask_for_timeout_poll)

		def get_models_names_and_ask_for_timeout_poll(message):
			models_input = message.text.split(', ')

			while True:
				for model_name in models_input:
					if model_name in AVAILABLE_MODELS:
						continue
					else:
						self.bot.send_message(self.chat_id, messages.WRONG_MODEL_NAME_MESSAGE)
						self.bot.register_next_step_handler(message, get_models_names_and_ask_for_timeout_poll)
						return
				break

			self.model_config.fill_models(models_input)

			self.bot.send_message(self.chat_id, messages.ASKING_FOR_TIMEOUT_MESSAGE)
			self.bot.register_next_step_handler(message, get_timeout_and_start_training_poll)

		def get_timeout_and_start_training_poll(message):

			while True:
				timeout_input = message.text

				if timeout_input.isnumeric() and 0 < int(timeout_input):
					break
				else:
					self.bot.send_message(self.chat_id, messages.WRONG_TIMEOUT_MESSAGE)
					self.bot.register_next_step_handler(message, get_timeout_and_start_training_poll)
					return

			self.model_config.fill_timeout(float(timeout_input))

			self.bot.send_message(self.chat_id, messages.MODEL_TRAINING_START_MESSAGE)

			self.execute_model_training()
			self.contact_user_after_training()

	def execute_model_training(self):
		model_training_executor = ModelTrainingFacade(self.model_config)
		train_data, val_data = model_training_executor.prepare_data()
		print(train_data.head())
		print(val_data.head())
		model_training_executor.create_and_train_model(train_data, val_data)

	def contact_user_after_training(self):

		self.bot.send_message(self.chat_id, messages.TRAINING_FINISHED_MESSAGE)

		zip_file = open(DATA_PATH.absolute().as_posix() + '/model_training_report.zip', 'rb')
		self.bot.send_document(self.chat_id, zip_file)
