import requests
import multiprocessing as mp
import logging
import time

# Настройка логирования
logging.basicConfig(filename='stress_test.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Функция для отправки одного запроса, принимающая неиспользуемый аргумент
def send_request(_):
    url = "http://158.160.118.234:8000/nanozymes_bot"
    headers = {"Content-Type": "application/json"}
    data = {
        "article": {
            "link": "https://doi.org/10.1039/C4RA15675G"
        },
        "query_text": "query: What is this article about?",
        "instruction": "",
        "context": ""
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.status_code, response.elapsed.total_seconds()
    except Exception as e:
        logging.error(f"Ошибка при отправке запроса: {e}")
        return None, None

# Количество запросов для отправки
num_requests = 50

if __name__ == '__main__':
    with mp.Pool(mp.cpu_count()) as pool:
        start = time.time()
        res = pool.map(send_request, range(num_requests))
        end = time.time()
        total_time = end - start
        logging.info(f"Общее время выполнения запросов: {total_time} секунд")
        for result in res:
            if result[0] is not None:
                logging.info(f"Статус код: {result[0]}, Время ответа: {result[1]} секунд")

# Вывод в консоль о завершении тестирования
print("Нагрузочное тестирование завершено. Результаты записаны в файл 'stress_test.log'")
