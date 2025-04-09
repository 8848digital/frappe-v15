import frappe

def execute():
    if frappe.conf.db_type == "mariadb":
        frappe.db.sql("ALTER TABLE `__UserSettings` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    elif frappe.conf.db_type == "postgres":
        default_collation = frappe.db.sql("SHOW LC_COLLATE", as_dict=True)[0]["lc_collate"]
        frappe.db.sql(f"""
            ALTER TABLE "__UserSettings" 
            ALTER COLUMN "data" TYPE TEXT COLLATE "{default_collation}";
        """)