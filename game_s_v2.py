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


def get_user_guess():
    guess_row = int(input("Rate die Zeile: "))
    guess_col = int(input("Rate die Spalte: "))
    return (guess_row, guess_col)


def is_guess_correct(guess, ships):
    for ship in ships:
        if guess in ship:
            ship.remove(guess)
            return True, not ship
    return False, False


def main():
    board_size = 10
    board = create_board(board_size)
    hidden_board = create_board(board_size)
    ship_sizes = [5, 4, 3, 3, 2]
    ships = []

    for size in ship_sizes:
        ships.append(place_ship(board, size, board_size))

    print("Lass uns Schiffe versenken spielen!")
    print_board(hidden_board)

    turns = 25  # Anzahl der Versuche
    sunk_ships = 0

    for turn in range(turns):
        print(f"Turn {turn + 1} von {turns}")
        guess = get_user_guess()

        if 0 <= guess[0] < board_size and 0 <= guess[1] < board_size:
            hit, sunk = is_guess_correct(guess, ships)
            if hit:
                print("Treffer!")
                hidden_board[guess[0]][guess[1]] = "X"
                if sunk:
                    sunk_ships += 1
                    print("Du hast ein Schiff versenkt!")
            else:
                if hidden_board[guess[0]][guess[1]] == "X":
                    print("Du hast dieses Feld bereits geraten.")
                else:
                    print("Daneben!")
                    hidden_board[guess[0]][guess[1]] = "X"
        else:
            print("Das ist nicht auf dem Ozean.")

        print_board(hidden_board)

        if sunk_ships == len(ship_sizes):
            print("Herzlichen Glückwunsch! Du hast alle Schiffe versenkt!")
            break

        if turn == turns - 1:
            print("Game Over. Du hast nicht alle Schiffe versenkt.")
            print("Die Schiffe waren an folgenden Positionen:")
            print_board(board)


if __name__ == "__main__":
    main()
