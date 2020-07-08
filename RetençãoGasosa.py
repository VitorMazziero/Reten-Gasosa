#Importação das bibliotecas
import tkinter as tk #Janela
import serial #Importação de dados do Arduino
import serial.tools.list_ports
import time #Contadores
import matplotlib.animation as animation
import matplotlib as plt; #Gráficos

from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style
from PIL import Image, ImageTk #Imagens e redimensionamento
from itertools import count 
from threading import Timer

#GIF do reator
class ImageLabel(tk.Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()
    def unload(self):
        self.config(image=None)
        self.frames = None
    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

#Imagens
def proxima(): #Airlift GIF
    lbl = ImageLabel(root)
    lbl.grid(row=0, column=19, rowspan=20, columnspan=2)
    lbl.load('Imagem1.gif')
    lbl.configure(background='white')
 
def anterior(): #Airlift sem bolha
    root.original1 = Image.open('Imagem2.gif') #Nome da imagem - Local da imagem > pasta do arquivo
    resized1 = root.original1.resize((155, 473),Image.ANTIALIAS) #Mudança de escala
    root.image1 = ImageTk.PhotoImage(resized1) 
    root.display1 = Label(root, image = root.image1)
    root.display1.grid(row=0, column=19, rowspan=20, columnspan=2) #Local na janela
    root.display1.configure(background='white')

#Início da janela 'root'
root = tk.Tk()
root.title('Retenção Gasosa') #Título do programa
root.configure(background='white') #plano de fundo da janela
plt.use("TkAgg") #Gráficos em tkinter

#Início da janela no centro da área de trabalho
w = 1250 
h = 675 
ws = root.winfo_screenwidth() #Largura da janela
hs = root.winfo_screenheight() # Altura da tela
x = (ws/2) - (w/2)
y = ((hs/2)-35) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

#Ícone do Programa
img = PhotoImage(file='ico.png') 
root.tk.call('wm', 'iconphoto', root._w, img)

#Imagem de fundo
root.original = Image.open('Imagem12.png') #Nome da imagem - Local da imagem > pasta do arquivo
resized = root.original.resize((1250, 675),Image.ANTIALIAS) #Mudança de escala
root.image = ImageTk.PhotoImage(resized) 
root.display = Label(root, image = root.image)
root.display.grid(row=0, column=0, columnspan=21, rowspan=22) #Local na janela
root.display.configure(background='white')

root.original8 = Image.open('1.PNG') 
resized8 = root.original8.resize((244, 18),Image.ANTIALIAS) 
root.image8 = ImageTk.PhotoImage(resized8) 
root.display8 = Label(root, image = root.image8)
root.display8.grid(row=19, column=19, columnspan=2) 
root.display8.configure(background='white')
    
#Parâmetros iniciais
#Entradas
Passo1=StringVar() #Diametro do reator
e2=Entry(root, textvariable=Passo1, width=10, justify= CENTER, font="Times 11", relief="flat", bd=5) #
e2.grid(row=1, column=0)
e2.insert(END, '0.125')
vol=StringVar() #Volume do reator
e7=Entry(root,textvariable=vol, width=10, justify= CENTER, font="Times 11", relief="flat", bd=5, background='white')
e7.grid(row=3, column=0)
e7.insert(END, '5')
Passo2=StringVar() #Distancia não aerado
e1=Entry(root,textvariable=Passo2, width=10, font="Times 11", justify= CENTER, relief="flat", bd=5)
e1.grid(row=11, column=4,columnspan=2)
reten=StringVar() #Retenção gasosa
e3=Entry(root,textvariable=reten, width=10, justify= CENTER, font="Times 11", relief="flat", bd=5)
e3.grid(row=11, column=12, columnspan=2)
dist=StringVar() #Distancia aerado
e6=Entry(root,textvariable=dist, width=10, justify= CENTER, font="Times 11", relief="flat", bd=5)
e6.grid(row=11, column=8, columnspan=2)
time1=StringVar() #Tempo de coleta de dados nao aerado
e4=Entry(root,textvariable=time1, width=10, justify= CENTER, font="Times 11", relief="flat", bd=5)
e4.grid(row=5, column=0)
e4.insert(END, '15')
time2=StringVar() #Tempo de coleta de dados aerado
e5=Entry(root,textvariable=time2, width=10, justify= CENTER, font="Times 11", relief="flat", bd=5)
e5.grid(row=7, column=0)
e5.insert(END, '45')
#Legendas 
l4=Label (root, text="PASSO 4:\n Distância entre sensor \n e líquido (com aeração) \nAperte 'Aerado' \nTempo de espera (s) \n↓", bd=5, relief="flat",
  font= "Times 11", width=19, bg='white', height=7)
l4.grid (row=6, column=0)
l2=Label (root, text="\nPASSO 1: \nDiâmetro do reator (m)\n↓", bd=5, relief="flat",
      font= "Times 11",width=19, bg='white')
l2.grid (row=0, column=0)
l2=Label (root, text="PASSO 2: \nVolume (L) \n↓", bd=5, relief="flat",
      font= "Times 11",width=19, bg='white')
l2.grid (row=2, column=0)
l3=Label (root, text="\nPASSO 3: \nDistância entre sensor \ne líquido (sem aeração) \nAperte 'Branco' \nTempo de espera (s) \n↓", bd=5, relief="flat",
      font= "Times 11", width=19, bg='white')
l3.grid (row=4, column=0)
l5=Label (root, text="Distância \n(sem aeração) (dsa)\n(cm)", bd=5, relief="flat",
              font= "Times 11",width=19, bg='white')
l5.grid (row=9, column=3,rowspan=2, columnspan=4)
l7=Label (root, text="Distância \n(aerado) (da)\n(cm)", bd=5, relief="flat",
      font= "Times 11",width=19, bg='white', height=2)
l7.grid (row=9, column=7, rowspan=2, columnspan=4)

l8=Label (root, text="PASSO 5: \nRepetir 'Aerado'\n ou 'Branco'", bd=5, relief="flat",
      font= "Times 11",width=17, bg='white')
l8.grid (row=9, column=15, rowspan=2, columnspan=4)
l6=Label (root, text="Retenção gasosa \nglobal (%)", bd=5, relief="flat",
      font= "Times 11",width=19, bg='white', height=2)
l6.grid (row=9, column=11, rowspan=2, columnspan=4)

#Imagem do reator
anterior()

#Funções de bloqueio de fechamento da janela
def close_program():
    root.destroy()
def disable_event():
    pass

#Encontrar arduino:
def encon_arduino(): #Função para deterninação da porta onde os dados serão coletados (para funcionar em diferentes PCs)
    for pinfo in serial.tools.list_ports.comports(): #procura na lista de informações das portas disponíveis
        if pinfo.description.startswith("Arduino"): Arduino=(pinfo.device) #pinfo.device=COM(n)
        return Arduino 

def runaniB(): #Animação do Branco
    #Listas: Aquisição dos dados
    Dados1=[]; Dados=[]; t=[] #Dados do sensor ja convertidos para float; #Dado bruto do Arduino ; #Dados de tempo
    #Grafico
    fig=Figure(figsize=(8,4), dpi=100) #Tamanho e qualidade da figura
    plot=fig.add_subplot(1,1,1) #Figura = Gráfico em subplot do Matlib
    plot.set_xlabel("Tempo (s)")
    plot.set_ylim(0, 80)
    plot.set_ylabel('Distância (cm)', color='k') # Legenda
    line, = plot.plot(t, Dados1, 'k', marker='o', markersize=4)
    #Reset de dados
    Dados1.clear(); Dados.clear(); t.clear()
    #Início da corrida
    ser=serial.Serial(encon_arduino(), 9600) #Local e taxa de atualização 
    if encon_arduino() is not None: ser.reset_input_buffer() #Reset buffer
    i=0; j=float(e4.get())  #Contadores de início (i) e fim (j)
    def branco(i): #Função branco
        if encon_arduino() is None: #Quando não for encontrado arduino
            #Imagem de Erro
            root.original7 = Image.open('ERRO.PNG') #Nome da imagem - Local da imagem > pasta do arquivo
            resized7 = root.original7.resize((60, 60),Image.ANTIALIAS) #Mudança de escala
            root.image7 = ImageTk.PhotoImage(resized7) 
            root.display7 = Label(root, image = root.image7)
            root.display7.grid(row=2, column=8, rowspan=3, columnspan=5) #Local na janela
            root.display7.configure(background='white')
            #Legenda do Erro
            l9=Label (root, text="ERRO: Sensor \nnão encontrado\n Conecte o sensor \ne aperte 'Branco'", bd=5, relief="flat",
                  font= "Times 11",width=25, height=4, bg='gray9', fg='white')
            l9.grid (row=3, column=8, rowspan=5,columnspan=5)
            ani.event_source.stop() #Parar animação
        else:
            if(ser.isOpen() == False): ser.open()
            e1.delete(0, 'end') #Reset dados para repetição
            arduinoData=ser.readline().decode('utf8') #Decodificação dos dados do arduino
            Dados.append(arduinoData)  #Dados do arduino
            Dados1.append(float(Dados[i])/10) #Dados de distância convertidos
            t.append(i/2) #Dados de tempo
            line.set_data(t, Dados1) #Dados do gráfico
            plot.set_xlim(0, (i/2)+1) #Limite do eixo X
            distancia1=(float(sum(Dados1))/float(len(Dados1))) #Dados de distância na janela
            e1.insert(END, round(distancia1, 3))
            root.protocol("WM_DELETE_WINDOW", disable_event) #Bloquear fechamento da janela
            if(i/2>=j): 
                ani.event_source.stop() #Parar animação
                ser.close() #Fechar porta serial
                anterior() #Mudar figura
                root.protocol("WM_DELETE_WINDOW", close_program)
    plotcanvas = FigureCanvasTkAgg(fig, root) #Gráfico
    plotcanvas.get_tk_widget().grid(column=1, row=1, columnspan=100, rowspan=60, sticky=NW)
    ani = animation.FuncAnimation(fig, branco, interval=250) #Animação da função Branco
   
def runaniA(): #Animação do aerado
    Dados2=[]; Dados=[] ; t=[] 
    #Grafico
    fig=Figure(figsize=(8,4), dpi=100) #Tamanho e qualidade da figura
    plot=fig.add_subplot(1,1,1) #Figura = Gráfico em subplot do Matlib
    plot.set_xlabel("Tempo (s)")
    plot.set_ylim(0, 80)
    plot.set_ylabel('Distância (cm)', color='k') # Legenda
    line, = plot.plot(t, Dados2, 'k', marker='o')
    #Reset de dados
    Dados.clear(); Dados2.clear(); t.clear()
    e3.delete(0, 'end')
    #Início da corrida
    ser=serial.Serial(encon_arduino(), 9600) #Local e taxa de atualização 
    if encon_arduino() is not None:
        ser.reset_input_buffer() #Reset buffer
    proxima() #Chamar figura
    i=0; j=float(e5.get())  #Contadores
    def aerado(i): #Função aerado
        if encon_arduino() is None: #Quando não for encontrado arduino
            #Imagem de Erro
            root.original7 = Image.open('ERRO.PNG') #Nome da imagem - Local da imagem > pasta do arquivo
            resized7 = root.original7.resize((60, 60),Image.ANTIALIAS) #Mudança de escala
            root.image7 = ImageTk.PhotoImage(resized7) 
            root.display7 = Label(root, image = root.image7)
            root.display7.grid(row=2, column=8, rowspan=3, columnspan=5) #Local na janela
            root.display7.configure(background='white')
            #Legenda do Erro
            l9=Label (root, text="ERRO: Sensor \nnão encontrado\n Conecte o sensor \ne aperte 'Branco'", bd=5, relief="flat",
                  font= "Times 11",width=25, height=4, bg='gray9', fg='white')
            l9.grid (row=3, column=8, rowspan=5,columnspan=5)
            ani.event_source.stop() #Parar animação
        else:
            if(ser.isOpen() == False): ser.open()
            e6.delete(0, 'end') #Reset dados para repetição
            arduinoData=ser.readline().decode('utf8') #Decodificação dos dados do arduino
            Dados.append(arduinoData)  #Dados do arduino
            Dados2.append(float(Dados[i])/10) #Dados de distância convertidos
            t.append(i/2) #Dados de tempo
            line.set_data(t, Dados2) #Dados do gráfico
            plot.set_xlim(0, (i/2)+1) #Limite do eixo X
            distancia2=(float(sum(Dados2))/float(len(Dados2)))
            e6.insert(END, round(distancia2, 3))
            root.protocol("WM_DELETE_WINDOW", disable_event)
            if(i/2>=j): 
                ani.event_source.stop() #Parar animação
                Retencao=(((float(e1.get())/100)-(distancia2/100))/((float(e1.get())/100)-(distancia2/100)+((float(e7.get())/1000)/(((float(e2.get())/2)**2)*3.1415926))))*100 #Cálculo da retenção
                e3.insert(END, round(Retencao, 3))  
                ser.close() #Fechar porta serial
                anterior() #Mudar figura
                root.protocol("WM_DELETE_WINDOW", close_program)
    plotcanvas = FigureCanvasTkAgg(fig, root) #Gráfico
    plotcanvas.get_tk_widget().grid(column=1, row=1, columnspan=100, rowspan=60, sticky=NW)
    ani = animation.FuncAnimation(fig, aerado, interval=250) #Animação da função Aerado

btn = Button(root, text="Branco", command=runaniB, bg='white', fg='black', width=15, height=3, font="Times 11", relief="groove", bd=5) #Botão de início do branco
btn.grid(row=9, column=0, rowspan=2) #Localização do Botão

btn = Button(root, text="Aerado", command=runaniA, bg='deepskyblue2', fg='white', width=15, height=3, font="Times 11", relief="groove", bd=5) #Botaão de início do aerado
btn.grid(row=11, column=0, rowspan=2) #Localização do Botão

root.mainloop() #Loop da janela





