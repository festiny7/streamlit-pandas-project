import streamlit as st
import pandas as pd
from PIL import Image

#  - - - - - HIDE STREAMLIT THINGS - - - - -
def hide_smt():
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility : hidden;}
                </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)


def icon():
    icon = r"C:\Users\charl\Desktop\github\streamlit\images\icon.png"
    icon = Image.open(icon)

    return icon


def logo():
    logo = r"C:\Users\charl\Desktop\github\streamlit\images\pa-logo.png"
    logo = Image.open(logo)

    return logo
