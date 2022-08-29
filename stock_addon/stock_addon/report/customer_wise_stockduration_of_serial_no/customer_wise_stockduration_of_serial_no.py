#Built by Devarsh Bhatt at Genirex
#Contact devarsh@genirex.com

import frappe
from frappe.utils import date_diff

def execute(filters=None):
	columns = get_columns()
	_filters = ""
	# if filters:
	# 	_filters = "where "
	# 	_filters = _filters + "purchase_date between '" + filters.get("from_date") + "' and '" + filters.get("to_date") +"' AND delivery_date between '"+filters.get("from_date") + "' and '" + filters.get("to_date") +"'" if filters.get("from_date") and filters.get("to_date")  else ""
	if filters.get("customer"):
		columns.append({
			"fieldname":"customer",
			"label": frappe._("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		})
		if "where" in _filters:
			_filters = _filters + " and "
		else:
			_filters = _filters + "where "
		_filters = _filters + "customer = '" + filters.get("customer") + "'"
	# else:
	# 	columns.append({
	# 		"fieldname":"customer",
	# 		"label": frappe._("Customer"),
	# 		"fieldtype": "Link",
	# 		"options": "Customer"
	# 	})
	if filters.get("commission_by"):
		if filters.get("commission_by") == frappe._("Item Wise"):
			columns.append({
				"fieldname":"commission_i",
				"label": frappe._("Kommission (I)"),
				"fieldtype": "Data"
			})
			columns.append({
				"fieldname":"project_i",
				"label": frappe._("Project (I)"),
				"fieldtype": "Link",
				"options": "Project"
			})
		# 	pass
		if filters.get("commission_by") == frappe._("Transaction Wise"):
			columns.append({
				"fieldname":"commission_t",
				"label": frappe._("Kommission (T)"),
				"fieldtype": "Data",
			})
			columns.append({
				"fieldname":"project_t",
				"label": frappe._("Project (T)"),
				"fieldtype": "Link",
				"options": "Project"
			})
			# if "where" in _filters:
			# 	_filters = _filters + " and "
			# else:
			# 	_filters = _filters + "where "
			# _filters = _filters + "project = '"+

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
		item_wise_i = None
		item_wise_t = None
		delivery_date = frappe.utils.getdate(sr.delivery_date if sr.delivery_date else frappe.utils.nowdate())
		if filters.get("commission_by") == frappe._("Item Wise"):
			if sr.purchase_document_type == "Purchase Receipt":
				item_wise_i = frappe.db.get_value("Purchase Receipt",  sr.purchase_document_no, ["project", "kommission"],as_dict=1)
			if sr.purchase_document_type == "Stock Entry":
				item_wise_i = frappe.db.get_value("Stock Entry Detail", sr.purchase_document_no, ["project", "kommission"],as_dict=1)
		if filters.get("commission_by") == frappe._("Transaction Wise"):
			if sr.purchase_document_type == "Purchase Receipt":
				item_wise_t = frappe.db.get_value("Purchase Receipt Item", {"parent": sr.purchase_document_no}, ["project", "kommission"],as_dict=1)
			if sr.purchase_document_type == "Stock Entry":
				item_wise_t = frappe.db.get_value("Stock Entry Detail", {"parent":sr.purchase_document_no}, ["project", "kommission"],as_dict=1)

		start = sr.delivery_date
		end = sr.creation_date
		if filters.get("to_date") and filters.get("from_date"):
			if sr.creation_date < frappe.utils.getdate(filters.get("from_date")):
				end = frappe.utils.getdate(filters.get("from_date"))
			elif sr.creation_date > frappe.utils.getdate(filters.get("from_date")):
				end = sr.creation_date
			else:
				end = frappe.utils.getdate(filters.get("from_date"))
			if sr.delivery_date and sr.delivery_date < frappe.utils.getdate(filters.get("to_date")):
				start = sr.delivery_date
			elif sr.delivery_date and sr.delivery_date > frappe.utils.getdate(filters.get("to_date")):
				start = frappe.utils.getdate(filters.get("to_date"))
			else:
				start = frappe.utils.getdate(filters.get("to_date"))
		diff = date_diff(start,end)+1
		if diff >= 0:
			data.append(
				{
					"sr_id":sr.sr_id,
					"creation_date": sr.creation_date,
					"delivery_date": delivery_date,
					"dis": diff,
					"creation_doctype": sr.purchase_document_type,
					"delivery_doctype": sr.delivery_document_type,
					"creation_docname": sr.purchase_document_no,
					"delivery_docname": sr.delivery_document_no,
					"item_code": sr.item_code,
					"customer": sr.customer,
					"project_i": item_wise_i.project if item_wise_i else "-",
					"commission_i": item_wise_i.kommission if item_wise_i else "-",
					"project_t":  item_wise_t.project if item_wise_t else "-",
					"commission_t": item_wise_t.kommission if item_wise_t else "-"
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
			"label": frappe._("Total No of Days in Stock"),
			"fieldname": "dis",
			"fieldtype": "Int",
		}
	]
	return columns