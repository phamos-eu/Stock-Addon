// Copyright (c) 2022, MIT and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Lagerbestand pro Projekt und Zustand"] = {
	"filters": [
		{
			"fieldname":"filter_date",
			"label": __("Datum (Stichtag)"),
			"fieldtype": "Date",
			"width": "60px"
		},
		{
			"fieldname":"project_receipt",
			"label": __("Project (Beleg)"),
			"fieldtype": "Link",
			"options": "Project",
			"width": "60px"
		},
		{
			"fieldname":"project_position",
			"label": __("Project (Position)"),
			"fieldtype": "Link",
			"options": "Project",
			"width": "60px"
		},
	]
};
