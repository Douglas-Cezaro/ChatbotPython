import json
from banco import *
from datetime import datetime
class Chatbot():
    def __init__(self, nome):
        try:
            memoria = open('Dicionarios/'+nome+'.json','r')
            memoriaDic = open('Dicionarios/dic'+nome+'.json','r')
            memoriaUser = open('Dicionarios/user.json','r')
            memoriaDia = open('Dicionarios/dia.json','r')
            memoriaSau = open('Dicionarios/saudacoes.json','r')
        except FileNotFoundError:
            memoria = open('Dicionarios/'+nome+'.json','w')
            memoriaDic = open('Dicionarios/dic'+nome+'.json','w')
            memoriaUser = open('Dicionarios/user.json','w')
            memoriaDia = open('Dicionarios/dia.json','w')
            memoriaSau = open('Dicionarios/saudacoes.json','w')
            memoria.write('["Cadê a coca Kalebinho?", "@ControleCoca 3 horas, quem paga a hoje?"]')
            memoriaDic.write('{"oi":"Meu nome é Kalebinho, sou um bot que posso lhe dizer quem é o pagante do nosso refrigerante", "tchau": "tchau"}')
            memoriaUser.write('["User"]')
            memoriaDia.write('["Que dia eu pago"]')
            memoriaSau.write('["Bom dia"]')
            memoria.close();
            memoriaDic.close();
            memoriaDia.close();
            memoriaUser.close();
            memoriaSau.close();
            memoriaLog.close();
            memoria = open('Dicionarios/'+nome+'.json','r')
            memoriaDic = open('Dicionarios/dic'+nome+'.json','r')
            memoriaUser = open('Dicionarios/user.json','r')
            memoriaDia = open('Dicionarios/dia.json','r')
            memoriaSau = open('Dicionarios/saudacoes.json','r')
            memoriaLog = open('log.json','r')
        self.nome = nome;
        self.conhecidos = json.load(memoria)
        self.frases  = json.load(memoriaDic)
        self.dia  = json.load(memoriaDia)
        try:
            self.user = json.load(memoriaUser)
        except json.JSONDecodeError:
            memoriaUser = open('Dicionarios/user.json','w')
            memoriaUser.write('["User"]')
            memoriaUser.close()
        self.saudacoes = json.load(memoriaSau)
        memoria.close();
        memoriaDic.close();
        memoriaDia.close();
        memoriaUser.close();
        self.historico = [None];

# Metodo pensa, vai pegar a frase e retornar uma resposta
    def pensa(self, frase):
        frase = frase.lower()
        if frase in self.conhecidos:
                self.chave = frase
                form = self.frases[self.chave]
                array = form.split(" ");
                if 'pagantee' in array:
                    Banco3 = Banco('host','port', 'username', 'password', 'db')
                    pagante = Banco3.paganteAtuall()
                    if pagante != None:
                        if pagante[0] == "Erro":
                            resp = 'Estou com problemas de memória, tente novamente!'
                        elif pagante != 'Erro':
                            resp = self.frases[self.chave]
                            resp = form.replace('pagantee', pagante)
                        else:
                            resp = 'A coca de hoje já foi paga!!'
                        return resp
                    else:
                        resp = 'Ninguém paga hoje!'
                        return resp

        if frase in self.dia:
            self.chave = frase
            form = self.frases[self.chave]
            array = form.split(" ");
            elemento = 'diaa'
            pos_i = 0 # variável provisória de índice
            for i in range (len(array)): # procurar em todas as listas internas
                if elemento in array[i]: # se encontrarmos elemento ('diaa')
                    pos_i = i # guardamos o índice i
                    Banco4 = Banco('host','port', 'username', 'password', 'db')
                    dia = Banco4.meuDiadePagar(self.user[0])
                    dataAtual = datetime.now().strftime('%Y-%m-%d')
                    if dia == None:
                        resp = 'Ainda não sabemos o seu dia de pagar'
                    elif dataAtual == dia:
                        resp = "Hoje é seu dia de pagar a coca"
                    elif dia[0] == "Erro":
                        resp = 'Estou com problemas de memória, tente novamente!'
                    elif dia != "Erro":
                        resp = form.replace(array[pos_i], dia)
                    return resp
                    break # saímos do loop interno

        ultimaFrase = self.historico[-1]

        if 'kkkkkk' in frase:
            return 'Que graça kkk'

        if ultimaFrase == 'Digite a frase: ':
            self.chave = frase
            return 'Digite a resposta: '

        if ultimaFrase == 'Digite a resposta: ':
            array = frase.split(" ");
            frase = frase.lower()
            resp = frase
            elemento = 'pagantee'
            elemento2 = 'diaa'
            elemento3 = 'name'
            if elemento in array:
                self.frases[self.chave] = resp
                self.conhecidos.append(self.chave.lower())
                self.gravaMemoria()
            if elemento2 in array:
                self.frases[self.chave] = resp
                self.dia.append(self.chave.lower())
                self.gravaMemoria()
            if elemento3 in array:
                self.frases[self.chave] = resp
                self.saudacoes.append(self.chave.lower())
                self.gravaMemoria()

            else:
                self.frases[self.chave] = resp
                self.gravaMemoria()

            return 'Aprendido!!'

        if frase in self.frases:
            return self.frases[frase]

        if frase == 'aprendeer kalebe':
            return 'Digite a frase: '

        if ultimaFrase == 'Oi meu nome é Kalebinho, sou um bot que posso lhe dizer quem é o pagante do nosso refrigerante':
            nome = self.pegaNome(frase)
            return frase
        try:
            resp = eval(frase)
            return resp
        except:
            pass
        return "Não entendi, repete por gentileza malandrão"

    def pegaNome(self, nome):
        if 'o meu nome eh' in nome:
            nome = nome[14:]
        nome = nome.title()
        return nome
    def gravaMemoria(self):
            memoria = open('Dicionarios/'+self.nome+'.json','w')
            memoriaDic = open('Dicionarios/dic'+self.nome+'.json','w')
            memoriaDia = open('Dicionarios/dia.json','w')
            memoriaSau = open('Dicionarios/saudacoes.json','w')
            memoria.write('')
            memoriaDic.write('')
            memoriaDia.write('')
            memoriaSau.write('')
            with open('Dicionarios/'+self.nome+'.json','a') as f:
                json.dump(self.conhecidos, f, indent=4)
                print('\n', file=f)
            with open('Dicionarios/dic'+self.nome+'.json','a') as f:
                json.dump(self.frases, f, indent=4)
                print('\n', file=f)
            with open('Dicionarios/dia.json','a') as f:
                json.dump(self.dia, f, indent=4)
                print('\n', file=f)
            with open('Dicionarios/saudacoes.json','a') as f:
                json.dump(self.saudacoes, f, indent=4)
                print('\n', file=f)
            memoria.close();
            memoriaDic.close();
            memoriaDia.close();
            memoriaSau.close();

    def fala(self, frase):
        self.historico.append(frase)
