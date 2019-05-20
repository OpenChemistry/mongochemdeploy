# openchemistry/torchani

## Image Description
```
docker run openchemistry/torchani -d
```

## Running Calculation
```
docker run -v $(pwd):/data openchemistry/torchani -g /data/geometry.cjson -p /data/parameters.json -o /data/out.cjson -s /data/scratch
```
