import json
import socket
from config.env_reader import ConfigReader as conf_reader



class DispServer:
    def __init__(self, disp_controller):
        self._disp = disp_controller
        self._sock = None

    def start(self):
        port = conf_reader.get_int("SERVER_PORT", 8080)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(("0.0.0.0", port))
        self._sock.listen(1)
        print("Server: listening on port", port)

        while True:
            client = None
            try:
                client, addr = self._sock.accept()
                self._handle(client)
            except Exception as exc:
                print("Server: error —", exc)
            finally:
                if client is not None:
                    client.close()

    def _handle(self, client):
        raw = client.recv(1024).decode("utf-8")
        if not raw:
            return

        first_line = raw.split("\r\n")[0]
        parts = first_line.split(" ")
        if len(parts) < 2:
            self._respond(client, 400, "Bad request")
            return

        method = parts[0]
        path = parts[1]

        if method == "POST" and path == "/msg":
            self._handle_status(client, raw)
        elif method == "GET" and path == "/health":
            self._respond(client, 200, "ok")
        else:
            self._respond(client, 404, "Not found")

    def _handle_status(self, client, raw):
        body_start = raw.find("\r\n\r\n")
        if body_start < 0:
            self._respond(client, 400, "No body")
            return

        body = raw[body_start + 4:]

        try:
            data = json.loads(body)
        except ValueError:
            self._respond(client, 400, "Invalid JSON")
            return

        info = data.get("info")
        if info is None:
            self._respond(client, 400, "Missing 'info' field")
            return

        ok = self._disp.show_time(info)
        if ok:
            self._respond(client, 200, info)
        else:
            self._respond(client, 400, "Unknown status: " + str(info))

    def _respond(self, client, code, message):
        if code == 200:
            status_text = "OK"
        elif code == 400:
            status_text = "Bad Request"
        else:
            status_text = "Not Found"

        response = "HTTP/1.1 " + str(code) + " " + status_text + "\r\n"
        response += "Content-Type: text/plain\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += message
        client.send(response.encode("utf-8"))
