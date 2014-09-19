#server class.  Will interact with protobuffer to parse messages and to call the correct function in the class KeyValueStore.  Needs to handle failure cases

from KeyValueStore import KeyValueStore as KVS
class Server:
	m_kvs = None
	def __init__(self, fileName):
		self.m_kvs = KVS(fileName)
