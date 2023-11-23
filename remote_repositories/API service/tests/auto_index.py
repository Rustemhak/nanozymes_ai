import os
from src.get_context import get_context

import logging


Logger = logging.getLogger('auto_index')
Logger.setLevel(logging.INFO)


file_handler = logging.FileHandler('logs/auto_index.log')
file_handler.setLevel(logging.INFO)

# Создаем форматтер для записи логов в удобочитаемом формате
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
Logger.addHandler(file_handler)
Logger.info("Start")
# Опционально, можно добавить обработчик для вывода логов в консоль
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.INFO)
# console_handler.setFormatter(formatter)
# Logger.addHandler(console_handler)
def find_csv_filenames(path_to_dir, prefix = "2023-08-15", suffix=".csv" ):
    filenames = os.listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith(suffix) and filename.startswith(prefix) ]

documents = find_csv_filenames("data/", prefix="", suffix=".pdf")
Logger.info(f"Start with len(documents), documents: {len(documents)}, {documents}")
i = 0
for document in documents:
    i += 1
    document = document.split(".pdf")[0]
    Logger.info(f"Success run with document: {i}, document: {document}")
    try:
        res = get_context(document, "")
        Logger.info(f"Success complete with document: {i}, document: {document}")
    except Exception as e:
        Logger.error(f"Error with document: {i}, document: {document}, error: {e}")
        continue

Logger.info(f"End with len(documents), documents: {len(documents)}, {documents}")
