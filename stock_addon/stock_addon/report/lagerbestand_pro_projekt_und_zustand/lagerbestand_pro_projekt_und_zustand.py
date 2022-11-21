#Built by Devarsh Bhatt at Genirex
#Contact devarsh@genirex.com

import frappe

def execute(filters=None):
	columns = get_columns()
	data = []
	date_filter = ""
	if filters.get("filter_date"):
		date_filter = " and posting_date = '{}'".format(filters.get("filter_date"))
	bin_item_qty = frappe.db.sql("select sum(actual_qty) as actual_qty, item_code from `tabBin` group by item_code",as_dict=1)
	for biq in bin_item_qty:
		sle = frappe.db.sql("select voucher_no, posting_date from `tabStock Ledger Entry` where item_code = '{}' {} order by posting_date desc limit 1".format(biq.item_code,date_filter),as_dict=True)
		if not sle:
			continue
		if filters.get('project_receipt'):
			se = frappe.db.get_value("Stock Entry", {"name":sle[0].voucher_no,"project": filters.get('project_receipt')}, ["project"])
			if not se :
				continue
		else:		
			se = frappe.db.get_value("Stock Entry", sle[0].voucher_no, ["project"])
		if filters.get('project_position'):
			sed = frappe.db.get_value("Stock Entry Detail", {"parent": sle[0].voucher_no,"item_code": biq.item_code, "project": filters.get('project_position')}, ["project"])
			if not sed:
				continue
		else:
			sed = frappe.db.get_value("Stock Entry Detail", {"parent": sle[0].voucher_no,"item_code": biq.item_code}, ["project"])

		new_ = frappe.db.count("Serial No", {"zustand": "Neu", "item_code": biq.item_code, "status": ['!=', "Delivered"]})
		used_ = frappe.db.count("Serial No", {"zustand": "Gebraucht", "item_code": biq.item_code, "status": ['!=', "Delivered"]})
		broken_ = frappe.db.count("Serial No", {"zustand": "Defekt", "item_code": biq.item_code, "status": ['!=', "Delivered"]})
		data.append({
			"item_code": biq.item_code,
			"actual_qty":biq.actual_qty,
			"project_receipt":se or "", #transaction
			"project_position":sed or "", #Child 
			"date":sle[0].posting_date, #Latest transaction
			"new": new_,
			"used": used_,
			"broken": broken_
		})

	return columns, data
def get_columns():
	columns = [
		{
			"label": frappe._("Artikel"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": "120px"
		},
		{
			"label": frappe._("Project Beleg"),
			"fieldname": "project_receipt",
			"fieldtype": "Link",
			"options": "Project"
		},
		{
			"label": frappe._("Project Position"),
			"fieldname": "project_position",
			"fieldtype": "Link",
			"options": "Project"
		},
		{
			"label": frappe._("Lagermenge"),
			"fieldname": "actual_qty",
			"fieldtype": "Number"
		},
		{
			"label": frappe._("Datum"),
			"fieldname": "date",
			"fieldtype": "Date"
		},
		{
			"label": frappe._("Neu"),
			"fieldname": "new",
			"fieldtype": "Number"
		},
		{
			"label": frappe._("Gebraucht"),
			"fieldname": "used",
			"fieldtype": "Number"
		},
		{
			"label": frappe._("Defekt"),
			"fieldname": "broken",
			"fieldtype": "Number"
		}
	]
	return columns