import socket
import threading

class Service:
    def __init__(self):
        # Initialize the memory state here
        self.memory_state = {}
        self.memory_state_history = []

    def handle_client(self, client_socket):
        while True:
            # Receive data from the client (Electron app)
            request = client_socket.recv(1024)
            if not request:
                break

            # Print the received data to the command prompt
            print("Received:", request.decode('utf-8'))
            decoded_data = request.decode('utf-8')

            # Process the received data (modify as needed)
            # For example, you can perform some computation or logic here
            # Try to convert the decoded data to a number
            try:
                processed_data = str(float(decoded_data))
                self.memory_state_history.append(float(decoded_data))
            except ValueError:
                # If conversion to a number fails, keep it as string
                processed_data = decoded_data
            
            
            # Store the processed data in the memory state
            self.memory_state['processed_data'] = processed_data

            # Send the processed data back to the client (Electron app)
            client_socket.send(processed_data.encode('utf-8'))
        

        # Close the client socket when the connection is closed
        client_socket.close()
        print("Memory state at end of connection:", self.memory_state_history)

    def start_service(self):
        # Change the port and hostname as needed
        host = '127.0.0.1'  # Listen on all network interfaces
        port = 3000

        # Create a TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the address and port
        server_socket.bind((host, port))

        # Start listening for incoming connections
        server_socket.listen(5)
        print(f'Service listening on {host}:{port}')

        while True:
            # Accept incoming connections
            client_socket, client_address = server_socket.accept()
            print(f'Accepted connection from {client_address[0]}:{client_address[1]}')

            # Handle the client connection in a separate thread
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == '__main__':
    service = Service()
    service.start_service()
