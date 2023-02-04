import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter
import tkinter as tk

# Links para hacer pruebas
# https://www.tutorialesprogramacionya.com/javaya/detalleconcepto.php?codigo=87
# https://wwwhatsnew.com/2013/08/23/extractcss-proyecto-de-codigo-libre-para-extraer-el-css-de-cualquier-documento-html/
# https://www.inesem.es/revistadigital/informatica-y-tics/como-extraer-el-css-de-una-web/

matriz_transiciones = [
    [0, ["#"], 1],
    [1, ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9","A", "B", "C", "D", "E", "F", "a", "b", "c", "d", "e", "f"], 2],
    [2, ["0","1", "2", "3", "4", "5", "6", "7", "8", "9","A", "B", "C", "D", "E", "F", "a", "b", "c", "d", "e", "f"], 3],
    [3, ["0","1", "2", "3", "4", "5", "6", "7", "8","9","A", "B", "C", "D", "E", "F", "a", "b", "c", "d", "e", "f"], 4],
    [4, ["0","1", "2", "3", "4", "5", "6", "7", "8", "9","A", "B", "C", "D", "E", "F", "a", "b", "c", "d", "e", "f"], 5],
    [5, ["0","1", "2", "3", "4", "5", "6", "7", "8", "9","A", "B", "C", "D", "E", "F", "a", "b", "c", "d", "e", "f"], 6],
    [6, ["0","1", "2", "3", "4", "5", "6", "7", "8", "9","A", "B", "C", "D", "E", "F", "a", "b", "c", "d", "e", "f"], 7],
]

def recorrido_matriz(text):
    estado_inicial = 0
    estado_actual = ""
    estado_colores = []
    index = 0
    while index < len(text):
        char = text[index]
        transicion_encontrada = False
        for transiciones in matriz_transiciones:
            if estado_inicial == transiciones[0] and char in transiciones[1]:
                estado_inicial = transiciones[2]
                estado_actual += char
                transicion_encontrada = True
                break
        if not transicion_encontrada:
            if estado_inicial == 7:
                estado_colores.append(estado_actual)
                estado_actual = ""
                estado_inicial = 0
                print("valido")
            else:
                estado_inicial = 0
                estado_actual = ""
        index += 1
    return estado_colores


root = tk.Tk()

entry = tk.Entry(root)

def boton():
    url = entry.get()
    extraer_style(url)

def interfaz_link():
    root.title("Automata de Colores Hexadecimales")

    label = tk.Label(root, text="")
    label.pack(pady=100) 

    label = tk.Label(root, text="Ingrese un enlace:")
    label.pack(pady=10)

    entry.pack(pady=10)


    submit = tk.Button(root, text="Analizar", command=boton)
    submit.pack(pady=10)

    root.geometry("800x600")
    root.mainloop()



def extraer_style(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    response = requests.get(url)
    html_content = response.content
    html_content = html_content.decode("utf-8")


    style_tags = soup.find_all('style')

    reglas_css = []
    for style_tag in style_tags:
        reglas_css.append(style_tag.string)

    reglas_css = [reglas for reglas in reglas_css if isinstance(reglas, str)]
    contenido_css = '\n'.join(reglas_css)

    with open('style.txt', "w", encoding="utf-8") as f:
        f.write(contenido_css + "\n" + html_content)


    with open("style.txt", "r", encoding='utf-8') as f:
        text = f.read()
        estado_colores = recorrido_matriz(text)
        print(estado_colores)
        mostrar_grafico(text)



def mostrar_grafico(text):
    estado_colores = recorrido_matriz(text)
    color_counts = dict(Counter(estado_colores))

    colores = list(color_counts.keys())
    frecuencia = list(color_counts.values())

    plt.bar(colores, frecuencia)
    plt.xlabel("Color Hexadecimal")
    plt.ylabel("Frecuencia")
    plt.title("Frecuencia de Colores Hexadecimales")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()



interfaz_link()