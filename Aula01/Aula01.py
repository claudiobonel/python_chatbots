import spacy

nlp = spacy.load("pt_core_news_sm")

#EXEMPLO 1 - Tokenização

texto = nlp(u'Eu estou aprendendo a utilizar chatbots.')

for token in texto:
    print(token.text, token.pos_)


#EXEMPLO 2 - Mais alguns atributos do token

texto2 = nlp(u'O canal do Youtube do "Prof. Claudio Bonel" está chegando a 11.000 inscritos.')

for token in texto2:
    print("- Texto:",token.text,
            " - Forma raiz:", token.lemma_,
            "Tipo da palavra:", token.pos_,
            "É letra:", token.is_alpha)


#EXEMPLO 3 - Buscando semelhanças

#QUERO APRENDIZADO E CONHECIMENTO
texto3 = input("Como posso te ajudar no dia de hoje?")
texto3 = nlp(texto3)

for token1 in texto3:
    for token2 in texto3:
        similaridade = round((token1.similarity(token2) * 100),2)
        print("A palavra {} é {}% similar a palavra {}".format(token1.text,similaridade,token2.text))

#EXEMPLO 4 - Busncado similaridade e comparando com as regras do meu chatbot

texto4 = input("Como posso te ajudar no dia de hoje?")
texto4 = nlp(texto4)
texto_comparativo = nlp("conhecimento")

def conhecimento():
    print("Fico feliz em saber que está em busca de conhecimento! Acesse http://youtube.com/c/ClaudioBonel e aprenda tudo sobre análise de dados!")

for token in texto4:
    similaridade = round((token.similarity(texto_comparativo) * 100),2)
    if similaridade == 100:
        #print("A palavra {} é {}% similar a palavra conhecimento".format(token.text,similaridade))
        conhecimento()
    elif similaridade >= 30 and similaridade < 100:
        pergunta_similidade = input("Você está em busca de conhecimento? (S para sim e N para não)")
        if pergunta_similidade.upper() == "S":
            print("A palavra {} é {}% similar a palavra conhecimento".format(token.text,similaridade))
            conhecimento()
        else:
            print("Ok! Por favor, refaça sua solicitação.")
    else:
        print("Não encontrei sua solicitação, por favor refaça.",similaridade)
