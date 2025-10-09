import uvicorn
import telebot
from fastapi import FastAPI, HTTPException
import random

import logging
from colorlog import ColoredFormatter

import datetime

#pip install fastapi uvicorn pydantic pytelegrambotapi

from pydantic import BaseModel

app = FastAPI()
bot = telebot.TeleBot("8407018520:AAGWhWY8yK-0lgYoeShAAN_oLUItqa-k8RY")


logger = logging.getLogger('backend')
logger.setLevel(logging.DEBUG)


file_handler = logging.FileHandler('app.log', 'a', encoding='utf-8')
file_handler.setLevel(logging.ERROR)

log_format = logging.Formatter('%(asctime)s  -  %(levelname)s:    %(message)s')

file_handler.setFormatter(log_format)

logger.addHandler(file_handler)

# Создаем обработчик (например, консольный)
handler = logging.StreamHandler()

    # Создаем форматтер с цветами
formatter = ColoredFormatter(
        '%(log_color)s%(levelname)s:     %(asctime)s -  %(name)s   -   %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    # Добавляем форматтер к обработчику
handler.setFormatter(formatter)

logger.addHandler(handler)

chat_id_admin = ""

class CheckTransfer(BaseModel):
    bank: str
    card: str
    crypto: str
    cryptoAmount: float
    holder: str
    rubAmount: float
    telegram: str


@app.get("/new_user")
def startMes():
    try:
        logger.info('Пользователь зашел на сайт')
        bot.send_message(
            chat_id=chat_id_admin,
            text=f"🔐 Зашел новый пользователь \n{datetime.datetime.now()}"
        )
        logger.info('Данные отправленны администратору')
        return {"Status": "good"}
    except Exception as ex:
        logger.error(ex)

        raise HTTPException(status_code=400, detail="Server cant send message")



@app.post("/new_order")
def startMes(data: CheckTransfer):
    try:
        text_message = data
        bot.send_message(
            chat_id=chat_id_admin,
            text=f"❗️Новая заявка на вывод \n{text_message}"
        )
        id = random.randint(99999, 1000000)
        return {"data": id}
    except Exception as ex:
        raise HTTPException(status_code=400, detail="Server cant send message")
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)