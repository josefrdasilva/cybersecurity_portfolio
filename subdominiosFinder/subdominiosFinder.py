import requests
import os
from concurrent.futures import ThreadPoolExecutor

def verificarSubdominio(sub):
    url = f"http://{sub}.{dominio}"
    try:
        requests.get(url, timeout=2)
        print(f"[+] Ativo: {url}")
    except requests.ConnectionError:
        pass

dominio = input("Digite o dominio: exemplo.com ")

caminho = os.path.join(os.path.dirname(__file__), "subdominios.txt")

with open(caminho) as f:
    lista = f.read().splitlines()

print(f"\nIniciando busca por subdominios ativos em: {dominio}\n")

with ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(verificarSubdominio, lista)

print("\nBusca concluida.")