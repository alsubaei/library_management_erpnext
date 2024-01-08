# Copyright (c) 2024, Faris Ansari and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_to_date,getdate
class BankLoan(Document):

    def before_insert(self):
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

    def before_submit(self):
        self.status ='Unpaid'

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

def check_loans():
    today = getdate()
    loans = frappe.db.get_list('Bank Loan',filters=[['status','in',['Unpaid','Partially paid']]])
    for loan in loans:
        loan = frappe.get_doc('Bank Loan',loan['name'])
        if loan.auto_repayment:
            print(loan)
            for payment in loan.schedule:
                print(loan,'===>',payment)
                if payment.payment_date == today and not payment.journal_entry:              
                    entry=frappe.new_doc("Journal Entry")
                    entry.posting_date=today
                    account=entry.append("accounts",{})
                    account.account = loan.loan_account
                    account.debit= loan.loan_amount
                    account.debit_in_account_currency=loan.loan_amount
                    account=entry.append("accounts",{})
                    account.account=loan.repayment_account
                    account.credit= loan.loan_amount
                    account.credit_in_account_currency=loan.loan_amount	
                    entry.insert()
                    entry.submit()
                    payment.journal_entry= entry.name
                    if payment.name == loan.schedule[-1].name:
                        loan.status='Paid'
                        print(payment,'Paid')
                    else:
                        loan.status='Partially paid'
                        print(payment,'Partially paid')
                    break
            loan.save()