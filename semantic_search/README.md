# Semantic search

pgvector

```bash
docker run -d -p 35432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres ankane/pgvector
```


clickhouse

```bash
docker pull clickhouse/clickhouse-server
docker run -d --name some-clickhouse-server --ulimit nofile=262144:262144 clickhouse/clickhouse-server
echo "SELECT 'Hello, ClickHouse!'" | docker run -i --rm --link some-clickhouse-server:clickhouse-server curlimages/curl 'http://clickhouse-server:8123/?query=' -s --data-binary @-
```

-e CLICKHOUSE_DB=my_database -e CLICKHOUSE_USER=username -e CLICKHOUSE_PASSWORD=password


elasticsearch
```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.11.1
docker run -p 9200:9200 -e "discovery.type=single-node" -e "ES_JAVA_OPTS=-Xms1024m -Xmx1024m" -e "xpack.security.enabled=false" elasticsearch:8.11.1
```