from kv739_client import kv739_client
import time

def basic_send_recieve_test(client):
  [ret, old_value] = client.kv739_put("hello", "world")
  print "ret = " + repr(ret) + ", old_value = " + repr(old_value)

  [ret, value] = client.kv739_get("hello")
  print "ret = " + repr(ret) + ", value = " + repr(value)

  time.sleep(1)

  [ret, old_value] = client.kv739_put("hello", "haha")
  print "ret = " + repr(ret) + ", old_value = " + repr(old_value)

# assumes a new kvstore
def set_new_stress_test(client, n, b1, b2):
    fail = False
    start_t = time.time()
    lats = []
    for i in range(0, n):
        start_l = time.time()
        [ret, old_value] = client.kv739_put((str(i)*b1)[0:128], (str(i)*b2)[0:2048])
        lats.append(time.time()-start_l)
        if int(ret) != 1 or old_value != "":
            print old_value
            fail = True
    
    print "set_new_stress_test passed:", not fail
    print "throughput:", (n / (time.time()-start_t)), "sets/sec"
    print "latency:"
    print ("\tmin: %fms, avg: %fms, max: %fms" 
           % (min(lats)*1000, (sum(lats) / float(len(lats)))*1000, max(lats)*1000))

# assumes a warm kvstore
def set_existing_stress_test(client, n, b1, b2):
    fail = False
    start_t = time.time()
    lats = []
    for i in range(0, n):
        start_l = time.time()
        [ret, old_value] = client.kv739_put((str(i)*b1)[0:128], (str(i)*b2)[0:2048])
        lats.append(time.time()-start_l)
        if int(ret) != 0 or old_value != (str(i)*b2)[0:2048]:
            fail = True
    print "set_existing_stress_test passed:", not fail
    print "throughput:", (n / (time.time()-start_t)), "sets/sec"
    print "latency:"
    print ("\tmin: %fms, avg: %fms, max: %fms" 
           % (min(lats)*1000, (sum(lats) / float(len(lats)))*1000, max(lats)*1000))


# assumes keys don't exist
def get_nonexisting_stress_test(client, n, b1, b2):
    fail = False
    start_t = time.time()
    lats = []
    for i in range (0, n):
        start_l = time.time()
        [ret, value] = client.kv739_get((str(i)*b1)[0:128])
        lats.append(time.time()-start_l)
        if int(ret) != 1 or value != "":
            fail = True
    print "get_nonexisting_stress_test passed:", not fail
    print "throughput:", (n / (time.time()-start_t)), "gets/sec"
    print "latency:"
    print ("\tmin: %fms, avg: %fms, max: %fms" 
           % (min(lats)*1000, (sum(lats) / float(len(lats)))*1000, max(lats)*1000))
    

# assumes keys exist
def get_existing_stress_test(client, n, b1, b2):
    fail = False
    start_t = time.time()
    lats = []
    for i in range (0, n):
        start_l = time.time()
        [ret, value] = client.kv739_get((str(i)*b1)[0:128])
        lats.append(time.time()-start_l)
        if int(ret) != 0 or value != (str(i)*b2)[0:2048]:
            fail = True
    print "get_existing_stress_test passed:", not fail
    print "throughput:", (n / (time.time()-start_t)), "gets/sec"
    print "latency:"
    print ("\tmin: %fms, avg: %fms, max: %fms" 
           % (min(lats)*1000, (sum(lats) / float(len(lats)))*1000, max(lats)*1000))


# set then get n times test
def set_getk_stress_test(client, n, k, b1, b2):
    fail = False
    start_t = time.time()
    for i in range(0, n):
        [ret, old_value] = client.kv739_put((str(i)*b1)[0:128], (str(i)*b2)[0:2048])
        if int(ret) != 0 or old_value != (str(i)*b2)[0:2048]:  
            fail = True
        for i in range(0, k):
            [ret, value] = client.kv739_get((str(i)*b1)[0:128])
            if int(ret) != 0 or value != (str(i)*b2)[0:2048]:
                fail = True
    print "set_getk_stress_test passed:", not fail
    print "throughput:", ((n*k) / (time.time()-start_t)), "set-kgets/sec"



if __name__ == "__main__":
  server_addr = "tcp://adelie-03.cs.wisc.edu:8000"
  client = kv739_client()
  if client.kv739_init(server_addr) != 0:
    print "Can't connect to Key-Value store server"
    exit(1)

  n = 10000
  k = 5
  b1 = 127
  b2 = 2000

  print "Testing Configuration:"
  print "\tn:", n
  print "\tk:", k
  print "\tb1:", b1
  print "\tb2:", b2
  
  basic_send_recieve_test(client)
  print "------------------------------------------"
  get_nonexisting_stress_test(client, n, b1, b2)
  print "------------------------------------------"  
  set_new_stress_test(client, n, b1, b2)
  print "------------------------------------------"
  set_existing_stress_test(client, n, b1, b2)
  print "------------------------------------------"
  get_existing_stress_test(client, n, b1, b2)
  print "------------------------------------------"
  set_getk_stress_test(client, n, k, b1, b2)
  print "------------------------------------------"
