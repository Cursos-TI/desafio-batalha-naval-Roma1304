import random

TAMANHO = 5
NUM_NAVIOS = 3

def criar_tabuleiro():
    return [["~"] * TAMANHO for _ in range(TAMANHO)]

def posicionar_navios(tabuleiro):
    navios = 0
    while navios < NUM_NAVIOS:
        linha = random.randint(0, TAMANHO - 1)
        coluna = random.randint(0, TAMANHO - 1)
        if tabuleiro[linha][coluna] != "N":
            tabuleiro[linha][coluna] = "N"
            navios += 1

def mostrar_tabuleiro(tabuleiro):
    print("  " + " ".join(str(i) for i in range(TAMANHO)))
    for i, linha in enumerate(tabuleiro):
        print(f"{i} " + " ".join(linha))

def revelar_navios(tabuleiro_jogador, tabuleiro_comp):
    for i in range(TAMANHO):
        for j in range(TAMANHO):
            if tabuleiro_comp[i][j] == "N":
                tabuleiro_jogador[i][j] = "N"

def jogar():
    tabuleiro_comp = criar_tabuleiro()
    tabuleiro_jogador = criar_tabuleiro()
    posicionar_navios(tabuleiro_comp)
    tentativas = 10
    acertos = 0

    print("=== BATALHA NAVAL ===")
    print("Tente afundar os 3 navios do inimigo!")
    print(f"Você tem {tentativas} tentativas.\n")

    while tentativas > 0 and acertos < NUM_NAVIOS:
        mostrar_tabuleiro(tabuleiro_jogador)
        try:
            linha = int(input("Linha (0-4): "))
            coluna = int(input("Coluna (0-4): "))
        except ValueError:
            print("Entrada inválida! Use números.")
            continue

        if not (0 <= linha < TAMANHO and 0 <= coluna < TAMANHO):
            print("Fora do tabuleiro!")
            continue

        if tabuleiro_jogador[linha][coluna] != "~":
            print("Você já atirou aqui!")
            continue

        if tabuleiro_comp[linha][coluna] == "N":
            print(f"💥 Acertou um navio em ({linha}, {coluna})!")
            tabuleiro_jogador[linha][coluna] = "X"
            acertos += 1
        else:
            print(f"🌊 Errou em ({linha}, {coluna})!")
            tabuleiro_jogador[linha][coluna] = "O"

        tentativas -= 1
        print(f"Tentativas restantes: {tentativas}\n")

    mostrar_tabuleiro(tabuleiro_jogador)

    if acertos == NUM_NAVIOS:
        print("🎉 Parabéns! Você venceu!")
    else:
        print("💀 Game over! Os navios sobreviveram.")
        print("Posições dos navios inimigos:")
        revelar_navios(tabuleiro_jogador, tabuleiro_comp)
        mostrar_tabuleiro(tabuleiro_jogador)

if __name__ == "__main__":
    jogar()