#Built by Devarsh Bhatt at Genirex
#Contact devarsh@genirex.com

import frappe
from frappe.utils import date_diff

def execute(filters=None):
	columns = get_columns()
	if filters.get("customer"):
		columns.append({
			"label": frappe._("Lagerkosten"),
			"fieldname": "storage_cost",
			"fieldtype": "Currency"
  		})
		columns.append({
			"fieldname":"customer",
			"label": frappe._("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		})
		columns.append({
			"fieldname":"commission",
			"label": frappe._("Kommission"),
			"fieldtype": "Data",
		})
		columns.append({
			"fieldname":"project",
			"label": frappe._("Project"),
			"fieldtype": "Link",
			"options": "Project"
		})
  
	data = []
	_query = """
	select name as sr_id, 
	item_code,
	purchase_date as creation_date, 
	delivery_date, 
	purchase_document_type, 
	delivery_document_type, 
	purchase_document_no, 
	delivery_document_no 
	from `tabSerial No`;
	"""
	serial_items = frappe.db.sql(_query, as_dict= True)
	for sr in serial_items:
		transaction_wise_data = None
		delivery_date = frappe.utils.getdate(sr.delivery_date if sr.delivery_date else frappe.utils.nowdate())
		if sr.purchase_document_type == "Purchase Receipt":
			transaction_wise_data = frappe.db.get_value("Purchase Receipt", sr.purchase_document_no, ["project", "kommission", "customer"],as_dict=1)
			sr.update({"customer":transaction_wise_data.customer })
		if sr.purchase_document_type == "Stock Entry":
			transaction_wise_data = frappe.db.get_value("Stock Entry", sr.purchase_document_no, ["project", "kommission", "customer"],as_dict=1)
			sr.update({"customer":transaction_wise_data.customer })

		start = sr.creation_date
		end = sr.delivery_date

		if filters.get("to_date") and filters.get("from_date"):
			if sr.creation_date < frappe.utils.getdate(filters.get("from_date")):
				start = frappe.utils.getdate(filters.get("from_date"))
				end = sr.delivery_date

			if sr.creation_date > frappe.utils.getdate(filters.get("from_date")):
				start = sr.creation_date
				end = frappe.utils.getdate(filters.get("to_date"))

			if sr.creation_date > frappe.utils.getdate(filters.get("from_date")) and delivery_date < frappe.utils.getdate(filters.get("to_date")):
				start = sr.creation_date
				end = sr.delivery_date

			if sr.creation_date <= frappe.utils.getdate(filters.get("from_date")):
				start = frappe.utils.getdate(filters.get("from_date"))
				end = frappe.utils.getdate(filters.get("to_date"))
				if delivery_date < frappe.utils.getdate(filters.get("to_date")):
					end = delivery_date
		diff = date_diff(end, start)

		if diff >= 0:
			diff = diff+1
			storage_factor = frappe.db.get_value("Item", sr.item_code, 'lagerplatzfaktor') or None
			cost_per_customer = frappe.db.get_value("Customer", sr.customer, 'lagerplatzkosten') or None
			if storage_factor == None or cost_per_customer == None:
				storage_cost = 0
			else:
				storage_cost = diff/storage_factor*cost_per_customer

		if diff < 0:
			continue
		if filters.get("customer") and transaction_wise_data and transaction_wise_data.customer != filters.get("customer"):
			continue
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
				"customer": transaction_wise_data.customer if transaction_wise_data else "",
				"project":  transaction_wise_data.project if transaction_wise_data else "",
				"commission": transaction_wise_data.kommission if transaction_wise_data else "",
				"storage_cost":storage_cost #Lagerkosten [€] (Automatische Berechnung = Lagerdauer / Lagerplatzfaktor * Lagerplatzkosten 
			}
		)
		
	return columns, data

def get_columns():
	columns = [
		{
			"label": frappe._("ID"),
			"fieldname": "sr_id",
			"fieldtype": "Link",
			"options": "Serial No"
		},
		{
			"label": frappe._("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"label": frappe._("Creation Doctype"),
			"fieldname": "creation_doctype",
			"fieldtype": "Select",
			"options": "Purchase Receipt\nStock Entry"
		},
		{
			"label": frappe._("Creation Docname"),
			"fieldname": "creation_docname",
			"fieldtype": "Dynamic Link",
			"options": "creation_doctype"
		},
		{
			"label": frappe._("Creation Date"),
			"fieldname": "creation_date",
			"fieldtype": "Data",
		},
		{
			"label": frappe._("Delivery Doctype"),
			"fieldname": "delivery_doctype",
			"fieldtype": "Select",
			"options": "Delivery Note\nStock Entry"
		},
		{
			"label": frappe._("Delivery Docname"),
			"fieldname": "delivery_docname",
			"fieldtype": "Dynamic Link",
			"options": "delivery_doctype"
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