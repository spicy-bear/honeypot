import logging
import socket

# Set up logger to write to syslog
logger = logging.getLogger("PortListener")
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address="/dev/log")
logger.addHandler(handler)

# Create a list of all common ports
common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 993, 995]

# Open a file to log SSH credentials
ssh_credentials_file = open("ssh_credentials.log", "w")

# Create a socket for each port and listen for connections
for port in common_ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", port))
    s.listen()
    logger.info(f"Listening on port {port}")

    # For each incoming connection on port 22 (SSH), log the credentials
    if port == 22:
        conn, addr = s.accept()
        logger.info(f"Received connection from {addr[0]}")
        data = conn.recv(1024)
        username, password = data.split(":")
        ssh_credentials_file.write(f"{username}:{password}\n")
        ssh_credentials_file.flush()

ssh_credentials_file.close()
