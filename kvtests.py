from kv739_client import kv739_client
import time

def basic_send_recieve_test(client):
  [ret, old_value] = client.kv739_set("hello", "world")
  print "ret = " + repr(ret) + ", old_value = " + repr(old_value)

  [ret, value] = client.kv739_get("hello")
  print "ret = " + repr(ret) + ", value = " + repr(value)

  time.sleep(5)

  [ret, old_value] = client.kv739_set("hello", "haha")
  print "ret = " + repr(ret) + ", old_value = " + repr(old_value)


# assumes a new kvstore
def set_new_stress_test(client, n, b):
    fail = False
    start_t = time.time()
    for i in range(0, n):
        [ret, old_value] = client.kv739_set(str(i), (str(i)*b)[0:128])
        if int(ret) != 1 or old_value != "":
            fail = True
    print "set_new_stress_test passed:", not fail
    print "throughput:", (n / (time.time()-start_t)), "sets/sec"

# assumes a warm kvstore
def set_existing_stress_test(client, n, b):
    fail = False
    start_t = time.time()
    for i in range(0, n):
        [ret, old_value] = client.kv739_set(str(i), (str(i)*b)[0:128])
        if int(ret) != 0 or old_value != (str(i)*b)[0:128]:
            fail = True
    print "set_existing_stress_test passed:", not fail
    print "throughput:", (n / (time.time()-start_t)), "sets/sec"


# assumes keys don't exist
def get_nonexisting_stress_test(client, n, b):
    fail = False
    start_t = time.time()
    for i in range (0, n):
        [ret, value] = client.kv739_get(str(i))
        if int(ret) != 1 or value != "":
            fail = True
    print "get_nonexisting_stress_test passed:", not fail
    print "throughput:", (n / (time.time()-start_t)), "gets/sec"


# assumes keys exist
def get_existing_stress_test(client, n, b):
    fail = False
    start_t = time.time()
    for i in range (0, n):
        [ret, value] = client.kv739_get(str(i))
        if int(ret) != 0 or value != (str(i)*b)[0:128]:
            fail = True
    print "get_existing_stress_test passed:", not fail
    print "throughput:", (n / (time.time()-start_t)), "gets/sec"


# set then get n times test
def set_getk_stress_test(client, n, k, b):
    fail = False
    start_t = time.time()
    for i in range(0, n):
        [ret, old_value] = client.kv739_set(str(i), (str(i)*b)[0:128])
        if int(ret) != 0 or old_value != (str(i)*b)[0:128]:  
            fail = True
        for i in range(0, k):
            [ret, value] = client.kv739_get(str(i))
            if int(ret) != 0 or value != (str(i)*b)[0:128]:
                fail = True
    print "set_getk_stress_test passed:", not fail
    print "throughput:", ((n*k) / (time.time()-start_t)), "set-kgets/sec"



if __name__ == "__main__":
  server_addr = "tcp://optimus.cs.wisc.edu:8000"
  client = kv739_client()
  if client.kv739_init(server_addr) != 0:
    print "Can't connect to Key-Value store server"
    exit(1)

  n = 1000
  k = 5
  b = 1
  
  print "Testing Configuration:"
  print "\tn:", n
  print "\tk:", k
  print "\tb:", b
  
  get_nonexisting_stress_test(client, n, b)
  set_new_stress_test(client, n, b)
  set_existing_stress_test(client, n, b)
  get_existing_stress_test(client, n, b)
  set_getk_stress_test(client, n, k, b)
