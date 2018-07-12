FROM nginx:latest

COPY ./images/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./pgtbl/tbl/staticfiles /usr/share/nginx/html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
