from scapy.all import *
import threading
import time
import socket
from colorama import Fore, Style, init
import requests

# Inicializa o colorama
init(autoreset=True)

# Dicionários e variáveis globais
dispositivos_na_rede = {}
contagem_conexoes_tcp = {}
contagem_bytes = {}
# Novo dicionário para rastrear pacotes SYN
syn_scan_tracker = {}
lock = threading.Lock()
ip_da_rede_cidr = None

# Configuração da API do AbuseIPDB (substitua pela sua chave)
ABUSEIPDB_API_KEY = "SUA_CHAVE_DE_API_AQUI"
ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"
ips_verificados_api = set()

def carregar_banco_de_dados_mac():
    mac_db = {}
    try:
        with open('mac_vendors.txt', 'r', encoding='utf-8') as f:
            for linha in f:
                if len(linha) > 20:
                    prefixo_mac = linha[:8].replace('-', ':').upper()
                    fabricante = linha[16:].strip()
                    mac_db[prefixo_mac] = fabricante
    except FileNotFoundError:
        print(f"{Fore.RED}Aviso: Arquivo 'mac_vendors.txt' não encontrado. A identificação do fabricante não funcionará.")
    return mac_db

mac_database = carregar_banco_de_dados_mac()

def obter_nome_do_host(ip):
    try:
        nome_host = socket.gethostbyaddr(ip)[0]
        return nome_host
    except socket.herror:
        return "Nome não resolvido"
    except Exception:
        return "Erro de resolução"

def obter_fabricante_por_mac(mac):
    if not mac_database:
        return "Fabricante desconhecido"
    prefixo_mac = mac[:8].upper()
    return mac_database.get(prefixo_mac, "Fabricante desconhecido")

def obter_ip_e_interface_da_rede():
    global ip_da_rede_cidr
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_local = s.getsockname()[0]
        s.close()
        
        for iface_name, iface_info in conf.ifaces.items():
            if iface_info.ip == ip_local:
                ip_da_rede_cidr = ".".join(ip_local.split('.')[:-1]) + ".0/24"
                return (ip_da_rede_cidr, iface_name)
        
        print(f"{Fore.RED}Não foi possível encontrar a interface para o IP local {ip_local}.")
        return None, None
    except Exception as e:
        print(f"{Fore.RED}Erro ao obter o IP/Interface: {e}. Usando valores padrão.")
        ip_da_rede_cidr = "192.168.1.0/24"
        return (ip_da_rede_cidr, conf.iface.name)

def verificar_ip_malicioso(ip):
    if not ip or ip in ips_verificados_api or not ABUSEIPDB_API_KEY or ABUSEIPDB_API_KEY == "SUA_CHAVE_DE_API_AQUI":
        return
    ips_verificados_api.add(ip)
    try:
        headers = {
            'Accept': 'application/json',
            'Key': ABUSEIPDB_API_KEY
        }
        params = {'ipAddress': ip, 'maxAgeInDays': '90'}
        response = requests.get(ABUSEIPDB_URL, headers=headers, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()['data']
            if data['isPublic'] and data['abuseConfidenceScore'] > 20:
                print(f"{Fore.RED}!!! ALERTA DE SEGURANÇA !!! O IP externo {ip} tem uma pontuação de abuso de {data['abuseConfidenceScore']}% e foi reportado {data['totalReports']} vezes.")
    except Exception:
        pass

def encontrar_dispositivos(ip_da_rede, interface):
    if not ip_da_rede or not interface:
        return
    print(f"{Fore.CYAN}Iniciando varredura ARP na rede {ip_da_rede} pela interface {interface}...")
    try:
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_da_rede), timeout=2, verbose=0, iface=interface)
    except Exception as e:
        print(f"{Fore.RED}Erro ao realizar a varredura ARP: {e}. Verifique as permissões de administrador (sudo).")
        return
    with lock:
        for sent, received in ans:
            mac_address = received.hwsrc
            ip_address = received.psrc
            nome_host = obter_nome_do_host(ip_address)
            fabricante = obter_fabricante_por_mac(mac_address)
            if ip_address not in dispositivos_na_rede:
                dispositivos_na_rede[ip_address] = mac_address
                print(f"{Fore.GREEN}  > Dispositivo encontrado: {Fore.YELLOW}IP {ip_address}{Fore.GREEN} | {Fore.YELLOW}Host {nome_host}{Fore.GREEN} | {Fore.YELLOW}Fabricante {fabricante}{Fore.GREEN} | {Fore.YELLOW}MAC {mac_address}")

