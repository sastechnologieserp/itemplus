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

    # Parse the JSON string to a Python list
    if isinstance(items, str):
        items = json.loads(items)

    csv_content = "Item Code,Item Name,Custom Hotkey,Custom Is Weight Item\n"
    for item in items:
        item_name = item["name"] if isinstance(item, dict) and "name" in item else item
        item_doc = frappe.get_doc("Item", item_name)
        csv_content += f"{item_doc.item_code},{item_doc.item_name},{getattr(item_doc, 'custom_hotkey', '')},{getattr(item_doc, 'custom_is_weight_item', '')}\n"

    file_name = "itmepuls.csv"
    file_path = get_site_path("public", "files", file_name)
    with open(file_path, 'w') as file:
        file.write(csv_content)

    file_url = f"/files/{file_name}"
    return {
        "file_url": file_url,
        "file_name": file_name
    }