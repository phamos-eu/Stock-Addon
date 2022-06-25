import frappe
from frappe.utils import date_diff

def execute(filters=None):
	columns = get_columns()
	data = []
	purchase_date = {}
	delivery_date = {}
	sr_no = frappe.db.sql("""
	select name as sr_no from `tabSerial No`;
	""", as_dict= True)
	for sr in sr_no:
		delivery_date = frappe.db.sql("""
		select posting_date from `tabStock Ledger Entry` where voucher_type = "Delivery Note" and serial_no like "%{}%";
		""".format(sr.sr_no),as_list= True)
		delivery_date = delivery_date[0][0] if len(delivery_date) else frappe.utils.nowdate()

		purchase_date = frappe.db.sql("""
		select posting_date from `tabStock Ledger Entry` where voucher_type = "Purchase Receipt" and serial_no like "%{}%";
		""".format(sr.sr_no),as_list= True)
		purchase_date =  purchase_date[0][0] if len(purchase_date) else frappe.utils.nowdate()
		dis = date_diff(delivery_date,purchase_date)
		data.append({ "sr_no": sr['sr_no'], "purchase_date": purchase_date, "delivery_date": delivery_date , "dis":  abs(dis)} )
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