import socket
import threading

target = input("Digite o IP ou site alvo: ")
portaInicial = int(input("Porta inicial: "))
portaFinal = int(input("Porta final: "))

print(f"\nIniciando scan em {target} de {portaInicial} ate {portaFinal}...\n")

def scan(porta):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        conexao = s.connect_ex((target, porta))
        if conexao == 0:
            print(f"[+] Porta {porta} aberta!")
        s.close()
    except:
        pass

threads = []

for porta in range(portaInicial, portaFinal + 1):
    t = threading.Thread(target=scan, args=(porta,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\nScan finalizado nas portas.")