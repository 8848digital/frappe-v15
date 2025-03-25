import frappe

def execute():
    if frappe.conf.db_type == "mariadb":
        frappe.db.sql("ALTER TABLE `__UserSettings` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    elif frappe.conf.db_type == "postgres":
        frappe.db.sql("""
            ALTER TABLE "__UserSettings" 
            ALTER COLUMN "data" TYPE TEXT COLLATE "C.UTF-8";
        """)