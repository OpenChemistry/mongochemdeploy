FROM node:8.0 AS BUILD

RUN apt-get update && apt-get -y install \
  git

RUN git clone https://github.com/OpenChemistry/mongochemclient && \
  cd mongochemclient && \
  git checkout workaround && \
  npm install && \
  npm run build

FROM nginx
COPY --from=build /mongochemclient/build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.girder.conf /etc/nginx/conf.d/girder.conf
