# Copyright (c) 2024, Faris Ansari and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_to_date,getdate,flt

class BankLoan(Document):

	def on_submit(self):
		entry=frappe.new_doc("Journal Entry")
		entry.posting_date=getdate()
		#حساب الذي أودع فيه القروض
		account=entry.append("accounts",{})
		account.account = self.disbursement_account
		account.debit= self.loan_amount
		account.debit_in_account_currency=self.loan_amount
		# حساب الذي أعطى الشركة القرض
		account=entry.append("accounts",{})
		account.account=self.loan_account
		account.credit= self.loan_amount
		account.credit_in_account_currency=self.loan_amount	
		entry.insert()
		entry.submit()


	def on_update(self):
		self.schedule=[]
		d=self.repayment_date
		amount=self.loan_amount+self.loan_amount*self.interest/100
		for i in range(int(self.repayment_months)):
			repayment=self.append("schedule",{})
			repayment.payment_date=d
			repayment.principal_amount=self.loan_amount/self.repayment_months
			repayment.interest_amount=repayment.principal_amount*self.interest/100
			repayment.total_payment=repayment.principal_amount+repayment.interest_amount
			repayment.balance_loan_amount=amount-repayment.total_payment
			amount=amount-repayment.total_payment
			d=add_to_date(d,months=1)
