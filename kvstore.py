import sys

class KeyValueStore:
    def __init__(self, filename):
        self.m_keyvalues = {}
        self.kvstore = filename
        self._read_kvstore()

    
    def _read_kvstore(self):
        with open(self.kvstore, 'rb') as kvstore:
            for kvpair in kvstore:
                key, value = kvpair.strip().split('||')
                self.m_keyvalues[key] = value

    
    def _write_kvstore(self, key, value):
        with open(self.kvstore, 'ab') as kvstore:
            kvstore.write('%s||%s\n' % (key,value))

    def set(self, key, value):
        old_value, result = self.get(key)
        self.m_keyvalues[key] = value
        
        try:
            self._write_kvstore(key, value)
        except Exception:
            result = -1
        
        return result, old_value

    def get(self, key):
        try:
            if self.m_keyvalues.has_key(key):
                return self.m_keyvalues[key], 0
            else:
                return None, 1
        except Exception:
            return None, -1
