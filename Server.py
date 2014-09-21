# server class.
# Will interact with protobuffer to parse messages
# and to call the correct function in the class KeyValueStore.
# Needs to handle failure cases

import sys
sys.path.insert(0, './modules')

from protobufrpc import tx
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
from kvservice_pb2 import KVService, KVService_Stub, SetRequest, GetRequest, Response
from KeyValueStore import KeyValueStore as KVS

class Server:
	m_kvs = None
	def __init__(self, fileName):
		self.m_kvs = KVS(fileName)
