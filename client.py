import socket
import json

HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345  # Porta su cui il server è in ascolto

    # Inizializza il client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))




for _ in range(3):
        password = input("Inserisci la password: ")
        client_socket.send(password.encode())

        response = client_socket.recv(1024).decode()
        print(response)

        if response == "Benvenuto nel sistema.":
            break
        elif response == "Password errata. Riprova.":
            continue

if "Benvenuto" in response:
        while True:
            scelta = input("Cosa vuoi fare? (C/L/M/E/exit): ")
            client_socket.send(scelta.encode())

            if scelta == "C":
                print(client_socket.recv(1024).decode(), end='')
                tabella = input()
                client_socket.send(tabella.encode())

                print(client_socket.recv(1024).decode(), end='')
                attributi = input().split(",")  
                client_socket.send(','.join(attributi).encode())

                print(client_socket.recv(1024).decode(), end='')
                valori = input().split(",")  
                client_socket.send(','.join(valori).encode())

                risposta_creazione = client_socket.recv(1024).decode()
                print(risposta_creazione)


            elif scelta == "L":
                print(client_socket.recv(4096).decode(),end='')
                tabella = input()
                client_socket.send(tabella.encode())
                
                print(client_socket.recv(4096).decode(),end='')
                attributi = input()
                client_socket.send(attributi.encode())

                datijson = client_socket.recv(4096).decode()
                desereliz_data = json.loads(datijson)

                nomi_campi = desereliz_data["nomi_campi"]
                risultati = desereliz_data["risultati"]

                print("Nomi dei campi della tabella:", nomi_campi)
                print("Risultati:")
                for riga in risultati:
                    print(riga)

            elif scelta == "M":
                print(client_socket.recv(1024).decode(), end='')
                tabella = input()
                client_socket.send(tabella.encode())

                print(client_socket.recv(1024).decode(), end='')
                attributo = input()
                client_socket.send(attributo.encode())

                print(client_socket.recv(1024).decode(), end='')
                vecchio_valore = input()
                client_socket.send(vecchio_valore.encode())

                print(client_socket.recv(1024).decode(), end='')
                nuovo_valore = input()
                client_socket.send(nuovo_valore.encode())

                risposta = client_socket.recv(1024).decode()
                print(risposta)

            elif scelta == "E":
                print(client_socket.recv(1024).decode(), end='')
                tabella = input()
                client_socket.send(tabella.encode())

                print(client_socket.recv(1024).decode(), end='')
                id_da_eliminare = input()
                client_socket.send(id_da_eliminare.encode())

                risposta = client_socket.recv(1024).decode()
                print(risposta)
            elif scelta == "exit":
                break

client_socket.close()