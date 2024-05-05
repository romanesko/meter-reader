# Сбор показаний счётчиков
<img src="https://github.com/romanesko/meter-reader/assets/1404610/6a80d82d-c4dd-424b-a98b-6e742291b6ec" alt="1" border="0" width="400"><img src="https://github.com/romanesko/meter-reader/assets/1404610/f1141b50-f84e-4350-9806-46c1d7cd4b95" alt="2" border="0" width="400">


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
