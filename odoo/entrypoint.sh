#!/bin/bash
set -e

# Generate odoo.conf from environment variables
cat > /etc/odoo/odoo.conf << EOF
[options]
; Addons paths
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons

; Data directory
data_dir = /var/lib/odoo

; Database connection from Railway environment
db_host = ${PGHOST:-localhost}
db_port = ${PGPORT:-5432}
db_user = ${PGUSER:-odoo}
db_password = ${PGPASSWORD:-odoo}
db_name = ${PGDATABASE:-odoo}

; Admin password for database management
admin_passwd = ${ODOO_ADMIN_PASSWORD:-admin}

; Server configuration
http_port = ${PORT:-8069}
proxy_mode = True
without_demo = True

; Performance settings
workers = ${ODOO_WORKERS:-2}
max_cron_threads = 1
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648
limit_request = 8192
limit_time_cpu = 600
limit_time_real = 1200

; Logging
log_level = info
log_handler = :INFO

; Security - disable database listing in production
list_db = ${ODOO_LIST_DB:-False}
EOF

echo "Odoo configuration generated with:"
echo "  Database Host: ${PGHOST:-localhost}"
echo "  Database Port: ${PGPORT:-5432}"
echo "  Database Name: ${PGDATABASE:-odoo}"
echo "  HTTP Port: ${PORT:-8069}"

# Check if this is first run (database needs initialization)
if [ "${ODOO_INIT_DB:-false}" = "true" ]; then
  echo "Initializing database with base modules..."
  exec odoo -i base,web,sale,purchase,stock,point_of_sale,website,website_sale,mrp --stop-after-init
else
  # Execute the original Odoo entrypoint
  exec /entrypoint.sh "$@"
fi
