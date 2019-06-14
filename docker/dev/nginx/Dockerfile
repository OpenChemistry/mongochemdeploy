FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.girder.conf /etc/nginx/conf.d/girder.conf
COPY wait-for-it.sh /wait-for-it.sh

ENTRYPOINT ["/wait-for-it.sh", "-t", "30", "hub:8000",  "--", "nginx", "-g", "daemon off;"]
