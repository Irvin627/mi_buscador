import concurrent.futures
import nltk
import urllib.request
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import requests
import json
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

nltk.download("stopwords")

def process_url(url):
    try:
        r = requests.head(url)
        html = urllib.request.urlopen(url).read()
        conexion = True
    except:
        conexion = False

    if conexion:
        soup = BeautifulSoup(html, 'html.parser')
        texto = soup.get_text()
        lines = (line.strip() for line in texto.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        texto = '\n'.join(chunk for chunk in chunks if chunk)
        raw = texto.lower()
        raw = re.sub(r"[^a-zA-Z0-9]+", " ", raw)  # Aplicar la expresión regular

        tokens = nltk.word_tokenize(raw)
        es_stops = set(stopwords.words('spanish'))
        en_stops = set(stopwords.words('english'))
        ge_stops = set(stopwords.words('german'))
        ch_stops = set(stopwords.words('chinese'))
        ru_stops = set(stopwords.words('russian'))
        tokens = [word for word in tokens if word not in es_stops and word not in en_stops and word not in ge_stops and word not in ch_stops and word not in ru_stops]

        dic_frecuencias = {}
        for palabra in tokens:
            if palabra in dic_frecuencias:
                dic_frecuencias[palabra] += 1
            else:
                dic_frecuencias[palabra] = 1

        return dic_frecuencias, url

    return None

def main():
    archivo = open("urls.txt", "r")
    diccionarioInv = {}  # Diccionario para el índice invertido

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for url in archivo:
            url = url.strip()
            futures.append(executor.submit(process_url, url))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                dic_frecuencias, url = result
                for palabra, frecuencia in dic_frecuencias.items():
                    if palabra in diccionarioInv:
                        diccionarioInv[palabra].append((url, frecuencia))
                    else:
                        diccionarioInv[palabra] = [(url, frecuencia)]

    # Escribe el diccionario invertido en el archivo JSON al final de todas las URLs procesadas
    with open("raiz_ind_inv.txt", "a") as archivoSalida:
        json.dump(diccionarioInv, archivoSalida)

    archivo.close()

if __name__ == "__main__":
    main()
