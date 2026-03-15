# Python WebScraper for Wikipedia (PT)

Este é um script simples em Python que utiliza as bibliotecas `requests` e `re` para extrair dados de artigos da **Wikipédia em Português** (`pt.wikipedia.org`).
O script foi projetado para ser leve e não ter dependências complexas.

---

## O que ele extrai?

Ao fornecer a URL de um artigo, o script irá extrair e imprimir no terminal três tipos de informação:

1.  **Sumário (TOC):** Os títulos das seções principais do artigo.
2.  **Nomes dos Arquivos de Imagem:** O nome dos arquivos de imagem (ex: `Python_logo_and_wordmark.svg`).
3.  **Links Internos:** Links para outros artigos dentro da própria Wikipédia. Links para seções da mesma página (`#`) ou para outras áreas (ex: `Ficheiro:`) são ignorados.

---

## Como usar

### Requisitos
- Python 3.x
- Biblioteca `requests`

### Instalação
Clone o repositório e instale a dependência:
```bash
git clone https://github.com/YuriCMarinho/WebScraper.git
cd WebScraper
pip install requests
