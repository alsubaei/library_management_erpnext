# Copyright (c) 2023, Faris Ansari and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Car(Document):

	def before_save(self):
		self.validate()

	def validate(self):
		carplate = self.carplate
		if len(carplate) != 8:
			frappe.throw(_('The carplate must be in this fomrat abcd-123'))
		if carplate[4] != '-' or  carplate[:4].isalpha() == False or carplate[5:].isnumeric() == False:
			frappe.throw(_('The carplate must be in this format abcd-123'))
