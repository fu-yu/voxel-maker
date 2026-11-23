import sys, re
from http.server import BaseHTTPRequestHandler, HTTPServer
out = sys.argv[1]
class H(BaseHTTPRequestHandler):
    def do_POST(self):
        name = re.sub(r'[^a-z0-9_]', '', self.path.strip('/'))[:40] or 'x'
        data = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        open(f'{out}/{name}.zip', 'wb').write(data)
        self.send_response(200); self.send_header('Access-Control-Allow-Origin', '*'); self.end_headers(); self.wfile.write(b'ok')
    def log_message(self, *a): pass
HTTPServer(('127.0.0.1', 8767), H).serve_forever()
