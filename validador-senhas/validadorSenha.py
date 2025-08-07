import string

def avaliarSenha(senha):
    pontos = 0

    if len(senha) >= 8:
        pontos += 1
    if any(c.islower() for c in senha):
        pontos += 1
    if any(c.isupper() for c in senha):
        pontos += 1
    if any(c.isdigit() for c in senha):
        pontos += 1
    if any(c in string.punctuation for c in senha):
        pontos += 1
    
    return pontos

def classificarSenha(pontos):
    if pontos == 5:
        return "Muito forte!"
    elif pontos >= 3:
        return "Mediana"
    else:
        return "Fraca"
    
senha = input("Digite a senha: ")

pontos = avaliarSenha(senha)
classific = classificarSenha(pontos)

print(f"\nSua senha foi classificada como {classific}")