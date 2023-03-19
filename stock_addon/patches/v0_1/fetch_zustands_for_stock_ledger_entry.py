import frappe

def execute():
    frappe.reload_doc("stock", "doctype", "stock_ledger_entry")
    for voucher in ["Stock Entry Detail", "Purchase Receipt Item"]:
        all_voucher = frappe.get_all(voucher, {"docstatus": ["=", "1"]}, ["parent", "item_code","zustand"] )
        for vchr in all_voucher:
            frappe.db.set_value("Stock Ledger Entry", {"voucher_no": vchr.parent},"zustand", vchr.zustand)
    frappe.db.commit()