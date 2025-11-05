import frappe
from erpnext.manufacturing.doctype.job_card.job_card import (
    JobCard
)


class CustomJobCard(JobCard):
    def add_time_log(self, args):

        if self.sequence_id >= 2 :

            query = f"""
						SELECT twoo.*
						FROM `tabWork Order Operation` twoo  
						WHERE twoo.parent = '""" + self.work_order  + """'
                              AND twoo.idx = """ + str(self.sequence_id - 1 ) + """
						ORDER BY twoo.idx DESC
                        LIMIT 1
						"""
        
            last_opercation_data = frappe.db.sql(query, as_dict=1)

            if last_opercation_data :
                  if last_opercation_data[0]['name'] :
                    last_opercation_doc_query =  f"""
                                                    SELECT tjc.*
                                                    FROM `tabJob Card` tjc  
                                                    WHERE tjc.operation_id = '""" + last_opercation_data[0]['name']  + """'
                                                        AND tjc.docstatus = 1
                                                    ORDER BY tjc.modified DESC
                                                    """
                    last_opercation_doc_data = frappe.db.sql(last_opercation_doc_query, as_dict=1)
                    if last_opercation_doc_data :
                         pass
                    else :
                         frappe.throw(
                                            f"Please complete <b>{last_opercation_data[0]['operation']}</b> to start this Job Card <b>{self.name}</b>."
                                    )

        super().add_time_log(args)
        # frappe.throw(
        #         "Please link a <b>Quality Inspection</b> document before completing this Job Card."
        # )

        # super().add_time_log(self, args)
    
    def on_submit(self) -> None:
		# super().on_submit()
		# self.set_onload("has_reserved_stock", True)
        if self.get("custom_inspection_required", False):
                        if self.quality_inspection:
                            qi_doc = frappe.get_doc("Quality Inspection", self.quality_inspection)

                            if qi_doc:
                                if qi_doc.get("docstatus") != 1 :
                                    frappe.throw(
                                            f"The linked Quality Inspection <b>{self.quality_inspection}</b> must be "
                                            f"<b>Submitted</b> before you can complete or submit this Job Card <b>{self.name}</b>."
                                    )
                        
                            if qi_doc.get("status") != "Accepted" :
                                    frappe.throw(
                                            f"The linked Quality Inspection <b>{self.quality_inspection}</b> must be "
                                            f"<b>Accepted</b> before you can complete or submit this Job Card <b>{self.name}</b>."
                                    )

                        else:
                            frappe.throw(
                                "Please link a <b>Quality Inspection</b> document before completing this Job Card."
                            )

        super().on_submit()
	


