# encoding: utf-8
"""
resource.py

Created by Thomas Mangin on 2015-05-15.
Copyright (c) 2015-2015 Exa Networks. All rights reserved.
"""

from exabgp.util import string_is_hex


class Resource (long):
	NAME = ''
	codes = {}
	names = {}

	cache = {}

	def __new__ (cls, *args):
		key = '//'.join((str(_) for _ in args))
		if key in Resource.cache.setdefault(cls,{}):
			return Resource.cache[cls][key]
		instance = long.__new__(cls,*args)
		Resource.cache[cls][key] = instance
		return instance

	def __str__ (self):
		return self.names.get(self,'unknown %s type %ld' % (self.NAME,long(self)))

	@classmethod
	def _value (cls,string):
		name = string.lower().replace('_','-')
		if name in cls.codes:
			return cls.codes[name]
		if string.isdigit():
			value = int(string)
			if value in cls.names:
				return value
		if string_is_hex(string):
			value = int(string[2:],16)
			if value in cls.names:
				return value
		raise ValueError('unknown %s %s' % (cls.NAME,name))

	@classmethod
	def named (cls,string):
		value = 0
		for name in string.split('+'):
			value += cls._value(name)
		return cls(value)
