import random
import socket
import threading
import time
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from pubsub.client import Client
from pubsub.server import Server
from functools import partial
NOME = ""
TOPICO = ""
USERS=[]
USR=[]
CANAIS=[]
CLIENTE=0
topicovigente=0
ip_local = socket.gethostbyname(socket.gethostname())
control=0

def main_chat():
    global CANAIS,CLIENTE,USERS,TOPICO,NOME
    def criacanal():

        nome = cria_canal.get()
        print("nome",nome)
        aux=CLIENTE._in(('shared', 'canal', str))
        aux= aux+':'+nome
        CLIENTE._out(('shared', 'canal', aux))
        #CLIENTE._out(('controle', "publico", "canal"))
       # time.sleep(11)
        #CLIENTE._in(('controle', "publico", str))
        pass

    def mudaservidor():
        pass

    def sendprivado():
        pass
    def sendgroup():
        pass


    janela = Tk()
    janela.geometry(("800x600"))




    janela.resizable(False, False)
    endereco = Entry(janela,width=75)

    endereco_muda=Button(janela,text="Mudar Servidor",command=mudaservidor)
    endereco_muda.place(x=475,y=10)
    endereco.place(x=10,y=10)
    cria_canal = Entry(janela,width=10)
    cria_canal.place(x=600,y=10)

    botao_cria=Button(janela,text="Criar Canal",command=criacanal)
    botao_cria.place(x=670,y=10)



    topicos = Canvas(janela, bg='white', width=250, height=200)
    #botoes para os topicos
    print(CANAIS,len(CANAIS))

    def muda_canal(x,y):
        global TOPICO,topicovigente
        if topicovigente!=0:
            topicovigente["bg"] = "#d3d3d3"
            topicovigente["fg"] = "black"
        TOPICO=x
        print(TOPICO)
        y["bg"]="black"
        y["fg"] = "white"
        topicovigente=y
        get_users(TOPICO)

    def srt():
        print("usr")
    def get_users(topico):
        global USERS,USR
        aux = CLIENTE._in(('user', topico, str))

        USERS=aux.split(":")
        try:
            USERS.index(NOME)
            CLIENTE._out(('user', topico, aux))
        except:
            print(aux + ':' + NOME)
            CLIENTE._out(('user', topico, CLIENTE._out(('user', topico, aux + ':' + NOME))))


        USR=[]
        for x in range(len(USERS)):
            user = Button(users, text=USERS[x],command=srt)
            USR.insert(x,user)
            user.grid(row=x)
    def inclui_canais(inicio):
        for x in range(inicio,len(CANAIS)):

            topic = Button(topicos,text=CANAIS[x],bg='#d3d3d3')
            topic["command"]=partial(muda_canal,CANAIS[x],topic)
            topic.grid(padx=5,row=0,column=x)
    inclui_canais(0)

    topicos.place(x=10,y=40)

    users = Canvas(janela, width=100, height=500)

    users.place(x=650,y=70)
    #botoes para os topicos
    def insert_public():  ###metodo de INSERIR MENSAGEM
        chat_public.configure(state='normal')
        chat_public.insert(END, NOME+": "+TOPICO+": "+entry_group.get())
        chat_public.insert(END, "\n")
        chat_public.see('end')
        chat_public.configure(state='disabled')
        entry_group.delete(0,END)

    def insert_private():  ###metodo de INSERIR MENSAGEM
        chat_private.configure(state='normal')
        print(entry_private.get())
        chat_private.insert(END, NOME+": "+TOPICO+": "+entry_private.get())
        chat_private.insert(END, "\n")
        chat_private.see('end')
        chat_private.configure(state='disabled')
        entry_private.delete(0,END)

    chat_public = ScrolledText(janela, width=75, height=10, state='disabled')
    chat_public.place(x=10, y=70)
    entry_group = Entry(janela, width=75)
    entry_group.place(x=10,y=245)
    send_group = Button(janela, text="Enviar Grupo", command=insert_public)
    send_group.place(x=475, y=245)

    chat_private = ScrolledText(janela, width=75, height=10, state='disabled')
    chat_private.place(x=10, y=300)
    entry_private = Entry(janela, width=75)
    entry_private.place(x=10, y=475)
    send_private = Button(janela, text="Enviar Privado", command=insert_private)
    send_private.place(x=475, y=475)








    def controle():
        global CANAIS,TOPICO,CLIENTE
        i=1
        while TOPICO=='':

            time.sleep(3)
        while True:
            aux=CLIENTE._rd(('controle', 'publico', str))
            print('aux',aux)
            time.sleep(10)
            if aux == "user":
                get_users(TOPICO)
            elif aux == "canal":
                print("canais")
                CANAIS=CLIENTE._rd(('shared', 'canal', str)).split(":")
                for x in range(len(CANAIS)):
                    topic = Button(topicos, text=CANAIS[x], bg='#d3d3d3')
                    topic["command"] = partial(muda_canal, CANAIS[x], topic)
                    topic.grid(padx=5, row=0, column=x)

    def canais():
        global CANAIS
        while True:
            time.sleep(2)
            aux=CLIENTE._rd(('shared', 'canal', str)).split(":")
            print(aux,len(aux),len(CANAIS))
            if len(aux)>len(CANAIS):
                inicio =len(CANAIS)
                CANAIS= aux
                inclui_canais(inicio)



    canal=threading.Thread(target=canais)
    canal.start()
    control = threading.Thread(target=controle)
    control.start()
    CLIENTE._out(('controle', 'publico', "user"))

    janela.mainloop()



def define_nome():

    def iniciar():
        global NOME, CLIENTE,USERS,CANAIS
        NOME=nome.get()
        try:
            CLIENTE=Client((endereco.get(), 5050))
            aux=CLIENTE._in(('user', 'publico', str))
            USERS=aux.split(":")
            CLIENTE._out(('user', 'publico', aux+':'+NOME))
            CANAIS=CLIENTE._rd(('shared', 'canal', str)).split(":")

        except:
            if(messagebox.askyesno(title="Servidor não existe", message=f"Servidor não existe, deseja iniciar um no ip{ip_local}?")):
                server = threading.Thread(target=lambda: Server.start_server(host=ip_local))
                server.start()
                CLIENTE = Client((endereco.get(), 5050))
                CLIENTE._out(('user', 'publico', NOME))
                CLIENTE._out(('user', 'todos', NOME))
                CLIENTE._out(('user', 'auxiliar', NOME))
                TOPICO='publico'
                CLIENTE._out(('shared', 'canal', 'publico:todos:auxiliar'))

                CANAIS='publico:todos:auxiliar'.split(":")
                print(CANAIS)
            else:
                return

        janela.destroy()
        main_chat()

    janela = Tk()
    janela.geometry(("150x150"))
    endereco=Entry(janela,width=20)
    nome=Entry(janela,width=20)
    iniciar = Button(janela,text="Inicar Chat",command=iniciar)



    endereco.insert(0,ip_local)
    aux = "Usuário" + str(random.randint(10000, 100000))
    nome.insert(0,aux)
    nome.grid(pady=10,padx=10,row=0)
    endereco.grid(pady=10,padx=10,row=1)
    iniciar.grid(pady=10,padx=10,row=2)
    janela.mainloop()


define_nome()


