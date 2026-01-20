FROM odoo:18

# Copy custom addons
COPY ./addons /mnt/extra-addons

# Copy custom entrypoint that handles environment variables
COPY ./entrypoint.sh /custom-entrypoint.sh

# Set proper permissions
USER root
RUN chown -R odoo:odoo /mnt/extra-addons && \
    chmod +x /custom-entrypoint.sh
USER odoo

# Set environment defaults
ENV ODOO_RC=/etc/odoo/odoo.conf
ENV PGHOST=localhost
ENV PGPORT=5432
ENV PGUSER=odoo
ENV PGPASSWORD=odoo
ENV PGDATABASE=odoo
ENV PORT=8069

# Expose Odoo port (Railway will override with $PORT)
EXPOSE 8069

# Use custom entrypoint
ENTRYPOINT ["/custom-entrypoint.sh"]
CMD ["odoo"]
