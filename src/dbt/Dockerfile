FROM ghcr.io/dbt-labs/dbt-postgres:1.8.latest
 
WORKDIR /usr/app
 
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
 
ENTRYPOINT ["/entrypoint.sh"]