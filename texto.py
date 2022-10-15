import urllib.request 
from bs4 import BeautifulSoup
import re
import sys 
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter.ttk import Treeview
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import numpy as np


correoencontrados = []


def lectura_de_datos(urlvalo):
   
    urlvalor =urlvalo
    
    with urllib.request.urlopen(urlvalor) as url:
        s = url.read()
        try:
            soup = BeautifulSoup(s)
        except:
            print("esta mal")
    
    



# eliminar todos los elementos de script y estilo
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

# extrae el puro texto
    text = soup.get_text()

# divide en líneas y elimina el espacio inicial y final en cada texto
    lines = (line.strip() for line in text.splitlines())

# ayuda a divir varios titulos en cada linea de cada uno
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

# ayuda a hacer saltos de lineas en cada texto
    text = '\n'.join(chunk for chunk in chunks if chunk)

#print(text)

#escritura en el txt
    try:
        with open('texto.txt', 'w') as f: 
            f.write(text)
            f.close()
        
    except:
        valordeverdad = False
        
        
#recuperacion de posibles correos
    with open('texto.txt') as archivo:
        print(type(archivo))
        for linea in archivo:
        #print(linea)
            if "@" in linea:
                correoencontrados.append(linea)
    borardatosdeltxt()
                
       
                
    #empezamos con 
    #abrimos el documento dodne se encuentran los datos del automata
    with open('data.txt') as f:
        lineas = f.readlines()
    i=0
    lista = []
    #Se limpia el texto donde se encuentran los datos del automata para crear listas donde podemos manejar los datos 
    #esto con la finalidad de poder manejar mas facil la informacion 
    while i < len(lineas):
        #se remplazan valores para limpiar el texto            
        lin = lineas[i].replace("=","")
        lin = lin.replace("  ","+")
        lin = lin.replace("\n","")
        lin = lin.replace("{","")
        lin = lin.replace("}","")
        lista.append(lin.split("+"))
        #print(lista[i])
        i = i + 1

    #una vez limpio el texto se crean las variables de tipo lista que usara el sistema
    #variable de estados
    q = lista[0][1].split(",")
    #variable del alfabeto
    s = lista[1][1].split(",")
    #aqui se agrega epsilon, si el epsilon lo agregan al alfabeto hay que comentar esta linea 
    #s.append('e')
    #variable de estado incial
    q0 = lista[2][1].split(",")
    #variable de estados finales 
    final = lista[3][1].split(",")
    #aplicamos un segundo filtro para obtener los estados de transicion
    aux = lista[4][1]
    r = aux[1:len(aux)-1].split("),(")
    #creamos nuestra lista donde estan los estados de transicion
    estados = []
    i=0
    while i < len(r):
        estados.append(r[i].split(","))
        i = i + 1
