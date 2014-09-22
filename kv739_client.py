import sys
sys.path.insert(0, './modules')

import socket
import struct
from kvservice_pb2 import *

class kv739_client:
  def __init__(self):
    self.tcpSocket = None

  def kv739_init(self, server):
    [protocol, address, port] = server.split(':')
    address = address.strip("/")
    port = int(port)

    if protocol != "tcp":
      print "Only support TCP right now!"
      return -1

    ret = 0
    self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      self.tcpSocket.connect((address, port))
    except socket.error:
      ret = -1

    return ret

  def send_buffer(self, buffer):
    networkOrderBufferLen = struct.pack("!I", len(buffer))

    buffer = networkOrderBufferLen + buffer
    bytesSent = 0
    while bytesSent < len(buffer):
      sent = self.tcpSocket.send( buffer[ bytesSent: ] )
      if sent == 0:
        raise RuntimeError( "socket connection broken" )
      bytesSent += sent

  def kv739_get(key):
    ret = 0
    getRequest = GetRequest()
    getRequest.id = "get"
    getRequest.key = key
    send_buffer(getRequest)

    buffer = self.tcpSocket.recv(struct.calcsize("!I"))
    if not buffer:
      ret = -1
    else:
      bufferLen = int(struct.unpack( "!I", buffer )[0])
      buffer = self.tcpSocket.recv(bufferLen)
      if not buffer:
        ret = -1

    if ret != -1:
      response = Response()
      response.ParseFromString(buffer)
      return [response.result, response.value]
    else:
      return [-1, '']

  def kv739_set(key, value):
    ret = 0
    setRequest = SetRequest()
    setRequest.id = "get"
    setRequest.key = key
    setRequest.value = value
    send_buffer(getRequest)

    buffer = self.tcpSocket.recv(struct.calcsize("!I"))
    if not buffer:
      ret = -1
    else:
      bufferLen = int(struct.unpack( "!I", buffer )[0])
      buffer = self.tcpSocket.recv(bufferLen)
      if not buffer:
        ret = -1

    if ret != -1:
      response = Response()
      response.ParseFromString(buffer)
      return [response.result, response.value]
    else:
      return [-1, '']