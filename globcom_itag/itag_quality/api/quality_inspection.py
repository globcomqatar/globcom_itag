# -*- coding: utf-8 -*-
# Copyright (c) 2026, Globcom ITAG
# License: MIT

"""
Generic API for creating inspection reports from Quality Inspection.

This module provides a configuration-driven approach to creating inspection reports.
No code changes needed when adding new inspection form types.

For implementation details, see: globcom_itag/itag_quality/README.md
"""

import frappe
from frappe import _


@frappe.whitelist()
def create_inspection_report(quality_inspection_name):
	"""
	Generic method to create any inspection report type.
	Works for all inspection forms - completely configuration-driven.

	This method:
	1. Gets the inspection form type from Quality Inspection
	2. Creates a new report of that type
	3. Auto-fetch populates fields from Quality Inspection
	4. Optionally runs form-specific hooks for special cases

	Args:
		quality_inspection_name (str): Name of Quality Inspection document

	Returns:
		dict: {
			"doctype": str,  # DocType of created report
			"name": str      # Name of created report document
		}

	Raises:
		frappe.ValidationError: If validation fails
		frappe.PermissionError: If user lacks permission

	Example:
		>>> create_inspection_report("QI-2026-0001")
		{"doctype": "Dimensional Inspection Report", "name": "DIR-2026-0001"}
	"""
	# Get Quality Inspection document
	qi = frappe.get_doc("Quality Inspection", quality_inspection_name)

	# Get DocType from select field (direct match - no mapping needed)
	doctype_to_create = qi.custom_inspection_form

	if not doctype_to_create:
		frappe.throw(_("Please select an Inspection Form first"))

	# Validate DocType exists
	if not frappe.db.exists("DocType", doctype_to_create):
		frappe.throw(_("Invalid Inspection Form: {0}").format(doctype_to_create))

	# Check user has permission to create this DocType
	if not frappe.has_permission(doctype_to_create, "create"):
		frappe.throw(_("You don't have permission to create {0}").format(doctype_to_create))

	# Create new report - auto-fetch handles field population
	report = frappe.get_doc({
		"doctype": doctype_to_create,
		"quality_inspection": qi.name  # This triggers all fetch_from fields!
	})

	# HOOK: Check if form-specific handler exists (before_create)
	# This allows special logic for forms that need more than auto-fetch
	hook_result = run_form_hook(doctype_to_create, "before_create", qi, report)
	if hook_result:
		report = hook_result  # Allow hook to modify the report

	# Save the report
	report.insert()

	# HOOK: After creation (for creating related docs, notifications, etc.)
	run_form_hook(doctype_to_create, "after_create", qi, report)

	return {
		"doctype": doctype_to_create,
		"name": report.name
	}


def run_form_hook(doctype_name, hook_type, qi, report):
	"""
	Execute form-specific hook if it exists.

	This function looks for optional hooks in inspection_hooks.py module.
	If no hook exists, it fails gracefully and returns None.

	Hook naming convention:
	- Function: {doctype_snake_case}_{hook_type}
	- Example: dimensional_inspection_report_before_create()

	Args:
		doctype_name (str): DocType name (e.g., "Dimensional Inspection Report")
		hook_type (str): "before_create" or "after_create"
		qi (Document): Quality Inspection document
		report (Document): Inspection report document

	Returns:
		For before_create: Modified report document or None
		For after_create: None

	Example:
		>>> # If hook exists: dimensional_inspection_report_before_create(qi, report)
		>>> run_form_hook("Dimensional Inspection Report", "before_create", qi, report)
		<Modified report object>

		>>> # If hook doesn't exist
		>>> run_form_hook("Visual Inspection Report", "before_create", qi, report)
		None
	"""
	# Convert DocType name to Python function name
	# "Dimensional Inspection Report" → "dimensional_inspection_report"
	function_name = frappe.scrub(doctype_name)
	hook_function_name = f"{function_name}_{hook_type}"

	# Try to import and run the hook
	try:
		# Look for hook in: globcom_itag.itag_quality.inspection_hooks
		hook_module = frappe.get_module("globcom_itag.itag_quality.inspection_hooks")

		if hasattr(hook_module, hook_function_name):
			hook_function = getattr(hook_module, hook_function_name)
			return hook_function(qi, report)

	except (ImportError, AttributeError):
		# No hook exists - this is fine, use generic behavior
		pass

	return None
