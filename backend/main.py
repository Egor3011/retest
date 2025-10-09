import uvicorn
import telebot
from fastapi import FastAPI, HTTPException
import random

import datetime

#pip install fastapi uvicorn pydantic pytelegrambotapi

from fastapi.responses import FileResponse

from pydantic import BaseModel

app = FastAPI()
bot = telebot.TeleBot("8407018520:AAGWhWY8yK-0lgYoeShAAN_oLUItqa-k8RY")

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
        bot.send_message(
            chat_id=chat_id_admin,
            text=f"🔐 Зашел новый пользователь \n{datetime.datetime.now()}"
        )
        return {"Status": "good"}
    except Exception as ex:
        raise HTTPException(status_code=400, detail="Server cant send message")



@app.get("/new_order")
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