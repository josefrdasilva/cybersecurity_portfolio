import os
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime

# Caminho para a pasta de resultados do scanner_avancado
WORKDIR = "nmap_results"
VULN_OUTPUT_TXT = "vulnerabilidades.txt"
VULN_OUTPUT_HTML = "vulnerabilidades.html"

def ler_hosts_xml(workdir):
    """Percorre todos os XMLs e retorna lista de IPs encontrados"""
    ips = set()
    for arquivo in os.listdir(workdir):
        if not arquivo.endswith(".xml"):
            continue
        caminho = os.path.join(workdir, arquivo)
        try:
            tree = ET.parse(caminho)
            root = tree.getroot()
            for host in root.findall("host"):
                status = host.find("status")
                if status is not None and status.get("state") != "up":
                    continue
                addr = host.find("address")
                if addr is not None:
                    ips.add(addr.get("addr"))
        except Exception:
            pass
    return sorted(list(ips))

def rodar_nmap_vuln(ip):
    """Executa o Nmap com --script vuln para um IP"""
    cmd = [
        "nmap",
        "-p",
        "--script", "vuln",
        ip
    ]
    print(f"[+] Escaneando vulnerabilidades em {ip}...")
    resultado = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return resultado.stdout

def gerar_html(relatorios):
    """Gera um HTML simples com os resultados"""
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""<html>
<head>
<meta charset="utf-8">
<title>Relatório de Vulnerabilidades</title>
<style>
body {{ font-family: Arial, sans-serif; padding: 20px; }}
pre {{ background: #f9f9f9; padding: 10px; border: 1px solid #ddd; }}
</style>
</head>
<body>
<h1>Relatório de Vulnerabilidades</h1>
<p>Gerado em {agora}</p>
"""
    for ip, texto in relatorios.items():
        html += f"<h2>Host: {ip}</h2>\n<pre>{texto}</pre>\n"
    html += "</body></html>"

    with open(VULN_OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] Relatório HTML salvo em {VULN_OUTPUT_HTML}")

def main():
    if not os.path.isdir(WORKDIR):
        print(f"ERRO: pasta {WORKDIR} não encontrada. Rode primeiro o scanner_avancado.py.")
        return

    ips = ler_hosts_xml(WORKDIR)
    if not ips:
        print("Nenhum IP encontrado nos XMLs.")
        return

    print(f"[+] IPs encontrados: {', '.join(ips)}")

    relatorios = {}
    with open(VULN_OUTPUT_TXT, "w", encoding="utf-8") as f:
        for ip in ips:
            saida = rodar_nmap_vuln(ip)
            relatorios[ip] = saida
            f.write(f"===== {ip} =====\n{saida}\n\n")

    print(f"[+] Relatório TXT salvo em {VULN_OUTPUT_TXT}")
    gerar_html(relatorios)

if __name__ == "__main__":
    main()