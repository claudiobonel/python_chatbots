#pip3 install pyTelegramBotAPI
#pip3 install --upgrade pyTelegramBotAPI
#pip3 install telebot
#pip3 install python-decouple
#Criar uma conta no stripe -> https://stripe.com/br
#Após criar a sua conta, habilitar a conta de pagamentos e preencher seus dados pessoais (física ou jurídica)
import telebot, csv
from decouple import config
import time
from datetime import datetime
from telebot.types import LabeledPrice

#Token de conexão com o bot do telegram
token = config("TOKEN_BOT")
bot = telebot.TeleBot(token)

#Token de conexão com o provedor de pagamentos
token_provedor = config("TOKEN_PROVEDOR")

#Criar o preço do meu produto
preco = [
    LabeledPrice(label='E-book Engenharia de Requisitos para Projetos de BI',amount=1000)
]

#SALVAR dados da conversa com o chatbot em arquivos csv
def salvar (arquivo, conversa: list):
    with open(arquivo,'a') as chat:
        e = csv.writer(chat)
        e.writerow(conversa)

#PARTE1: Iniciar a conversa com o BOT
@bot.message_handler(commands=['start','iniciar'])
def start(message):
    bot.send_message(message.chat.id, "Faaala coisa rica! Tudo bem com vc?",timeout=120)

#Função de compra
@bot.message_handler(commands=['comprar'])
def comprar(message):
    bot.send_invoice(
        message.from_user.id,
        title='Engenharia de Requisitos para BI',
        description='Potencialize a assertividade e o resultado de suas soluções de análise de dados, utilizando as melhores práticas da Engenharia de Software!',
        provider_token=token_provedor,
        currency='BRL',
        photo_url=config('IMAGEM_PRODUTO'),
        photo_height=512,
        photo_size=512,
        photo_width=512,
        is_flexible=False,
        prices=preco,
        invoice_payload="PAYLOAD"
    )

#Função de pré-checkout. Verificação dos dados do cartão
@bot.pre_checkout_query_handler(func=lambda query:True)
def verificar_cartao(pre_checkout_query):
    bot.answer_pre_checkout_query(
        pre_checkout_query.id,ok=True,error_message="Houve falha na confirmação de sua operadora de cartão. Dessa forma, não conseguimos verificar a compra, mas convém entrar em contato com sua operadora de cartão."
    )

#Função para validação do pagamento
@bot.message_handler(content_types=['successful_payment'])
def pgto_confirmado(message):
    salvar('compra_efetuada.csv',[message.chat.id,message.from_user.username,message.text,datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    doc = open("Dadoteca.pdf","rb")
    bot.send_message(message.chat.id, 'Show! Pagamento confirmado! Partiu download. Já já você receberá o seu aquivo, aqui mesmo no chat!')
    bot.send_document(message.chat.id,doc,timeout=180)
    time.sleep(2)
    bot.send_message(message.chat.id, "Obrigado pela confiança! Querendo reiniciar nossa conversa, basta digitar iniciar.")
    time.sleep(2)
    bot.send_message(message.chat.id, "Tmj e boas análises!")

@bot.message_handler(regexp='iniciar')
def iniciar(message):
    salvar('iniciar.csv',[message.chat.id,message.from_user.username,message.text,datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    bot.send_message(message.chat.id, "Faaala coisa rica! Tudo bem com vc?",timeout=120)

@bot.message_handler(regexp=r'tudo|td|paz|sim')
def pergunta(message):
    salvar('saudacao.csv',[message.chat.id,message.from_user.username,message.text,datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    time.sleep(7)
    bot.send_message(message.chat.id, "Que bom, coisa rica! Bora realizar a compra do ebook Engenharia de Requisitos para projetos de Business Intelligence?\n \nTu sabia que ao final dos estudos você potencializará a assertividade e o resultado de suas soluções de análise de dados, utilizando as melhores práticas da engenharia de software, que é a mesma que os profissionais mais experientes do mercado utilizam??\n \nSabia que você responderia SIM! Então, clique em /comprar para efetuar o pagamento e receber o seu arquivo, aqui mesmo no chat, pelo valor de R$ 10,00.\n \nDo contrário, digite Depois, para realizar a compra em uma próxima oportunidade.",timeout=120)

#PARTE2: Download ou Playlist
'''
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
'''
@bot.message_handler(regexp='depois')
def convencimento(message):
    time.sleep(6)
    bot.send_message(message.chat.id, "É sério? Tu não vai querer?\n \nVou te dar mais uma chance para você /comprar o guia definitivo da Engenharia de Requisitos para análise de dados, aumentando os seus resultados e assertividade da sua solução de BI e, em paralelo reduzir os riscos de indefinições, falta de alinhamento e, consequentemente, fracassso da sua solução!",timeout=120)
    time.sleep(6)
    bot.send_message(message.chat.id, "Tu já sabe o que tem que fazer, né? Mas, vou repetir! rssss. Clique em /comprar para colocar em prática tudo que os profissionais mais experientes do mercado já fazem ou digite Tchau, para pensar um pouco mais sobre a compra.",timeout=120)

@bot.message_handler(regexp='tchau')
def tchau(message):
    salvar('compra_nao_efetuada.csv',[message.chat.id,message.from_user.username,message.text,datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    time.sleep(2)
    bot.send_message(message.chat.id, "Teimosão, hein! rssss",timeout=120)
    time.sleep(6)
    bot.send_message(message.chat.id, "Rsssss brincadeiras a parte, se quser reforçar o seu conhecimento em projetos de BI, assista a playlist gratuita, no link https://youtube.com/playlist?list=PLPP4r1UqnhGp13iYi4C1WN99o3SSgCpXJ",timeout=120)
    time.sleep(2)
    bot.send_message(message.chat.id, "Caso mude de ideia, basta digitar iniciar, para reiniciarmos o nosso papo e, quem sabe para você realizar a compra.",timeout=120)
    time.sleep(2)
    bot.send_message(message.chat.id, "Tmj e boas análises!",timeout=120)

bot.polling(non_stop=True, interval=0) #sondagem, verificar se há mensagens