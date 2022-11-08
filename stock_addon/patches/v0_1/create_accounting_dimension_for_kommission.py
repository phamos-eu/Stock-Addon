import frappe

def execute():
	frappe.reload_doc('accounts', 'doctype', 'accounting_dimension')
	frappe.reload_doc("stock_addon", "doctype", "kommission")
	if frappe.db.exists("Accounting Dimension", "Kommission"):
		return
	ad = frappe.new_doc("Accounting Dimension")
	ad.document_type= "Kommission"
	ad.label= "Kommission"
	ad.insert(ignore_permissions=True)
	ad.save()
	print(ad)
	frappe.db.commit()
	