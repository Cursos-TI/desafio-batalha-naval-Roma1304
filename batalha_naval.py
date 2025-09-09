import random

# Tamanho do tabuleiro
TAMANHO = 5
NUM_NAVIOS = 3

# Criar um tabuleiro vazio
def criar_tabuleiro():
    return [["~"] * TAMANHO for _ in range(TAMANHO)]

# Mostrar o tabuleiro (sem mostrar navios inimigos)
def mostrar_tabuleiro(tabuleiro, mostrar_navios=False):
    print("  " + " ".join(str(i) for i in range(TAMANHO)))
    for idx, linha in enumerate(tabuleiro):
        linha_visivel = []
        for celula in linha:
            if celula == "N" and not mostrar_navios:
                linha_visivel.append("~")
            else:
                linha_visivel.append(celula)
        print(str(idx) + " " + " ".join(linha_visivel))
    print()

# Posicionar navios aleatoriamente
def posicionar_navios(tabuleiro):
    navios = 0
    while navios < NUM_NAVIOS:
        x = random.randint(0, TAMANHO - 1)
        y = random.randint(0, TAMANHO - 1)
        if tabuleiro[x][y] != "N":
            tabuleiro[x][y] = "N"
            navios += 1

# Jogada do jogador
def jogada(tabuleiro_inimigo, x, y):
    if tabuleiro_inimigo[x][y] == "N":
        tabuleiro_inimigo[x][y] = "X"
        print("💥 Acertou um navio!")
        return True
    elif tabuleiro_inimigo[x][y] in ["X", "O"]:
        print("⚠️ Já atirou aí.")
        return None
    else:
        tabuleiro_inimigo[x][y] = "O"
        print("🌊 Água!")
        return False

# Verificar se todos os navios foram afundados
def verificar_derrota(tabuleiro):
    for linha in tabuleiro:
        if "N" in linha:
            return False
    return True

# Jogo principal
def jogar():
    jogador = criar_tabuleiro()
    computador = criar_tabuleiro()

    posicionar_navios(jogador)
    posicionar_navios(computador)

    print("🌊 Batalha Naval - Você vs Computador 🌊")
    rodada = 1

    while True:
        print(f"\n🔁 Rodada {rodada}")
        print("Seu tabuleiro:")
        mostrar_tabuleiro(jogador, mostrar_navios=True)
        print("Tabuleiro do computador:")
        mostrar_tabuleiro(computador)

        try:
            x = int(input("Linha (0 a 4): "))
            y = int(input("Coluna (0 a 4): "))
        except ValueError:
            print("❌ Entrada inválida. Use números.")
            continue

        if not (0 <= x < TAMANHO and 0 <= y < TAMANHO):
            print("❌ Coordenadas fora do tabuleiro.")
            continue

        resultado = jogada(computador, x, y)
        if resultado is None:
            continue

        if verificar_derrota(computador):
            print("🎉 Você venceu! Todos os navios inimigos foram afundados!")
            break

        # Jogada aleatória do computador
        while True:
            x_pc = random.randint(0, TAMANHO - 1)
            y_pc = random.randint(0, TAMANHO - 1)
            if jogador[x_pc][y_pc] in ["X", "O"]:
                continue
            print(f"💣 O computador atira em ({x_pc}, {y_pc})...")
            jogada(jogador, x_pc, y_pc)
            break

        if verificar_derrota(jogador):
            print("💀 Você perdeu! O computador afundou todos os seus navios.")
            break

        rodada += 1

# Executar o jogo
if __name__ == "__main__":
    jogar()