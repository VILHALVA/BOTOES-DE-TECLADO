import telebot
from telebot import types
from TOKEN import TOKEN
import os

bot = telebot.TeleBot(TOKEN)

def listar_fotos(diretorio):
    return [f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))]

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    diretorio_fotos = "./FOTOS"
    fotos = listar_fotos(diretorio_fotos)
    
    for i, foto in enumerate(fotos):
        item = types.KeyboardButton(f"FOTO {i + 1}")
        markup.add(item)
    
    bot.send_message(message.chat.id, "😀Escolha uma foto para enviar:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith("FOTO"))
def handle_message(message):
    try:
        numero_foto = int(message.text.split(" ")[1])
        enviar_foto(message, numero_foto - 1)
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "🤬Por favor, escolha uma foto válida!")

def enviar_foto(message, index):
    diretorio_fotos = "./FOTOS"
    fotos = listar_fotos(diretorio_fotos)
    
    if 0 <= index < len(fotos):
        caminho_foto = os.path.join(diretorio_fotos, fotos[index])
        with open(caminho_foto, 'rb') as foto:
            bot.send_photo(message.chat.id, foto)
    else:
        bot.send_message(message.chat.id, "😢Foto não encontrada.")

bot.polling()
