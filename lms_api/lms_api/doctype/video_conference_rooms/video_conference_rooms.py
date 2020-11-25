# -*- coding: utf-8 -*-
# Copyright (c) 2020, Wela School System and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class VideoConferenceRooms(Document):
	def validate(self):
		self.autorename()
	
	def autorename(self):
		new_name = ""
		for e in self.room_name:
			if e == " ":
				new_name += "-"
			elif e == "-":
				new_name += "-"
			else:
				if e.isalnum():
					new_name +=e
		# new_name = ''.join(e for e in self.room_name if " " else e.isalnum())
		self.room_name = new_name
