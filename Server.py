# server class.
# Will interact with protobuffer to parse messages
# and to call the correct function in the class KeyValueStore.
# Needs to handle failure cases

import sys
sys.path.insert(0, './modules')

from kvservice_pb2 import *
from protobufrpc.synchronous import TcpServer

from KeyValueStore import KeyValueStore

#class Server:
#	m_kvs = None
#	def __init__(self, fileName):
#		self.m_kvs = KVS(fileName)

class KeyValueService (KVService):
  
  def __init__(self, filename):
    """
    When the server is started we need to connect to the
    KeyValueStore before handling any incoming requests.
    """

    self.m_kvs = KeyValueStore(filename)  
  
  def set(self, rpc_controller, request, done):
    response = Response()
    response.result = 1
    response.value = ""
    
    # send the set to KeyValueStore
    self.m_kvs.put(request.key, request.value)
    
    done(response)

  def get(self, rpc_controller, request, done):
    response = Response()
    response.result = 1
    response.value = ""
    
    # send the get to KeyValueStore
    self.m_kvs.get(request.key)
    
    done(response)


# hardcoding the filename for the moment
testService = KeyValueService("kvstore.txt")


#testService = KeyValueService()
server = TcpServer(("localhost", 8080), testService)
server.serve_forever()
