from datetime import datetime
from typing import List

import pandas as pd
import streamlit as st

from config import set_config
from models import Counter

set_config()
import auth
import repo

auth.check_login()

st.header("Ввод показаний счетчиков")

tab1, tab2 = st.tabs(["Ввод показаний", "Статистика"])

try:
    data: List[Counter] = repo.get_fields_description()
except Exception as e:
    st.error(str(e))
    st.stop()


def validate_form(data: List[Counter]):
    if repo.check_date_exists(st.session_state.get("date")):
        raise ValueError("Показания за эту дату уже введены")

    for item in data:
        if not item.value:
            raise ValueError(f"{item.title}: показания не введены")
        try:
            item.value = int(item.value)
        except Exception:
            raise ValueError(f"{item.title}: показания  должны быть числом")

        if item.max_val and item.value < item.max_val:
            raise ValueError(f"{item.title}: новые показания не могут быть меньше предыдущих")


def save_values(data: List[Counter]):
    for item in data:
        if item.max_val:
            item.value = item.value - item.max_val
    date = st.session_state.get("date")
    repo.save_values(date, data)


form_ready = True


def before_submit():
    st.session_state.error = None
    #
    hash = {}
    for field in [f for f in st.session_state if f.startswith('form.')]:
        hash[field.split('.')[1]] = st.session_state[field]

    for idx, item in enumerate(data):
        item.value = hash[item.key]
        data[idx] = item

    try:
        validate_form(data)
        save_values(data)

        for item in st.session_state:
            if item.startswith('form.'):
                st.session_state[item] = ''

    except Exception as e:

        st.session_state.error = e
        return


with tab1:
    submitted = False

    with st.form(key="form"):
        st.date_input("Дата", value=datetime.now(), key="date")
        cols = st.columns(2)
        for i, val in enumerate(data):
            val.new_val = cols[i % 2].text_input(val.title, placeholder=val.max_val, value=val.value,
                                                 key='form.' + val.key)

        submitted = st.form_submit_button("Сохранить", on_click=before_submit)

    if submitted:

        if st.session_state.get('error'):
            st.error(st.session_state.error)
        else:
            st.success("Показания сохранены")


def debug_generate_random_data():
    import lib
    x = lib.generate_random_numbers(730, 5, 15, [1.2, 0.7, 1.2, 1.5, 1.2, 1, 0.8, 1.2])
    repo.set_random(selected_type.id, datetime.now() - pd.Timedelta(days=730), x)


with tab2:
    min_date = st.date_input("Дата от", value=datetime.now() - pd.Timedelta(days=30))
    max_date = st.date_input("Дата до", value=datetime.now())

    hm = {d.title: d for d in data}

    selected_type_title = st.selectbox("Тип показаний", options=hm.keys())

    if selected_type_title:
        selected_type = hm[selected_type_title]

        chart_data = repo.get_graph(selected_type.id, min_date, max_date)

        if len(chart_data):
            st.line_chart(chart_data)

        stat_all = repo.get_stat(selected_type.key, '2021-01-01', '2121-12-31')
        if stat_all.max_val:
            stat_interval = repo.get_stat(selected_type.key, min_date, max_date)
            col1, col2 = st.columns([1, 1], gap="medium")

            col1.dataframe(
                chart_data.style.highlight_max(axis=0, color='#FF000010').highlight_min(axis=0, color='#0000FF10'),
                use_container_width=True,
                height=200)

            col2.subheader("Статистика")
            col2.caption("В сравнении с историей всех измерений")

            sc1, sc2, sc3 = col2.columns(3, gap="small")

            min_diff = stat_interval.min_val - stat_all.min_val
            med_diff = stat_interval.median - stat_all.median
            max_diff = stat_interval.max_val - stat_all.max_val

            sc1.metric("Минимум", stat_interval.min_val, min_diff if min_diff > 0 else '')
            sc2.metric("Среднее", stat_interval.median, med_diff if med_diff > 0 else '')
            sc3.metric("Максимум", stat_interval.max_val, max_diff if max_diff > 0 else '')

    if st.query_params.get("debug"):
        if st.button("Сгенерировать", on_click=debug_generate_random_data):
            st.rerun()
