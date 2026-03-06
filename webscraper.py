import re
import requests

def ehValido (url: str):
    return (re.search("pt.wikipedia.org", url))




url = input(str("Digite a URL da página do wikipedia: "))

print(ehValido(url))

