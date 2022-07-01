// Copyright (c) 2022, MIT and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer wise Stockduration of Serial No"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			// "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			// "reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			// "default": frappe.datetime.get_today(),
			// "reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"customer",
			"label": __("Choose Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			// "default": frappe.datetime.get_today(),
			// "reqd": 1,
			"width": "60px"
		}
	]
};
