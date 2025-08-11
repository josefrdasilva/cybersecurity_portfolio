import scapy.all as scapy
import socket
import nmap
import sys
import requests
from colorama import Fore, Style, init

init(autoreset=True)

def get_network_prefix():
    """Tenta obter o prefixo da rede local."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip + "/24"
    except Exception as e:
        print(f"{Fore.YELLOW}[AVISO] Não foi possível obter o IP local. Usando 192.168.1.0/24 como padrão. Erro: {e}")
        return "192.168.1.0/24"

def get_vendor_from_mac(mac_address):
    """Consulta uma API para obter o fabricante a partir do MAC Address."""
    try:
        url = f"https://api.macvendors.com/{mac_address}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "Desconhecido"
    except requests.exceptions.RequestException:
        return "Falha na consulta"

def scan_network(ip):
    """Escaneia a rede e retorna uma lista de dispositivos."""
    print(f"{Fore.CYAN}Escaneando a rede {ip}... Isso pode levar alguns segundos.{Style.RESET_ALL}")
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    devices_list = []
    for element in answered_list:
        ip_addr = element[1].psrc
        mac_addr = element[1].hwsrc
        
        try:
            hostname = socket.gethostbyaddr(ip_addr)[0]
        except (socket.herror, socket.gaierror):
            hostname = "Nome não disponível"

        vendor = get_vendor_from_mac(mac_addr)
        
        devices_list.append({"ip": ip_addr, "mac": mac_addr, "hostname": hostname, "vendor": vendor})
        
    return devices_list

def print_results(devices_list):
    """Exibe os dispositivos encontrados de forma organizada."""
    if not devices_list:
        print(f"{Fore.RED}Nenhum dispositivo encontrado na rede.")
        return

    print("\n" + "="*80)
    print(f"{Fore.GREEN}Dispositivos encontrados na rede:")
    print("="*80)
    print(f"{'IP':<16}{'MAC Address':<20}{'Nome do Dispositivo':<25}{'Fabricante':<20}")
    print("-"*80)
    for device in devices_list:
        print(f"{Fore.YELLOW}{device['ip']:<16}{device['mac']:<20}{device['hostname']:<25}{device['vendor']:<20}")
    print("="*80 + "\n")

def scan_ports(ip_address):
    """Escaneia as portas mais comuns de um IP."""
    nm = nmap.PortScanner()
    try:
        print(f"{Fore.CYAN}Iniciando escaneamento de portas para {ip_address}...{Style.RESET_ALL}")
        nm.scan(ip_address, '1-1024')
        
        if ip_address in nm.all_hosts():
            host = nm[ip_address]
            print(f"{Fore.MAGENTA}--- Portas abertas para {ip_address} ({host.hostname()}) ---{Style.RESET_ALL}")
            for proto in host.all_protocols():
                ports = host[proto].keys()
                if ports:
                    sorted_ports = sorted(ports)
                    for port in sorted_ports:
                        state = host[proto][port]['state']
                        name = host[proto][port]['name']
                        print(f"  {Fore.GREEN}Porta {port}/{proto} - Estado: {state} - Serviço: {name}")
            print("\n")
        else:
            print(f"{Fore.YELLOW}Não foi possível escanear portas para {ip_address}.")
            
    except nmap.nmap.PortScannerError as e:
        print(f"{Fore.RED}Erro no escaneamento de portas para {ip_address}: {e}")
    except Exception as e:
        print(f"{Fore.RED}Ocorreu um erro inesperado durante o escaneamento de portas: {e}")

if __name__ == "__main__":
    network_prefix = get_network_prefix()
    devices = scan_network(network_prefix)
    print_results(devices)

    if devices:
        choice = input(f"{Fore.BLUE}Deseja escanear as portas abertas de cada dispositivo? (s/n): {Style.RESET_ALL}")
        if choice.lower() == 's':
            for device in devices:
                scan_ports(device['ip'])
    
    print(f"{Fore.GREEN}Fim da execução.{Style.RESET_ALL}")