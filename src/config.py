import streamlit as st


def set_config():
    st.set_page_config(
        page_title="Счетчики",
        initial_sidebar_state='collapsed'
    )
    st.markdown("""
    <style>

    .block-container
    {
        padding-top: 1rem;
        padding-bottom: 1rem;
        margin-top: 1rem;
    }
    
    h2 {padding-top:0}
    header {display:none!important}

    </style>
    """, unsafe_allow_html=True)
