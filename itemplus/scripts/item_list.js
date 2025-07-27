frappe.listview_settings["Item"] = {
    onload(listview) {
        console.log("Item List View Loaded");

        // Add as a menu item (top-right menu)
        if (listview.page && listview.page.add_menu_item) {
            listview.page.add_menu_item("Export Items", function () {
                const items = listview.get_checked_items();
                frappe.call({
                    method: "itemplus.api.export_items",
                    freeze: true,
                    args: { items: items },
                    callback: function (r) {
                        if (r.message && r.message.file_url) {
                            const a = document.createElement('a');
                            a.href = r.message.file_url;
                            a.download = r.message.file_name || 'itmepuls.csv';
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                            frappe.msgprint(__("Items exported and download started."));
                        } else {
                            frappe.msgprint(__("Export failed or no file generated."));
                        }
                    },
                });
            });
        }

        if (listview.page && listview.page.add_inner_button) {
            listview.page.add_inner_button("Export Items", function () {
                const items = listview.get_checked_items();
                frappe.call({
                    method: "itemplus.api.export_items",
                    freeze: true,
                    args: { items: items },
                    callback: function (r) {
                        if (r.message && r.message.file_url) {
                            const a = document.createElement('a');
                            a.href = r.message.file_url;
                            a.download = r.message.file_name || 'itmepuls.csv';
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                            frappe.msgprint(__("Items exported and download started."));
                        } else {
                            frappe.msgprint(__("Export failed or no file generated."));
                        }
                    },
                });
            });
        }
    }
};