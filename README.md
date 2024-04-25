# Сбор показаний счётчиков
<img src="https://private-user-images.githubusercontent.com/1404610/325642641-5a44a0ca-1357-4d03-b0b2-1b7d5c85f4e5.jpg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTQwNTQxNzksIm5iZiI6MTcxNDA1Mzg3OSwicGF0aCI6Ii8xNDA0NjEwLzMyNTY0MjY0MS01YTQ0YTBjYS0xMzU3LTRkMDMtYjBiMi0xYjdkNWM4NWY0ZTUuanBnP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI0MDQyNSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDA0MjVUMTQwNDM5WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ZjBmMWI3MDc3ZTRmYWY4ZmZhMWU4OTAzMWRhZTFhNjQzYjYyYTExYTQ2NTE3YjQ1NmY0MmQzYzZmNGNjODM4YSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmYWN0b3JfaWQ9MCZrZXlfaWQ9MCZyZXBvX2lkPTAifQ.8GoDQ5viAbuukZzhCT5pgbnDPXxjJKS_2MC_67zvbzU" width="500" /> <img src="https://private-user-images.githubusercontent.com/1404610/325642649-9efe7f83-0dd4-44fe-9189-feba397896a0.jpg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTQwNTQxNzksIm5iZiI6MTcxNDA1Mzg3OSwicGF0aCI6Ii8xNDA0NjEwLzMyNTY0MjY0OS05ZWZlN2Y4My0wZGQ0LTQ0ZmUtOTE4OS1mZWJhMzk3ODk2YTAuanBnP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI0MDQyNSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDA0MjVUMTQwNDM5WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9NjcwNWI1N2UwZWE5MGI0MDZmZTFhYmUzNThjZWMzMDhkYTcwNmZlMDE0YzlhY2ZlNjk0MDVlOWJmOWQ1OWVhNiZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmYWN0b3JfaWQ9MCZrZXlfaWQ9MCZyZXBvX2lkPTAifQ.gGzcNZgtrTyagvdu--GO-uI9K5uGB16wb8_KEPCEo5E" width="500" />



## Подготовка к запуску

Подготовить таблицы в базе

```sql
create schema meter;

create table meter.desc(  
    id bigserial primary key,  
    key text not null,  
    title text not null  
);  
  
create table meter.values(  
    id bigserial primary key ,  
    date date not null ,  
    type_id bigint references meter.desc,  
    val int not null,  
    created_at timestamp not null  default now()  
);  
  
insert into meter.desc(key, title) values  
    ('cooling','Хладоустановка'),  
    ('gas','Газ'),  
    ('vru','ВРУ'),  
    ('big_vent','Большая вентиляция'),  
    ('cold_water','ХВС'),  
    ('water_treatment','Водоподготовка');
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

Запуск в интерактивном режиме
```bash
docker run -it --rm -v $(PWD)/secrets.toml:/app/.streamlit/secrets.toml -p 8501:8501 savarez/meter-reader
```
Запуск в фоне
```bash
docker run -d -v $(PWD)/secrets.toml:/app/.streamlit/secrets.toml -p 8501:8501 savarez/meter-reader
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
