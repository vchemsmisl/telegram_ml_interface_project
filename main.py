import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

from src.tgbot import TgBot
from src.model import AutoMLModelConfig

config = AutoMLModelConfig()
bot = TgBot(config)

bot.request_parameters_from_user()

bot.contact_user_after_training()
