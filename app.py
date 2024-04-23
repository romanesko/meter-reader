from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

st.header("Показания")

tab1, tab2 = st.tabs(["Ввод показаний", "Статистика"])

with tab1:
    st.date_input("Дата", value=datetime.now())
    st.number_input("Хладоустановка", value=None, step=1)
    st.number_input("Газ", value=None, step=1)
    st.number_input("ВРУ", value=None, step=1)
    st.number_input("Большая вентиляция", value=None, step=1)
    st.number_input("ХВС", value=None, step=1)
    st.number_input("Водоподготовка", value=None, step=1)

with tab2:
    st.date_input("Дата от", value=None)
    st.date_input("Дата до", value=datetime.now())
    st.selectbox("Тип показаний",
                 options=["Хладоустановка", "Газ", "ВРУ", "Большая вентиляция", "ХВС", "Водоподготовка"])
    chart_data = pd.DataFrame(np.random.randn(20, 1), columns=["a"])

    st.line_chart(chart_data)
