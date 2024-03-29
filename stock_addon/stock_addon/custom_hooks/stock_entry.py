import frappe
import time

def fetch_condition_from_stock_entry(self,method):
    time.sleep(5)
    for item in self.items:
        list_serial = []
        if item.serial_no:
            list_serial = item.serial_no.split('\n')
        for ls in list_serial:
            add_value = {"zustand":item.zustand}
            if self.project:
                add_value.update({"project":self.project})
            frappe.db.set_value("Serial No", ls, add_value)