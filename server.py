import socket
import threading

# Lista para armazenar os clientes conectados
clients = []

def handle_client(client_socket, client_address, client_name):
    while True:
        try:
            # Recebe a mensagem do cliente
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                # Se a mensagem estiver vazia, o cliente desconectou
                remove_client(client_socket, client_name)
                break

            # Adiciona o nome do cliente à mensagem
            message_with_name = f"{client_name}: {message}"

            # Transmite a mensagem para todos os clientes conectados
            broadcast(message_with_name, client_socket)

        except Exception as e:
            print(f"Erro durante o tratamento do cliente {client_name}: {e}")
            remove_client(client_socket, client_name)
            break

def broadcast(message, sender_socket):
    for client, _ in clients:
        if client != sender_socket:
            try:
                # Envia a mensagem para todos os clientes, exceto o remetente
                client.send(message.encode("utf-8"))
            except Exception as e:
                print(f"Erro ao enviar mensagem para um cliente: {e}")

def remove_client(client_socket, client_name):
    # Remove o cliente da lista
    clients.remove((client_socket, client_name))
    print(f"Cliente {client_name} desconectado.")
    broadcast(f"O cliente {client_name} saiu do chat.", client_socket)

def start_server():
    host = "127.0.0.1"
    port = 55555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"Servidor escutando em {host}:{port}")

    while True:
        # Aceita a conexão do cliente
        client_socket, client_address = server.accept()

        # Recebe o nome do cliente
        client_name = client_socket.recv(1024).decode("utf-8")

        # Adiciona o cliente à lista
        clients.append((client_socket, client_name))

        print(f"Novo cliente conectado: {client_name}")

        # Envia mensagem de boas-vindas para o cliente
        client_socket.send("Bem-vindo ao chat!".encode("utf-8"))

        # Inicia uma nova thread para lidar com o cliente
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address, client_name)
        )
        client_thread.start()

if __name__ == "__main__":
    start_server()
