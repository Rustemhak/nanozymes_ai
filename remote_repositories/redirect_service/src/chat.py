import os
from time import sleep

import openai

# from src.logger import Logger

print("SUCCESS IN CHAT")


class BaseLLM:
    def __call__(self, query, instructions, context, previous_questions):
        raise NotImplementedError


class ChatGPT(BaseLLM):
    openai.api_key = os.environ['OPENAI_API_KEY']
    llm_model = 'gpt-3.5-turbo'

    def __call__(self, query, instructions, context, previous_questions):
        # Создаем экземпляр чата
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Замените на вашу модель
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",
                 "content": self.TEMPLATE(
                     query=query,
                     context=context,
                     previous_questions=previous_questions,
                     instructions=instructions)}
            ],
            max_tokens=1024,
            temperature=0.0
        )

        # Получаем ответ
        response = chat.choices[0].message['content']
        print(response)

        # Logger.info((
        # f"{query=}\n\n"
        # f"{instructions=}\n\n"
        # f"{context=}\n\n"
        # f"{response=}\n\n"
        # ))
        return response

    def TEMPLATE(self, query, instructions, context, previous_questions):
        return f"""Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text below, say "I don't know".
        \n\nQuestion: {str(query)}
        \n\nInstructions for answer: {str(instructions)}
        \n\nContext: {str(context)}
        """

