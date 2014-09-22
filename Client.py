import sys
sys.path.insert(0, './modules')

from kvservice_pb2 import *
from protobufrpc.synchronous import Proxy, TcpChannel
from google.protobuf.text_format import *
from sys import stdout

if __name__ == "__main__":
  
  # open the tcp channel
  channel = TcpChannel(("localhost", 8080))
  proxy = Proxy(KVService_Stub(channel))
  
  # test of SetRequest
  request = SetRequest()
  request.key = "Hello"
  request.value = "World"
  response = proxy.KVService.set(request)
  for r in response:
    PrintMessage(r, stdout, 0)

  # test of GetRequest
  request = GetRequest()
  request.key = "Hello"
  response = proxy.KVService.get(request)
  for r in response:
    PrintMessage(r, stdout, 0)
