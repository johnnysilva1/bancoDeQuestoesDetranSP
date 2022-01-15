import re
from bs4 import BeautifulSoup
import requests
import time
import json


def baixaImagem(nome, url):
    url_base = "https://www.detran.sp.gov.br/detran-prova/simulado_questoes/"
    try:
        url = url_base + url
        with requests.get(url, stream=True) as r:
            with open("./imagens/" + nome + ".jpg", "wb") as fd:
                for pedaco in r.iter_content(chunk_size=128):
                    fd.write(pedaco)

    except Exception as err:
        print(err)


def exportaQuestoesParaJson():
    contador = 0
    dicionario = {}
    padraoPlaca = "[A-Z]-\d*[a-z]*"

    with open("questoes.txt") as f:
        for linha in f:
            if linha.startswith("\n"):
                pass
            elif linha.startswith("A)"):
                dicionario[contador]["alternativas"]["a"] = linha.replace("\n", "")[3:]
            elif linha.startswith("B)"):
                dicionario[contador]["alternativas"]["b"] = linha.replace("\n", "")[3:]
            elif linha.startswith("C)"):
                dicionario[contador]["alternativas"]["c"] = linha.replace("\n", "")[3:]
            elif linha.startswith("D)"):
                dicionario[contador]["alternativas"]["d"] = linha.replace("\n", "")[3:]
                contador += 1

            else:
                dicionario[contador] = {}
                dicionario[contador]["questao"] = linha.replace("\n", "")
                dicionario[contador]["alternativas"] = {}
                dicionario[contador]["resposta"] = ""

                deuMatch = re.findall(padraoPlaca, dicionario[contador]["questao"])
                if deuMatch:
                    dicionario[contador]["imagens"] = []
                    for placa in deuMatch:
                        dicionario[contador]["imagens"].append(placa)

                    print(dicionario[contador]["imagens"])

    with open("questoes.json", "w") as f:
        json.dump(dicionario, f)


def identificaPlacaNaQuestao():
    lista = []

    with open("questoes.htm") as fp:
        soup = BeautifulSoup(fp, features="html.parser")

    questoes = soup.findAll("b")

    padrao = re.compile("[A-Z]-\d*[a-z]*")
    for questao in questoes:
        deuMatch = padrao.search(str(questao))
        if deuMatch:
            lista.append((deuMatch.group(0), questao.img["src"]))

    for imagem in lista:
        baixaImagem(imagem[0], imagem[1])
        time.sleep(0.3)


if __name__ == "__main__":
    exportaQuestoesParaJson()
