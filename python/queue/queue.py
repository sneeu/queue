import SocketServer 


_PORT = 1982
_QUEUE = []


class QueueHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global _QUEUE
        line = self.request.recv(1024).strip()
        if line[:5] == 'PUSH ':
            _QUEUE.append(line[5:])
            self.request.sendall("{'status': 'OK'}\n")
            return
        elif line == 'POP':
            if len(_QUEUE) == 0:
                self.request.sendall("{'status': 'EMPTY'}\n")
            else:
                item = _QUEUE[0]
                if len(_QUEUE) > 1:
                    _QUEUE = _QUEUE[1:]
                else:
                    _QUEUE = []
                self.request.sendall("{'status': 'OK', 'payload': %s}\n" % item)
        elif line == 'STAT':
            self.request.sendall("{'status': 'OK', 'payload': %d}\n" % len(_QUEUE))
        else:
            self.request.sendall("{'status': 'ERR'}\n")


def start_server():
    server = SocketServer.TCPServer(('localhost', _PORT), QueueHandler)
    server.serve_forever()

if __name__ == '__main__':
    start_server()
