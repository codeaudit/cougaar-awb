import SimpleXMLRPCServer
import xmlrpclib
from ServerMethods import ServerMethods
class ServletDataReceiver:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    def serve(self):
        receiver = ServerMethods()    
        server = SimpleXMLRPCServer.SimpleXMLRPCServer((self.host, self.port))
        server.register_instance(receiver)
        print 'ServletDataReceiver @', self.host, ":", self.port
        server.serve_forever()

if __name__ == '__main__':
    s = ServletDataReceiver("localhost", 8000)
    s.serve()