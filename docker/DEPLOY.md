To redeploy run the following commands to ensure images and containers are successfully rebuilt:

```bash
docker-compose down --rmi local --v
docker-compose build --no-cache
docker-compose up --force-recreate
```
