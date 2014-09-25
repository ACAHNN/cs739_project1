from kv739_client import kv739_client

# Assume key-value store is empty when we try to run the cases
if __name__ == "__main__":
  fake_server_addr = "tcp://xxx.edu:8000"
  #server_addr = "tcp://optimus.cs.wisc.edu:8000"

  if not server_addr:
    print "specify the server address"
    exit(1)

  client = kv739_client()

  # Verify kv739_init return -1 in case of error
  if client.kv739_init(fake_server_addr) != -1:
    print "Failed! kv_739_init() should return -1 in case of fail"
  else:
    print "Passed"

  # Verify kv739_init can connect to server and return 0
  if client.kv739_init(server_addr) != 0:
    print "Can't connect to Key-Value store server"
    print "Failed! kv739_init() should be able to connect to test server"
    exit(1)
  else:
    print "Passed"

  # Verify the behavior of kv739_put() and kv739_get()
  [ret, old_value] = client.kv739_put("hello", "world")
  if ret != 1 or old_value != "":
    print "Failed! return value should be 1 because hello/world doesn't exist in store"
  else:
    print "Passed"


  [ret, old_value] = client.kv739_put("hello", "madison")
  if ret != 0 or old_value != "world":
    print "Failed! return value should be 0, old_value should be 'world'"
  else:
    print "Passed"

  [ret, old_value] = client.kv739_put("hello[", "madison")
  if ret != -1 or old_value != "":
    print "Failed! kv739_put() should reject invalid key/value"
  else:
    print "Passed"

  [ret, old_value] = client.kv739_put("hello[", "madison]")
  if ret != -1 or old_value != "":
    print "Failed! kv739_put() should reject invalid key/value"
  else:
    print "Passed"

  [ret, old_value] = client.kv739_get("hello")
  if ret != 0 or old_value != "madison":
    print "Failed! kv739_get() should be able to get the value for key"
  else:
    print "Passed"

  [ret, old_value] = client.kv739_get("hello1")
  if ret != 1 or old_value != "":
    print "Failed! kv739_get() should return 1 if the key doesn't exist in store"
  else:
    print "Passed"

  [ret, old_value] = client.kv739_get("hello[")
  if ret != -1 or old_value != "":
    print "Failed! kv739_get() should return -1 if the key is not valid"
  else:
    print "Passed"

  [ret, old_value] = client.kv739_get("hello]")
  if ret != -1 or old_value != "":
    print "Failed! kv739_get() should return -1 if the key is not valid"
  else:
    print "Passed"

  # Verify the kv739_put() and kv739_get() can handle parameter with maximum length
  [ret, old_value] = client.kv739_put('h'*128, 'w'*2048)
  if ret != 1 or old_value != "":
    print "Failed! return value should be 1"
  else:
    print "Passed"

  [ret, old_value] = client.kv739_get('h'*128)
  if ret != 0 or old_value != 'w'*2048:
    print "Failed! return value should be 0"
  else:
    print "Passed"
