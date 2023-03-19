import frappe 


def fetch_zustand(self,method):
	doc = frappe.get_doc(self.voucher_type,self.voucher_no)
	for i in doc.items:
		if i.item_code == self.item_code:
			frappe.set_value(self.doctype, self.name, "zustand", i.zustand)
			break