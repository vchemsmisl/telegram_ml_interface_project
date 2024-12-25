import telebot
from constants_and_messages import (
	BOT_TOKEN,
	STARTING_MESSAGE_TRUE,
	STARTING_MESSAGE_FALSE
)

class TgBot:

	def __init__(self):
		self.bot = telebot.TeleBot(BOT_TOKEN)
		self.name = 'vchemsmisl_bot'

	# def start_bot(self):
	# 	self.bot.infinity_polling()

	def start(self):

		@self.bot.message_handler(content_types=['text'])
		def starting_message(message):
			chat_id = message.from_user.id

			if message.text in ['/start', '/help']:
				self.bot.send_message(chat_id, STARTING_MESSAGE_TRUE)
				
			else:
				self.bot.send_message(chat_id, STARTING_MESSAGE_FALSE)




bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.from_user.id, "ты пидор")

@bot.message_handler(func=lambda message: message.text == 'ass')
def echo_all(message):
	bot.send_message(message.from_user.id, message.text)

bot.infinity_polling()