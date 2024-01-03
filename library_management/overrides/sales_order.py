from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
import frappe
from frappe.utils import getdate, date_diff

class CustomSalesOrder(SalesOrder):
	def before_save(self):
		now = getdate()
		diff = date_diff(self.delivery_date, now)
		self.custom_till_delivery_date = diff
