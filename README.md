# Сбор показаний счётчиков
<img src="https://private-user-images.githubusercontent.com/1404610/325642641-5a44a0ca-1357-4d03-b0b2-1b7d5c85f4e5.jpg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTQ3MjM2MzcsIm5iZiI6MTcxNDcyMzMzNywicGF0aCI6Ii8xNDA0NjEwLzMyNTY0MjY0MS01YTQ0YTBjYS0xMzU3LTRkMDMtYjBiMi0xYjdkNWM4NWY0ZTUuanBnP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI0MDUwMyUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDA1MDNUMDgwMjE3WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9OWU1Mjc5MWQ3ZmIwZDUwNzU3NjIwMWFjZjZiODk4ZDcxMTVjMjE0NDA2NTdhMWFkN2NmNDAwYTZjZmNiYjRjMiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmYWN0b3JfaWQ9MCZrZXlfaWQ9MCZyZXBvX2lkPTAifQ.G4MCHnjJufULPeTuHsLoGxfq09B6VeFjVk0TymsVfbA" alt="1" border="0" width="500"><img src="https://private-user-images.githubusercontent.com/1404610/325642649-9efe7f83-0dd4-44fe-9189-feba397896a0.jpg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTQ3MjM2MzcsIm5iZiI6MTcxNDcyMzMzNywicGF0aCI6Ii8xNDA0NjEwLzMyNTY0MjY0OS05ZWZlN2Y4My0wZGQ0LTQ0ZmUtOTE4OS1mZWJhMzk3ODk2YTAuanBnP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI0MDUwMyUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDA1MDNUMDgwMjE3WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ZWViYjU3ODBhZjdlNmI5MGE2NDkwYjM2OGI2MTlhNzU4ZWU0ZjgzMWY0MjYwMTNjNjdhNDI5ODJmYmQzYjM1NiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmYWN0b3JfaWQ9MCZrZXlfaWQ9MCZyZXBvX2lkPTAifQ.aViFbVsjxEkC8BnFPq-UA0RIZmmSCY4INMcJGJ-Ia5M" alt="2" border="0" width="500">


## Подготовка к запуску

Подготовить таблицы в базе

```sql
create schema meter;

create table meter.users (
    id serial primary key,
    name text not null ,
    login text not null,
    password text not null,
    token text not null);

alter table meter.users owner to meter;

create table meter.desc(  
    id bigserial primary key,  
    key text not null,  
    title text not null  
);  

alter table meter.desc owner to meter;
  
create table meter.values(  
    id bigserial primary key ,  
    date date not null ,  
    type_id bigint references meter.desc,  
    val int not null,  
    created_at timestamp not null  default now(),
    created_by int not null references meter.users(id)
);  
  
alter table meter.values owner to meter;

insert into meter.desc(key, title) values  
    ('cooling','Хладоустановка'),  
    ('gas','Газ'),  
    ('vru','ВРУ'),  
    ('big_vent','Большая вентиляция'),  
    ('cold_water','ХВС'),  
    ('water_treatment','Водоподготовка');



GRANT ALL ON SCHEMA meter TO meter;  
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA meter TO meter;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA meter TO meter;

insert into meter.users(name, login, password, token) values('Admin','admin','--admin-pass--','--any-random-string--');
```

### Запуск через докер

понадобится файл `secrets.toml` с содержимым:

```toml
[connections.docker]
dialect = "postgresql"
host = "host.docker.internal"
port = "5432"
database = "meter"
username = "meter"
password = ""
```

`Makefile` для запуска:
```Makefile
run:
        @docker run -it --rm --name=meter --pull=always -v $(PWD)/secrets.toml:/app/.streamlit/secrets.toml -p 8501:8501 savarez/meter-reader
start:
        @docker run -d --rm --name=meter --pull=always -v $(PWD)/secrets.toml:/app/.streamlit/secrets.toml -p 8501:8501 savarez/meter-reader
stop:
        @docker stop meter
```

### Локальынй запуск
понадобится файл `secrets.toml` с содержимым:

```toml
[connections.local]
dialect = "postgresql"
host = "localhost"
port = "5432"
database = "meter"
username = "meter"
password = ""
```


Запуск:
```bash
pip install -r requirements.txt
cd src
PROFILE=local streamlit run app.py
```
