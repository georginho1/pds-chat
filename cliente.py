import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            # Recebe e imprime mensagens do servidor
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            break

def start_client():
    host = "127.0.0.1"
    port = 55555

    client_name = input("Digite seu nome: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Envia o nome do cliente para o servidor
    client_socket.send(client_name.encode("utf-8"))

    # Inicia uma thread para receber mensagens do servidor
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        # Envia mensagens para o servidor
        message = input()
        client_socket.send(message.encode("utf-8"))

if __name__ == "__main__":
    start_client()
