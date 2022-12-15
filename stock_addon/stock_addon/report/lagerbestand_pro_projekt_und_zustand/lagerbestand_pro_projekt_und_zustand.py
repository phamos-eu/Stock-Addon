#Built by Devarsh Bhatt at Phamos
#Contact devarsh.bhat@phamos.eu

import frappe

def execute(filters=None):
	columns = get_columns(filters.get('screen_size'))
	data = []
	where = "1=1"
	if filters.get("project"):
		where = f"{where} and project = '{filters.get('project')}'"
	if filters.get("filter_date"):
		where = f"{where} and purchase_date <= '{filters.get('filter_date')}'"
	else:
		where = f"{where} and status='Active'"
	query = f"select project, purchase_date, item_code, count(item_code) as item_code_count from `tabSerial No` where {where} group by item_code, project order by purchase_date desc"
	serials = frappe.db.sql(query, as_dict=1)
	for serial in serials:
		if serial.get("project"):
			where = f"{where} and project = '{serial.get('project')}'"
		new_ = frappe.db.sql(f"select count(zustand) as zustand from `tabSerial No` where {where} and item_code = '{serial.get('item_code')}' and zustand = 'Neu' group by item_code, project order by purchase_date desc" , as_dict=1) or []
		used_ = frappe.db.sql(f"select count(zustand) as zustand from `tabSerial No` where {where} and item_code = '{serial.get('item_code')}' and zustand = 'Gebraucht' group by item_code, project order by purchase_date desc" , as_dict=1) or []
		broken_ = frappe.db.sql(f"select count(zustand) as zustand from `tabSerial No` where {where} and item_code = '{serial.get('item_code')}' and zustand = 'Defekt' group by item_code, project order by purchase_date desc" , as_dict=1) or []

		data.append({
			"item_code": serial.get('item_code'),
			"actual_qty":serial.item_code_count,
			"project":serial.get('project') or "", 
			"date":serial.get('purchase_date') or "", #Latest transaction
			"new": new_[0].zustand if new_ else 0,
			"used": used_[0].zustand if used_ else 0,
			"broken": broken_[0].zustand if broken_ else 0
		})

	return columns, data
def get_columns(screen_size):
	columns = [
		{
			"label": frappe._("Artikel"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": screen_size*0.3,
			"align": "left"
		},
		{
			"label": frappe._("Project"),
			"fieldname": "project",
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
			"fieldtype": "Number",
			"width": screen_size*0.07,
		},
		{
			"label": frappe._("Gebraucht"),
			"fieldname": "used",
			"fieldtype": "Number",
			"width": screen_size*0.07,
		},
		{
			"label": frappe._("Defekt"),
			"fieldname": "broken",
			"fieldtype": "Number",
			"width": screen_size*0.07,
		}
	]
	return columns