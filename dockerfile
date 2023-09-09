# Используем базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости проекта в контейнер
COPY requirements.txt .

# Устанавливаем зависимости проекта
RUN pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Открываем порт, на котором будет работать приложение Streamlit
EXPOSE 8501

# Запускаем приложение Streamlit
CMD ["streamlit", "run", "ai_talks/chat.py"]
# sudo docker build -t front_bootcamp:v0 .
# sudo docker run -d --restart unless-stopped -p 8501:8501 -v /home/roman/project/AI-Talks/ai_talks/assets/pdf:/app/ai_talks/assets/pdf -e OPENAI_API_KEY=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 front_bootcamp:v0