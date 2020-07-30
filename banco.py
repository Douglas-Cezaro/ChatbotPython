import mysql.connector
from datetime import datetime
import json
class Banco():
    def __init__(self, host,port, user, password, database):
        try:
            self.mydb = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
                )
            self.mydberror = []
            self.mydberror.append("Sucesso")
            self.dataAtual = datetime.now().strftime('%Y-%m-%d')
        except mysql.connector.Error as err:
            self.mydberror = []
            cod = "Cod error: ", err.errno # error number
            msg = "Mensagem error: ", err.msg  # error message
            self.mydberror.append("Erro")
            self.mydberror.append(cod)
            self.mydberror.append(msg)

    def paganteAtuall(self):
        if self.mydberror[0] == "Erro":
            return self.mydberror
        else:
            mycursor = self.mydb.cursor()
            paganteAtual = mycursor.execute("SELECT pagantes.nome FROM controlecoca inner join pagantes on controlecoca.codPagante = pagantes.id where data= '"+self.dataAtual+"' and pago <> 'PAGO'")
            myresult = mycursor.fetchall()
            text = 'zero'
            for x in myresult:
                text = ''.join(x)
                return text

    def paganteAtual(self):
        if self.mydberror[0] == "Erro":
            return self.mydberror
        else:
            mycursor = self.mydb.cursor()
            paganteAtual = mycursor.execute("SELECT pagantes.nome,controlecoca.pago FROM controlecoca inner join pagantes on controlecoca.codPagante = pagantes.id where data= '"+self.dataAtual+"'")
            myresult = mycursor.fetchall()
            for x in myresult:
                return x

    def meuDiadePagar(self, pagante):
        if self.mydberror[0] == "Erro":
            return self.mydberror
        else:
            mycursor = self.mydb.cursor()
            meuDiadePagar = mycursor.execute("SELECT controlecoca.data FROM controlecoca inner join pagantes on controlecoca.codPagante = pagantes.id where controlecoca.pago <> 'PAGO'  and pagantes.nome like '%"+pagante+"%'")
            myresult = mycursor.fetchall()
            text = ''
            mycursor.close()
            for x in myresult:
                text = ''.join(x)
                return text

    def pagantes(self, pagante):
        if self.mydberror[0] == "Erro":
            return self.mydberror
        else:
            mycursor = self.mydb.cursor()
            meuDiadePagar = mycursor.execute("select nome from pagantes where inativo <> 'T' and nome like '%"+pagante+"%'")
            myresult = mycursor.fetchall()
            array = []
            for x in myresult:
                text = ''.join(x)
                array.append(text)
            return array

    def meuUltimopag(self, pagante):
        if self.mydberror[0] == "Erro":
            return self.mydberror
        else:
            mycursor = self.mydb.cursor()
            meuDiadePagar = mycursor.execute("SELECT controlecoca.data FROM controlecoca inner join pagantes on controlecoca.codPagante = pagantes.id where controlecoca.pago = 'PAGO'  and pagantes.nome like '%"+pagante+"%' order by data desc limit 1")
            myresult = mycursor.fetchall()
            text = 'teste'
            array = []
            for x in myresult:
                text = ''.join(x)
                array.append(text)
            return array
