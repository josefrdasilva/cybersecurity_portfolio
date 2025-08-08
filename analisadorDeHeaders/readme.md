# Analisador de Headers de Segurança HTTP

Este projeto é um script simples em Python que se conecta a um site, obtém os **HTTP Response Headers** e verifica a presença de alguns cabeçalhos de segurança importantes.

## Funcionalidades

- Conexão com um domínio via protocolo HTTP ou HTTPS.
- Verificação se o site está usando HTTPS.
- Checagem da presença dos seguintes cabeçalhos de segurança:
  - Content-Security-Policy
  - Strict-Transport-Security
  - X-Frame-Options
  - X-Content-Type-Options
  - Referrer-Policy
  - Permissions-Policy

## Como executar

1. Certifique-se de ter o Python 3 instalado.
2. Instale a biblioteca necessária:
   pip install requests

    Salve o código em um arquivo, por exemplo: analisador_headers.py.

    Execute no terminal:

    python analisador_headers.py

    Digite a URL que deseja analisar (com ou sem https://).

## Exemplo de uso

Digite a URL do site: https://www.exemplo.com

Analisando header de: https://www.exemplo.com

Protocolo seguro (HTTPS): SIM
Content-Security-Policy: PRESENTE!
Strict-Transport-Security: PRESENTE!
X-Frame-Options: AUSENTE!
X-Content-Type-Options: PRESENTE!
Referrer-Policy: AUSENTE!
Permissions-Policy: AUSENTE!

## Requisitos

    Python 3.x

    Biblioteca requests

## Objetivo educacional

Este projeto foi criado com o objetivo de praticar:

    Uso de bibliotecas externas em Python

    Conexões HTTP/HTTPS

    Análise de segurança web básica

## Aviso: Utilize esta ferramenta apenas para fins educacionais e em domínios que você tenha permissão para analisar.