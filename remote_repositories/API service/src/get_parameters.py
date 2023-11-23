import numpy as np
import pandas as pd

from src.logger import Logger

# Заглушка
df = pd.read_csv("data/nanozymes_extended.csv")

def get_parameters(K_m: str = None, V_max: str = None) -> dict:
    if K_m is None and V_max is None:
        distance = None
    elif K_m is None:
        distance = lambda value: abs(float(value['Vmax, mM/s']) - float(V_max))
    elif V_max is None:
        distance = lambda value: abs(float(value['Km, mM']) - float(K_m))
    else:
        distance = lambda value: abs(float(value['Vmax, mM/s']) - float(V_max)) + abs(float(value['Km, mM']) - float(K_m))
    # Создаем список для хранения расстояний между значениями и целевыми значениями
    distances = []
    Logger.info("in get_parameters")
    # Проходимся по каждому значению в данных
    for _, value in df.iterrows():
        # Вычисляем расстояние между значениями K_m и V_max
        try:
            # Logger.info("value", value)
            # Logger.info("value['Vmax, mM/s']", value['Vmax, mM/s'])
            _distance = distance(value)
            # Добавляем расстояние и значение в список distances
            distances.append((_distance, value))
        except ValueError:
            continue
    
    # Сортируем список distances по расстоянию в порядке возрастания
    distances.sort(key=lambda x: x[0])
    Logger.info("distances")
    Logger.info(
        [{
            "distance": distance,
            **value,
        } for distance, value in distances[:5]
    ])

    # Возвращаем топ N наиболее похожих значений
    return [{
            "distance": distance,
            ** value,
        } for distance, value in distances[:5]
    ]
