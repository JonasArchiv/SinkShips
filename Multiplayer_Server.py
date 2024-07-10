import socket
import threading
import random

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

def all_ships_sunk(ships):
    return all(len(ship) == 0 for ship in ships)

def handle_client(client_socket, opponent_socket, board, hidden_board, ships, opponent_hidden_board, opponent_ships):
    while True:
        try:
            guess = client_socket.recv(1024).decode('utf-8')
            guess = tuple(map(int, guess.split(',')))

            hit = False
            sunk = False
            if 0 <= guess[0] < 10 and 0 <= guess[1] < 10:
                for ship in ships:
                    if guess in ship:
                        ship.remove(guess)
                        hit = True
                        sunk = not ship
                        break

            if hit:
                hidden_board[guess[0]][guess[1]] = "X"
                client_socket.send("Treffer!".encode('utf-8'))
                if sunk:
                    client_socket.send("Du hast ein Schiff versenkt!".encode('utf-8'))
                    if all_ships_sunk(ships):
                        client_socket.send("Gewonnen!".encode('utf-8'))
                        opponent_socket.send("Verloren!".encode('utf-8'))
                        break
            else:
                if hidden_board[guess[0]][guess[1]] == "X":
                    client_socket.send("Bereits geraten.".encode('utf-8'))
                else:
                    hidden_board[guess[0]][guess[1]] = "X"
                    client_socket.send("Daneben!".encode('utf-8'))

            opponent_socket.send(f"{guess[0]},{guess[1]}".encode('utf-8'))
        except:
            client_socket.close()
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(2)
    print("Server läuft und wartet auf Spieler...")

    clients = []

    while len(clients) < 2:
        client_socket, addr = server.accept()
        print(f"Verbindung von {addr} akzeptiert.")
        clients.append(client_socket)
        client_socket.send("Willkommen! Warte auf einen anderen Spieler...".encode('utf-8'))

    board1 = create_board(10)
    hidden_board1 = create_board(10)
    ships1 = [place_ship(board1, size, 10) for size in [5, 4, 3, 3, 2]]

    board2 = create_board(10)
    hidden_board2 = create_board(10)
    ships2 = [place_ship(board2, size, 10) for size in [5, 4, 3, 3, 2]]

    clients[0].send("Spieler 1, dein Zug!".encode('utf-8'))
    clients[1].send("Spieler 2, dein Zug!".encode('utf-8'))

    threading.Thread(target=handle_client, args=(clients[0], clients[1], board1, hidden_board1, ships1, hidden_board2, ships2)).start()
    threading.Thread(target=handle_client, args=(clients[1], clients[0], board2, hidden_board2, ships2, hidden_board1, ships1)).start()

if __name__ == "__main__":
    main()
