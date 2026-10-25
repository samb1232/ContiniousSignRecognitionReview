FROM nginx:stable-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html search-data.json /usr/share/nginx/html/
COPY support/ /usr/share/nginx/html/support/
EXPOSE 80
