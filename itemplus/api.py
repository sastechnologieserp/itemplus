import frappe
import json
from frappe.utils import get_site_path

@frappe.whitelist()
def export_items(items):
    """
    Export items to a CSV file and return a file URL for download.
    """
    if not items:
        frappe.throw("No items to export.")

    if isinstance(items, str):
        items = json.loads(items)

    csv_content = "Item Code,Item Name,Custom Hotkey,Custom Is Weight Item,Shelf Life In Days,Barcode Type,DB Code,Item Price\n"
    for item in items:
        item_name = item["name"] if isinstance(item, dict) and "name" in item else item
        item_doc = frappe.get_doc("Item", item_name)
        shelf_life = getattr(item_doc, 'shelf_life_in_days', '')
        barcode_type = '101'
        db_code = '21'
        item_price = ''
        cost_center = getattr(item_doc, 'cost_center', None)
        if cost_center:
            price = frappe.db.get_value("Item Price", {"item_code": item_doc.item_code, "selling": 1, "cost_center": cost_center}, "price_list_rate")
            item_price = price if price is not None else ''
        else:
            price = frappe.db.get_value("Item Price", {"item_code": item_doc.item_code, "selling": 1}, "price_list_rate")
            item_price = price if price is not None else ''
        csv_content += f"{item_doc.item_code},{item_doc.item_name},{getattr(item_doc, 'custom_hotkey', '')},{getattr(item_doc, 'custom_is_weight_item', '')},{shelf_life},{barcode_type},{db_code},{item_price}\n"

    file_name = "itmepuls.csv"
    file_path = get_site_path("public", "files", file_name)
    with open(file_path, 'w') as file:
        file.write(csv_content)

    file_url = f"/files/{file_name}"
    return {
        "file_url": file_url,
        "file_name": file_name
    }