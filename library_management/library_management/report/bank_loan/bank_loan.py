# Copyright (c) 2024, Faris Ansari and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters=filters)
    data = get_data(filters=filters)
    chart = get_chart(data)
    cards = get_card(chart)
    return columns, data, None, chart, cards

def get_columns(filters=None):
    columns = [
        {
            "fieldname": "bank",
            "label": _("Bank Name"),
            "fieldtype": "Link",
            "options": "Bank Loan",
        },
        {
            "fieldname": "total_loans",
            "label": _("Total Loans"),
            "fieldtype": "Currency",
        },
        {
            "fieldname": "total_interest",
            "label": _("Total Interest"),
            "fieldtype": "Currency",
        },
        {
            "fieldname": "total_repayments",
            "label": _("Total Repayments"),
            "fieldtype": "Currency",
        },
        {
            "fieldname": "outstanding_amounts",
            "label": _("Outstanding Amounts"),
            "fieldtype": "Currency",
        },
    ]
    return columns

def get_data(filters=None):
    data = []
    loan_amount = 0
    interest = 0
    repayments = 0
    banks = frappe.db.get_list("Bank Person")
    for bank in banks:
        list = {"bank": bank["name"]}
        loans = frappe.db.get_list("Bank Loan", filters={"bank_name": bank["name"]})
        for loan in loans:
            loan = frappe.get_doc("Bank Loan", loan["name"])
            loan_amount += loan.loan_amount
            interest += loan.loan_amount * loan.interest / 100
            for repayment in loan.schedule:
                if repayment.journal_entry:
                    repayments += repayment.total_payment
        list["total_loans"] = loan_amount
        list["total_interest"] = interest
        list["total_repayments"] = repayments
        list["outstanding_amounts"] = loan_amount + interest - repayments
        data.append(list)
    return data

def get_chart(data):
    banks_list = [item["bank"] for item in data]
    loan_amounts_list = [item["total_loans"] for item in data]
    total_interest_list = [item["total_interest"] for item in data]
    outstanding_amounts_list = [item["outstanding_amounts"] for item in data]
    chart = {
        "data": {
            "labels": banks_list,
            "datasets": [
                {"name": "Total Loans", "values": loan_amounts_list},
                {"name": "Total Interest", "values": total_interest_list},
                {"name": "Outstanding Amounts", "values": outstanding_amounts_list},
            ],
        },
        "type": "bar",
    }

    return chart

def get_card(chart):
    loan_amounts = chart["data"]["datasets"][0]["values"]
    interest_amounts = chart["data"]["datasets"][1]["values"]
    outstanding_amounts = chart["data"]["datasets"][2]["values"]
    loan_amounts_sum = sum(loan_amounts)
    interest_amounts_sum = sum(interest_amounts)
    outstanding_amounts_sum = sum(outstanding_amounts)
    card = [
        {
            "label": "Total Loans",
            "datatype": "Currency",
            "value": loan_amounts_sum,
          #  "value": "{:,.2f}".format(loan_amounts_sum),
            "indicator": "red",
        },
        {
            "label": "Total Interest",
            "datatype": "Currency",
            "value": interest_amounts_sum,
            "indicator": "blue",
        },
        {
            "label": "Total Outstanding Amounts",
            "datatype": "Currency",
            "value": outstanding_amounts_sum,
            "indicator": "green",
        },
    ]
    return card
