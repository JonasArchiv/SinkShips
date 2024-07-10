import random

def print_board(board):
    for row in board:
        print(" ".join(row))

def create_board(size):
    return [["O"] * size for _ in range(size)]

def place_ship(board, ship_size, size):
    placed = False
    while not placed:
        orientation = random.choice(["horizontal", "vertical"])
        if orientation == "horizontal":
            ship_row = random.randint(0, size - 1)
            ship_col = random.randint(0, size - ship_size)
            if all(board[ship_row][ship_col + i] == "O" for i in range(ship_size)):
                for i in range(ship_size):
                    board[ship_row][ship_col + i] = "S"
                placed = True
                return [(ship_row, ship_col + i) for i in range(ship_size)]
        else:
            ship_row = random.randint(0, size - ship_size)
            ship_col = random.randint(0, size - 1)
            if all(board[ship_row + i][ship_col] == "O" for i in range(ship_size)):
                for i in range(ship_size):
                    board[ship_row + i][ship_col] = "S"
                placed = True
                return [(ship_row + i, ship_col) for i in range(ship_size)]

def get_user_guess(player):
    print(f"Spieler {player}, dein Zug:")
    guess_row = int(input("Rate die Zeile: "))
    guess_col = int(input("Rate die Spalte: "))
    return (guess_row, guess_col)

def is_guess_correct(guess, ships):
    for ship in ships:
        if guess in ship:
            ship.remove(guess)
            return True, not ship
    return False, False

def all_ships_sunk(ships):
    return all(len(ship) == 0 for ship in ships)

def main():
    board_size = 10
    ship_sizes = [5, 4, 3, 3, 2]

    board1 = create_board(board_size)
    hidden_board1 = create_board(board_size)
    ships1 = [place_ship(board1, size, board_size) for size in ship_sizes]

    board2 = create_board(board_size)
    hidden_board2 = create_board(board_size)
    ships2 = [place_ship(board2, size, board_size) for size in ship_sizes]

    print("Lass uns Schiffe versenken spielen!")
    turns = 20

    for turn in range(turns):
        print(f"Spieler 1, dein Zug:")
        print_board(hidden_board2)
        guess = get_user_guess(1)
        if 0 <= guess[0] < board_size and 0 <= guess[1] < board_size:
            hit, sunk = is_guess_correct(guess, ships2)
            if hit:
                print("Treffer!")
                hidden_board2[guess[0]][guess[1]] = "X"
                if sunk:
                    print("Du hast ein Schiff versenkt!")
            else:
                if hidden_board2[guess[0]][guess[1]] == "X":
                    print("Du hast dieses Feld bereits geraten.")
                else:
                    print("Daneben!")
                    hidden_board2[guess[0]][guess[1]] = "X"
        else:
            print("Das ist nicht auf dem Ozean.")
        print_board(hidden_board2)
        
        if all_ships_sunk(ships2):
            print("Spieler 1 hat gewonnen! Herzlichen Glückwunsch!")
            break
        
        print(f"Spieler 2, dein Zug:")
        print_board(hidden_board1)
        guess = get_user_guess(2)
        if 0 <= guess[0] < board_size and 0 <= guess[1] < board_size:
            hit, sunk = is_guess_correct(guess, ships1)
            if hit:
                print("Treffer!")
                hidden_board1[guess[0]][guess[1]] = "X"
                if sunk:
                    print("Du hast ein Schiff versenkt!")
            else:
                if hidden_board1[guess[0]][guess[1]] == "X":
                    print("Du hast dieses Feld bereits geraten.")
                else:
                    print("Daneben!")
                    hidden_board1[guess[0]][guess[1]] = "X"
        else:
            print("Das ist nicht auf dem Ozean.")
        print_board(hidden_board1)
        
        if all_ships_sunk(ships1):
            print("Spieler 2 hat gewonnen! Herzlichen Glückwunsch!")
            break

    if not all_ships_sunk(ships1) and not all_ships_sunk(ships2):
        print("Das Spiel ist unentschieden!")

if __name__ == "__main__":
    main()
