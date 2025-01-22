import socket 

PING_RESP = b"+PONG\r\n"
SESSION_END = b"\r\n"
REQ_SIZE = 1024

def process_ping(client_socket):
    try:
        client_socket.send(PING_RESP)
    except Exception:
        print("Error processing PONG")

# Reads newline terminated request from client
def process_client(client_socket, client_address):
    while True:
        try: 
            client_req = client_socket.recv(REQ_SIZE)
            if client_req == SESSION_END: # Client ended connection
                break

            process_ping(client_socket)

        except Exception:
            raise Exception("Error handling client {client_address}: {e}")
    
    client_socket.close()


def main():    
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print("="*10)
            print(f"New connection from {client_address}")

            process_client(client_socket, client_address)
        except KeyboardInterrupt:
            print("\nShutting down server")
            break

    server_socket.close()
    


if __name__ == "__main__":
    main()
