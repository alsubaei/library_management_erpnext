# Copyright (c) 2024, Faris Ansari and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns= get_columns(filters=filters)
	data= get_data(filters= filters)
	return columns, data

def get_columns(filters= None):
	columns = [
		{
            'fieldname': 'bank',
            'label': _('Bank Name'),
            'fieldtype': 'Link',
            'options': 'Bank Loan'
		},{
            'fieldname': 'total_loans',
            'label': _('Total Loans'),
            'fieldtype': 'Currency',
		},{
            'fieldname': 'total_interests',
            'label': _('Total Interests'),
            'fieldtype': 'Currency',
		},{
            'fieldname': 'total_repayments',
            'label': _('Total Repayments'),
            'fieldtype': 'Currency',
		},{
            'fieldname': 'outstanding_amounts',
            'label': _('Outstanding Amounts'),
            'fieldtype': 'Currency'
		}
	]
	return columns

def get_data(filters=None):
	data=[]
	loan_amount= 0
	interests= 0
	repayments= 0
	banks = frappe.db.get_list('Bank Person')
	for bank in banks:
		list={'bank':bank["name"]}
		loans= frappe.db.get_list('Bank Loan',filters={'bank_name':bank["name"]})
		for loan in loans:
			loan= frappe.get_doc('Bank Loan',loan['name'])
			loan_amount +=loan.loan_amount
			interests +=  loan.loan_amount*loan.interest/100
			for repayment in loan.schedule:
				if repayment.journal_entry:
					repayments+= repayment.total_payment
		list['total_loans']=loan_amount
		list['total_interests']=interests
		list['total_repayments']=repayments
		list['outstanding_amounts']=loan_amount+interests-repayments
		data.append(list)
	print(data)
	return data