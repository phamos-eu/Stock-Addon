// Copyright (c) 2022, MIT and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer wise Stockduration of Serial No"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "60px"
		},
		{
			"fieldname":"customer",
			"label": __("Choose Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": "60px"
		},
		{
			"fieldname":"commission_by",
			"label": __(""),
			"fieldtype": "Select",
			"options": ["",__("Item Wise"),__("Transaction Wise")],
			"width": "60px"
		}
	]
};
