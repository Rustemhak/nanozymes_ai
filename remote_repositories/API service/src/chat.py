import os
from time import sleep

import openai

from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.chains import RetrievalQA
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.vectorstores import FAISS

from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredPDFLoader


from src.logger import Logger

print("SUCCESS IN CHAT")


class BaseLLM:
    def __call__(self, query, instructions, context, previous_questions):
        raise NotImplementedError
    

class ChatGPT(BaseLLM):
    openai.api_key = os.environ['OPENAI_API_KEY']
    llm_model = 'gpt-3.5-turbo'


    # chat = ChatOpenAI(temperature=0.0, model=llm_model, max_tokens=1024)
    embeddings = OpenAIEmbeddings()

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

        # Создаем экземпляр векторных представлений (embeddings)
        # embeddings = openai.Embedding.create(
        #     inputs=[
        #         "This is a sample sentence.",
        #         "Another sample sentence."
        #     ]
        # )

        # Получаем векторные представления
        # vector_embeddings = embeddings['data']

        # print(vector_embeddings)
        Logger.info((
        f"{query=}\n\n"
        f"{instructions=}\n\n"
        f"{context=}\n\n"
        f"{response=}\n\n"
        ))
        return response
    
    def TEMPLATE(self, query, instructions, context, previous_questions):
        return f"""Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text below, say "I don't know".
        \n\nQuestion: {str(query)}
        \n\nInstructions for answer: {str(instructions)}
        \n\nContext: {str(context)}
        """

