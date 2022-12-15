//Built by Devarsh Bhatt at Phamos
//Contact devarsh.bhat@phamos.eu

frappe.query_reports["Lagerbestand pro Projekt und Zustand"] = {
	"filters": [
		{
			"fieldname": "filter_date",
			"label": __("Datum (Stichtag)"),
			"fieldtype": "Date",
			"width": "60px"
		},
		{
			"fieldname": "project",
			"label": __("Project (Position)"),
			"fieldtype": "Link",
			"options": "Project",
			"width": "60px"
		},
		{
			"fieldname": "screen_size",
			"label": "",
			"fieldtype": "Data",
			"hidden": 1,
			"default": window.innerWidth
		},
	]
};
