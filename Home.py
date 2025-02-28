import streamlit as st
from util import logo

# Sidebar for assessment info
with st.sidebar:
    logo()
    st.markdown('<p style="color:white;">This tool helps you identify your skill level and recommends LinkedIn Learning courses based on your assessment.</p>', unsafe_allow_html=True)

import streamlit as st

st.markdown(
    '<h1 style="color:white;font-size: 70px; display:inline;">Unlock Your </h1>'
    '<h1 style="color:white; font-size: 70px; background: -webkit-linear-gradient(#0084ff, #00fbff); '
    '-webkit-background-clip: text; -webkit-text-fill-color: transparent; display:inline;">Potential.</h1>',
    unsafe_allow_html=True
)

st.markdown('<h1 style="color:white;font-size: 1px;"> </h1>', unsafe_allow_html=True)

st.markdown(
    '<div style="text-align: right;">'
    '<h1 style="color:white; font-size: 70px; background: -webkit-linear-gradient(#0084ff, #00fbff);'
    '-webkit-background-clip: text; -webkit-text-fill-color: transparent; display:inline;">link.ai</h1>'
    '<h1 style="color:white;font-size: 50px;">where your career meets smarter growth.</h1>'
    , unsafe_allow_html=True)
