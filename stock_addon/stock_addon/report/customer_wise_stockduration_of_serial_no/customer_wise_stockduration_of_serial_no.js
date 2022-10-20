// Built by Devarsh Bhatt at Genirex
// Contact devarsh@genirex.com


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
		}
	]
};
