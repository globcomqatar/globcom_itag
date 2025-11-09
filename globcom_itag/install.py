import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from globcom_itag.globcom_itag.constants.custom_fields import CUSTOM_FIELDS
from globcom_itag.globcom_itag.constants.property_setters import PROPERTY_SETTER


def create_property_setter() :
    for property in PROPERTY_SETTER :
        make_property_setter(doctype = property.get("doctype", ""),
                             for_doctype = property.get("doctype_or_field", "DocField"),
                             fieldname = property.get("field_name", ""),
                             property = property.get("property", ""),
                             property_type = property.get("property_type", ""),
                             value = property.get("value", ""),
                             is_system_generated = property.get("is_system_generated", 1),
                             validate_fields_for_doctype=False)

def after_install():

    create_custom_fields(CUSTOM_FIELDS, ignore_validate=True, update=True)
    create_property_setter()