#se termina de crear la lista de estados de transicion

    #validaciones de correos electronicos
    correosvalidos = []
    
    for x in range(len(correoencontrados)):
        
        while  correoencontrados:
            print(" ")
            print('Documento leido con exito')
            #leemos la cadena ingresada
            valor= correoencontrados[x]
            cadena = list(valor)
                    
            #INICIO DE AFND
            valoresusados = " "
            estado_final = False
            #al ser un afnd estte puede tomar multiples caminos por lo cual esta lista sirve para analizar dichos caminos
            estados_actuales = []
            #el primer elemento a analizar sera el estado inicial
            estados_actuales.append(q0[0])
            
            while cadena:
                #con los elementos de la cadena ingresada buuscamoss que dicha transicion exista en el alfabeto 
                if(cadena[0] in s):
                    num_estados = len(estados_actuales)
                    
                    for i in range(len(estados)):    
                        for j in range(num_estados):
                            #buscamos que los posibles caminos tengan una trancision si estos la tienen agregan un elementto a la lista de estados actuales para su posterior analisis
                            if estados[i][0] == estados_actuales[j] and estados[i][1] == cadena[0]:
                                #actualziamos los estados actuales
                                #print("este es el valor de i",i,"y este es el valo0r de j",j)
                                estados_actuales.append(estados[i][2])
                                #print(estados_actuales[j])
                    for y in range(num_estados):
                        #una vez analizados todos los estados posibles los removemos
                        estados_actuales.remove(estados_actuales[0])
                    #print(estados_actuales)
                    #recuperacion de correos
                    valoresusados = valoresusados + cadena[0]
                    
                    cadena.remove(cadena[0])
                else:
                    cadena.remove(cadena[0])
                    

            for i in range(len(estados_actuales)):
                #si los ultimos estados encontrados son parte de los estados finales consideramos que es una cadena valida 
                 
               
                if(estados_actuales[i] in final):
                    #si la cadena es valida marcamos como true de lo contrario es un false
                    estado_final = True
                    
                    
                    
                else:
                    estado_final = False

            #imprimimmos si la cadena es valida o no
            if estado_final == True:
                correos = valoresusados
                correosvalidos.append(correos)
                
                    
                correosencontradosvalidos = np.array(correosvalidos)
                contenedor = str(correosencontradosvalidos)

                cal = contenedor.replace("[","")
                lista = cal.replace("]","")
                limp = lista.replace("'","")
                limpio = limp.replace("'","")


                

                
                    
                with open('correosrescatados.txt', 'w') as f:
                    f.write(limpio)
                    f.close()
                
                    
                #messagebox.showinfo("Mensaje del AFND","La cadena ingresada es valida")
                print("cadena valida")
                break
            else:
                #messagebox.showinfo("Mensaje del AFND","La cadena ingresada NO es valida")
                print("cadena invalida")
                break
            
            
    correoencontrados.clear()
    with open('correosrescatados.txt') as f:
        vacio = f.readlines()
        print(vacio)
        if vacio == []:
            mb.showerror("Mensaje", "No se encontraron correos que sean validos")
        else:
            datosfinales()
    if valordeverdad == False:
        mb.showerror("Mensaje", "pagina protegida")
    else:
        datosfinales()
    
    
    
def borardatosdeltxt():
    with open('correosrescatados.txt','w') as f:
        pass
    
        
  

def datosfinales():
    mostrardatos()
    
    
#iniciamos la parte visual la interfas
def inicio():
    #colores
    fondoentrar="#00c2cb"
    textocolor = "#FFFFFF"
    
     
    ventana = tk.Tk()
    ventana.title("ventana")
    ventana.geometry("500x500+500+50")
    ventana.resizable(width=False, height=False)

    fondo = tk.PhotoImage(file="inicio.png")
    fondo1 =  tk.Label(ventana, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)
    usuario = tk.StringVar()
    #Entradas
    entrada = tk.Entry(ventana, textvar=usuario, width=71, relief="flat", bg=textocolor)
    entrada.place(x=34, y=230)
    
    #clase para extraer el texto del input
    def sacarvalor():
        print(f"esto trae usuario {usuario.get()}")  
        urlvalo = usuario.get()
        usuario.set('')
        lectura_de_datos(urlvalo)
        
        
    
    # Botones
    boton = tk.Button(ventana, text = "lectura", cursor ="hand2",command=sacarvalor ,bg=fondoentrar, width = 12, relief="flat", font =("Comic Sans MS" , 12 , "bold"))
    boton.place (x=180, y=355)
    
    
    ventana.mainloop()
    
        
        
#mostramos los datos que recuperamos
def mostrardatos():
    ventana = Tk()
    ventana.title('correos validos')
    ventana.geometry('400x300')
    ventana['bg']='#fb0'

    tabla = ttk.Treeview(ventana, columns=1, height=50)
    tabla.pack(pady=15, padx=10)
    tabla.column("#0", width=500, minwidth=100)
    tabla.heading("#0", text="correos",anchor=CENTER)

    with open('correosrescatados.txt') as archivo:
        print(type(archivo))
        for linea in archivo:
            if linea == " ":
                print("no hay valores")
            else:
                tabla.insert('',0,text=linea)

    tabla.pack()

    ventana.mainloop()


if __name__ == '__main__':
    inicio()
