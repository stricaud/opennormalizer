#!/usr/bin/env python3

## This file is part of OpenNormalizer
## Copyright (C) 2012 Sebastien Tricaud <sebastien@honeynet.org>
## License: DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE v2, December 2004

import xml.etree.ElementTree as etree

class NormalizerHandler_Exception(Exception):
	pass

class NormalizerHandler:
	"""
	Take a normalization xml file and create a python structure we can use.
	"""
	head = {}
	_slicer_id = 0
	slicers = []

	_debug = 0		# Switch to '1' to print extra debug output
	
	def __init__(self, _filename):
		self.filename = _filename
		self._parse(self.filename)

	def _parse(self, filename):
		xmlfile = etree.parse(filename)
		xmlroot = xmlfile.getroot()
		self._check_root_version(xmlroot)

		xmlhead = xmlroot.find("head")
		if xmlhead == None:
			raise NormalizerHandler_Exception("XML file '%s' contains no header" % (filename))
		self._parse_head(xmlhead)

		xmlslice = xmlroot.find("slice")	
		if xmlslice == None:
			raise NormalizerHandler_Exception("XML file '%s' contains no slice" % (filename))
		self._parse_slice(xmlslice)

	def _check_root_version(self, normalizerroot):
		version = normalizerroot.attrib['version']
		if (version != '1.0'):
			raise NormalizerHandler_Exception("Bad Normalizer Version: %s" % (version))

	def _parse_head(self, headroot):
		for el in headroot:
			if el.tag == "tags":
				self.head[el.tag] = el.text.split(',')
			else:
				self.head[el.tag] = el.text
		# print(str(self.head))

	def print_slicer(self, parsed_slicer):
		print("[%d] %s (%s) -> %d cols" % (parsed_slicer['id'], parsed_slicer['type'], parsed_slicer['name'], parsed_slicer['n_columns']))
		print("data:%s" % (parsed_slicer['data']))
		for col in parsed_slicer['columns']:
			print("\t%s" % (col))
		# print("parsed_columns:'%s'" % (str(parsed_slicer['columns'])))

	def _parse_slice(self, slice_root):
		slicer = slice_root.find("slicer")
		if slicer == None:
			raise NormalizerHandler_Exception("The slice comes with no slicer. Nothing to do!")
		parsed_slicer = self._parse_slicer(slicer)
		self.slicers.insert(0, parsed_slicer) # It is added after all the recusive parsing. It is not fair to be at the end ;-)

		if self._debug:
			self.print_slicer(parsed_slicer)

	def _parse_slicer(self, slicer_root):
		slicer = {}
		slicer['id'] = self._slicer_id
		self._slicer_id += 1
		slicer['type'] = slicer_root.attrib['type']
		try:
			slicer['name'] = slicer_root.attrib['name']
		except:
			slicer['name'] = ""
		
		slicer['data'] = slicer_root.find(slicer['type']).text
		if slicer['data'] is not None:
			slicer['data'] = slicer['data'].strip()
		slicer['n_columns'] = self._get_n_columns_for_slicer(slicer_root)

		columns = slicer_root.find("columns")		
		slicer['columns'] = self._parse_columns(columns)

		return slicer

	def _parse_columns(self, columns_root):
		columns = []
		for column in columns_root:
			col = self._parse_column(column)
			if col['slicer'] is not None:
				parsed_slicer = self._parse_slicer(col['slicer'])
				self.slicers.insert(0, parsed_slicer) # We want the slicers to appear in order

				if self._debug:
					self.print_slicer(parsed_slicer)
			columns.append(col)

		return columns

	def _parse_column(self, column_root):
		column = {}
		# Name
		try:
			column['name'] = column_root.attrib['name']
		except:
			column['name'] = ""
		# Type
		try:
			column['type'] = column_root.attrib['type']
		except:
			column['type'] = ""
		# Group
		try:
			column['group'] = column_root.attrib['group']
		except:
			column['group'] = ""
		# Tags
		try:
			column['tags'] = column_root.attrib['tags'].split(',')
		except:
			column['tags'] = []

		column_options = {}
		column_slicer = None
		for option in column_root:
			if option.tag != "slicer": # slicer is not an option
				column_options[option.tag] = option.text
			else:
				column_slicer = option
				column['slicer-id'] = self._slicer_id

		column['option'] = column_options
		column['slicer'] = column_slicer

		return column

	def _get_n_columns_for_slicer(self, slicer_root):
		columns = slicer_root.find("columns")
		if columns == None:
			raise NormalizerHandler_Exception("No columns for the slicer '%s'!" % (slicer_root.tag))
		return len(columns)	

	def get_head(self):
		return self.head

	def get_slicers(self):
		return self.slicers

	def get_col(self, n):
		slicer = self.slicers[0] # FIXME, don't rely on the first slicer!
		return slicer['columns'][n]

if __name__ == "__main__":
	nh = NormalizerHandler("../../normalizers/syslog.normalizer")
	head = nh.get_head()
	# print(str(head))
	slicers = nh.get_slicers()
	for slicer in slicers:
		nh.print_slicer(slicer)
