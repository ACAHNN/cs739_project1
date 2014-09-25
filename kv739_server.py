import sys
sys.path.insert(0, './modules')

import socket
import struct
import SocketServer
from kvservice_pb2 import *
from kvstore import *

class kv739_server(SocketServer.TCPServer):
  def __init__(self, host):
    SocketServer.TCPServer.__init__(self, host, TcpRequestHandler)

class TcpRequestHandler(SocketServer.BaseRequestHandler):
  
  def __init__(self, request, client_address, server):
    # TODO: kvstore is hardcoded at the moment
    self.m_kvs = KeyValueStore('kvstore.txt')      
    SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)  
  
  def handle(self):
    while True:
      buffer = self.request.recv(struct.calcsize("!I"))
      # TODO: possible to receive random data?
      if (len(buffer) < struct.calcsize("!I")):
        break

      bufferLen = int(struct.unpack("!I", buffer)[0])
      buffer = self.request.recv(bufferLen)
      self.buffer_received(buffer)

  def send_string(self, buffer):
    networkOrderBufferLen = struct.pack("!I", len(buffer))

    buffer = networkOrderBufferLen + buffer
    bytesSent = 0
    while bytesSent < len(buffer):
      sent = self.request.send(buffer[bytesSent:])
      if sent == 0:
        raise RuntimeError("socket connection broken")
      bytesSent += sent

  def buffer_received(self, data):
    request = Request()
    request.ParseFromString(data)
    response = Response()
    response.id = request.id
    
    if request.type == "set":
      result, old_value = self.m_kvs.set(request.key, request.value)
      response.result = result;
      if old_value:
        response.value = old_value
      else:
        response.value = ""
    
    elif request.type == "get":
      value, result = self.m_kvs.get(request.key)
      response.result = result
      if value:
        response.value = value
      else:
        response.value = ""
    
    else:
      response.result = -1
      response.value = ""

    self.send_string(response.SerializeToString())
