import os
import logging


Logger = logging.getLogger('nanozymes_bot')
Logger.setLevel(logging.INFO)

# Создаем обработчик для записи логов в файл
file_handler = logging.FileHandler('logs/nanozymes_bot.log')
file_handler.setLevel(logging.INFO)

# Создаем форматтер для записи логов в удобочитаемом формате
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
Logger.addHandler(file_handler)

# Опционально, можно добавить обработчик для вывода логов в консоль
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.INFO)
# console_handler.setFormatter(formatter)
# Logger.addHandler(console_handler)
