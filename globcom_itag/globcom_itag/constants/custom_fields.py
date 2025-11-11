CUSTOM_FIELDS = {
    "Work Order Operation": [
        {
            "fieldname": "custom_quality_inspection_required",
            "label": "Quality Inspection Required",
            "fieldtype": "Check",
            "insert_after": "sequence_id",
        }, 
    ],
    "Job Card": [
        {
            "fieldname": "custom_operation_description",
            "label": "Operation Description",
            "fieldtype": "Small Text",
            "read_only": "1",
            "insert_after": "operation",
        }, 
        {
            "fieldname": "custom_inspection_required",
            "label": "Inspection Required",
            "fieldtype": "Check",
            "read_only": "1",
            "insert_after": "column_break_fcmp",
        }, 
    ],
}