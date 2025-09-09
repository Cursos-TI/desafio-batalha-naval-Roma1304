import random
import os

BOARD_SIZE = 10
SHIP_SIZES = {
    'Porta-aviões': 5,
    'Encouraçado': 4,
    'Cruzador': 3,
    'Submarino': 3,
    'Destroyer': 2
}

EMPTY = '~'
MISS = 'O'
HIT = 'X'
SHIP = '■'

def create_board():
    """Cria tabuleiro vazio."""
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def print_board(board, hide_ships=False):
    """Exibe o tabuleiro formatado no terminal."""
    print("  " + " ".join([chr(ord('A') + i) for i in range(BOARD_SIZE)]))
    for idx, row in enumerate(board):
        line = f"{idx+1:2} "
        for cell in row:
            if cell == SHIP and hide_ships:
                line += EMPTY + " "
            else:
                line += cell + " "
        print(line)
    print()

def place_ship(board, size):
    """Posiciona um navio de tamanho 'size' aleatoriamente no tabuleiro."""
    placed = False
    while not placed:
        orientation = random.choice(['H', 'V'])
        if orientation == 'H':
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - size)
            if all(board[row][col + i] == EMPTY for i in range(size)):
                for i in range(size):
                    board[row][col + i] = SHIP
                placed = True
        else:
            row = random.randint(0, BOARD_SIZE - size)
            col = random.randint(0, BOARD_SIZE - 1)
            if all(board[row + i][col] == EMPTY for i in range(size)):
                for i in range(size):
                    board[row + i][col] = SHIP
                placed = True

def get_input_position():
    """Solicita uma posição do jogador e retorna os índices da linha e coluna."""
    while True:
        move = input("Digite a posição (ex: A5): ").replace(" ", "").upper()
        if len(move) < 2 or not move[0].isalpha() or not move[1:].isdigit():
            print("Formato inválido.")
            continue
        col = ord(move[0]) - ord('A')
        row = int(move[1:]) - 1
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        print("Posição fora do tabuleiro.")

def player_turn(enemy_board, display_board):
    """Executa o turno do jogador."""
    print("Seu turno:")
    while True:
        row, col = get_input_position()
        if display_board[row][col] in [HIT, MISS]:
            print("Você já atirou aqui.")
            continue
        if enemy_board[row][col] == SHIP:
            print("💥 Acertou!")
            display_board[row][col] = HIT
            enemy_board[row][col] = HIT
        else:
            print("💨 Errou.")
            display_board[row][col] = MISS
            enemy_board[row][col] = MISS
        break

class AI:
    def __init__(self):
        self.previous_hits = []
        self.possible_targets = []
        self.shots = set()

    def choose_target(self):
        """Escolhe o próximo alvo da IA."""
        if self.previous_hits:
            self.update_possible_targets()
            while self.possible_targets:
                r, c = self.possible_targets.pop()
                if (r, c) not in self.shots:
                    return r, c
        while True:
            r = random.randint(0, BOARD_SIZE - 1)
            c = random.randint(0, BOARD_SIZE - 1)
            if (r, c) not in self.shots:
                return r, c

    def update_possible_targets(self):
        """Atualiza a lista de possíveis alvos ao redor dos acertos anteriores."""
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        new_targets = []
        for r, c in self.previous_hits:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and (nr, nc) not in self.shots:
                    new_targets.append((nr, nc))
        random.shuffle(new_targets)
        self.possible_targets.extend(new_targets)

    def turn(self, player_board):
        """Executa o turno da IA."""
        r, c = self.choose_target()
        self.shots.add((r, c))
        print(f"\nIA atirou em {chr(c + ord('A'))}{r+1}")
        if player_board[r][c] == SHIP:
            print("🔥 IA acertou seu navio!")
            player_board[r][c] = HIT
            self.previous_hits.append((r, c))
        else:
            print("🌊 IA errou.")
            player_board[r][c] = MISS
            self.previous_hits = [pos for pos in self.previous_hits if player_board[pos[0]][pos[1]] == HIT]

def check_victory(board):
    """Retorna True se todos os navios foram afundados."""
    for row in board:
        if SHIP in row:
            return False
    return True

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== BATALHA NAVAL: NÍVEL MESTRE ===\n")

    player_board = create_board()
    enemy_board = create_board()
    player_view = create_board()

    for name, size in SHIP_SIZES.items():
        place_ship(player_board, size)
        place_ship(enemy_board, size)

    ai = AI()

    while True:
        print("Seu Tabuleiro:")
        print_board(player_board)

        print("Tabuleiro Inimigo:")
        print_board(player_view, hide_ships=True)

        player_turn(enemy_board, player_view)
        if check_victory(enemy_board):
            print("🎉 Você venceu! Todos os navios inimigos foram afundados.")
            print("\nTabuleiro Inimigo (revelado):")
            print_board(enemy_board)
            break

        ai.turn(player_board)
        if check_victory(player_board):
            print("☠️ A IA venceu. Todos os seus navios foram afundados.")
            print("\nSeu Tabuleiro Final:")
            print_board(player_board)
            break

if __name__ == "__main__":
    main()