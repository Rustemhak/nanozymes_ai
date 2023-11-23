import streamlit as st

# Заголовок приложения
st.title("Минимальное Streamlit-приложение")

# Текстовый блок
st.write("Привет, это минимальное Streamlit-приложение!")

# Вывод графика
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
st.pyplot(plt)
