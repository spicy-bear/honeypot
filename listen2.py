import logging
import sys

from socketserver import TCPServer, ThreadingTCPServer

logger = logging.getLogger("port-listener")
logger.setLevel(logging.INFO)

# Log to syslog
syslog_handler = logging.handlers.SysLogHandler()
syslog_formatter = logging.Formatter("%(name)s: %(message)s")
syslog_handler.setFormatter(syslog_formatter)
logger.addHandler(syslog_handler)

# Log to file
file_handler = logging.FileHandler("ssh_credentials.log")
file_formatter = logging.Formatter("%(asctime)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


class PortListener(ThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

    def handle_request(self):
        logger.info(f"Connection from {self.client_address} on port {self.server_address[1]}")
        if self.server_address[1] == 22:
            # Log credentials from SSH connections
            logger.info(f"Credentials: {self.request.recv(1024).decode()}")
        super().handle_request()


if __name__ == "__main__":
    # Listen on all common ports
    for port in range(1, 65535):
        try:
            server = PortListener(("0.0.0.0", port), TCPServer)
        except OSError:
            continue
        else:
            server.serve_forever()
