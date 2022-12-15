#pip3 install pyTelegramBotAPI
#pip3 install --upgrade pyTelegramBotAPI
#pip3 install telebot
#pip3 install python-decouple
import telebot, csv
from decouple import config
import time
from datetime import datetime

token = config("TOKEN_BOT")

bot = telebot.TeleBot(token)

#SALVAR dados da conversa com o chatbot em arquivos csv
def salvar (arquivo, conversa: list):
    with open(arquivo,'a') as chat:
        e = csv.writer(chat)
        e.writerow(conversa)

#PARTE1: Iniciar a conversa com o BOT
@bot.message_handler(commands=['start','iniciar'])
def start(message):
    bot.send_message(message.chat.id, "Faaala coisa rica! Tudo bem com vc?",timeout=120)

@bot.message_handler(regexp='iniciar')
def iniciar(message):
    salvar('iniciar.csv',[message.chat.id,message.from_user.username,message.text,datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    bot.send_message(message.chat.id, "Faaala coisa rica! Tudo bem com vc?",timeout=120)

@bot.message_handler(regexp=r'tudo|td|paz|sim')
def pergunta(message):
    salvar('saudacao.csv',[message.chat.id,message.from_user.username,message.text,datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    bot.send_message(message.chat.id, "Bora fazer o download do arquivo? Digite Bora, para receber o arquivo ou digite Depois, para uma próxima oportunidade.",timeout=120)

#PARTE2: Download ou Playlist
@bot.message_handler(regexp='bora')
def download(message):
    salvar('compra_efetuada.csv',[message.chat.id,message.from_user.username,message.text,datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    doc = open("Dadoteca.pdf","rb")
    bot.send_message(message.chat.id, "Show! Partiu download!",timeout=120)
    time.sleep(2)
    bot.send_document(message.chat.id, doc, timeout=120)
    time.sleep(4)
    bot.send_message(message.chat.id, "Obrigado pelo download! Apreveite o livro! Querendo reinicar nossa conversa digite iniciar",timeout=120)
    time.sleep(2)
    bot.send_message(message.chat.id, "Tmj e boas análises!",timeout=120)

@bot.message_handler(regexp='depois')
def convencimento(message):
    time.sleep(6)
    bot.send_message(message.chat.id, "É sério? Tu não vai querer? Vou te dar mais uma chance de saber tudo e mais um pouco sobre metodologias de projetos de BI. Bora fazer fazer o download?",timeout=120)
    time.sleep(6)
    bot.send_message(message.chat.id, "Tu já sabe o que tem que digitar, né? rssss Mas, vou te lembrar, por via das dúvidas. Digite Bora para receber esse arquivo! Do contrário, digite Tchau, vou ficar triste, mas fazer o que :(",timeout=120)

@bot.message_handler(regexp='tchau')
def tchau(message):
    salvar('compra_nao_efetuada.csv',[message.chat.id,message.from_user.username,message.text,datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    time.sleep(2)
    bot.send_message(message.chat.id, "Teimosão, hein!",timeout=120)
    time.sleep(6)
    bot.send_message(message.chat.id, "Rsssss brincadeiras a parte, se quser reforçar o seu conhecimento em projetos de BI, assista a playlist gratuita, no link https://youtube.com/playlist?list=PLPP4r1UqnhGp13iYi4C1WN99o3SSgCpXJ",timeout=120)
    time.sleep(2)
    bot.send_message(message.chat.id, "Caso mude de ideia, basta digitar iniciar, para iniciar o papo e realizar o download.",timeout=120)
    time.sleep(2)
    bot.send_message(message.chat.id, "Tmj e boas análises!",timeout=120)

bot.polling() #sondagem, verificar se há mensagens