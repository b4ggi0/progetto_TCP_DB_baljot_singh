import socket
import json
import mysql.connector
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345  # Porta su cui il server è in ascolto
MAX = 3  # Numero massimo di tentativi di password consentiti

PASSWORD_CORRETTA = "12345"
lock = threading.Lock()

def get_database_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        database="progetto_tepsit",
        port=3306,
    )


def creazione(cursor, tabella, attributi, valori):
    lock.acquire()
    conn = get_database_connection()
    cursor = conn.cursor()

    query = f"INSERT INTO {tabella} ({', '.join(attributi)}) VALUES ({', '.join(['%s']*len(valori))})"

    cursor.execute(query, valori)

    conn.commit()
    cursor.close()
    conn.close()
    lock.release()
    return "Operazione di creazione eseguita con successo."


def lett(cursor, tabella, attributi):
    lock.acquire()
    conn = get_database_connection()
    cursor = conn.cursor()

    query = f"SELECT {attributi} FROM {tabella}"

    cursor.execute(query)

    nomi_campi = [i[0] for i in cursor.description]

    risultati = cursor.fetchall()

    cursor.close()
    conn.close()
    lock.release()
    return {"nomi_campi": nomi_campi, "risultati": risultati}


def eliminazione(cursor, tabella, id):
    lock.acquire()
    conn = get_database_connection()
    cursor = conn.cursor()

    query = f"DELETE FROM {tabella} WHERE id = %s"

    cursor.execute(query, (id,))

    conn.commit()
    cursor.close()
    conn.close()
    lock.release()
    return "Operazione di eliminazione eseguita con successo."


def modifica(cursor, tabella, attributi, vecchio_valore, nuovo_valore):
    lock.acquire()
    conn = get_database_connection()
    cursor = conn.cursor()

    query = f"UPDATE {tabella} SET {attributi} = %s WHERE {attributi} = %s"
    cursor.execute(query, (nuovo_valore, vecchio_valore))
    conn.commit()

    cursor.close()
    conn.close()
    lock.release()
    return "Operazione di modifica eseguita con successo."


def gestisci_connessione(conn):
    # La funzione sessione() ora è incorporata qui

    tentativi = 0
    autenticato = False

    while tentativi < MAX:
        password_tentativo = conn.recv(1024).decode()

        if password_tentativo == PASSWORD_CORRETTA:
            autenticato = True
            conn.send("Benvenuto nel sistema.".encode())
            break
        else:
            conn.send("Password errata. Riprova.".encode())
            tentativi += 1

    if not autenticato:
        conn.close()
        return

    # Connessione al database
    db_conn = get_database_connection()
    cursor = db_conn.cursor()

    while True:

        scelta = conn.recv(1024).decode()

        if scelta == "C":
            cursor.execute("SHOW TABLES")
            tabelle_disponibili = [table[0] for table in cursor.fetchall()]
            conn.send(f"Tabelle disponibili: {', '.join(tabelle_disponibili)}\nSu quale vuoi agire? ".encode())
            tabella = conn.recv(1024).decode()
            conn.send("Inserisci gli attributi da creare (separati da virgola): ".encode())
            attributi = conn.recv(1024).decode().split(',')
            conn.send(f"Inserisci i valori degli attributi per {attributi} (separati da virgola): ".encode())
            valori = conn.recv(1024).decode().split(',')
            risposta = creazione(cursor, tabella, attributi, valori)
            conn.send(risposta.encode())

        elif scelta == "L":
            cursor.execute("SHOW TABLES")
            tabelle_disponibili = [table[0] for table in cursor.fetchall()]

            conn.send(f"Tabelle disponibili: {', '.join(tabelle_disponibili)}\nSu quale vuoi agire? ".encode())

            tabella = conn.recv(1024).decode()

            conn.send("Inserisci gli attributi da visualizzare (separati da virgola): ".encode())
            attributi = conn.recv(1024).decode()

            data = lett(cursor, tabella, attributi)

            dati_json = json.dumps(data)
            conn.send(dati_json.encode())

        elif scelta == "M":
            cursor.execute("SHOW TABLES")
            tabelle_disponibili = [table[0] for table in cursor.fetchall()]
            conn.send(f"Tabelle disponibili: {', '.join(tabelle_disponibili)}\nSu quale vuoi agire? ".encode())
            tabella = conn.recv(1024).decode()

            conn.send("Inserisci l'attributo su cui agire: ".encode())
            attributo = conn.recv(1024).decode()

            conn.send(f"Inserisci il valore attuale per {attributo}: ".encode())
            vecchio_valore = conn.recv(1024).decode()

            conn.send(f"Inserisci il nuovo valore per {attributo}: ".encode())
            nuovo_valore = conn.recv(1024).decode()

            risposta = modifica(cursor, tabella, attributo, vecchio_valore, nuovo_valore)
            conn.send(risposta.encode())

        elif scelta == "E":
            cursor.execute("SHOW TABLES")
            tabelle_disponibili = [table[0] for table in cursor.fetchall()]
            conn.send(f"Tabelle disponibili: {', '.join(tabelle_disponibili)}\nSu quale vuoi agire? ".encode())
            tabella = conn.recv(1024).decode()

            conn.send("Inserisci l'ID della tabella da eliminare: ".encode())
            id_da_eliminare = conn.recv(1024).decode()

            risposta = eliminazione(cursor, tabella, id_da_eliminare)
            conn.send(risposta.encode())

        elif scelta == "exit":
            break

    cursor.close()
    db_conn.close()
    conn.close()


# Inizializza il server
conn_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_server.bind((HOST, PORT))
conn_server.listen(5)  # Numero massimo di connessioni in attesa

print("Server in ascolto su ", HOST, ":", PORT)

# Accetta le connessioni dei client
while True:
    conn, client_address = conn_server.accept()
    print("Connessione accettata da ", client_address)

    # Avvia un thread per gestire la connessione
    threading.Thread(target=gestisci_connessione, args=(conn,)).start()