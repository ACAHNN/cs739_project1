# server class.
# Will interact with protobuffer to parse messages
# and to call the correct function in the class KeyValueStore.
# Needs to handle failure cases

import sys
sys.path.insert(0, './modules')

from kvservice_pb2 import *
from protobufrpc.synchronous import TcpServer

from KeyValueStore import KeyValueStore as KVS

#class Server:
#	m_kvs = None
#	def __init__(self, fileName):
#		self.m_kvs = KVS(fileName)

class KeyValueService (KVService):
  def set(self, rpc_controller, request, done):
    response = Response()
    response.result = 1
    response.value = ""
    done(response)

  def get(self, rpc_controller, request, done):
    response = Response()
    response.result = 1
    response.value = ""
    done(response)

testService = KeyValueService()
server = TcpServer(("localhost", 8080), testService)
server.serve_forever()