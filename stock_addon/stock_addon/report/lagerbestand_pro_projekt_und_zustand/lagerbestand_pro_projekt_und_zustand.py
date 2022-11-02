#Built by Devarsh Bhatt at Genirex
#Contact devarsh@genirex.com

import json
import frappe
from erpnext.stock.dashboard.item_dashboard import get_data
def execute(filters=None):
	columns = get_columns()
	data = []
	stocks_per_item = get_data()
	item_total_stock = {}
	for stock in stocks_per_item:
		if stock.item_code in item_total_stock:
			item_total_stock.update({stock.item_code: item_total_stock[stock.item_code] + stock.actual_qty})
		else:
			item_total_stock.update({stock.item_code: stock.actual_qty})
		# print(stock,"===========")
	# query_ = """
	# 	select name, item_code , qty_after_transaction as actual_qty, posting_date as date, serial_no, 
	# 	from `tabStock Ledger Entry`;
	# """
	# stock_serial_item= []
	stock_serial_item = [item.name for item in frappe.db.sql("select name from `tabItem` where is_stock_item = 1 and has_serial_no = 1",as_dict=True)]
	for i in stock_serial_item:
		sle = frappe.db.sql("select voucher_no, posting_date from `tabStock Ledger Entry` where item_code = '{}' order by posting_date desc limit 1".format(i),as_dict=True)
		# if filters.get("filter_date"):
			# sle = frappe.db.sql("select voucher_no, posting_date from `tabStock Ledger Entry` where item_code = '{}' AND posting_date = '{}' order by posting_date desc limit 1".format(i,filters.get("filter_date")),as_dict=True) or None
			# print("------------------", sle, filters.get("filter_date"))
		if not sle:
			continue
		se = frappe.db.get_value("Stock Entry", sle[0].voucher_no, ["project"])
		sed = frappe.db.get_value("Stock Entry Detail", {"parent": sle[0].voucher_no,"item_code": i}, ["project"])
		new_ = frappe.db.count("Serial No", {"zustand": "Neu", "item_code": i, "status": ['!=', "Delivered"]})
		used_ = frappe.db.count("Serial No", {"zustand": "Gebraucht", "item_code": i, "status": ['!=', "Delivered"]})
		broken_ = frappe.db.count("Serial No", {"zustand": "Defekt", "item_code": i, "status": ['!=', "Delivered"]})
		data.append({
			"item_code": i,
			"actual_qty":item_total_stock[i],
			"project_receipt":se or "", #transaction
			"project_position":sed or "", #Child 
			"date":sle[0].posting_date, #Latest transaction
			"new": new_,
			"used": used_,
			"broken": broken_
		})
	# data_ = []
	# for d in data:
	# 	if filters and filters.get("filter_date") and filters.get("filter_date") == d['date'].strftime("%Y-%m-%d"):
	# 		data_.append(d)
	# 	if data_:
	# 		data = data_
	# 		# data_ = []
	# 	if filters and filters.get("project_receipt") and filters.get("project_receipt") == d['project_receipt']:
	# 		data_.append(d)
	# 	if data_:
	# 		data = data_
		# 	data_ = []
		# if filters and filters.get("project_position") and filters.get("project_position") == d['project_position']:
		# 	data_.append(d)
		# if data_:
		# 	data = data_
		# 	data_ = []

	return columns, data
def get_columns():
	columns = [
		# {
		# 	"label": frappe._("Stock Ledger Entry"),
		# 	"fieldname": "sle",
		# 	"fieldtype": "Link",
		# 	"options": "Stock Ledger Entry",
		# 	"width": "120px"
		# },
		{
			"label": frappe._("Artikel"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": "120px"
		},
		# {
		# 	"label": frappe._("Lagerhaus"),
		# 	"fieldname": "warehouse",
		# 	"fieldtype": "Link",
		# 	"options": "Warehouse"
		# },
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