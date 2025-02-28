import streamlit as st
from util import logo

with st.sidebar:
    logo()

def add_feature(text, description, align):

    st.markdown(
        f'<div style="text-align: {align};">'
        f'<h1 style="color:#0096FF;font-size: 28px;">{text}</h1>'
        , unsafe_allow_html=True
    )

    st.markdown(
        f'<div style="text-align: {align};">'
        f'<h6 style="color:white;font-size: 18px;">{description}</h6>'
        , unsafe_allow_html=True
    )

    st.markdown('<h1 style="color:white;font-size: 10px;"> </h1>', unsafe_allow_html=True)

add_feature('Personalized Course Recommendations', 'Get AI-driven course suggestions tailored to your skill level—beginner, intermediate, or advanced—ensuring efficient learning and career growth.', 'left')

add_feature('Mentor Matching Based on Your Needs', 'Connect with experienced mentors who align with your career goals, industry, and learning objectives for personalized guidance.', 'right')

add_feature('Comprehensive CV Analysis for Career Growth', 'Identify missing skills and optimize your resume based on industry trends, making you a stronger candidate for your desired roles.', 'left')