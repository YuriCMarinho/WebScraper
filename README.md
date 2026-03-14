# WebScraper (Wikipedia) — Python

Script simples em Python para fazer scraping de páginas da **Wikipédia em português (pt.wikipedia.org)**.  
Ele baixa o HTML do artigo e imprime no terminal:

- Títulos do sumário (TOC)
- Arquivos de imagem presentes na página
- Links internos para outros artigos

## Requisitos
- Python 3
- Biblioteca `requests`

Instalação:
```bash
pip install requests
```

## Como usar
Execute:
```bash
python webscraper.py
```

Depois digite a URL de um artigo da Wikipédia PT, por exemplo:
```text
https://pt.wikipedia.org/wiki/Python
```

## Observações
- O script valida se a URL contém `pt.wikipedia.org`.
- A extração é feita com **regex** diretamente no HTML (pode quebrar se a estrutura da Wikipédia mudar).
