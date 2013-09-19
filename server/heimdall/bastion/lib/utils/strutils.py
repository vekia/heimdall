#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

This file is part of Heimdall.

Heimdall is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Heimdall is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Heimdall.  If not, see <http://www.gnu.org/licenses/>. 

Authors: 
- Vandecappelle Steeve<svandecappelle@vekia.fr>
- Sobczak Arnaud<asobczack@vekia.fr>

# Name:         strutils.py
# Author:       Vandecappelle Steeve & Sobczak Arnaud
# Copyright:    (C) 2013-2014 Vandecappelle Steeve & Sobczak Arnaud
# Licence:      GNU General Public Licence version 3
# Website:      http://vekia.github.io/heimdall/
# Email:        svandecappelle at vekia.fr
"""

def file_len(fname):
	"""
	Return the file line number
	"""
	with open(fname) as f:
		for i, l in enumerate(f, 1):
			pass
		return i


def convert_list_to_str(val_list):
	"""
	Return a String value of a parameter tuple. pattern (val1,val2, etc...)
	"""
	i = 0
	valueStr = ""
	if len(val_list) > 0: 
		for value in val_list:
			if i > 0:
				valueStr = valueStr + "," + str(value)
			else:
				valueStr = valueStr + str(value)
			i = i + 1
	return valueStr

def convert_list_to_str_insert(val_list):
	"""
	Return a String value of a parameter tuple. pattern (val1,val2, etc...)
	"""
	i = 0
	valueStr = ""
	if len(val_list) > 0: 
		for value in val_list:
			if i > 0:
				valueStr = valueStr + "," + str(value)
			else:
				valueStr = valueStr + str(value)
			i = i + 1
	return valueStr