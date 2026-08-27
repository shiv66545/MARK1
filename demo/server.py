from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import json


HOST = "0.0.0.0"
PORT = 8080


class APIHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):
        response = json.dumps(data).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(response)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):

        if self.path == "/api/status":
            self.send_json(200, {
                "status": "online",
                "server": "Python HTTPS Backend"
            })

        elif self.path == "/api/data":
            self.send_json(200, {
                "message": "Hello from HTTPS Python!",
                "data": [10, 20, 30, 40]
            })

        else:
            self.send_json(404, {
                "error": "Endpoint not found"
            })

    def do_POST(self):

        if self.path == "/api/data":

            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)

            try:
                data = json.loads(body.decode("utf-8"))

                print("Received:", data)

                self.send_json(200, {
                    "success": True,
                    "received": data
                })

            except json.JSONDecodeError:
                self.send_json(400, {
                    "success": False,
                    "error": "Invalid JSON"
                })

        else:
            self.send_json(404, {
                "error": "Endpoint not found"
            })


def main():

    server = HTTPServer((HOST, PORT), APIHandler)

    # Create HTTPS/TLS context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    context.load_cert_chain(
        certfile="server.crt",
        keyfile="server.key"
    )

    server.socket = context.wrap_socket(
        server.socket,
        server_side=True
    )

    print(f"HTTPS server running on https://localhost:{PORT}")
    print("Press CTRL+C to stop.")

    server.serve_forever()


if __name__ == "__main__":
    main()