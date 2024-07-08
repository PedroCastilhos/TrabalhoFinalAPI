import matplotlib.pyplot as plt
import numpy as np
import requests

token = ""
usuarioNome = ""

def titulo(texto, sublinhado="-"):
    print()
    print(texto)
    print(sublinhado*40)

def login():
    titulo("Login do Usuário")
    email = input("E-mail: ")
    senha = input("Senha: ")

    response = requests.post("http://localhost:3000/login", 
                             json={"email": email, "senha": senha})

    if response.status_code != 200:
        print("Erro... Login ou Senha inválidos")
        return

    dados = response.json()
    global token 
    global usuarioNome
    token = dados['token']
    usuarioNome = dados['nome']
    print(f"Bem-vindo ao sistema: {usuarioNome}")

def inclusao():
    titulo("Inclusão de Chinelos")

    if not token:
        print("Erro... Você deve logar-se primeiro")
        return

    marca = input("Qual a marca: ")
    cor = input("Cor: ")
    tamanho = int(input("Tamanho: "))
    preco = float(input("Preço: "))

    response = requests.post("http://localhost:3000/chinelos", 
                             json={"marca": marca, "cor": cor, "tamanho": tamanho, "preco": preco},
                             headers={"Authorization": f"Bearer {token}"})

    if response.status_code == 201:
        dados = response.json()
        print(f"Ok... Chinelo cadastrado com o código {dados['id']}")
    else:
        print(f"Erro... Não foi possível cadastrar o Chinelo")

def listar():
    titulo("Listagem de Chinelos")

    if not token:
        print("Erro... Você deve logar-se primeiro")
        return

    response = requests.get("http://localhost:3000/chinelos", 
                            headers={"Authorization": f"Bearer {token}"})

    if response.status_code != 200:
        print("Erro... Não foi possível conectar com a API")
        return

    dados = response.json()
    for chinelo in dados:
        print(f"ID: {chinelo['id']}, Marca: {chinelo['marca']}, Cor: {chinelo['cor']}, Tamanho: {chinelo['tamanho']}, Preço: {chinelo['preco']}")

def alterar():
    titulo("Alteração de Chinelos")

    if not token:
        print("Erro... Você deve logar-se primeiro")
        return

    id_chinelo = int(input("ID do Chinelo a ser alterado: "))
    marca = input("Nova marca: ")
    cor = input("Nova cor: ")
    tamanho = int(input("Novo tamanho: "))
    preco = float(input("Novo preço: "))

    response = requests.put(f"http://localhost:3000/chinelos/{id_chinelo}", 
                            json={"marca": marca, "cor": cor, "tamanho": tamanho, "preco": preco},
                            headers={"Authorization": f"Bearer {token}"})

    if response.status_code == 200:
        print(f"Ok... Chinelo alterado com sucesso")
    else:
        print(f"Erro... Não foi possível alterar o Chinelo")

def excluir():
    titulo("Exclusão de Chinelos")

    if not token:
        print("Erro... Você deve logar-se primeiro")
        return

    id_chinelo = int(input("ID do Chinelo a ser excluído: "))

    response = requests.delete(f"http://localhost:3000/chinelos/{id_chinelo}",
                               headers={"Authorization": f"Bearer {token}"})

    if response.status_code == 200:
        print(f"Ok... Chinelo excluído com sucesso")
    else:
        print(f"Erro... Não foi possível excluir o Chinelo")

def agrupar_por_cor():
    titulo("Agrupamento de Chinelos por Cor")

    if not token:
        print("Erro... Você deve logar-se primeiro")
        return

    response = requests.get("http://localhost:3000/chinelos", 
                            headers={"Authorization": f"Bearer {token}"})

    if response.status_code != 200:
        print("Erro... Não foi possível conectar com a API")
        return

    dados = response.json()
    agrupamento = {}
    
    for chinelo in dados:
        cor = chinelo['cor']
        if cor not in agrupamento:
            agrupamento[cor] = []
        agrupamento[cor].append(chinelo)
    
    for cor, chs in agrupamento.items():
        print(f"\nCor: {cor}")
        for chinelo in chs:
            print(f"ID: {chinelo['id']}, Marca: {chinelo['marca']}, Tamanho: {chinelo['tamanho']}, Preço: {chinelo['preco']}")

