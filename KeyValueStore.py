#!/usr/bin/python

class KeyValueStore:
	m_keyValues = {}
	m_backingStore = 0
	def __init__(self, fileName):
		m_backingStore = open(fileName, "w+")		
		#read from backing store and place into dictionary

	def put(key, value, oldValue):
		success = get(key, tmpOldValue)
		m_keyValues[key] = value


		#write/update to backing store
		return success			
	def get(key, value):
		#what is a failure case for this?? spec says to return -1 on failure
		if m_keyValues.has_key(key):
			value = m_keyValues[key]
			return 0
		else:
			return 1 
x = KeyValueStore("test")
print "hello world"
