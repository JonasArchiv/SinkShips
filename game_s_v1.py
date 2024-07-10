import random


def print_board(board):
    for row in board:
        print(" ".join(row))


def create_board(size):
    return [["O"] * size for _ in range(size)]


def place_ship(board, size):
    ship_row = random.randint(0, size - 1)
    ship_col = random.randint(0, size - 1)
    board[ship_row][ship_col] = "S"
    return (ship_row, ship_col)


def get_user_guess():
    guess_row = int(input("Rate die Zeile: "))
    guess_col = int(input("Rate die Spalte: "))
    return (guess_row, guess_col)


def is_guess_correct(guess, ship_location):
    return guess == ship_location


def main():
    board_size = 5
    board = create_board(board_size)
    ship_location = place_ship(board, board_size)
    print("Lass uns Schiffe versenken spielen!")
    print_board(board)

    for turn in range(4):
        print(f"Turn {turn + 1}")
        guess = get_user_guess()

        if is_guess_correct(guess, ship_location):
            print("Herzlichen Glückwunsch! Du hast mein Schiff versenkt!")
            break
        else:
            if 0 <= guess[0] < board_size and 0 <= guess[1] < board_size:
                if board[guess[0]][guess[1]] == "X":
                    print("Du hast dieses Feld bereits geraten.")
                else:
                    print("Daneben!")
                    board[guess[0]][guess[1]] = "X"
            else:
                print("Das ist nicht auf dem Ozean.")
        print_board(board)

        if turn == 3:  # Letzter Versuch, ändere die == X für die Anzahl der Versuche
            print("Game Over. Das Schiff war an Position:", ship_location)
            print_board(board)


if __name__ == "__main__":
    main()