def agrupar_por_preco():
    titulo("Agrupamento de Chinelos por Preço")

    if not token:
        print("Erro... Você deve logar-se primeiro")
        return

    response = requests.get("http://localhost:3000/chinelos", 
                            headers={"Authorization": f"Bearer {token}"})

    if response.status_code != 200:
        print("Erro... Não foi possível conectar com a API")
        return

    dados = response.json()
    agrupamento = {}
    
    for chinelo in dados:
        preco = chinelo['preco']
        if preco not in agrupamento:
            agrupamento[preco] = []
        agrupamento[preco].append(chinelo)
    
    for preco, chs in agrupamento.items():
        print(f"\nPreço: {preco}")
        for chinelo in chs:
            print(f"ID: {chinelo['id']}, Marca: {chinelo['marca']}, Cor: {chinelo['cor']}, Tamanho: {chinelo['tamanho']}")

def agrupar_por_tamanho():
    titulo("Agrupamento de Chinelos por Tamanho")

    if not token:
        print("Erro... Você deve logar-se primeiro")
        return

    response = requests.get("http://localhost:3000/chinelos", 
                            headers={"Authorization": f"Bearer {token}"})

    if response.status_code != 200:
        print("Erro... Não foi possível conectar com a API")
        return

    dados = response.json()
    agrupamento = {}
    
    for chinelo in dados:
        tamanho = chinelo['tamanho']
        if tamanho not in agrupamento:
            agrupamento[tamanho] = []
        agrupamento[tamanho].append(chinelo)
    
    for tamanho, chs in agrupamento.items():
        print(f"\nTamanho: {tamanho}")
        for chinelo in chs:
            print(f"ID: {chinelo['id']}, Marca: {chinelo['marca']}, Cor: {chinelo['cor']}, Preço: {chinelo['preco']}")

def grafico():
    titulo("Gráfico comparando Cor e Marca")

    cor1 = input("1ª Cor: ")
    cor2 = input("2ª Cor: ")
    cor3 = input("3ª Cor: ")

    faixas = ("Até 5 anos", "Entre 6 e 10 anos", "Acima de 10 anos")
    animais = {
        cor1: [0, 0, 0],
        cor2: [0, 0, 0],
        cor3: [0, 0, 0],
    }

    response = requests.get("http://localhost:3000/chinelos")

    if response.status_code != 200:
        print("Erro... Não foi possível conectar com a API")
        return

    dados = response.json()

    for linha in dados:
        if linha['cor'] == cor1:
            if linha['idade'] <= 5:
                animais[cor1][0] += 1
            elif linha['idade'] <= 10:
                animais[cor1][1] += 1          
            else:
                animais[cor1][2] += 1   
        elif linha['cor'] == cor2:
            if linha['idade'] <= 5:
                animais[cor2][0] += 1
            elif linha['idade'] <= 10:
                animais[cor2][1] += 1          
            else:
                animais[cor2][2] += 1   
        elif linha['cor'] == cor3:
            if linha['idade'] <= 5:
                animais[cor3][0] += 1
            elif linha['idade'] <= 10:
                animais[cor3][1] += 1          
            else:
                animais[cor3][2] += 1   

    x = np.arange(len(faixas))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in animais.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    ax.set_ylabel('Quantidades')
    ax.set_title('Gráfico Comparativo por marca')
    ax.set_xticks(x + width, faixas)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 10)

    plt.show()

def main():
    while True:
        titulo("Menu Principal")
        print("1. Login")
        print("2. Incluir chinelo")
        print("3. Listar chinelos")
        print("4. Alterar chinelo")
        print("5. Excluir chinelo")
        print("6. Agrupar chinelos por cor")
        print("7. Agrupar chinelos por preço")
        print("8. Agrupar chinelos por tamanho")
        print("9. Gerar gráfico")
        print("0. Sair")

        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            login()
        elif opcao == 2:
            inclusao()
        elif opcao == 3:
            listar()
        elif opcao == 4:
            alterar()
        elif opcao == 5:
            excluir()
        elif opcao == 6:
            agrupar_por_cor()
        elif opcao == 7:
            agrupar_por_preco()
        elif opcao == 8:
            agrupar_por_tamanho()
        elif opcao == 9:
            grafico()
        elif opcao == 0:
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
