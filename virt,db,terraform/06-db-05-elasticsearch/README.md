# 6.5. Elasticsearch — Алексей Храпов

## Задача 1

В этом задании вы потренируетесь в:
- установке elasticsearch
- первоначальном конфигурировании elastcisearch
- запуске elasticsearch в docker

Используя докер образ [centos:7](https://hub.docker.com/_/centos) как базовый и 
[документацию по установке и запуску Elastcisearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html):

- составьте Dockerfile-манифест для elasticsearch
- соберите docker-образ и сделайте `push` в ваш docker.io репозиторий
- запустите контейнер из получившегося образа и выполните запрос пути `/` c хост-машины

Требования к `elasticsearch.yml`:
- данные `path` должны сохраняться в `/var/lib`
- имя ноды должно быть `netology_test`

В ответе приведите:
- текст Dockerfile манифеста
- ссылку на образ в репозитории dockerhub
- ответ `elasticsearch` на запрос пути `/` в json виде

Подсказки:
- возможно вам понадобится установка пакета perl-Digest-SHA для корректной работы пакета shasum
- при сетевых проблемах внимательно изучите кластерные и сетевые настройки в elasticsearch.yml
- при некоторых проблемах вам поможет docker директива ulimit
- elasticsearch в логах обычно описывает проблему и пути ее решения

Далее мы будем работать с данным экземпляром elasticsearch.

### Ответ:

Dockerfile:
```bash
#Elasticsearch
FROM centos:7
LABEL ElasticSearch 7.17.1\
    (c)Alexey Khrapov

ENV PATH=/usr/lib:/usr/lib/jvm/jre-11/bin:$PATH

RUN yum install java-11-openjdk wget perl-Digest-SHA -y 

RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.1-linux-x86_64.tar.gz \
    && wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.1-linux-x86_64.tar.gz.sha512 \
    && shasum -a 512 -c elasticsearch-7.17.1-linux-x86_64.tar.gz.sha512 \ 
    && tar -xzf elasticsearch-7.17.1-linux-x86_64.tar.gz \
    && yum upgrade -y
    
ADD elasticsearch.yml /elasticsearch-7.17.1/config/
ENV JAVA_HOME=/elasticsearch-7.17.1/jdk/
ENV ES_HOME=/elasticsearch-7.17.1
RUN groupadd elasticsearch \
    && useradd -g elasticsearch elasticsearch
    
RUN mkdir /var/lib/logs \
    && chown elasticsearch:elasticsearch /var/lib/logs \
    && mkdir /var/lib/data \
    && chown elasticsearch:elasticsearch /var/lib/data \
    && chown -R elasticsearch:elasticsearch /elasticsearch-7.17.1/
RUN mkdir /elasticsearch-7.17.1/snapshots &&\
    chown elasticsearch:elasticsearch /elasticsearch-7.17.1/snapshots
    
USER elasticsearch
CMD ["/usr/sbin/init"]
CMD ["/elasticsearch-7.17.1/bin/elasticsearch"]
```
Ссылка на репозиторий: https://hub.docker.com/r/ahr22/elasticsearch

Ответ на запрос:
```bash
kad@g-deb-test:~/elastic$ curl -X GET 'http://localhost:9200'
{
  "name" : "454d0ccfdfae",
  "cluster_name" : "netology_test",
  "cluster_uuid" : "OB2jcjTERt2Ym9Z0BgTf4A",
  "version" : {
    "number" : "7.17.1",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "e5acb99f822233d62d6444ce45a4543dc1c8059a",
    "build_date" : "2022-02-23T22:20:54.153567231Z",
    "build_snapshot" : false,
    "lucene_version" : "8.11.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

---

## Задача 2

В этом задании вы научитесь:
- создавать и удалять индексы
- изучать состояние кластера
- обосновывать причину деградации доступности данных

Ознакомтесь с [документацией](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) 
и добавьте в `elasticsearch` 3 индекса, в соответствии со таблицей:

| Имя | Количество реплик | Количество шард |
|-----|-------------------|-----------------|
| ind-1| 0 | 1 |
| ind-2 | 1 | 2 |
| ind-3 | 2 | 4 |

Получите список индексов и их статусов, используя API и **приведите в ответе** на задание.

Получите состояние кластера `elasticsearch`, используя API.

Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?

Удалите все индексы.

**Важно**

При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард,
иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.

### Ответ:

Добавление индексов:
```bash
kad@g-deb-test:~/elastic$ curl -X PUT localhost:9200/ind-1 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'
{"acknowledged":true,"shards_acknowledged":true,"index":"ind-1"}
kad@g-deb-test:~/elastic$ curl -X PUT localhost:9200/ind-2 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 2,  "number_of_replicas": 1 }}'
{"acknowledged":true,"shards_acknowledged":true,"index":"ind-2"}
kad@g-deb-test:~/elastic$ curl -X PUT localhost:9200/ind-3 -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 4,  "number_of_replicas": 2 }}'
{"acknowledged":true,"shards_acknowledged":true,"index":"ind-3"}
```
Список индексов:
```bash
kad@g-deb-test:~/elastic$ curl -X GET 'http://localhost:9200/_cat/indices?v'
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases osHCyOZCRPGW3Ps9XkpBNw   1   0         41            0     39.5mb         39.5mb
green  open   ind-1            R59xm-lNTsOdtQf_5eHAIA   1   0          0            0       226b           226b
yellow open   ind-3            5XpOt7ZKQrmB9qk1_mss5Q   4   2          0            0       904b           904b
yellow open   ind-2            1gg0WsDSQ0ej-6PqrRSJsQ   2   1          0            0       452b           452b
```
Статус индексов:
```bash
kad@g-deb-test:~/elastic$ curl -X GET 'http://localhost:9200/_cluster/health/ind-1?pretty'
{
  "cluster_name" : "netology_test",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 1,
  "active_shards" : 1,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}
