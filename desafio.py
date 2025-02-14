#Desafio 1: Sequência de Fibonacci
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    seq = [0, 1]
    for _ in range(n - 2):
        seq.append(seq[-1] + seq[-2])
    
    return seq

n = 10
print(fibonacci(n))



#Desafio 2: Implementação de Algoritmo de Busca Binária
def busca_binaria(lista, alvo):
    inicio, fim = 0, len(lista) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        if lista[meio] == alvo:
            return meio  #Retorna o índice do número
        elif lista[meio] < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1

    return -1  #Se não encontrou o número

lista = [4, 5, 11, 21, 24, 27, 69, 106]
alvo = 69
print(busca_binaria(lista, alvo))



#Desafio 3: Cálculo de Números Perfeitos
def numero_perfeito(n):
    if n < 2:
        return False
    
    soma_divisores = sum(i for i in range(1, n) if n % i == 0)
    return soma_divisores == n

n = 27
print(numero_perfeito(n))  #Saída: True



#Desafio 4: Substring Palindrômica Mais Longa
def maior_palindromo(s):
    if not s:
        return ""
    
    def expandir_do_centro(esq, dir):
        while esq >= 0 and dir < len(s) and s[esq] == s[dir]:
            esq -= 1
            dir += 1
        return s[esq+1:dir]

    maior = ""
    for i in range(len(s)):
        #Expansão para palíndromos ímpar
        p1 = expandir_do_centro(i, i)
        #Expansão para palíndromos par
        p2 = expandir_do_centro(i, i+1)

        #Verifica a maior substring palindrômica
        if len(p1) > len(maior):
            maior = p1
        if len(p2) > len(maior):
            maior = p2

    return maior

s = "antedeguemon"
print(maior_palindromo(s))



#Desafio 5: Simulação de Saque em Caixa Eletrônico
def saque_caixa(valor):
    notas = [100, 50, 20, 10, 5, 2, 1]  #Lista das notas disponíveis
    resultado = {}

    for nota in notas:
        if valor >= nota:
            quantidade = valor // nota  #Quantidade de notas dessa
            resultado[nota] = quantidade
            valor -= quantidade * nota  #Reduz o restante

    return resultado

valor = 411
resultado = saque_caixa(valor)

for nota, qtd in resultado.items():
    print(f"{qtd} nota(s) de {nota}")
