# API service
## Описание

Схема, описывающая логику сервиса: 
https://miro.com/app/board/uXjVNdSWWvM=/?share_link_id=404762759941

Сервис для доступа по API:
1) POST `/nanozymes_bot`
```json
POST /nanozymes_bot
{
	"article": { // статья, по которой пользователь спрашивает вопрос
			"link": "<doi_url>",
	}
	"query_text": "<текст запроса>",
	"instruction": "<инструкции для chatGPT>",
	"context": "<предыдущие сообщения пользователя>"
}
result:
{
	"answer": "<ответ на запрос с заданным контекстом пользователю>",
	"context": "<предыдущие сообщения пользователя + новый запрос>",
}
```
2) POST `/nanozymes_bot`
```json
POST /nanozymes_bot
{
	"params": {"v_max": "<v_max_value>", "k_m": "<K_m_value>"},
}
result:
{
	"articles": { // возвращем top-5 статей
		"article_1": {
			"<parameter1>": "<параметр1>",
			"<parameter2>": "<параметр2>",
			...
			"<parameterN>": "<параметрN>" // параметры для соответствующей статьи
		},
		"article_2": ...
		...
		"article_5": ...
	}
}
```
## Запуск
Для отладки сервиса выполните следующие команды:
1) `docker build -t api-service .`
2) `docker run -it --rm -v "$(pwd):/app" -p 8000:8000 api-service bash`
После выполнения команды (2) вы перейдете внутрь контейнера, `-v "$(pwd):/app"` позволяет редактировать файлы извне контейнера.


Для запуска сервиса выполните следующие команды:
1) `docker build -t api-service .`
2) `docker run -d --restart=always -v "$(pwd)/data:/app/data" -v "$(pwd)/logs:/app/logs" -p 8000:8000 -e OPENAI_API_KEY=YOUR_API_KEY api-service`

Примечания: 
1) директория `data` должна содержать статьи в `pdf` формате.
2) директория `data/embeddings` должна содержать предварительно посчитанные FAISS индексы



P.S.: `pyproject.toml` не использовать!

## Команда
- Роман Сим
- Роман Одобеску
- Олег Загорулько
- Сабина Мирзаева
- Рустем Хакимуллин


