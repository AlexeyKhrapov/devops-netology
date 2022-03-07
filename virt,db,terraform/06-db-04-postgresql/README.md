# 6.4. PostgreSQL — Алексей Храпов

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.

Подключитесь к БД PostgreSQL используя `psql`.

Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.

**Найдите и приведите** управляющие команды для:
- вывода списка БД
- подключения к БД
- вывода списка таблиц
- вывода описания содержимого таблиц
- выхода из psql

### Ответ:

- Вывод списка БД:
```bash
postgres=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
(3 rows)
```
- Подключение к БД:
```bash
postgres=# \c postgres
Password: 
You are now connected to database "postgres" as user "postgres".
```
- Вывод списка таблиц:
```bash
postgres=# \dt
Did not find any relations.
postgres=# \dtS
                    List of relations
   Schema   |          Name           | Type  |  Owner   
------------+-------------------------+-------+----------
 pg_catalog | pg_aggregate            | table | postgres
 pg_catalog | pg_am                   | table | postgres
 pg_catalog | pg_amop                 | table | postgres
 pg_catalog | pg_amproc               | table | postgres
 ...
```
- Вывод описания содержимого таблиц (\d[S+] NAME):
```bash
postgres=# \dS+ pg_am
                                  Table "pg_catalog.pg_am"
  Column   |  Type   | Collation | Nullable | Default | Storage | Stats target | Description 
-----------+---------+-----------+----------+---------+---------+--------------+-------------
 oid       | oid     |           | not null |         | plain   |              | 
 amname    | name    |           | not null |         | plain   |              | 
 amhandler | regproc |           | not null |         | plain   |              | 
 amtype    | "char"  |           | not null |         | plain   |              | 
Indexes:
    "pg_am_name_index" UNIQUE, btree (amname)
    "pg_am_oid_index" UNIQUE, btree (oid)
Access method: heap
```
- Выход:
```bash
postgres=# \q
```

---

## Задача 2

Используя `psql` создайте БД `test_database`.

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-04-postgresql/test_data).

Восстановите бэкап БД в `test_database`.

Перейдите в управляющую консоль `psql` внутри контейнера.

Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.

Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats), найдите столбец таблицы `orders` 
с наибольшим средним значением размера элементов в байтах.

**Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.

### Ответ:

```bash
postgres=# CREATE DATABASE test_database;
CREATE DATABASE
postgres=# \q
root@f1c1f82f2810:/# cd /var/lib/postgresql/data/
root@f1c1f82f2810:/var/lib/postgresql/data# psql -U postgres -f ./test_dump.sql test_database
SET
SET
SET
SET
SET
 set_config 
------------
 
(1 row)

SET
SET
SET
SET
SET
SET
CREATE TABLE
ALTER TABLE
CREATE SEQUENCE
ALTER TABLE
ALTER SEQUENCE
ALTER TABLE
COPY 8
 setval 
--------
      8
(1 row)

ALTER TABLE
root@f1c1f82f2810:/var/lib/postgresql/data# psql -U postgres
psql (13.6 (Debian 13.6-1.pgdg110+1))
Type "help" for help.

postgres=# \c test_database 
You are now connected to database "test_database" as user "postgres".
test_database=# ANALYZE VERBOSE public.orders;
INFO:  analyzing "public.orders"
INFO:  "orders": scanned 1 of 1 pages, containing 8 live rows and 0 dead rows; 8 rows in sample, 8 estimated total rows
ANALYZE
test_database=# SELECT avg_width FROM pg_stats WHERE tablename='orders';
 avg_width 
-----------
         4
        16
         4
(3 rows)
```

---


## Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

Предложите SQL-транзакцию для проведения данной операции.

Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?

### Ответ:

```bash
test_database=# alter table orders rename to orders_simple;
ALTER TABLE
test_database=# create table orders (id integer, title varchar(80), price integer) partition by range(price);
CREATE TABLE
test_database=# create table orders_2 partition of orders for values from (0) to (499);
CREATE TABLE
test_database=# create table orders_1 partition of orders for values from (499) to (999999999);
CREATE TABLE
test_database=# insert into orders (id, title, price) select * from orders_simple;
INSERT 0 8
```
При начальном проектировании таблиц можно было сделать таблицу orders секционированной, 
тогда не пришлось бы переименовывать исходную таблицу и переносить данные в новую.

---

## Задача 4

Используя утилиту `pg_dump` создайте бекап БД `test_database`.

Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?

### Ответ:

```bash
root@f1c1f82f2810:/# pg_dump -U postgres -d test_database >test_database_dump.sql
```
Чтобы добавить уникальности значению столбца `title` таблиц `test_database`, 
можно, например, добавить первичный ключ или создать индекс: `CREATE INDEX ON orders ((lower(title)));`.
Также можно добавить ограничение уникальности: 
```bash
ALTER TABLE ONLY orders_1 ADD UNIQUE (title);
ALTER TABLE ONLY orders_2 ADD UNIQUE (title);
```
Для обеспечения полной уникальности столбца `title` стоило бы установить ограничения до шардирования.
Во всяком случае мне не удалось реализовать это ограничение только по одному столбцу после разбиения.