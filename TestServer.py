import sys
import socket
sys.path.insert(0, './modules')

from kvservice_pb2 import *
from kv739_server import *


server = kv739_server((socket.getfqdn(), 8000))
#server = kv739_server(("adelie-01.cs.wisc.edu", 8000))
server.serve_forever()
