FROM rocker/shiny:4.4.1

RUN apt-get update && apt-get install -y --no-install-recommends curl nginx \
  && rm -rf /var/lib/apt/lists/*

COPY shiny-server.conf /etc/shiny-server/shiny-server.conf
COPY nginx.conf /etc/nginx/sites-available/default
COPY app /srv/shiny-server/dsn
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
  && rm -f /etc/nginx/sites-enabled/default \
  && ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

EXPOSE 3838
ENTRYPOINT ["/entrypoint.sh"]
