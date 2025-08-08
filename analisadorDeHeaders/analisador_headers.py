import requests

headers_seguranca = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy"
]

url = input("Digite a URL do site: ")

if not url.startswith("http"):
    url = "https://" + url

try:
    resposta = requests.get(url)
    print(f"\nAnalisando header de: {url}\n")

    if url.startswith("https"):
        print("Protocolo seguro (HTTPS): SIM")
    else:
        print("Protocolo seguro (HTTPS): NÃO")

    for header in headers_seguranca:
        if header in resposta.headers:
            print(f"{header}: PRESENTE!")
        else:
            print(f"{header}: AUSENTE!")
except requests.exceptions.RequestException as e:
    print(f"Erro ao conectar: {e}")