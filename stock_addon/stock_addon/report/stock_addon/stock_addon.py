import frappe
from frappe.utils import date_diff

def execute(filters=None):
	columns = get_columns()
	data = []
	serial_items = frappe.db.sql("""
	select name as sr_no, purchase_date, delivery_date from `tabSerial No`;
	""", as_dict= True)
	for sr in serial_items:
		delivery_date = sr.delivery_date if sr.delivery_date else frappe.utils.nowdate()
		data.append({"sr_no":sr.sr_no, "purchase_date": sr.purchase_date, "delivery_date": delivery_date, "dis": date_diff(delivery_date,sr.purchase_date) })
	return columns, data

def get_columns():
	columns = [
		{
			"label": "Serial No",
			"fieldname": "sr_no",
			"fieldtype": "Data",
		},
		{
			"label": "Purchase Date",
			"fieldname": "purchase_date",
			"fieldtype": "date",
		},
		{
			"label": "Delivery Date",
			"fieldname": "delivery_date",
			"fieldtype": "date",
		},
		{
			"label": "Days in Stock",
			"fieldname": "dis",
			"fieldtype": "Int",
		},
		]
	return columns