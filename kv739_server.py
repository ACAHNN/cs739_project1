import sys
sys.path.insert(0, './modules')

import socket
import struct
import SocketServer
from kvservice_pb2 import *

class kv739_server(SocketServer.TCPServer):
  def __init__(self, host):
    SocketServer.TCPServer.__init__(self, host, TcpRequestHandler)

class TcpRequestHandler(SocketServer.BaseRequestHandler):
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

    if request.id == "set":
      response.result = 0;
      response.value = ""
    elif request.id == "get":
      response.result = 0
      response.value = "World"
    else:
      response.result = -1
      response.value = ""

    self.send_string(response.SerializeToString())