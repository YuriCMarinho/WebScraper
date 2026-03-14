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
    padrao_toc = r'<span class="vector-toc-numb">[0-9.]+</span>\s*<span>([^<]+)</span>'
    padrao_img = r'<a href="/wiki/Ficheiro:([^"]+)"[^>]*class="mw-file-description"'

    artigo_atual = url.split("/wiki/") [1] #pega o que vem depois de wiki
    padrao_link = rf'<a href="/wiki/(?!{artigo_atual}")([^":#]+)"'#pega todos os links que tem comeco = wiki(links internos)
                                              #retira todos os liks com ":" , "#", e artigos que se referenciam
    
    html = getHTML(url)
    print(re.findall(padrao_toc, html))
    print(re.findall(padrao_img, html))
    print(re.findall(padrao_link, html))




cabecalhos = {
    'User-Agent': 'WebScraper/1.0 (emailexemplo@gmail.com)'
}


url = input(str("Digite a URL da página do wikipedia: "))
url_limpa = re.sub(r'\s+', '', url) # retira todos os espaços no final

if (ehValido(url_limpa) == None):
    exit()

getInfo(url_limpa)


