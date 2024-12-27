import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

from src.tgbot import TgBot
from src.model import AutoMLModelConfig


def main():

    config = AutoMLModelConfig()
    bot = TgBot(config)

    bot.execute_model_training_bot_interface()
    bot.start_infinity_polling()

if __name__ == '__main__':
    main()
