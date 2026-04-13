from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "0.0.0.0"
PORT = 8080


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            body = b"Hello from Effective Mobile!"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Structured logging: timestamp, method, path, status
        print(f"[backend] {self.address_string()} - {format % args}", flush=True)


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), Handler)
    print(f"[backend] Server started on {HOST}:{PORT}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[backend] Shutting down", flush=True)
        server.server_close()
