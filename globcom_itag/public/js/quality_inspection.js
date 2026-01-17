/**
 * Client Script for Quality Inspection
 * Handles "Start Inspection" button to create inspection reports
 *
 * This is a generic implementation that works for ALL inspection form types.
 * No changes needed when adding new inspection forms.
 *
 * For implementation details, see: globcom_itag/itag_quality/README.md
 */

frappe.ui.form.on('Quality Inspection', {
	/**
	 * Handle "Start Inspection" button click
	 * Creates a new inspection report based on selected form type
	 */
	custom_start_inspection: function(frm) {
		// Validation: Check if inspection form is selected
		if (!frm.doc.custom_inspection_form) {
			frappe.msgprint({
				title: __('Inspection Form Required'),
				message: __('Please select an Inspection Form first'),
				indicator: 'red'
			});
			return;
		}

		// Validation: Document must be saved
		if (frm.is_new()) {
			frappe.msgprint({
				title: __('Save Required'),
				message: __('Please save the Quality Inspection first'),
				indicator: 'orange'
			});
			return;
		}

		// Call generic API to create inspection report
		frappe.call({
			method: 'globcom_itag.itag_quality.api.quality_inspection.create_inspection_report',
			args: {
				quality_inspection_name: frm.doc.name
			},
			freeze: true,
			freeze_message: __('Creating Inspection Report...'),
			callback: function(r) {
				if (r.message) {
					// Success - navigate to the new inspection report
					frappe.set_route('Form', r.message.doctype, r.message.name);

					// Show success message
					frappe.show_alert({
						message: __('Inspection Report {0} created successfully', [r.message.name]),
						indicator: 'green'
					}, 5);
				}
			},
			error: function(r) {
				// Error handling - show user-friendly message
				frappe.msgprint({
					title: __('Error Creating Report'),
					message: r.message || __('An error occurred while creating the inspection report'),
					indicator: 'red'
				});
			}
		});
	}
});
