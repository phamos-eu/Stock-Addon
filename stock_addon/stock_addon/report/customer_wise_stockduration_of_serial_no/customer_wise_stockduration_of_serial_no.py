#Built by Devarsh Bhatt at Genirex
#Contact devarsh@genirex.com

import frappe
from frappe.utils import date_diff

def execute(filters=None):
	columns = get_columns()
	_filters = ""
	if filters:
		_filters = "where "
		_filters = _filters + "purchase_date between '" + filters.get("from_date") + "' and '" + filters.get("to_date") +"' AND delivery_date between '"+filters.get("from_date") + "' and '" + filters.get("to_date") +"'" if filters.get("from_date") and filters.get("to_date")  else ""
	if filters.get("customer"):
		if "where" in _filters:
			_filters = _filters + " and "
		else:
			_filters = _filters + "where "
		_filters = _filters + "customer = '" + filters.get("customer") + "'"
	else:
		columns.pop()
	data = []
	_query = """
	select name as sr_id, 
	item_code,
	customer, 
	purchase_date as creation_date, 
	delivery_date, 
	purchase_document_type, 
	delivery_document_type, 
	purchase_document_no, 
	delivery_document_no 
	from `tabSerial No` {};
	""".format(_filters) 
	serial_items = frappe.db.sql(_query, as_dict= True)
	for sr in serial_items:
		delivery_date = sr.delivery_date if sr.delivery_date else frappe.utils.nowdate()	
		data.append(
			{
				"sr_id":sr.sr_id,
				"creation_date": sr.creation_date,
				"delivery_date": delivery_date,
				"dis": date_diff(delivery_date,sr.creation_date),
				"creation_doctype": sr.purchase_document_type,
				"delivery_doctype": sr.delivery_document_type,
				"creation_docname": sr.purchase_document_no,
				"delivery_docname": sr.delivery_document_no,
				"item_code": sr.item_code,
				"customer": sr.customer,
			}
		)

	return columns, data

def get_columns():
	columns = [
		{
			"label": frappe._("ID"),
			"fieldname": "sr_id",
			"fieldtype": "Data",
		},
		{
			"label": frappe._("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Data",
		},
		{
			"label": frappe._("Creation Doctype"),
			"fieldname": "creation_doctype",
			"fieldtype": "Data",
		},
		{
			"label": frappe._("Creation Docname"),
			"fieldname": "creation_docname",
			"fieldtype": "Data",
		},
		{
			"label": frappe._("Creation Date"),
			"fieldname": "creation_date",
			"fieldtype": "Data",
		},
		{
			"label": frappe._("Delivery Doctype"),
			"fieldname": "delivery_doctype",
			"fieldtype": "Data",
		},
		{
			"label": frappe._("Delivery Docname"),
			"fieldname": "delivery_docname",
			"fieldtype": "Data",
		},
		{
			"label": frappe._("Delivery Date"),
			"fieldname": "delivery_date",
			"fieldtype": "date",
		},
		{
			"label": frappe._("No of Days in Stock"),
			"fieldname": "dis",
			"fieldtype": "Int",
		},
		{
			"fieldname":"customer",
			"label": frappe._("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		}
		]
	return columns