#!/usr/bin/python

#TODO: Decide the failure models for KeyValueStore and handle them accordingly

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
		"""
		Whenever a Server instance comes on line it will
		initialize an instance of KeyValueStore which will
		then read in the key value pairs from the persistent
		store (a file in this case). The file is read from 
		start to finish which allows it replay key value 
		updates as a log. An new key value pair will always be
		read last and therefore overwrite a stale version.
		"""
		
		# open the persistent key value store
		with open(self.backingStore, "rb") as ifile:
			for line in ifile:
				key, value = line.split("||")
				
				self.m_keyValues[key] = value
		
	
	def _write_backstore(self, key, value):
		
		# write a key value pair to the backstore
		with open(self.backingStore, "ab") as ifile:
			ifile.write("%s || %s\n" % (key, value))
	
	def put(self, key, value):
		
		#what is the failure case for this?
		oldValue,success = self.get(key)
		self.m_keyValues[key] = value

		# make the key value update persistent
		self._write_backstore(key, value)

		return oldValue, success			
	
	def get(self,key):
		
		#what is a failure case for this?? spec says to return -1 on failure
		if self.m_keyValues.has_key(key):
			value = self.m_keyValues[key]
			return value, 0
		else:
			return None, 1 
