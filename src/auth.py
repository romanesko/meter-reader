import datetime
from time import sleep

import extra_streamlit_components as stx
import streamlit as st

import repo

cookie_manager = stx.CookieManager()


def login():
    token = repo.auth(st.session_state.login, st.session_state.password)
    if token:
        cookie_manager.set('token', token, expires_at=datetime.datetime.now() + datetime.timedelta(days=30),
                           max_age=60 * 60 * 24 * 30)
        st.rerun()


def check_login():
    token = cookie_manager.get('token')
    user = repo.get_user_by_token(token)
    if not token or not user:
        st.text_input('Login', key='login')
        st.text_input('Password', type='password', key='password')
        if st.button('Login', on_click=login):
            st.error('Invalid login or password')
        st.stop()
    with st.sidebar:
        st.write(user.name)
        if st.button('Logout'):
            logout()
    return user


def logout():
    cookie_manager.delete('token')
    sleep(1)
    st.rerun()
