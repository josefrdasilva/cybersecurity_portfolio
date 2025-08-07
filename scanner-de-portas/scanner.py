import socket

alvo = input("Digite o IP alvo: ")

portaInicio = int(input("Porta inicial: "))
portaFim = int(input("Porta final: "))

print(f"\ Verificando {alvo} de {portaInicio} a {portaFim}")

for porta in range(portaInicio, portaFim + 1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    resultado = sock.connect_ex((alvo, porta))

    if resultado == 0:
        print(f"Porta {porta} aberta")
    else:
        print(f"Porta {porta} fechada")

    sock.close()