import frappe
import json
from frappe.utils import get_site_path

@frappe.whitelist()
def export_items(items=None):
    """
    Export CSV of items where custom_is_weight_item = 1.
    - If no selection (items=None or empty): export all weight items.
    - If selection provided: export only selected items that are weight items.
    """

    selected_item_names = []

    try:
        # Check if items are passed and non-empty
        if items:
            if isinstance(items, str):
                items = json.loads(items)
            if not isinstance(items, list):
                items = []

            for item in items:
                item_name = item.get("name") if isinstance(item, dict) else item
                if not item_name:
                    continue
                is_weight = frappe.db.get_value("Item", item_name, "custom_is_weight_item")
                if is_weight == 1:
                    selected_item_names.append(item_name)

        # If no items passed or none selected, fallback to all weight items
        if not selected_item_names:
            selected_item_names = frappe.get_all("Item", filters={"custom_is_weight_item": 1}, pluck="name")

        # Still nothing? Then throw an error
        if not selected_item_names:
            return {"error": "No weight items found to export."}

        # CSV header
        csv_content = "Item Code,Item Name,Custom Hotkey,Custom Is Weight Item,Shelf Life In Days,Barcode Type,DB Code,Item Price\n"

        for item_name in selected_item_names:
            item_doc = frappe.get_doc("Item", item_name)
            shelf_life = getattr(item_doc, 'shelf_life_in_days', '') or ''
            barcode_type = '101'
            db_code = '21'
            item_price = ''

            cost_center = getattr(item_doc, 'cost_center', None)
            if cost_center:
                item_price = frappe.db.get_value("Item Price", {
                    "item_code": item_doc.item_code,
                    "selling": 1,
                    "cost_center": cost_center
                }, "price_list_rate") or ''
            else:
                item_price = frappe.db.get_value("Item Price", {
                    "item_code": item_doc.item_code,
                    "selling": 1
                }, "price_list_rate") or ''

            csv_content += f"{item_doc.item_code},{item_doc.item_name},{getattr(item_doc, 'custom_hotkey', '')},{getattr(item_doc, 'custom_is_weight_item', '')},{shelf_life},{barcode_type},{db_code},{item_price}\n"

        # Write file
        file_name = "itemplus.csv"
        file_path = get_site_path("public", "files", file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(csv_content)

        return {
            "file_url": f"/files/{file_name}",
            "file_name": file_name
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Item Export Failed")
        return {"error": f"Item Export Failed: {str(e)}"}
