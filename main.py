import tkinter as tk
from pyad import *
from pythonping import ping
import pyad.adquery
import random
import string


#função para gerar senha aleatoria
def gerar_senha():
    letras_maiusculas = string.ascii_uppercase
    letras_minusculas = string.ascii_lowercase
    digitos = string.digits
    simbolos = string.punctuation

    caracteres = letras_maiusculas + letras_minusculas + digitos + simbolos
    #elimina caracteres dificeis de encontrar
    eliminadificeis=['¨',"'",'´','|','§','~','º','ª','^',',','`','"','<','>','?']
    for i in eliminadificeis:
        caracteres=caracteres.replace(i, '#')

    senha = ''.join(random.choice(caracteres) for _ in range(12))

    return senha


#testa conexão com o servidor onde esta o DC
def teste_conect(host):
    try:
        pingar = ping(host, count=2, verbose=False,timeout=1)
        if all(response.success for response in pingar):
            return ('Conexão com o AD ok')
        else:
            return ('Sem conexão com o AD (Verifique sua conexão com a rede Enaex ou VPN)')
    except:
        pass
resultadoping = teste_conect('10.60.30.3')
search = pyad.adquery.ADQuery()
#procura o usuario digitado no campo do TK
def procurausuario(samaccountname):
    samaccountname = search.execute_query(
        attributes=['cn', 'sAMAccountName', 'mail'],
        where_clause="sAMAccountName = '{}'".format(samaccountname)
    )

    for row in search.get_results():
        user = aduser.ADUser.from_cn(row['cn'])
        resultado = [('CPF:', user.get_attribute('cpf')), ('Matricula:', user.get_attribute('matricula')),('Nascimento:', user.get_attribute('birthday'))]

        resultado2 = str(resultado)
       #limpa o resultado da pesquisa para mostrar um resultado mais clean
        elimina = ['[', ']', ',', '"', ')', '(', "'"]
        for i in elimina:
            resultado2 = resultado2.replace(i, ' ')

        return resultado2


    return 'Usuário não encontrado :C'
#função criada para mostrar o resultado no TK
def buscar_usuario():
    resultado = procurausuario(username.get())
    lbl_resultado_var.set(resultado)

#função para ativar o botao
def recuperaresultado():
    resultadosenha = gerar_senha()
    caixa_texto.delete(1.0, tk.END)
    caixa_texto.insert(tk.END, resultadosenha)
##configuração de janela e widgets do TK
janela = tk.Tk()

#janela.iconbitmap(# icone que deseja usar )
janela.geometry('500x220')
janela.title('EasyCheck')
janela.minsize(500, 220)
janela.maxsize(500, 220)

lbl_resultado_var = tk.StringVar()
lbl_resultado = tk.Label(janela, textvariable=lbl_resultado_var)
lbl_resultado.grid(row=10, column=1, columnspan=4)

lbl_conexao_var = tk.Label()
lbl_conexao = tk.Label(janela, text=f'{resultadoping}')
lbl_conexao.place(relx=0.0, rely=1.0,anchor='sw')

texto = tk.Label(janela, text="Digite um usuário")
texto.grid(column=1, row=0, columnspan=4)

username = tk.Entry(janela, width=85)
username.grid(column=1, row=1, columnspan=4)

botao = tk.Button(janela, text="Buscar", command=buscar_usuario)
botao.place(relx=0.5,rely=0.4,anchor='center')

caixa_texto = tk.Text(janela, wrap="word", height=1, width=24)
caixa_texto.place(relx=0.5, rely=0.7, anchor='center')


botaosenha = tk.Button(janela, text='Gerar Senha', command=recuperaresultado)
botaosenha.place(relx=0.5, rely=0.56,anchor='center')




janela.mainloop()

