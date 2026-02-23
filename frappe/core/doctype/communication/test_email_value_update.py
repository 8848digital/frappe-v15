import frappe
from frappe.tests.utils import FrappeTestCase


class TestEmailTemplateValueUpdate(FrappeTestCase):

    def setUp(self):
        frappe.db.set_single_value("System Settings", "global_enable", 1)

        # Create Test DocType record (use ToDo for simplicity)
        self.doc = frappe.get_doc({
            "doctype": "ToDo",
            "description": "Old Description",
            "status": "Open"
        }).insert()

        # Create Email Template
        self.template = frappe.get_doc({
            "doctype": "Email Template",
            "name": "Test Template",
            "subject": "Test",
            "response": "Test Body",
            "enable_value_update": 1,
            "status_update": [{
                "doctype_name": "ToDo",
                "update_doc_field": "status",
                "update_doc_data": "Closed"
            }],
            "exclude_valuess": []
        }).insert()

    def tearDown(self):
        frappe.db.rollback()

    # ---------------------------------------------------------
    # 1️⃣ Happy Path Test
    # ---------------------------------------------------------
    def test_field_updates_when_conditions_met(self):
        from frappe.core.doctype.communication.email import make
        print("TEST IS RUNNING")
        make(
            doctype="ToDo",
            name=self.doc.name,
            subject="Test",
            content="Test",
            email_template=self.template.name,
        )

        self.doc.reload()
        self.assertEqual(self.doc.status, "Closed")

    # ---------------------------------------------------------
    # 2️⃣ global_enable disabled
    # ---------------------------------------------------------
    def test_no_update_when_global_disabled(self):
        frappe.db.set_single_value("System Settings", "global_enable", 0)

        from frappe.core.doctype.communication.email import make

        make(
            doctype="ToDo",
            name=self.doc.name,
            subject="Test",
            content="Test",
            email_template=self.template.name,
        )

        self.doc.reload()
        self.assertEqual(self.doc.status, "Open")

    # ---------------------------------------------------------
    # 3️⃣ Field excluded
    # ---------------------------------------------------------
    def test_excluded_field_not_updated(self):
        self.template.append("exclude_valuess", {
            "doctype_name": "ToDo",
            "exclude_values": "status"
        })
        self.template.save()

        from frappe.core.doctype.communication.email import make

        make(
            doctype="ToDo",
            name=self.doc.name,
            subject="Test",
            content="Test",
            email_template=self.template.name,
        )

        self.doc.reload()
        self.assertEqual(self.doc.status, "Open")

    # ---------------------------------------------------------
    # 4️⃣ No matching doctype
    # ---------------------------------------------------------
    def test_no_update_if_doctype_not_matching(self):
        self.template.status_update[0].doctype_name = "Sales Order"
        self.template.save()

        from frappe.core.doctype.communication.email import make

        make(
            doctype="ToDo",
            name=self.doc.name,
            subject="Test",
            content="Test",
            email_template=self.template.name,
        )

        self.doc.reload()
        self.assertEqual(self.doc.status, "Open")

    # ---------------------------------------------------------
    # 5️⃣ No save if value already same
    # ---------------------------------------------------------
    def test_no_update_if_value_same(self):
        self.doc.status = "Closed"
        self.doc.save()

        from frappe.core.doctype.communication.email import make

        make(
            doctype="ToDo",
            name=self.doc.name,
            subject="Test",
            content="Test",
            email_template=self.template.name,
        )

        self.doc.reload()
        self.assertEqual(self.doc.status, "Closed")