def analisar_pacote(pacote):
    with lock:
        if IP in pacote:
            ip_origem = pacote[IP].src
            ip_destino = pacote[IP].dst
            nome_host_origem = obter_nome_do_host(ip_origem)

            tamanho_pacote = len(pacote)
            contagem_bytes[ip_origem] = contagem_bytes.get(ip_origem, 0) + tamanho_pacote
            
            if not ip_origem.startswith("192.168.") and not ip_origem.startswith("10."):
                verificar_ip_malicioso(ip_origem)

            if TCP in pacote:
                tcp_origem = pacote[TCP].sport
                tcp_destino = pacote[TCP].dport
                
                # --- NOVO: Lógica de detecção de SYN Scan ---
                # A flag 'S' (SYN) indica uma tentativa de iniciar uma conexão
                if pacote[TCP].flags == 'S':
                    if ip_origem not in syn_scan_tracker:
                        syn_scan_tracker[ip_origem] = {}
                    
                    syn_scan_tracker[ip_origem][tcp_destino] = time.time()
                    
                    # Remove entradas antigas para evitar falsos positivos
                    for port, timestamp in list(syn_scan_tracker[ip_origem].items()):
                        if time.time() - timestamp > 5: # Remove portas com mais de 5 segundos
                            del syn_scan_tracker[ip_origem][port]
                    
                    # Se mais de 5 portas foram escaneadas em 5 segundos, avisa.
                    if len(syn_scan_tracker[ip_origem]) > 5:
                        print(f"{Fore.RED}!!! ALERTA DE VARREDURA (NMAP): Possível varredura de porta SYN de {nome_host_origem} ({ip_origem}) !!!")
                        # Limpa o rastreador para evitar alertas repetidos
                        syn_scan_tracker[ip_origem].clear()
                # --- Fim da nova lógica ---

                # Lógica antiga de varredura de porta (também útil para outros tipos de varredura)
                if ip_origem not in contagem_conexoes_tcp:
                    contagem_conexoes_tcp[ip_origem] = set()
                contagem_conexoes_tcp[ip_origem].add(tcp_destino)

                if len(contagem_conexoes_tcp[ip_origem]) > 10:
                    print(f"{Fore.RED}!!! ATIVIDADE SUSPEITA: Possível varredura de porta de {nome_host_origem} ({ip_origem}) !!!")
                    
                if not ip_origem.startswith("192.168.") and ip_destino.startswith("192.168."):
                     print(f"{Fore.YELLOW}Conexão de entrada detectada: {ip_origem} -> {nome_host_origem} ({ip_destino}):{tcp_destino}")

                print(f"{Fore.YELLOW}Pacote TCP: {nome_host_origem} ({ip_origem}) -> {ip_destino}:{tcp_destino}")
            
            elif UDP in pacote:
                udp_origem = pacote[UDP].sport
                udp_destino = pacote[UDP].dport
                print(f"{Fore.CYAN}Pacote UDP: {nome_host_origem} ({ip_origem}) -> {ip_destino}:{udp_destino}")

            if Raw in pacote:
                payload = pacote[Raw].load
                if 'HTTP' in pacote and 'password' in payload.lower().decode('utf-8', 'ignore'):
                    print(f"{Fore.RED}!!! ALERTA DE SEGURANÇA: Credenciais em texto simples detectadas de {nome_host_origem} ({ip_origem}) !!!")
                if b'admin' in payload.lower():
                    print(f"{Fore.RED}!!! AVISO: Palavra 'admin' encontrada no payload do pacote de {nome_host_origem} ({ip_origem}) !!!")
                
def exibir_resumo_trafego():
    while True:
        time.sleep(60)
        with lock:
            print(f"\n{Fore.BLUE}--- Resumo de Tráfego de Rede (últimos 60s) ---")
            if not contagem_bytes:
                print("Nenhum tráfego detectado.")
            top_5_consumidores = sorted(contagem_bytes.items(), key=lambda item: item[1], reverse=True)[:5]
            for ip, bytes_usados in top_5_consumidores:
                megabytes = bytes_usados / 1024 / 1024
                print(f"  > {ip} ({obter_nome_do_host(ip)}): {megabytes:.2f} MB")
            contagem_bytes.clear()
            print(f"{Fore.BLUE}---------------------------------------------")

def capturar_pacotes(interface):
    if not interface:
        return
    print(f"\n{Fore.MAGENTA}Iniciando a captura de pacotes na interface {interface}. Pressione Ctrl+C para parar...")
    try:
        sniff(iface=interface, prn=analisar_pacote, store=0)
    except Exception as e:
        print(f"{Fore.RED}Erro ao capturar pacotes: {e}. Verifique as permissões de administrador (sudo).")

def main():
    ip_da_rede, interface = obter_ip_e_interface_da_rede()
    if not ip_da_rede or not interface:
        print(f"{Fore.RED}Não foi possível iniciar o monitoramento. Verifique a configuração da sua rede.")
        return
    thread_dispositivos = threading.Thread(target=encontrar_dispositivos, args=(ip_da_rede, interface))
    thread_resumo_trafego = threading.Thread(target=exibir_resumo_trafego)
    thread_dispositivos.start()
    thread_resumo_trafego.start()
    time.sleep(3)
    capturar_pacotes(interface)

if __name__ == "__main__":
    main()