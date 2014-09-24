#import sys
#sys.path.insert(0, './modules')

from kv739_client import kv739_client
import time

if __name__ == "__main__":
  server_addr = "tcp://adelie-02.cs.wisc.edu:8000"
  client = kv739_client()
  if client.kv739_init(server_addr) != 0:
    print "Can't connect to Key-Value store server"
    exit(1)

  [ret, old_value] = client.kv739_set("hello", "world")
  print "ret = " + repr(ret) + ", old_value = " + repr(old_value)

  [ret, value] = client.kv739_get("hello")
  print "ret = " + repr(ret) + ", value = " + repr(value)

  time.sleep(5)

  [ret, old_value] = client.kv739_set("hello", "haha")
  print "ret = " + repr(ret) + ", old_value = " + repr(old_value)
