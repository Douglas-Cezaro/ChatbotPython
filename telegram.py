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
rec = sr.Recognizer()
dataAtual = datetime.now().strftime('%Y-%m-%d')
if(os.path.exists('log/log-'+dataAtual+'.json')):
    print('existe')
else:
    print('Não existe')
    memoriaLog = open('log/log-'+dataAtual+'.json','w')
    memoriaLog = open('log/log-'+dataAtual+'.json','r')
    log = []
    memoriaLog.close()
    log.append('Criação de arquivo')
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log.append('Data: '+ data)
    with open('log/log-'+dataAtual+'.json', 'a') as f:
        json.dump(log, f, indent=4)
        print('\n', file=f)
    memoriaLog.close();

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
        if content_type == 'text':
            frase = msg['text']
            frase = frase.lower()
            validar = frase.lower()
            log.append('Frase: '+validar)
            if validar == 'figurinha':
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
            if validar == 'pagante atual':
                Banco1 = Banco('host','port', 'username', 'password', 'db')
                nome_user = msg['from']['first_name']
                validarpagante = Banco1.pagantes(nome_user)
                if len(validarpagante) < 2:
                    nome_user = msg['from']['first_name']
                else:
                    nome_user = msg['from']['last_name']

                pagante = Banco1.paganteAtual()

                if pagante == None:
                    resp = "Hoje ninguém paga!!"
                    log.append('Resposta: '+resp)
                    memoriaLog.close()
                    memoriaLog = open('log/log-'+dataAtual+'.json','w')
                    dataAtual = datetime.now().strftime('%Y-%m-%d')
                    with open('log/log-'+dataAtual+'.json', 'a') as f:
                        json.dump(log, f, indent=4)
                        print('\n', file=f)
                    memoriaLog.close();
                else:
                    if pagante[1] == 'PAGO':
                        resp = "A coca de hoje já foi pega pelo " + pagante[0]
                        log.append('Resposta: '+resp)
                        memoriaLog.close()
                        memoriaLog = open('log/log-'+dataAtual+'.json','w')
                        dataAtual = datetime.now().strftime('%Y-%m-%d')
                        with open('log/log-'+dataAtual+'.json', 'a') as f:
                            json.dump(log, f, indent=4)
                            print('\n', file=f)
                        memoriaLog.close();

                    elif pagante[0] == "Erro":
                        resp = "Estou com problemas de memória, tente novamente!"
                        log.append('Resposta: '+resp)
                        erro = "Erro Banco"
                        codError = pagante[1]
                        MsgError = pagante[2]
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

                    elif nome_user in pagante[0]:
                        resp = "Hoje é seu dia de pagar a coca!!"
                        log.append('Resposta: '+resp)
                        memoriaLog.close()
                        memoriaLog = open('log/log-'+dataAtual+'.json','w')
                        dataAtual = datetime.now().strftime('%Y-%m-%d')
                        with open('log/log-'+dataAtual+'.json', 'a') as f:
                            json.dump(log, f, indent=4)
                            print('\n', file=f)
                            memoriaLog.close();
                    else:
                        resp = "Hoje é dia do " + pagante[0]+ " pagar nossa coca!!"
                        log.append('Resposta: '+resp)
                        memoriaLog.close()
                        memoriaLog = open('log/log-'+dataAtual+'.json','w')
                        dataAtual = datetime.now().strftime('%Y-%m-%d')
                        with open('log/log-'+dataAtual+'.json', 'a') as f:
                            json.dump(log, f, indent=4)
                            print('\n', file=f)
                            memoriaLog.close();
            elif validar == 'meu dia de pagar':
                nome_user = msg['from']['first_name']
                Banco2 = Banco('host','port', 'username', 'password', 'db')
                validarpagante = Banco2.pagantes(nome_user)
                dataAtual = datetime.now().strftime('%Y-%m-%d')

                if len(validarpagante) < 2:
                    pagante = Banco2.meuDiadePagar(nome_user)
                else:
                    nome_user = msg['from']['last_name']
                    pagante = Banco2.meuDiadePagar(nome_user)

                if pagante == None:
                    resp = "Ainda não sabemos o seu dia de pagar"
                    log.append('Resposta: '+resp)
                    memoriaLog.close()
                    memoriaLog = open('log/log-'+dataAtual+'.json','w')
                    dataAtual = datetime.now().strftime('%Y-%m-%d')
                    with open('log/log-'+dataAtual+'.json', 'a') as f:
                        json.dump(log, f, indent=4)
                        print('\n', file=f)
                    memoriaLog.close();
                elif pagante[0] == "Erro":
                    resp = "Estou com problemas de memória, tente novamente!"
                    log.append('Resposta: '+resp)
                    erro = "Erro Banco"
                    codError = pagante[1]
                    MsgError = pagante[2]
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

                elif dataAtual == pagante:
                    resp = "Hoje é seu dia de pagar a coca!!"
                    log.append('Resposta: '+resp)
                    memoriaLog.close()
                    memoriaLog = open('log/log-'+dataAtual+'.json','w')
                    dataAtual = datetime.now().strftime('%Y-%m-%d')
                    with open('log/log-'+dataAtual+'.json', 'a') as f:
                        json.dump(log, f, indent=4)
                        print('\n', file=f)
                    memoriaLog.close();
                else:
                    data = pagante
                    cr_date = datetime.strptime(data, '%Y-%m-%d')
                    dataFormatada = cr_date.strftime("%d/%m/%Y")
                    resp = "Seu dia de pagar: "+dataFormatada
                    log.append('Resposta: '+resp)
                    memoriaLog.close()
                    memoriaLog = open('log/log-'+dataAtual+'.json','w')
                    dataAtual = datetime.now().strftime('%Y-%m-%d')
                    with open('log/log-'+dataAtual+'.json', 'a') as f:
                        json.dump(log, f, indent=4)
                        print('\n', file=f)
                    memoriaLog.close();
            elif validar == 'meu ultimo pagamento':
                Banco3 = Banco('host','port', 'username', 'password', 'db')
                nome_user = msg['from']['first_name']
                validarpagante = Banco3.pagantes(nome_user)
                if len(validarpagante) < 2:
                    nome_user = msg['from']['first_name']
                else:
                    nome_user = msg['from']['last_name']
                pagante = Banco3.meuUltimopag(nome_user)
                if pagante[0] == "Erro":
                    resp = "Estou com problemas de memória, tente novamente!"
                    log.append('Resposta: '+resp)
                    erro = "Erro Banco"
                    codError = pagante[1]
                    MsgError = pagante[2]
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
                elif pagante[0] != "Erro":
                    data = pagante[0]
                    cr_date = datetime.strptime(data, '%Y-%m-%d')
                    dataFormatada = cr_date.strftime("%d/%m/%Y")
                    resp = "O ultimo dia que você pagou foi " + dataFormatada
                    log.append('Resposta: '+resp)
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
                array = resp.split(" ");
                elemento = 'name'
                pos_i = 0 # variável provisória de índice
                for i in range (len(array)): # procurar em todas as listas internas
                    if elemento in array[i]: # se encontrarmos elemento ('name')
                        pos_i = i # guardamos o índice i
                        resp = resp.replace(array[pos_i], nome_user)

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
                        teste = sr.AudioFile(converted_audio_filename)
                        with teste as source:
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
                        validar = frase.lower()
                        if validar == 'pagante atual':
                            Banco4 = Banco('host','port', 'username', 'password', 'db')
                            nome_user = msg['from']['first_name']
                            validarpagante = Banco4.pagantes(nome_user)

                            if len(validarpagante) < 2:
                                nome_user = msg['from']['first_name']
                            else:
                                nome_user = msg['from']['last_name']

                            pagante = Banco4.paganteAtual()
                            if pagante == None:
                                resp = "Hoje ninguém paga!!"
                                log.append('Resposta: '+resp)
                                memoriaLog.close()
                                memoriaLog = open('log/log-'+dataAtual+'.json','w')
                                dataAtual = datetime.now().strftime('%Y-%m-%d')
                                with open('log/log-'+dataAtual+'.json', 'a') as f:
                                    json.dump(log, f, indent=4)
                                    print('\n', file=f)
                                memoriaLog.close();
                            else:
                                if pagante[1] == 'PAGO':
                                    resp = "A coca de hoje já foi pega pelo " + pagante[0]
                                    log.append('Resposta: '+resp)
                                    memoriaLog.close()
                                    memoriaLog = open('log/log-'+dataAtual+'.json','w')
                                    dataAtual = datetime.now().strftime('%Y-%m-%d')
                                    with open('log/log-'+dataAtual+'.json', 'a') as f:
                                        json.dump(log, f, indent=4)
                                        print('\n', file=f)
                                    memoriaLog.close();

                                elif pagante[0] == "Erro":
                                    resp = "Estou com problemas de memória, tente novamente!"
                                    log.append('Resposta: '+resp)
                                    erro = "Erro Banco"
                                    codError = pagante[1]
                                    MsgError = pagante[2]
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

                                elif nome_user in pagante[0]:
                                    resp = "Hoje é seu dia de pagar a coca!!"
                                    log.append('Resposta: '+resp)
                                    memoriaLog.close()
                                    memoriaLog = open('log/log-'+dataAtual+'.json','w')
                                    dataAtual = datetime.now().strftime('%Y-%m-%d')
                                    with open('log/log-'+dataAtual+'.json', 'a') as f:
                                        json.dump(log, f, indent=4)
                                        print('\n', file=f)
                                        memoriaLog.close();
                                else:
                                    resp = "Hoje é dia do " + pagante[0]+ " pagar nossa coca!!"
                                    log.append('Resposta: '+resp)
                                    memoriaLog.close()
                                    memoriaLog = open('log/log-'+dataAtual+'.json','w')
                                    dataAtual = datetime.now().strftime('%Y-%m-%d')
                                    with open('log/log-'+dataAtual+'.json', 'a') as f:
                                        json.dump(log, f, indent=4)
                                        print('\n', file=f)
                                        memoriaLog.close();

                        elif validar == 'meu dia de pagar':
                            nome_user = msg['from']['first_name']
                            Banco5 = Banco('host','port', 'username', 'password', 'db')
                            validarpagante = Banco5.pagantes(nome_user)
                            if len(validarpagante) < 2:
                                pagante = Banco5.meuDiadePagar(nome_user)
                            else:
                                nome_user = msg['from']['last_name']
                                pagante = Banco5.meuDiadePagar(nome_user)

                            if pagante == '':
                                resp = "Ainda não sabemos o seu dia de pagar"
                                log.append('Resposta: '+resp)
                                memoriaLog.close()
                                memoriaLog = open('log/log-'+dataAtual+'.json','w')
                                dataAtual = datetime.now().strftime('%Y-%m-%d')
                                with open('log/log-'+dataAtual+'.json', 'a') as f:
                                    json.dump(log, f, indent=4)
                                    print('\n', file=f)
                                memoriaLog.close();

                            elif pagante[0] == "Erro":
                                resp = "Estou com problemas de memória, tente novamente!"
                                log.append('Resposta: '+resp)
                                erro = "Erro Banco"
                                codError = pagante[1]
                                MsgError = pagante[2]
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

                            elif dataAtual == pagante:
                                resp = "Hoje é seu dia de pagar a coca!!"
                                log.append('Resposta: '+resp)
                                memoriaLog.close()
                                memoriaLog = open('log/log-'+dataAtual+'.json','w')
                                dataAtual = datetime.now().strftime('%Y-%m-%d')
                                with open('log/log-'+dataAtual+'.json', 'a') as f:
                                    json.dump(log, f, indent=4)
                                    print('\n', file=f)
                                memoriaLog.close();
                            else:
                                resp = "Seu dia de pagar: "+pagante
                                log.append('Resposta: '+resp)
                                memoriaLog.close()
                                memoriaLog = open('log/log-'+dataAtual+'.json','w')
                                dataAtual = datetime.now().strftime('%Y-%m-%d')
                                with open('log/log-'+dataAtual+'.json', 'a') as f:
                                    json.dump(log, f, indent=4)
                                    print('\n', file=f)
                                memoriaLog.close();
                        elif validar == 'meu ultimo pagamento':
                            Banco6 = Banco('host','port', 'username', 'password', 'db')
                            nome_user = msg['from']['first_name']
                            validarpagante = Banco5.pagantes(nome_user)
                            if len(validarpagante) < 2:
                                nome_user = msg['from']['first_name']
                            else:
                                nome_user = msg['from']['last_name']

                            pagante = Banco6.meuUltimopag(nome_user)
                            if pagante[0] == "Erro":
                                resp = "Estou com problemas de memória, tente novamente!"
                                log.append('Resposta: '+resp)
                                erro = "Erro Banco"
                                codError = pagante[1]
                                MsgError = pagante[2]
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
                            elif pagante[0] != "Erro":
                                data = pagante[0]
                                cr_date = datetime.strptime(data, '%Y-%m-%d')
                                dataFormatada = cr_date.strftime("%d/%m/%Y")
                                resp = "O ultimo dia que você pagou foi " + dataFormatada
                                log.append('Resposta: '+resp)
                                memoriaLog.close()
                                memoriaLog = open('log/log-'+dataAtual+'.json','w')
                                dataAtual = datetime.now().strftime('%Y-%m-%d')
                                with open('log/log-'+dataAtual+'.json', 'a') as f:
                                    json.dump(log, f, indent=4)
                                    print('\n', file=f)
                                memoriaLog.close();
                        else:
                            # Senão for nem meu dia de pagar e nem Pagante atual ele segue
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
            frase = 'Desculpe, ainda não compreendo imagens!!'
            memoriaLog.close()
            memoriaLog = open('log/log-'+dataAtual+'.json','w')
            log.append('Resposta: '+resp)
            dataAtual = datetime.now().strftime('%Y-%m-%d')
            with open('log/log-'+dataAtual+'.json', 'a') as f:
                json.dump(log, f, indent=4)
                print('\n', file=f)
            memoriaLog.close();
            Bot.fala(resp)
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
            array = resp.split(" ");
            elemento = 'name'
            pos_i = 0 # variável provisória de índice
            for i in range (len(array)): # procurar em todas as listas internas
                if elemento in array[i]: # se encontrarmos elemento ('name')
                    pos_i = i # guardamos o índice i
                    resp = resp.replace(array[pos_i], nome_user)

                    break # saímos do loop interno
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
            if (frase != 'figurinha'):
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

telegram.message_loop(recebendoMsg)
while True:
    pass
