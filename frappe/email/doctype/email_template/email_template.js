// Copyright (c) 2018, Frappe Technologies and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Email Template", {
// 	refresh: function () {},
// });




frappe.ui.form.on("Document Exclude Status", {
	doctype_name: function (frm, cdt, cdn) {
			var row = locals[cdt][cdn];
			if (!row.doctype_name) {
				return;
			}
			frappe.model.with_doctype(row.doctype_name, () => {
				const fieldnames = frappe
					.get_meta(row.doctype_name)
					.fields.filter((field) => !frappe.model.no_value_type.includes(field.fieldtype))
					.map((field) => field.fieldname);

				frm.fields_dict.exclude_valuess.grid.update_docfield_property(
					"exclude_field",
					"options",
					[""].concat(fieldnames)
				);
			});
		},
    exclude_field: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn]; // Get the current row of the child table
		// Make sure that exclude_field is an array (in case it is not)
		var selected_values = Array.isArray(child.exclude_field) ? child.exclude_field : child.exclude_field.split(', ');
		// Get the existing exclude_value (if any)
		var existing_values = child.exclude_values ? child.exclude_values.split(', ') : [];

		// Combine existing and selected values, removing duplicates
		var combined_values = Array.from(new Set(existing_values.concat(selected_values)));

		// Update the exclude_values field with the combined values
		child.exclude_values = combined_values.join(', ');
		// Refresh the field to show the updated exclude_value
		frm.refresh_field('exclude_valuess');
	}


});