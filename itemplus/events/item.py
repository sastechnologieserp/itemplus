import frappe
def on_update(doc, method=None):
    if doc.custom_is_weight_item:
        if not doc.custom_hotkey:
            frappe.throw("Custom Hotkey is required for weight items.")
    if not len(doc.item_code) == 5:
        frappe.throw("Item Code must be 5 numbers.")
    