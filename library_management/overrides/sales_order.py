from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
import frappe
from frappe.utils import getdate, date_diff

class CustomSalesOrder(SalesOrder):
	def before_save(self):
		now = getdate()
		diff = date_diff(self.delivery_date, now)
		self.custom_till_delivery_date = diff

def update_days_of_delivery():
	now= getdate()
	orders = frappe.db.get_list('Sales Order', 
					filters=[['status','in',['Draft','To Deliver','To Deliver and Bill']]],
					fields=['name','delivery_date','status','custom_till_delivery_date'])
	for order in orders:
		diff = date_diff(order['delivery_date'],now)
		frappe.db.set_value('Sales Order',order['name'],'custom_till_delivery_date',diff, update_modified=False)
	frappe.db.commit()
