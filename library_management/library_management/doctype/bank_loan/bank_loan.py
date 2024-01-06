# Copyright (c) 2024, Faris Ansari and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_to_date

class BankLoan(Document):
	def on_update(self):
		self.schedule =[]
		date= self.repayment_date
		amount= self.load_amount + self.load_amount * self.interest /100
		for i in range(int(self.repayment_months)):
			repayment = self.append('schedule',{})
			repayment.payment_date = date
			repayment.principal_amount= self.load_amount/self.repayment_months
			repayment.interest_amount= repayment.principal_amount * self.interest/100
			repayment.total_payment= repayment.principal_amount + repayment.interest_amount
			repayment.balance_loan_amount = amount- repayment.total_payment
			amount -= repayment.total_payment
			date = add_to_date(date, months=1)
