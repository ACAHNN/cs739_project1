import sys
sys.path.insert(0, './modules')

from kvservice_pb2 import *
from kv739_server import *

server = kv739_server(("localhost", 8000))
server.serve_forever()