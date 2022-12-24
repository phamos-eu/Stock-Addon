#Built by Devarsh Bhatt at Phamos
#Contact devarsh.bhat@phamos.eu

import frappe

def execute(filters=None):
	columns = get_columns(filters.get('screen_size'))
	data = []
	where = ""
	where_project = ""
	zustand_where = ""
	# where_modified = ""
	if filters.get("project"):
		where_project = f" where name= '{filters.get('project')}'"
	if filters.get("filter_date"):
		where = f"and posting_date <= '{filters.get('filter_date')}'"
		zustand_where = f"and purchase_date <= '{filters.get('filter_date')}'"

	project_list = [v.name for v in frappe.db.sql(f"""select name from `tabProject`{where_project}""",as_dict=1)]
	project_list.append("")
	item_list = frappe.get_all("Item", filters={'has_serial_no':1},pluck='name')

	for project in project_list:
		if project == "":
			project_conditions = f"and project is NULL"
		else:
			project_conditions = f"and project='{project}'"
		for item in item_list:
			qty_date = frappe.db.sql(f"""select qty_after_transaction as qty, posting_date from `tabStock Ledger Entry` where item_code='{item}'{project_conditions} {where} order by posting_date desc LIMIT 1""",as_dict=1)
			if qty_date:
				new_serial = frappe.db.sql(f"""select count(zustand='Neu') as qty from `tabSerial No` where item_code='{item}'{project_conditions} and status='Active' and zustand='Neu' {zustand_where}""",as_dict=1)
				used_serial = frappe.db.sql(f"""select count(zustand='Gebrauch') as qty from `tabSerial No` where item_code='{item}'{project_conditions} and status='Active' and zustand='Gebrauch' {zustand_where}""",as_dict=1)
				defected_serial = frappe.db.sql(f"""select count(zustand='Defekt') as qty from `tabSerial No` where item_code='{item}'{project_conditions} and status='Active' and zustand='Defekt' {zustand_where}""",as_dict=1)
				data.append({
					"item_code": item,
					"project": project,
					"actual_qty":qty_date[0].get('qty'),
					"date": qty_date[0].get('posting_date'),
					"new": new_serial[0].get('qty'),
					"used": used_serial[0].get('qty'),
					"broken": defected_serial[0].get('qty')
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
			"fieldtype": "Date",
			"width": screen_size*0.07
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