#Built by Devarsh Bhatt at Phamos
#Contact devarsh.bhat@phamos.eu

import frappe

def execute(filters=None):
	columns = get_columns()
	data = []
	where = "1=1"
	if filters.get("project_position"):
		where = f"{where} and project = '{filters.get('project_position')}'"
	if filters.get("filter_date"):
		where = f"{where} and purchase_date <= '{filters.get('filter_date')}'"
	serials = frappe.db.sql(f"select project, purchase_date, item_code, count(item_code) as item_code_count from `tabSerial No` where {where} and status='Active' group by item_code, project order by purchase_date desc" , as_dict=1)

	for serial in serials:
		new_ = frappe.db.sql(f"select count(zustand) as zustand from `tabSerial No` where {where} and status='Active' and item_code = '{serial.get('item_code')}' and project = '{serial.get('project')}' and zustand = 'Neu' group by item_code, project order by purchase_date desc" , as_dict=1) or []
		used_ = frappe.db.sql(f"select count(zustand) as zustand from `tabSerial No` where {where} and status='Active' and item_code = '{serial.get('item_code')}' and project = '{serial.get('project')}' and zustand = 'Gebraucht' group by item_code, project order by purchase_date desc" , as_dict=1) or []
		broken_ = frappe.db.sql(f"select count(zustand) as zustand from `tabSerial No` where {where} and status='Active' and item_code = '{serial.get('item_code')}' and project = '{serial.get('project')}' and zustand = 'Defekt' group by item_code, project order by purchase_date desc" , as_dict=1) or []

		data.append({
			"item_code": serial.get('item_code'),
			"actual_qty":serial.item_code_count,
			"project_position":serial.get('project') or "", 
			"date":serial.get('purchase_date') or "", #Latest transaction
			"new": new_[0].zustand if new_ else 0,
			"used": used_[0].zustand if used_ else 0,
			"broken": broken_[0].zustand if broken_ else 0
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