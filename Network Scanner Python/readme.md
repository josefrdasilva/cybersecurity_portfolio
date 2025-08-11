## Escaneador de Rede Python

Este é um script em Python que escaneia a rede local para descobrir dispositivos conectados. Ele fornece informações detalhadas sobre cada dispositivo, incluindo IP, MAC Address, nome do host (quando disponível) e o fabricante da placa de rede. O script também oferece a opção de escanear portas abertas em cada dispositivo encontrado.

## Funcionalidades

    Escaneamento de Dispositivos: Identifica todos os dispositivos online na sua rede local (sub-rede).

    Detalhes do Dispositivo: Retorna o IP, MAC Address e o Nome do Host de cada aparelho.

    Identificação do Fabricante: Consulta uma API online para determinar o fabricante do dispositivo a partir do seu MAC Address.

    Escaneamento de Portas: Opcionalmente, escaneia as portas TCP mais comuns (1-1024) para identificar serviços em execução.

    Interface Simples: Uma interface de linha de comando clara para interação.

## Pré-requisitos

Para executar este script, você precisará ter o Python 3.x instalado, juntamente com as seguintes bibliotecas e ferramentas:

1. Bibliotecas Python

Instale todas as bibliotecas necessárias usando o pip:
Bash

pip install scapy colorama python-nmap requests

    scapy: Utilizado para o escaneamento de rede via protocolo ARP.

    colorama: Utilizado para adicionar cores ao terminal, melhorando a visualização.

    python-nmap: É a interface Python para o Nmap.

    requests: Utilizado para consultar a API de fabricantes (macvendors.com).

2. Ferramenta Nmap

O escaneamento de portas depende da ferramenta Nmap, que deve ser instalada separadamente em seu sistema operacional.

    Windows: Baixe e instale do site oficial do Nmap.

    Linux (Ubuntu/Debian): Use sudo apt-get install nmap.

    macOS: Use o Homebrew com brew install nmap.

## Como Usar

    Salve o código do script em um arquivo chamado network-scanner.py.

    Abra o terminal (ou Prompt de Comando, como administrador no Windows).

    Importante: Este script requer permissões de administrador para funcionar corretamente, pois manipula pacotes de rede.

        No Linux/macOS, use sudo:

sudo python3 network-scanner.py

No Windows, execute o Prompt de Comando como administrador e depois execute o script:


        python network-scanner.py

    O script irá escanear a rede e exibir uma lista de dispositivos encontrados.

    Em seguida, ele perguntará se você deseja escanear as portas. Digite s para sim ou n para não.

## Possíveis Erros e Soluções

    ModuleNotFoundError: No module named '...': Este erro indica que uma das bibliotecas Python não foi instalada. Certifique-se de que o comando pip install foi executado corretamente para todas as bibliotecas listadas nos pré-requisitos.

    "Permission denied" ou outros erros de permissão: O script falhará ao tentar escanear a rede sem as permissões adequadas. Lembre-se de executá-lo com sudo (Linux/macOS) ou como administrador (Windows).

    "Nmap is not installed": Certifique-se de que a ferramenta Nmap foi instalada em seu sistema, conforme descrito nos pré-requisitos. A biblioteca python-nmap é apenas uma interface para a ferramenta e não a instala.