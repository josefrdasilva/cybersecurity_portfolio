## Descobridor de Subdomínios (Subdomain Finder)

Este projeto é um script em Python que busca subdomínios ativos de um domínio alvo usando uma lista de subdomínios comuns. Ele testa vários subdomínios em paralelo para acelerar a análise.
## Funcionalidades

    Permite que o usuário insira um domínio (exemplo.com).

    Carrega uma lista de subdomínios de um arquivo chamado subdominios.txt que deve estar na mesma pasta do script.

    Faz requisições HTTP para os subdomínios gerados (ex: http://admin.exemplo.com).

    Exibe quais subdomínios estão ativos (responderam à requisição).

    Usa múltiplas threads para acelerar a busca.

## Como usar

    Tenha o Python 3 instalado no seu computador.

    Instale a biblioteca requests, se ainda não tiver, executando no terminal:

pip install requests

    Certifique-se de que o arquivo subdominios.txt está na mesma pasta que o script Python.
    Exemplo do conteúdo do subdominios.txt (várias linhas, cada subdomínio em uma linha):

www
mail
ftp
cpanel
webmail
blog
dev
test
api
shop
support
admin
portal
app
vpn
news
m
secure
files
dashboard

    Salve o script Python na mesma pasta com o nome, por exemplo, subdominiosFinder.py.

    Execute o script no terminal (no diretório onde está o script e o arquivo subdominios.txt):

python subdominiosFinder.py

    Quando o script pedir, digite o domínio que deseja analisar (somente o domínio, sem http:// ou www). Exemplo:

google.com

    O script irá exibir na tela os subdomínios ativos, por exemplo:

[+] Ativo: http://www.google.com
[+] Ativo: http://mail.google.com
[+] Ativo: http://api.google.com

    Quando terminar, verá a mensagem:

Busca concluida.

## Requisitos

    Python 3.x

    Biblioteca requests (pip install requests)

## Objetivo educacional

Este projeto ajuda a entender conceitos básicos de reconhecimento em segurança da informação, como mapeamento da superfície de ataque através de subdomínios. Também serve para praticar programação em Python, uso de bibliotecas e paralelismo simples com threads.