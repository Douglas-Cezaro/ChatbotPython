import mysql.connector
from datetime import datetime
import json
class Banco():
    def __init__(self, host,port, user, password, database):
        # Validação de erros com try except
        try:
            self.mydb = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
                )
            # Se acaso ocorrer tudo certo self.mydberror terá o valor "Sucesso"
            self.mydberror = []
            self.mydberror.append("Sucesso")
            self.dataAtual = datetime.now().strftime('%Y-%m-%d')
        except mysql.connector.Error as err:
            # Se acaso ocorrer erro a self.mydberror terá o valor Erro, código do erro e a mensagem do erro
            self.mydberror = []
            cod = "Cod error: ", err.errno # código do erro
            msg = "Mensagem error: ", err.msg  # mensagem de erro
            self.mydberror.append("Erro")
            self.mydberror.append(cod)
            self.mydberror.append(msg)

    # Criar os métodos que vão ser utilizados no chatbot
    def teste(self):
        # antes de tentar executar o SQL, precisamos validar senão ocorreu erro
        if self.mydberror[0] == "Erro":
            # se self.mydberror[0] for igual a "Erro" quer dizer que ocorreu algum erro de comunicação com o banco de dados
            # irá retornar os erros
            return self.mydberror

        else:
            # se der tudo certo, vai ser executado o SQL
            # passando pelo try except
            try:
                mycursor = self.mydb.cursor()
                teste = mycursor.execute("SELECT * FROM teste ")
                myresult = mycursor.fetchall()
                return myresult
                
            except mysql.connector.Error as err:
                return err