#!/usr/bin/python

class KeyValueStore:
	m_keyValues = {}
	m_backingStore = 0
	def __init__(self, fileName):
		self.m_backingStore = open(fileName, "ab")		
		#do pickle stuff
		
	def put(self, key, value):
		#what is the failure case for this?
		oldValue,success = self.get(key)
		self.m_keyValues[key] = value

	#	m_backingStore.write(str(m_keyValues)) pickle stuff

		return oldValue, success			
	def get(self,key):
		#what is a failure case for this?? spec says to return -1 on failure
		if self.m_keyValues.has_key(key):
			value = self.m_keyValues[key]
			return value, 0
		else:
			return None, 1 
