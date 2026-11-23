import socket, struct
class Rcon:
    def __init__(self, host='127.0.0.1', port=25598, pw='localtest'):
        self.s = socket.create_connection((host, port), timeout=120); self.i = 0
        self._send(3, pw); self._recv()
    def _send(self, t, body):
        self.i += 1; b = body.encode('utf-8')
        self.s.sendall(struct.pack('<iii', len(b) + 10, self.i, t) + b + b'\0\0')
    def _read(self, n):
        buf = b''
        while len(buf) < n:
            c = self.s.recv(n - len(buf))
            if not c: raise IOError('closed')
            buf += c
        return buf
    def _recv(self):
        n, = struct.unpack('<i', self._read(4)); d = self._read(n)
        return d[8:-2].decode('utf-8', 'replace')
    def cmd(self, c):
        self._send(2, c); return self._recv()