kad@g-deb-test:~/elastic$ curl -X GET 'http://localhost:9200/_cluster/health/ind-2?pretty'
{
  "cluster_name" : "netology_test",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 2,
  "active_shards" : 2,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 2,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 50.0
}
kad@g-deb-test:~/elastic$ curl -X GET 'http://localhost:9200/_cluster/health/ind-3?pretty'
{
  "cluster_name" : "netology_test",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 4,
  "active_shards" : 4,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 8,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 50.0
}

```
Статус кластера:
```bash
kad@g-deb-test:~/elastic$ curl -XGET localhost:9200/_cluster/health/?pretty=true
{
  "cluster_name" : "netology_test",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 10,
  "active_shards" : 10,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 10,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 50.0
}
```
Удаление индексов:
```bash
kad@g-deb-test:~/elastic$ curl -X DELETE 'http://localhost:9200/ind-1?pretty'
{
  "acknowledged" : true
}
kad@g-deb-test:~/elastic$ curl -X DELETE 'http://localhost:9200/ind-2?pretty'
{
  "acknowledged" : true
}
kad@g-deb-test:~/elastic$ curl -X DELETE 'http://localhost:9200/ind-3?pretty'
{
  "acknowledged" : true
}
kad@g-deb-test:~/elastic$ curl -X GET 'http://localhost:9200/_cat/indices?v'
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases osHCyOZCRPGW3Ps9XkpBNw   1   0         41            0     39.5mb         39.5mb
```

Часть индексов и кластер находится в состоянии yellow потому, что у них указано число 
реплик, тогда как других серверов нет, соответсвено, реплицировать некуда.

---

## Задача 3

В данном задании вы научитесь:
- создавать бэкапы данных
- восстанавливать индексы из бэкапов

Создайте директорию `{путь до корневой директории с elasticsearch в образе}/snapshots`.

Используя API [зарегистрируйте](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#snapshots-register-repository) 
данную директорию как `snapshot repository` c именем `netology_backup`.

**Приведите в ответе** запрос API и результат вызова API для создания репозитория.

Создайте индекс `test` с 0 реплик и 1 шардом и **приведите в ответе** список индексов.

[Создайте `snapshot`](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html) 
состояния кластера `elasticsearch`.

**Приведите в ответе** список файлов в директории со `snapshot`ами.

Удалите индекс `test` и создайте индекс `test-2`. **Приведите в ответе** список индексов.

[Восстановите](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html) состояние
кластера `elasticsearch` из `snapshot`, созданного ранее. 

**Приведите в ответе** запрос к API восстановления и итоговый список индексов.

Подсказки:
- возможно вам понадобится доработать `elasticsearch.yml` в части директивы `path.repo` и перезапустить `elasticsearch`

### Ответ:

```bash
# 
kad@g-deb-test:~/elastic$ curl -XPOST localhost:9200/_snapshot/netology_backup?pretty -H 'Content-Type: application/json' -d'{"type": "fs", "settings": { "location":"/elasticsearch-7.17.1/snapshots" }}'
{
  "acknowledged" : true
}
kad@g-deb-test:~/elastic$ curl -X GET  'http://localhost:9200/_snapshot/netology_backup?pretty'
{
  "netology_backup" : {
    "type" : "fs",
    "settings" : {
      "location" : "/elasticsearch-7.17.1/snapshots"
    }
  }
}
kad@g-deb-test:~/elastic$ curl -X PUT localhost:9200/test -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'
{"acknowledged":true,"shards_acknowledged":true,"index":"test"}
kad@g-deb-test:~/elastic$ curl -X GET 'http://localhost:9200/test?pretty'
{
  "test" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "1",
        "provided_name" : "test",
        "creation_date" : "1646676513411",
        "number_of_replicas" : "0",
        "uuid" : "X1qwslmXQ6mhPexI0fFvEg",
        "version" : {
          "created" : "7170199"
        }
      }
    }
  }
}
kad@g-deb-test:~/elastic$ curl -X PUT localhost:9200/_snapshot/netology_backup/elasticsearch?wait_for_completion=true
{"snapshot":{"snapshot":"elasticsearch","uuid":"iu6ArqJzT5a1NPf3ZZsEGw","repository":"netology_backup","version_id":7170199,"version":"7.17.1","indices":[".ds-ilm-history-5-2022.03.07-000001",".ds-.logs-deprecation.elasticsearch-default-2022.03.07-000001",".geoip_databases","test"],"data_streams":["ilm-history-5",".logs-deprecation.elasticsearch-default"],"include_global_state":true,"state":"SUCCESS","start_time":"2022-03-07T18:12:31.938Z","start_time_in_millis":1646676751938,"end_time":"2022-03-07T18:12:33.138Z","end_time_in_millis":1646676753138,"duration_in_millis":1200,"failures":[],"shards":{"total":4,"failed":0,"successful":4},"feature_states":[{"feature_name":"geoip","indices":[".geoip_databases"]}]}}
kad@g-deb-test:~/elastic$ docker exec -ti elastic ls -la /elasticsearch-7.17.1/snapshots
total 60
drwxr-xr-x 1 elasticsearch elasticsearch  4096 Mar  7 18:12 .
drwxr-xr-x 1 elasticsearch elasticsearch  4096 Mar  7 17:18 ..
-rw-r--r-- 1 elasticsearch elasticsearch  1425 Mar  7 18:12 index-0
-rw-r--r-- 1 elasticsearch elasticsearch     8 Mar  7 18:12 index.latest
drwxr-xr-x 6 elasticsearch elasticsearch  4096 Mar  7 18:12 indices
-rw-r--r-- 1 elasticsearch elasticsearch 29303 Mar  7 18:12 meta-iu6ArqJzT5a1NPf3ZZsEGw.dat
-rw-r--r-- 1 elasticsearch elasticsearch   712 Mar  7 18:12 snap-iu6ArqJzT5a1NPf3ZZsEGw.dat
kad@g-deb-test:~/elastic$ curl -X GET 'http://localhost:9200/_cat/indices?v'
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases osHCyOZCRPGW3Ps9XkpBNw   1   0         41            0     39.5mb         39.5mb
green  open   test             X1qwslmXQ6mhPexI0fFvEg   1   0          0            0       226b           226b
kad@g-deb-test:~/elastic$ curl -X DELETE 'http://localhost:9200/test?pretty'
{
  "acknowledged" : true
}
kad@g-deb-test:~/elastic$ curl -X PUT localhost:9200/test-2?pretty -H 'Content-Type: application/json' -d'{ "settings": { "number_of_shards": 1,  "number_of_replicas": 0 }}'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test-2"
}
kad@g-deb-test:~/elastic$ curl -X GET 'http://localhost:9200/_cat/indices?v'
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases osHCyOZCRPGW3Ps9XkpBNw   1   0         41            0     39.5mb         39.5mb
green  open   test-2           amUysbiHQLaTBTgERhLUUg   1   0          0            0       226b           226b
kad@g-deb-test:~/elastic$ curl -X POST localhost:9200/_snapshot/netology_backup/elasticsearch/_restore?pretty -H 'Content-Type: application/json' -d'{"include_global_state":true,"rename_pattern":"(.+)","rename_replacement":"restored-$1"}'
{
  "accepted" : true
}
kad@g-deb-test:~/elastic$ curl -X GET 'http://localhost:9200/_cat/indices?v'
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases Mgx5s9NiTbuiKCAlp6WRiA   1   0         41            0     39.5mb         39.5mb
green  open   test-2           amUysbiHQLaTBTgERhLUUg   1   0          0            0       226b           226b
green  open   restored-test    h4zlYVUTTHqZFYbKVrKw4w   1   0          0            0       226b           226b
```

