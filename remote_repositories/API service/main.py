import os
from typing import List, Dict
from src.logger import Logger

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import httpx
import uvicorn
import json

from src.find_similar import find_similar
from src.find_params import SubstanceSizeExtractor
from src.pdf2text import PDF2text
from src.get_parameters import get_parameters

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Установите "*" для разрешения доступа со всех источников
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все HTTP методы
    allow_headers=["*"],  # Разрешить все заголовки
)


class NanozymesBotRequest(BaseModel):
    query_text: str
    instruction: str
    context: str
    article: dict


class NanozymesBotResponse(BaseModel):
    answer: str
    context: str


class FindParametersRequest(BaseModel):
    k_m: str
    v_max: str


class FindParametersResponse(BaseModel):
    articles: dict


def call_gpt_service(query, instructions, context, previous_questions):
    request_data = {
        "query": query,
        "instructions": instructions,
        "context": str(context.tolist()),
        "previous_questions": previous_questions,
    }

    with httpx.Client() as client:
        response = client.post(
            os.environ['REDIRECT_IP_HOST'],
            json=request_data,
        )

        if response.status_code == 200:
            response_data = response.json()
            return response_data["llm_response"]

        response.raise_for_status()


@app.post("/nanozymes_bot", response_model=NanozymesBotResponse)
async def handler_nanozymes_bot(request: NanozymesBotRequest):
    Logger.info(f"/nanozymes_bot::request : {request}")
    try:
        link = request.article.get("link", None)
        if link is None:
            return {"answer": "No link", "context": request.context}
        document = link.split("/")[-1]
        get_context_for_query = find_similar(document, request.query_text)

        # Отправляем запрос к микросервису GPT
        llm_response = call_gpt_service(
            query=request.query_text,
            instructions=request.instruction,
            context=get_context_for_query[0],
            previous_questions=request.context,
        )

        new_context = request.context + "\n\n" + request.query_text + "\n\nresponse: " + llm_response + "\n\n"
        return {"answer": llm_response, "context": new_context}
    except BaseException as e:
        error_message = f"Error: {document} - {e}"
        # Logger.error(error_message)
        return {"answer": "Error, " + str(document) + " " + str(e), "context": request.context}


@app.post("/find_parameters", response_model=FindParametersResponse)
async def handler_find_parameters(request: FindParametersRequest):
    Logger.info(f"/find_parameters::request : {request}")
    try:
        k_m = request.k_m
        v_max = request.v_max
        if k_m is None and v_max is None:
            return {"articles": {}}
        articles: List[Dict[str, str]] = get_parameters(k_m, v_max)

        result = {}
        for id, article in enumerate(articles, start=1):
            result[f"article_{id}"] = {}
            for key, value in article.items():
                result[f"article_{id}"][key] = str(value)

        Logger.info(f"/find_parameters::result : {result}")

        return {"articles": result}
    except BaseException as e:
        error_message = f"Error: {e}"
        # Logger.error(error_message)
        return {"articles": {}}


if __name__ == "__main__":
    Logger.info("RUN SERVER")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
