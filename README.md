# Сбор показаний счётчиков

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
[connections.docker]
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