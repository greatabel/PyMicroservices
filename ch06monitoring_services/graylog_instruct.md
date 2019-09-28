最好使用docker-compose 使用我这个file，而不要用官方的：官方的太慢了

http://docs.graylog.org/en/latest/pages/installation/docker.html

<!-- docker pull graylog
docker pull mongo
docker pull elasticsearch

docker run --name mongo -d mongo:latestx
docker run --name elasticsearch     -e "http.host=0.0.0.0"     -e "ES_JAVA_OPTS=-Xms512m -Xmx512m"     -d elasticsearch:latest


docker run --name graylog --link mongo --link elasticsearch     -p 9000:9000 -p 12201:12201 -p 1514:1514     -e GRAYLOG_HTTP_EXTERNAL_URI="http://127.0.0.1:9000/"     -d graylog/graylog:latest
 -->