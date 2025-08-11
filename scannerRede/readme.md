## Port Scanner em Python
## Descrição

Este projeto é um scanner de portas desenvolvido em Python, capaz de verificar quais portas estão abertas em um determinado host.
É uma ferramenta útil para testes de segurança, auditorias e aprendizado sobre redes.

## Funcionalidades

    Escaneia portas TCP de um host específico.

    Permite configurar o intervalo de portas a ser testado.

    Exibe apenas as portas abertas.

    Código simples e adaptável para estudos.

## Tecnologias Utilizadas

    Python 3.x

    Biblioteca socket (nativa do Python)

## Como Usar

    Clone este repositório:

    Execute o script no terminal:

python scanner_avancado.py

    Insira o IP ou domínio que deseja escanear e o intervalo de portas.
    python scanner_avancado.py --network 192.168.0.0/24

    Se quiser escanear todas as portas e o OS
    python scanner_avancado.py --network 192.168.0.0/24 --ports all --threads 50 --detect-os

    Para salvar resultado em um arquivo
    python scanner_avancado.py --network 192.168.0.0/24 --output resultados.txt

## Exemplo de Uso

Digite o host a ser escaneado: 192.168.0.10
Digite a porta inicial: 1
Digite a porta final: 1000

Porta 22 aberta
Porta 80 aberta
Porta 443 aberta

## Aviso Importante

## Este projeto é apenas para fins educacionais e testes autorizados.
## Não utilize para invadir sistemas ou redes sem permissão.