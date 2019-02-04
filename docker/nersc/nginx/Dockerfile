FROM nginx
COPY ./devops/docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /client/build/ /etc/nginx/html/
