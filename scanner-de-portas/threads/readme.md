# Port Scanner em Python com Multithreading

Este projeto é um scanner de portas TCP simples desenvolvido em Python. Ele utiliza múltiplas threads para acelerar o processo de verificação de portas abertas em um host especificado.

## Como funciona

O script solicita ao usuário:

- Um IP ou nome de domínio (site) como alvo
- Um intervalo de portas a serem escaneadas

Para cada porta dentro do intervalo, o programa tenta se conectar usando a biblioteca `socket`. Se a conexão for bem-sucedida (código de retorno igual a 0), a porta é considerada aberta. O processo é executado em paralelo utilizando a biblioteca `threading`.

## Requisitos

- Python 3.x

## Como usar

1. Salve o código em um arquivo chamado `scanner.py`
2. Execute no terminal ou prompt de comando: python scanner.py
3. Informe os dados quando solicitado:

Digite o IP ou site alvo: scanme.nmap.org
Porta inicial: 75
Porta final: 85


## Exemplo de saída

Iniciando scan em scanme.nmap.org de 75 ate 85...

[+] Porta 80 aberta!

Scan finalizado nas portas.

## Tecnologias utilizadas

- `socket` – Biblioteca padrão do Python para conexões de rede TCP
- `threading` – Para execução paralela de múltiplas verificações

## Aviso legal

Este script foi desenvolvido exclusivamente para fins educacionais.  
Não utilize este código para escanear dispositivos ou redes sem autorização.  
No Brasil, o uso indevido de ferramentas desse tipo pode ser considerado crime conforme a Lei 12.737/2012 (Lei Carolina Dieckmann).

## Aprendizados

Este projeto tem como objetivo reforçar os seguintes conceitos:

- Conceitos de portas TCP e conexões de rede
- Manipulação de sockets em Python
- Execução paralela com múltiplas threads

## Autor

Este projeto foi desenvolvido por José Francisco como parte dos estudos na área de redes e cibersegurança.