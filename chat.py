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
DIRETO=""
TOPICO = ""
USERS=[]
USR=[]
CANAIS=[]
CLIENTE=0
topicovigente=0
ip_local = socket.gethostbyname(socket.gethostname())
control=0
BOOL=TRUE

def main_chat():
    global CANAIS,CLIENTE,USERS,TOPICO,NOME
    def criacanal():

        nome = cria_canal.get()
        print("nome",nome)
        aux=CLIENTE._in(('shared', 'canal', str))
        aux= aux+':'+nome
        CLIENTE._out(('shared', 'canal', aux))


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
    endereco.insert(0,"Chat no endereço: "+ip_local)
    endereco["state"]='disabled'

    endereco_muda=Button(janela,text="Mudar Servidor",command=mudaservidor)
    #endereco_muda.place(x=475,y=10)
    endereco.place(x=10,y=10)
    cria_canal = Entry(janela,width=10)
    cria_canal.place(x=600,y=10)

    botao_cria=Button(janela,text="Criar Canal",command=criacanal)
    botao_cria.place(x=670,y=10)



    topicos = Canvas(janela, bg='white', width=250, height=200)
    #botoes para os topicos

    def muda_canal(topic,button):
        global TOPICO,topicovigente
        print("entering",topic,button)
        CLIENTE2 = Client((ip_local, 5050))
        if TOPICO==topic:
            return
        if topicovigente!=0:
            topicovigente["bg"] = "#d3d3d3"
            topicovigente["fg"] = "black"
        print('topico',TOPICO)
        CLIENTE2._out((TOPICO, "mensagem publica", "mudou"))
        CLIENTE2._out((TOPICO, NOME, "mudou"))
        aux = CLIENTE2._in(('user', TOPICO, str))
        aux = aux.split(":")
        print("AUXILIAR",aux,"AUXILIAR")
        aux.remove(NOME)
        aux = ":".join(aux)
        print("users depois",aux)
        if (aux==""):
            CLIENTE2._out(('user', TOPICO, "VAZIO"))
        else:
            CLIENTE2._out(('user', TOPICO, aux))
        CLIENTE2.close()
        TOPICO=topic
        for i in USR:
            i.destroy()
        button["bg"]="black"
        button["fg"] = "white"
        topicovigente=button
        get_users()

    def srt(text):
        global DIRETO
        DIRETO=text
        lbl_direto["text"]=DIRETO


    def get_users():
        global USERS,USR,ip_local,TOPICO
        CLIENTE2 = Client((ip_local, 5050))
        aux2 = CLIENTE2._in(('user', TOPICO, str))
        if aux2 == 'VAZIO':
            CLIENTE2._out(('user', TOPICO, NOME))
            user = Button(users, text=NOME,state=DISABLED)
            USERS.append(NOME)
            USR.insert(0, user)
            user.grid(row=0)
            return
        CLIENTE2._out(('user', TOPICO, aux2 + ":" + NOME))
        print(USERS,"USERS")
        aux2=NOME+":"+aux2
        USERS=aux2.split(":")

        print("teste envio",CLIENTE2._rd(('user', TOPICO, str)))
        CLIENTE2.close()
        atualizanome()


    def atualizanome():
        global USR,USERS
        CLIENTE2 = Client((ip_local, 5050))
        aux = CLIENTE2._rd(('user', TOPICO, str))
        USERS = aux.split(":")
        for i in USR:
            i.destroy()
        USR = []
        for x in range(len(USERS)):
            user = Button(users, text=USERS[x])
            user["command"]=partial(srt,USERS[x])
            if(USERS[x]==NOME):
                user["state"]=DISABLED
            USR.insert(x,user)
            user.grid(row=x)
        CLIENTE2.close()


    def inclui_canais(inicio):
        for x in range(inicio,len(CANAIS)):
            topic = Button(topicos,text=CANAIS[x],bg='#d3d3d3')
            topic["command"]=partial(muda_canal,CANAIS[x],topic)
            topic.grid(padx=5,row=0,column=x)
            CLIENTE._out(('user', CANAIS[x], "VAZIO"))

    inclui_canais(0)

    topicos.place(x=10,y=40)

    atualizar=Button(janela,text="Atualizar Usuarios",command=atualizanome)
    atualizar.place(x=650, y=40)

    users = Canvas(janela, width=100, height=500)

    users.place(x=650,y=70)
    #botoes para os topicos

    def insert_public():  ###metodo de INSERIR MENSAGEM
        texto=entry_group.get()
        CLIENTE._out((TOPICO,"mensagem publica",NOME+": "+TOPICO+": "+texto))
        entry_group.delete(0,END)
        #time.sleep(1)
        CLIENTE._in((TOPICO, "mensagem publica", str))

    def insert_private():  ###metodo de INSERIR MENSAGEM

        texto=entry_private.get()
        CLIENTE._out((TOPICO, DIRETO, NOME + ": " + TOPICO + ": " + texto))
        chat_private.configure(state='normal')
        chat_private.insert(END, NOME+": "+TOPICO+": "+texto)
        chat_private.insert(END, "\n")
        chat_private.see('end')
        chat_private.configure(state='disabled')
        entry_private.delete(0,END)
        CLIENTE._in((TOPICO, DIRETO, str))

    chat_public = ScrolledText(janela, width=75, height=10, state='disabled')
    chat_public.place(x=10, y=70)
    entry_group = Entry(janela, width=75)
    entry_group.place(x=10,y=245)
    send_group = Button(janela, text="Enviar Grupo", command=insert_public)
    send_group.place(x=475, y=245)

    lbl_direto=Label(janela, width=20, text=DIRETO)
    lbl_direto.place(x=10, y=270)

    chat_private = ScrolledText(janela, width=75, height=10, state='disabled')
    chat_private.place(x=10, y=300)
    entry_private = Entry(janela, width=75)
    entry_private.place(x=10, y=475)
    send_private = Button(janela, text="Enviar Privado", command=insert_private)
    send_private.place(x=475, y=475)


    def msg_publica():
        global BOOL
        CLIENTE2 = Client((ip_local, 5050))
        while BOOL:
            mensagem_publica=CLIENTE2._rd((TOPICO,"mensagem publica", str))
            if(mensagem_publica=="mudou"):
                CLIENTE._in((TOPICO,"mensagem publica", str))
                time.sleep(2)
            else:
                chat_public.configure(state='normal')
                chat_public.insert(END, mensagem_publica)
                chat_public.insert(END, "\n")
                chat_public.see('end')
                chat_public.configure(state='disabled')

    def msg_particular():
        global BOOL
        CLIENTE2 = Client((ip_local, 5050))
        while BOOL:
            mensagem_particular=CLIENTE2._rd((TOPICO,NOME, str))
            if(mensagem_particular=="mudou"):
                CLIENTE._in((TOPICO,NOME, str))
                time.sleep(2)
            else:
                chat_private.configure(state='normal')
                chat_private.insert(END, mensagem_particular)
                chat_private.insert(END, "\n")
                chat_private.see('end')
                chat_private.configure(state='disabled')

    privado = threading.Thread(target=msg_particular)
    privado.start()
    publico = threading.Thread(target=msg_publica)
    publico.start()

    def mensagem():
        global BOOL
        time.sleep(10)

        while BOOL:
            print("msg",CLIENTE._rd((TOPICO,"mensagem publica", str)))
        #publico = CLIENTE._rd(('mensagem', TOPICO, str))
        #print("msg", publico)
        #private = CLIENTE._rd((NOME, TOPICO, str))
        #print("msg",private)
        #print(publico,"msg",private)

    msg = threading.Thread(target=mensagem)
    #msg.start()


    def canais():
        global CANAIS
        while BOOL:
            time.sleep(2)
            atualizanome()
            aux=CLIENTE._rd(('shared', 'canal', str)).split(":")
            if len(aux)>len(CANAIS):
                inicio =len(CANAIS)
                CANAIS= aux
                inclui_canais(inicio)

    canal=threading.Thread(target=canais)
    canal.start()

    janela.mainloop()



