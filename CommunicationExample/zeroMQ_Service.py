import zmq
import threading

class Service:
    def __init__(self):
        # Initialize the memory state here
        self.memory_state = {}
        self.memory_state_history = []

    def handle_client(self):
        context = zmq.Context()
        # Create a ZeroMQ REP socket
        socket = context.socket(zmq.REP)
        socket.bind("tcp://127.0.0.1:3000")

        while True:
            # Receive data from the client (Electron app)
            request = socket.recv()
            decoded_data = request.decode('utf-8')

            # Print the received data to the command prompt
            print("Received:", decoded_data)

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
            socket.send(processed_data.encode('utf-8'))
            print("Memory state at end of connection:", self.memory_state_history)

        # Close the socket when the connection is closed
        socket.close()
        

    def start_service(self):
        # Start the client handler in a separate thread
        client_handler = threading.Thread(target=self.handle_client)
        client_handler.start()
        print("Service started.")

if __name__ == '__main__':
    service = Service()
    service.start_service()
