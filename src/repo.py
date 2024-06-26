import datetime
import random
import string
from typing import List

import streamlit as st
from sqlalchemy import text

from models import Counter, Stat, User

conn = st.connection("env:PROFILE", type="sql")


def get_fields_description() -> List[Counter]:
    out = []
    for i in conn.query(
            'select d.id, d.key, d.title, coalesce(sum(v.val),0) as max_val from meter.desc d left join meter.values v on v.type_id = d.id group by d.id;',
            ttl=1).itertuples():
        out.append(Counter(i.id, i.key, i.title, i.max_val, None))
    return out


def save_values(*, date, items: List[Counter], user):
    ins_data = [{"date": date, "type_id": i.id, "val": i.value, "created_by": user.id} for i in items]

    with conn.session as session:
        for d in ins_data:
            query = f"""INSERT INTO meter.values ("date","type_id","val", "created_by") VALUES (:date,:type_id,:val, :created_by);"""
            session.execute(text(query), d)
        session.commit()


def check_date_exists(d) -> bool:
    return \
        conn.query('''select exists(select 1 from meter.values where date = :d limit 1)''', ttl=0, params={'d': d}).get(
            'exists').iloc[0]


def get_stat(key: str, min_date, max_date):
    query = '''select a.id,a.key,a.title, coalesce(a.min,0) as min, coalesce(a.max,0) as max, coalesce((SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY val) AS median FROM meter.values where type_id = a.id
and date between :min_date and :max_date),0) as median from (
select d.id, d.key, d.title, min(v.val), max(v.val)  from meter.desc d left join meter.values v on v.type_id = d.id and v.date between :min_date and :max_date where d.key = :key group by d.id) a;
'''
    out = 0
    for i in conn.query(query, ttl=0, params={'key': key, 'min_date': min_date, 'max_date': max_date}).itertuples():
        out = Stat(i.id, i.key, i.title, i.min, i.max, i.median)
    return out


def get_graph(id: int, min_date, max_date):
    query = '''select date, val from meter.values where type_id = :id and date between :min_date and :max_date order by date;'''
    return conn.query(query, ttl=0, params={'id': id, 'min_date': min_date, 'max_date': max_date}).set_index('date')


def set_random(id: int, min_date: datetime.date, random_numbers):
    with conn.session as session:
        for i in random_numbers:
            query = f"""INSERT INTO meter.values ("date","type_id","val","created_by") VALUES (:date,:type_id,:val, 1);"""
            session.execute(text(query), {"date": min_date, "type_id": id, "val": i})
            min_date += datetime.timedelta(days=1)
        session.commit()


def __generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def auth(login, password):
    res = conn.query("select * from meter.users where login = :login and password=:password",
                     params={'login': login, 'password': password}, ttl=0).get('id')
    if not res.empty:
        id = int(res.iloc[0])
        token = __generate_random_string(128)
        with conn.session as session:
            session.execute(text("update meter.users set token = :token where id = :id"), {'token': token, 'id': id})
            session.commit()

        return token
    return None


@st.cache_data(ttl=60)
def get_user_by_token(token):
    if token is None:
        return None

    res = conn.query("select id,name from meter.users where token = :token", params={'token': token}, ttl=0)

    if not res.empty:
        row = res.iloc[0]
        user = User(int(row['id']), str(row['name']))
        return user
    else:
        print('No user found for token', token)

    return None
