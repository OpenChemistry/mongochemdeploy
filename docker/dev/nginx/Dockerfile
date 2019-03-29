FROM node:10 AS build

RUN apt-get update && apt-get -y install \
  git

RUN git clone https://github.com/OpenChemistry/mongochemclient && \
  cd mongochemclient && \
  npm install && \
  REACT_APP_DEPLOYMENT=development npm run build

FROM nginx
COPY --from=build /mongochemclient/build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.girder.conf /etc/nginx/conf.d/girder.conf
COPY wait-for-it.sh /wait-for-it.sh

ENTRYPOINT ["/wait-for-it.sh", "-t", "30", "hub:8000",  "--", "nginx", "-g", "daemon off;"]