def define_nome():

    def iniciar():
        global NOME, CLIENTE,USERS,CANAIS,TOPICO,ip_local
        NOME=nome.get()
        try:
            CLIENTE=Client((endereco.get(), 5050))
            ip_local=endereco.get()
            aux=CLIENTE._in(('user', 'publico', str))

            if(aux=="VAZIO"):
                CLIENTE._out(('user', 'publico', NOME))
                USERS.append(NOME)
            else:
                CLIENTE._out(('user', 'publico', aux + ':' + NOME))
                aux = NOME + ":" + aux
                USERS = aux.split(":")
            TOPICO = 'publico'
            CANAIS=CLIENTE._rd(('shared', 'canal', str)).split(":")

        except:
            if(messagebox.askyesno(title="Servidor não existe", message=f"Servidor não existe, deseja iniciar um no ip{ip_local}?")):
                server = threading.Thread(target=lambda: Server.start_server(host=ip_local))
                server.start()
                CLIENTE = Client((endereco.get(), 5050))
                CLIENTE._out(('user', 'publico', NOME))
                CLIENTE._out(('user', 'todos', "VAZIO"))
                CLIENTE._out(('user', 'auxiliar', "VAZIO"))
                TOPICO='publico'
                CLIENTE._out(('shared', 'canal', 'publico:todos:auxiliar'))
                CANAIS='publico:todos:auxiliar'.split(":")

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


