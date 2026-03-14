import re
import requests

def ehValido (url: str): # se não tiver isso, retorna None
    return (re.search("pt.wikipedia.org.", url))

def tryResponse (response):
    if response.status_code == 200:
        print("Sucesso!")
    elif response.status_code == 404:
        print("Não encontrado.")
    else:
        print(f"Erro: {response.status_code}")


def getHTML (url: str): # pega o html da url
    response = requests.get(url, headers= cabecalhos)
    tryResponse(response)
    html = response.text
    return html

def getInfo (url: str):
    padrao_toc = r'<span class="vector-toc-numb">[0-9]</span>\s*<span>([^<]+)</span>'
    padrao_img = r'<a href="/wiki/Ficheiro:([^"]+)"[^>]*class="mw-file-description"'

    html = getHTML(url)
    print(re.findall(padrao_toc, html))
    print(re.findall(padrao_img, html))



cabecalhos = {
    'User-Agent': 'WebScraper/1.0 (emailexemplo@gmail.com)'
}


url = input(str("Digite a URL da página do wikipedia: "))
# re.sub('\s+$', "", url) # retira todos os espaços no final

if (ehValido(url) == None):
    exit()

getInfo(url)

# https://pt.wikipedia.org/wiki/Immanuel_Kant

