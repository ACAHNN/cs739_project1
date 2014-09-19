#!/usr/bin/python

class KeyValueStore:
	m_keyValues = {}
	m_backingStore = 0
	def __init__(self, fileName):
		m_backingStore = open(fileName, "w+")		


x = KeyValueStore("test")
