import socket

def print_board(board):
    for row in board:
        print(" ".join(row))

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    while True:
        response = client.recv(1024).decode('utf-8')
        if response == "Gewonnen!" or response == "Verloren!":
            print(response)
            break
        elif response == "Bereits geraten.":
            print(response)
        elif response.startswith("Treffer!") or response.startswith("Daneben!") or response.startswith("Du hast ein Schiff versenkt!"):
            print(response)
        else:
            guess = input("Rate die Zeile und Spalte (z.B. 3,4): ")
            client.send(guess.encode('utf-8'))

if __name__ == "__main__":
    main()
