import logging
from logging import handlers
import socket

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
syslog_handler = handlers.SysLogHandler()
logger.addHandler(syslog_handler)

# Open a file for logging ssh credentials
credentials_file = open("ssh_credentials.txt", "a")

# Create a socket for listening on all common ports
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 0))

# Listen on all common ports
for port in range(1, 65535):
    try:
        sock.listen(1)
        logger.info(f"Listening on port {port}")
    except OSError:
        # Port is not open
        pass

# Continuously accept connections on the socket
while True:
    conn, addr = sock.accept()
    data = conn.recv(1024)

    # Log the received data
    logger.info(f"Received data from {addr}: {data}")

    # If the connection is on port 22 (ssh), log the credentials
    if addr[1] == 22:
        credentials_file.write(f"Credentials from {addr}: {data}\n")

# Close the socket and the credentials file
sock.close()
credentials_file.close()
