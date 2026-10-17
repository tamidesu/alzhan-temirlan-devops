import json
import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = json.loads((ROOT / "config/student.json").read_text())
VERSION = Path(__file__).with_name("version.txt").read_text().strip()

def student_info():
    return {
        key: os.environ.get("STUDENT_" + key.upper(), value)
        for key, value in DEFAULTS.items()
    }



def render():
    student = student_info()
    return (
        "================================\n"
        "DevOps Student Application\n"
        "================================\n"
        f"Name: {student['name']}\n"
        f"Surname: {student['surname']}\n"
        f"Group: {student['group']}\n"
        f"Student ID: {student['id']}\n"
        "Course: DevOps\n"
        f"Application Version: {VERSION}\n"
        "Application is running successfully!\n"
    )

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/health"):
            self.send_error(404)
            return

        text = render() if self.path == "/" else "OK\n"
        body = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(render(), flush=True)
    print(f"Listening on port {port}", flush=True)
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nApplication stopped.", flush=True)
    finally:
        server.server_close()
