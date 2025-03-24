import frappe

def execute():
    if frappe.db.db_type == "mariadb":
        frappe.db.sql("ALTER TABLE __UserSettings CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    elif frappe.db.db_type == "postgres":
        frappe.db.sql("""
            ALTER TABLE "__UserSettings" 
            ALTER COLUMN "value" TYPE TEXT COLLATE "en_US.utf8";
        """)