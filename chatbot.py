import json
from banco import *
import os
from datetime import datetime
class Chatbot():
    def __init__(self, nome):
        try:
            memoriaDic = open('Dicionarios/dic'+nome+'.json','r')
            memoriaUser = open('Dicionarios/user.json','r')
        except FileNotFoundError:
            if os.path.exists('Dicionarios') == False:
                os.mkdir("Dicionarios")
            memoriaDic = open('Dicionarios/dic'+nome+'.json','w')
            memoriaUser = open('Dicionarios/user.json','w')
            memoriaDic.write('{"oi":"Meu nome é Bot, tudo bem?", "tchau": "tchau"}')
            memoriaUser.write('["User"]')
            memoriaDic.close();
            memoriaDic = open('Dicionarios/dic'+nome+'.json','r')
            memoriaUser = open('Dicionarios/user.json','r')
        self.frases  = json.load(memoriaDic)
        try:
            self.user = json.load(memoriaUser)
        except json.JSONDecodeError:
            memoriaUser = open('Dicionarios/user.json','w')
            memoriaUser.write('["User"]')
            memoriaUser.close()
        memoriaDic.close();
        memoriaUser.close();
        self.historico = [None];

# Metodo pensa, vai pegar a frase e retornar uma resposta
    def pensa(self, frase):
        frase = frase.lower()
        ultimaFrase = self.historico[-1]

        if 'kkkkkk' in frase:
            return 'Que graça kkk'

        if ultimaFrase == 'Digite a frase: ':
            self.chave = frase
            return 'Digite a resposta: '

        if ultimaFrase == 'Digite a resposta: ':
            frase = frase.lower()
            resp = frase
            self.frases[self.chave] = resp
            self.gravaMemoria()

            return 'Aprendido!!'

        if frase in self.frases:
            return self.frases[frase]

        # palavra chave para bot aprender
        if frase == 'aprender':
            return 'Digite a frase: '
            
        try:
            resp = eval(frase)
            return resp
        except:
            pass
        return "Não entendi, repete por gentileza malandrão"

# metodo para gravar frases
    def gravaMemoria(self):
            memoriaDic = open('Dicionarios/dic'+self.nome+'.json','w')
            memoriaDic.write('')
            with open('Dicionarios/dic'+self.nome+'.json','a') as f:
                json.dump(self.frases, f, indent=4)
                print('\n', file=f)
            memoriaDic.close();

    def fala(self, frase):
        self.historico.append(frase)
