#Built by Devarsh Bhatt at Phamos
#Contact devarsh.bhat@phamos.eu

import frappe

def execute(filters=None):
    columns = get_columns(filters.get('screen_size'))
    data = []
    where_clause = ""

    if filters:
        if filters.get("project"):
            where_clause += f" AND sle.project = '{filters.get('project')}'"
        if filters.get("filter_date"):
            where_clause += f" AND sle.posting_date <= '{filters.get('filter_date')}'"

    stock_ledger_entries = frappe.db.sql(f"""
        SELECT sle.item_code, sle.project,
            SUM(sle.actual_qty) AS actual_qty,
            (SELECT qty_after_transaction FROM `tabStock Ledger Entry`
             WHERE item_code = sle.item_code AND posting_date <= sle.posting_date {where_clause}
             ORDER BY posting_date DESC LIMIT 1) AS qty_after_transaction,
            MAX(sle.posting_date) AS posting_date,
            SUM(CASE WHEN sle.zustand = 'Neu' THEN sle.actual_qty ELSE 0 END) AS new,
            SUM(CASE WHEN sle.zustand = 'Gebraucht' THEN sle.actual_qty ELSE 0 END) AS used,
            SUM(CASE WHEN sle.zustand = 'Defekt' THEN sle.actual_qty ELSE 0 END) AS broken
        FROM `tabStock Ledger Entry` sle
        WHERE sle.docstatus = 1 {where_clause}
        GROUP BY sle.item_code, sle.project
        ORDER BY sle.item_code, sle.project
    """, as_dict=True)

    for sle in stock_ledger_entries:
        row = {
            "item_code": sle.item_code,
            "project": sle.project,
            "actual_qty": sle.actual_qty,
            "date": sle.posting_date,
            "new": sle.new,
            "used": sle.used,
            "broken": sle.broken
        }
        data.append(row)

    return columns, data

def get_columns(screen_size):
	columns = [
		{
			"label": frappe._("Artikel"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": screen_size*0.25,
			"align": "left"
		},
		{
			"label": frappe._("Project"),
			"fieldname": "project",
			"fieldtype": "Link",
			"options": "Project",
			"width": screen_size*0.07
   
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