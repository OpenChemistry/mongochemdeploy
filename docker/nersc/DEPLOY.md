Creating Volumes for the stack
------------------------------

```
rancher volume create --driver rancher-nfs web-certbot-webroot.oc
rancher volume create --driver rancher-nfs web-certs.oc
rancher volume create --driver rancher-nfs app-assetstore.oc
rancher volume create --driver rancher-nfs app-keys.oc
rancher volume create --driver rancher-nfs db-mongodb.oc

```


Setting up DH parameters for NGINX
-----------------------------------

Mount the key volume into a container and exec into it and running the following
command.

```
openssl dhparam -out /etc/letsencrypt/ssl-dhparams.pem 2048
````

Here is an example of a compose block to do the mounting, in this case we are
using the Girder image.

```
  web-dhparams-setup:
    image:  girder/girder:2.x-maintenance-py3
    command: -d mongodb://db-mongodb:27017/girder
    cap_drop:
      - ALL
    volumes:
      - web-certs.oc:/etc/letsencrypt
      - web-certbot-webroot.oc:/data/letsencrypt
    links:
      - db-mongodb
    depends_on:
      - db-mongodb
```

Once the command has been run the container can be removed from the stack.
