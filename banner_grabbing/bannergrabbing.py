import socket

host = input("Digite o domino: ")
porta = int(input("Digite a porta: "))

s = socket.socket()
s.settimeout(2)
s.connect((host, porta))
banner = s.recv(1024)
print("Banner:", banner.decode(errors='ignore'))
s.close()