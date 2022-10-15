import frappe
import time

def fetch_condition_from_stock_entry(self,method):
    time.sleep(5)
    for item in self.items:
        list_serial = item.serial_no.split('\n')
        for ls in list_serial:
            frappe.db.set_value("Serial No", ls, "zustand",item.zustand)