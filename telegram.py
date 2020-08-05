import telepot
from chatbot import Chatbot
from tempfile import mkstemp
import subprocess
import os
import speech_recognition as sr
from banco import *
from datetime import datetime
import os.path
import random

Bot = Chatbot('NOME BOT')
telegram = telepot.Bot("APIKEYTELEGRAM");

# iniciando Recognizer utilizado para reconhecer voz 
rec = sr.Recognizer()
dataAtual = datetime.now().strftime('%Y-%m-%d')
Banco = Banco('host','port', 'username', 'password', 'database')
teste = Banco.teste()

# Validar se existe arquivo de log do dia
if(os.path.exists('log/log-'+dataAtual+'.json')):
    print('existe')
else:
    # Senão existe, ele vai ser criado
    print('Não existe')
    memoriaLog = open('log/log-'+dataAtual+'.json','w')
    memoriaLog = open('log/log-'+dataAtual+'.json','r')
    # Gravando dados no log
    log = []
    memoriaLog.close()
    log.append('Criação de arquivo')
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.append('Data: '+ data)
    with open('log/log-'+dataAtual+'.json', 'a') as f:
        json.dump(log, f, indent=4)
        print('\n', file=f)
    memoriaLog.close();

# metodo que recebe as mensagens do telegram
def recebendoMsg(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        memoriaUser = open('Dicionarios/user.json','w')
        dataAtual = datetime.now().strftime('%Y-%m-%d')
        memoriaLog = open('log/log-'+dataAtual+'.json','r')
        nome_user = msg['from']['first_name']
        nome_userlast = msg['from']['last_name']
        memoriaUser.write('["'+nome_user+'", "'+nome_userlast+'"]')
        log = json.load(memoriaLog)
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log.append('Data: '+ data)
        usuario = nome_user+' ' + msg['from']['last_name']
        log.append('Usuario: '+usuario)
        log.append('Type: '+content_type)
        memoriaLog.close()
        memoriaLog = open('log/log-'+dataAtual+'.json','w')
        dataAtual = datetime.now().strftime('%Y-%m-%d')
        with open('log/log-'+dataAtual+'.json', 'a') as f:
            json.dump(log, f, indent=4)
            print('\n', file=f)
        memoriaLog.close();

        # Validando se a mensagem é texto
        if content_type == 'text':
            frase = msg['text']
            frase = frase.lower()
            validar = frase.lower()
            log.append('Frase: '+validar)

            if teste[0] == "Erro":
                resp = "Estou com problemas de memória, tente novamente!"
                log.append('Resposta: '+resp)
                erro = "Erro Banco"
                codError = teste[1]
                MsgError = teste[2]
                log.append(erro)
                log.append(codError)
                log.append(MsgError)
                memoriaLog.close()
                memoriaLog = open('log/log-'+dataAtual+'.json','w')
                dataAtual = datetime.now().strftime('%Y-%m-%d')
                with open('log/log-'+dataAtual+'.json', 'a') as f:
                    json.dump(log, f, indent=4)
                    print('\n', file=f)
                memoriaLog.close();
            else:
                resp = Bot.escuta(frase)
                resp = Bot.pensa(frase)
                log.append('Resposta: '+resp)
                memoriaLog.close()
                memoriaLog = open('log/log-'+dataAtual+'.json','w')
                dataAtual = datetime.now().strftime('%Y-%m-%d')
                with open('log/log-'+dataAtual+'.json', 'a') as f:
                    json.dump(log, f, indent=4)
                    print('\n', file=f)
                memoriaLog.close();
                Bot.fala(resp)

                # Validar se é voz
        elif content_type == 'voice':
                        msg['content_type'] = 'voice'
                        _, voice_filename = mkstemp(prefix='voice-', suffix='.oga')
                        _, converted_audio_filename = mkstemp(prefix='converted-audio-', suffix='.wav')
                        telegram.download_file(msg['voice']['file_id'], voice_filename)
                                     #Convertendo oga para wav
                        subprocess.call('ffmpeg -y -i ' + voice_filename +' '
                           + converted_audio_filename, shell=True)

                              # abrindo o arquivo
                        aud = sr.AudioFile(converted_audio_filename)
                        with aud as source:
                             audio = rec.record(source)
                        try:
                            # fazendo a leitura do audio e transformando em texto
                            frase = rec.recognize_google(audio, language='pt')
                            log.append("Resultado Captura Audio: " + frase )
                            memoriaLog.close()
                            memoriaLog = open('log/log-'+dataAtual+'.json','w')
                            dataAtual = datetime.now().strftime('%Y-%m-%d')
                            with open('log/log-'+dataAtual+'.json', 'a') as f:
                                json.dump(log, f, indent=4)
                                print('\n', file=f)
                            memoriaLog.close();

                        except sr.UnknownValueError:
                            log.append('Resposta: Deu erro na identificacao')
                            memoriaLog.close()
                            memoriaLog = open('log/log-'+dataAtual+'.json','w')
                            dataAtual = datetime.now().strftime('%Y-%m-%d')
                            with open('log/log-'+dataAtual+'.json', 'a') as f:
                                json.dump(log, f, indent=4)
                                print('\n', file=f)
                            memoriaLog.close();
                            return 'Não entendi'

                        if teste[0] == "Erro":
                            resp = "Estou com problemas de memória, tente novamente!"
                            log.append('Resposta: '+resp)
                            erro = "Erro Banco"
                            codError = teste[1]
                            MsgError = teste[2]
                            log.append(erro)
                            log.append(codError)
                            log.append(MsgError)
                            memoriaLog.close()
                            memoriaLog = open('log/log-'+dataAtual+'.json','w')
                            dataAtual = datetime.now().strftime('%Y-%m-%d')
                            with open('log/log-'+dataAtual+'.json', 'a') as f:
                                json.dump(log, f, indent=4)
                                print('\n', file=f)
                            memoriaLog.close();
                        
                        else:
                            Bot.escuta(frase.lower())
                            resp = Bot.pensa(frase.lower())
                            array = resp.split(" ");
                            elemento = 'name'
                            pos_i = 0 # variável provisória de índice
                            for i in range (len(array)): # procurar em todas as listas internas
                                if elemento in array[i]: # se encontrarmos elemento ('name')
                                    pos_i = i # guardamos o índice i
                                    resp = form.replace(array[pos_i], nome_user)

                                    break # saímos do loop interno
                            log.append('Resposta: '+resp)
                            memoriaLog.close()
                            memoriaLog = open('log/log-'+dataAtual+'.json','w')
                            dataAtual = datetime.now().strftime('%Y-%m-%d')
                            with open('log/log-'+dataAtual+'.json', 'a') as f:
                                json.dump(log, f, indent=4)
                                print('\n', file=f)
                            memoriaLog.close();
                            Bot.fala(resp)
                            with open(voice_filename, 'rb') as file:
                                msg['content'] = file.read()

        elif (content_type == 'photo') or (content_type == 'document'):
            resp = 'Desculpe, ainda não compreendo imagens!!'
            memoriaLog.close()
            memoriaLog = open('log/log-'+dataAtual+'.json','w')
            log.append('Resposta: '+resp)
            dataAtual = datetime.now().strftime('%Y-%m-%d')
            with open('log/log-'+dataAtual+'.json', 'a') as f:
                json.dump(log, f, indent=4)
                print('\n', file=f)
            memoriaLog.close();
            Bot.fala(resp)

            # os Stickers fiz uma API de figurinhas e cada vez é enviado uma figurinha aleatoria
        elif (content_type == 'sticker'):
            chatID = msg['chat']['id']
            b = random.randint(1, 137)
            sticker_url = "http://pretojoia.com.br/figurinhas/"+str(b)+".webp"
            memoriaLog.close()
            log.append('Resposta: '+sticker_url)
            memoriaLog = open('log/log-'+dataAtual+'.json','w')
            dataAtual = datetime.now().strftime('%Y-%m-%d')
            with open('log/log-'+dataAtual+'.json', 'a') as f:
                json.dump(log, f, indent=4)
                print('\n', file=f)
            memoriaLog.close();
            try:
                telegram.sendSticker(chatID, sticker_url)
            except telepot.exception.TelegramError as e:
                memoriaLog.close()
                memoriaLog = open('log/log-'+dataAtual+'.json','w')
                erro = "[!]Erro ao enviar a mensagem: " + str(e.json)
                log.append(erro)
                with open('log/log-'+dataAtual+'.json', 'a') as f:
                    json.dump(log, f, indent=4)
                    print('\n', file=f)
                memoriaLog.close()
        else:
            resp = Bot.escuta(frase)
            resp = Bot.pensa(frase)
            log.append('Resposta: '+resp)
            Bot.fala(resp)
            memoriaLog.close()
            memoriaLog = open('log/log-'+dataAtual+'.json','w')
            dataAtual = datetime.now().strftime('%Y-%m-%d')
            with open('log/log-'+dataAtual+'.json', 'a') as f:
                json.dump(log, f, indent=4)
                print('\n', file=f)
            memoriaLog.close();
        chatID = msg['chat']['id']
        if (content_type != 'sticker'):

            try:
                telegram.sendMessage(chatID, resp)
            except telepot.exception.TelegramError as e:
                memoriaLog.close()
                memoriaLog = open('log/log-'+dataAtual+'.json','w')
                erro = "[!]Erro ao enviar a mensagem: " + str(e.json)
                log.append(erro)
                with open('log/log-'+dataAtual+'.json', 'a') as f:
                    json.dump(log, f, indent=4)
                    print('\n', file=f)
                memoriaLog.close()

# OBS, para tratar esse erro foi preciso editar o arquivo C:\Users\Douglas Cezaro\AppData\Local\Programs\Python\Python38-32\Lib\site-packages\telepot __init__.py
# ajustar as Exception para não retornar os erros
if telegram.message_loop(recebendoMsg) != None:
    sucesso = "Sucesso"
else:
    memoriaLog = open('log/log-'+dataAtual+'.json','r')
    log = []
    log = json.load(memoriaLog)
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.append('Data: '+ data)
    memoriaLog.close()
    erro = "[!]Erro conexão"
    log.append(erro)
    memoriaLog = open('log/log-'+dataAtual+'.json','w')
    with open('log/log-'+dataAtual+'.json', 'a') as f:
        json.dump(log, f, indent=4)
        print('\n', file=f)
    memoriaLog.close()
while True:
    pass
