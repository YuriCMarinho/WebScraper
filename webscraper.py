import re
import requests

cabecalhos = {
    'User-Agent': 'WebScraper/1.0 (emailexemplo@gmail.com)'
}


def ehValido(url: str):  # Verifica se a URL pertence à Wikipédia em português
    return re.search("pt.wikipedia.org.", url)

def getHTML(url: str):  # pega o html da url e usa 'cabecalhos' para se identificar para o servidor
    response = requests.get(url, headers=cabecalhos, timeout=15)
    if response.status_code != 200:
        raise Exception(f"Erro HTTP {response.status_code}")
    html = response.text
    return html


def getInfo(url: str):
    padrao_toc = r'<span class="vector-toc-numb">[0-9.]+</span>\s*<span>([^<]+)</span>' # busca números e o texto dentro dos spans do índice
    padrao_img = r'<a href="/wiki/Ficheiro:([^"]+)"[^>]*class="mw-file-description"' # busca os links de imagem

    artigo_atual = url.split("/wiki/") [1]                        # pega o que vem depois de wiki
    padrao_link = rf'<a href="/wiki/(?!{artigo_atual}")([^":#]+)"'# busca todos os links que tem comeco = wiki(links internos)
                                                                  # retira todos os links com ":" , "#", e artigos que se referenciam

    html = getHTML(url)
    toc = re.findall(padrao_toc, html)
    images = re.findall(padrao_img, html)
    links = list(dict.fromkeys(re.findall(padrao_link, html)))

    return {
        "article": artigo_atual.replace("_", " "),
        "toc": toc,
        "images": images,
        "links": links,
    }

if __name__ == "__main__": # Só roda no terminal se executar diretamente (python webscraper.py)
    url = input(str("Digite a URL da página do wikipedia: "))
    url_limpa = re.sub(r'\s+', '', url)  # retira todos os espaços no final

    if ehValido(url_limpa) is None:
        exit()

    info = getInfo(url_limpa)
    print("\n--- Sumário ---")
    print(info["toc"])
    print("\n--- Imagens ---")
    print(info["images"])
    print("\n--- Links ---")
    print(info["links"])
