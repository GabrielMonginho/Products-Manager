from tkinter import ttk
from tkinter import *
import sqlite3


class Produto:
    db='database/produtos.db'
    def __init__(self, root):
        self.janela=root
        self.janela.title("App Gestor de Produtos")  # Título da janela
        self.janela.resizable(1, 1)  # Ativar a redimensionamento da janela. Para desativá - la: (0, 0)
        self.janela.wm_iconbitmap('recursos/icon.ico')
        self.janela.geometry("400x650")


        frame=LabelFrame(self.janela, text="Registar um novo Produto", font=('Calibri', 16, 'bold'))
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20) #columnspan indica o comprimento

        # Label Nome
        self.etiqueta_nome = Label(frame,text="Nome: ", font=('Calibri', 13))  # Etiqueta de texto localizada no frame
        self.etiqueta_nome.grid(row = 1, column = 0) # Posicionamento através de grid
        # Entry Nome (caixa de texto que irá receber o nome)
        self.nome= Entry(frame, font=('Calibri', 13)) # Caixa de texto (input de texto) localizada no frame
        self.nome.focus() # Para que o foco do rato vá a esta Entry no início
        self.nome.grid(row = 1, column = 1)

        # Label Preço
        self.etiqueta_preço= Label(frame, text=('Preço: '), font=('Calibri', 13)) # Etiqueta de texto localizada no frame

        self.etiqueta_preço.grid(row = 2, column = 0) # Entry Preço (caixa de texto que irá receber o preço)
        self.preço= Entry(frame, font=('Calibri', 13)) # Caixa de texto (input de texto) localizada no frame
        self.preço.grid(row = 2, column = 1)

        self.mensagem= Label(text='', fg='red')
        self.mensagem.grid(row=3, column = 0, columnspan = 2, sticky=(W+E))

        #Button Guardar
        s=ttk.Style()
        s.configure('my.TButton',font=('Calibri', 14, 'bold'))
        self.adicionar_produto= ttk.Button(frame, text="Guardar Produto", command=self.add_produto, style='my.TButton')
        self.adicionar_produto.grid(row = 3, columnspan = 2, sticky=W+E)




        #Tabela de produtos

        style=ttk.Style()
        style.configure("mystyle.Treeview",highlightthickness=0, bd=0,font=('Calibri',11))
        style.configure("mystyle.Treeview.Heading", font=('Calibri',13,'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea',{'sticky': 'nswe'})]) # Eliminar as bordas

        #Estrutura da tabela
        self.tabela=ttk.Treeview(height = 20,columns = 2, style="mystyle.Treeview")
        self.tabela.grid(row=4, column = 0, columnspan = 2)
        self.tabela.heading('#0', text="Nome", anchor=CENTER)
        self.tabela.heading('#1', text="Preço", anchor=CENTER)


        #Botão Eliminar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.eliminar=ttk.Button(text='ELIMINAR', command=self.del_produto, style='my.TButton')
        self.eliminar.grid(row=5, column = 0, sticky=W+E)
        self.editar=ttk.Button(text='EDITAR', command=self.edit_produto, style='my.TButton')
        self.editar.grid(row=5, column=1, sticky=W+E)

        # Chamada ao método get_produtos() para obter a listagem de produtos ao início da app
        self.get_produtos()



    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con: # Iniciamos uma conexão com a base de dados (alias con)
            cursor=con.cursor() # Criamos um cursor da conexão para poder operar na base de dados
            resultado=cursor.execute(consulta, parametros) # Preparar a consulta SQL (com parâmetros se os há)
            con.commit() # Executar a consulta SQL preparada anteriormente
        return resultado # Restituir o resultado da consulta SQL

    def get_produtos(self):
        # O primeiro, ao iniciar a app, vamos limpar a tabela se tiver dados residuais ou antigos

        registos_tabela = self.tabela.get_children()# Obter todos os dados da tabela
        for linha in registos_tabela:
            self.tabela.delete(linha)

        # Consulta SQL
        query = 'SELECT * FROM produto ORDER BY id DESC'
        registos_db = self.db_consulta(query) # Faz-se a chamada ao método db_consultas
        print(registos_db) # Mostram-se os resultados

        for linha in registos_db:
            print(linha)
            self.tabela.insert('',0, text=linha[1], values=linha[2])



    def validação_nome(self):
        nome_input=self.nome.get()
        return len(nome_input) != 0

    def validação_preço(self):
        preço_input = self.preço.get()
        return len(preço_input) != 0

    def add_produto(self):
        if self.validação_nome() and self.validação_preço():
            query='INSERT INTO produto Values(NULL,?,?)'
            self.db_consulta(query, parametros=(self.nome.get(), self.preço.get()))
            self.mensagem['text'] = 'Produto {} adicionado com êxito'.format(self.nome.get()) # Label localizada entre o botão e a tabela
            self.nome.delete(0,END)
            self.preço.delete(0,END)
            self.get_produtos()
            #Para Debug
            #print(self.nome.get())
            #print(self.preço.get())

        elif self.validação_nome() and self.validação_preço() == False:
            self.mensagem['text'] = "O preço é obrigatório"
        elif self.validação_nome() == False and self.validação_preço():
            self.mensagem['text'] = "O nome é obrigatório"
        else:
            self.mensagem['text'] = "O nome e preço são obrigatórios"



    def del_produto(self):
        #Para debug
        #print(self.tabela.item(self.tabela.selection()))
        #print(self.tabela.item(self.tabela.selection())['text'])
        #print(self.tabela.item(self.tabela.selection())['values'])
        #print(self.tabela.item(self.tabela.selection())['values'][0])
        self.mensagem['text'] = ''
        try:
            self.tabela.item(self.tabela.selection())['text'][0]
        except IndexError as e:
            self.mensagem['text'] = 'Por favor,selecione um produto'
            return

        self.mensagem['text'] = ''
        nome=self.tabela.item(self.tabela.selection())['text']
        query='DELETE FROM produto WHERE nome=?'
        self.db_consulta(query,(nome,))
        self.mensagem['text'] = 'Produto {} eliminado com êxito'.format(nome)
        self.get_produtos()


    def edit_produto(self):
        self.mensagem['text'] = ''
        try:
            self.tabela.item(self.tabela.selection())['text'][0]
        except IndexError as e:
            self.mensagem['text'] = 'Por favor,selecione um produto'
            return

        self.mensagem['text'] = ''
        nome=self.tabela.item(self.tabela.selection())['text']
        old_preço=self.tabela.item(self.tabela.selection())['values'][0]

        self.janela_editar=Toplevel()
        self.janela_editar.title('Editar Produto')
        self.janela_editar.resizable(1,1)
        self.janela_editar.wm_iconbitmap('recursos/icon.ico')

        titulo=Label(self.janela_editar,text='Edição de Produtos', font=('Calibri', 30, 'bold'))
        titulo.grid(row=0, column = 0)
        frame_ep=LabelFrame(self.janela_editar, text='Editar o seguinte Produto', font=('Calibri', 16, 'bold'))
        frame_ep.grid(row = 1, column = 0, columnspan = 20, pady = 20)
        self.etiqueta_nome_antigo=Label(frame_ep, text='Nome antigo: ', font=('Calibri', 13))
        self.etiqueta_nome_antigo.grid(row = 2,column = 0)

        self.input_nome_antigo=Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=nome), state='readonly', font=('Calibri', 13))
        self.input_nome_antigo.grid(row = 2, column = 1)

        self.etiqueta_novo_nome=Label(frame_ep, text = 'Novo nome: ', font=('Calibri', 13))
        self.etiqueta_novo_nome.grid(row = 3, column = 0)
        self.input_nome_novo=Entry(frame_ep, font=('Calibri', 13))
        self.input_nome_novo.grid(row = 3, column = 1)
        self.input_nome_novo.focus()

        self.etiqueta_preço_antigo=Label(frame_ep, text='Preço antigo: ', font=('Calibri', 13))
        self.etiqueta_preço_antigo.grid(row=4, column=0)
        self.input_preço_antigo=Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=old_preço), state='readonly', font=('Calibri', 13))
        self.input_preço_antigo.grid(row=4, column=1)

        self.etiqueta_preço_novo=Label(frame_ep, text='Preço Novo: ', font=('Calibri', 13))
        self.etiqueta_preço_novo.grid(row=5, column=0)
        self.input_preço_novo=Entry(frame_ep, font=('Calibri', 13))
        self.input_preço_novo.grid(row=5, column=1)

        #Botão Atualizar Produto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.botao_atualizar=ttk.Button(frame_ep, text='Atualizar Produto', style='my.TButton', command=lambda:
        self.atualizar_produtos(self.input_nome_novo.get(),
        self.input_nome_antigo.get(),
        self.input_preço_novo.get(),
        self.input_preço_antigo.get()))

        self.botao_atualizar.grid(row=6, columnspan=2, sticky=W+E)

    def atualizar_produtos(self, nome_novo, nome_antigo, preço_novo, preço_antigo):
        query = 'UPDATE produto SET nome=?,preço=? WHERE nome=? AND preço=?'
        produto_modificado = False

        if nome_novo != '' and preço_novo != '':
            parametros = (nome_novo, preço_novo, nome_antigo, preço_antigo)
            produto_modificado = True
        elif nome_novo == '' and preço_novo != '':
            parametros = (nome_antigo,preço_novo, nome_antigo, preço_antigo)
            produto_modificado = True
        elif nome_novo != '' and preço_novo == '':
            parametros = (nome_novo,preço_antigo,nome_antigo,preço_antigo)
            produto_modificado = True

        if(produto_modificado):
            self.db_consulta(query, parametros)
            self.janela_editar.destroy()
            self.mensagem['text'] = 'Produto {} foi alterado com êxito'.format(nome_antigo)
            self.get_produtos()
        else:
            self.janela_editar.destroy()
            self.mensagem['text'] = 'Produto {} NÃO foi atualizado'.format(nome_antigo)


if __name__=='__main__':
    root=Tk() # Instância da janela principal
    app=Produto(root)  # Envia-se para a classe Produto o controlo sobre a janela root
    root.mainloop() # Começamos o ciclo de aplicação, é como um while True

