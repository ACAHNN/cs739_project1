#!/usr/bin/python

#TODO: Decide the failure models for KeyValueStore and handle them accordingly

#TODO: Add some form of check pointing (where we rewrite the permanent backstore to remove old key value pairs

class KeyValueStore:	
	def __init__(self, fileName):
		# in memory key value store
		self.m_keyValues = {}		

		# reference to backing file name so we can
		# open and close the file as needed
		self.backingStore = fileName
		
		# populate the in memory key value store
		self._read_backstore()

		
	def _read_backstore(self):
		# open the persistent key value store
		with open(self.backingStore, "rb") as ifile:
			for line in ifile:
				key, value = line.strip().split("||")
				
				self.m_keyValues[key] = value
		for k,v in self.m_keyValues.items():
			print k, v
	
	def _write_backstore(self, key, value):
		
		# write a key value pair to the backstore
		with open(self.backingStore, "ab") as ifile:
			ifile.write("%s||%s\n" % (key, value))
	
	def put(self, key, value):
		
		#what is the failure case for this?
		oldValue, success = self.get(key)
		
		self.m_keyValues[key] = value

		# make the key value update persistent
		self._write_backstore(key, value)

		return success, oldValue

	def get(self, key):
		
		#what is a failure case for this?? spec says to return -1 on failure
		if self.m_keyValues.has_key(key):
			value = self.m_keyValues[key]
			return value, 0
		else:
			return None, 1 
