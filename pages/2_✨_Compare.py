import streamlit as st
import pandas as pd
import plotly_express as px
import mymodules

st.set_page_config(
    page_title="Bar Chart Comparison", layout="wide", initial_sidebar_state="collapsed"
)

header = st.container()
with header:
    st.markdown("## Compare the providers\n\n ----", unsafe_allow_html=True)

mymodules.hide_smt()


#  - - - - - SIDEBAR - - - - -
with st.sidebar:
    st.text("Upload your file.")
    uploaded_file = st.file_uploader("Choose a CSV file.", type=["csv"])

    charge_number_input = st.number_input(
        "Charge",
        help="For example if you type 1, the orders with more than $1 will appear.",
    )
    link_text_input = st.text_input(
        "Link",
        help="You can write the link of the order. This filter doesn't combine with the others.\n\nSo an order that is not in the user filter may also appear.",
    )
    logo = st.image(mymodules.logo())

if uploaded_file is None:
    st.info(f"### You should upload a CSV file to compare providers.")
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    df["Service"] = df["Service"].str.slice(0, 25).apply(lambda x: x + "...")
    df["Orders Count"] = 1
    userList = list(df["User"].unique())
    col1, col2 = st.columns(2)

    comparisonType = st.radio(
        "Please choose the comparison type.", ("Graph", "Table"), horizontal=True
    )
    comparison1, comparison2 = st.columns(2)

    with comparison1:
        option = st.selectbox(
            label="Select the provider",
            options=userList,
        )
        if comparisonType == "Graph":
            dff2 = list(
                df[df["User"] == f"{option}"].groupby("Service").sum()["Charge"]
            )
            servis_listesi2 = list(df.loc[df["User"] == f"{option}"].Service.unique())
            quantity_listesi = list(
                df[df["User"] == f"{option}"].groupby("Service").sum()["Quantity"]
            )
            fig = px.bar(
                x=servis_listesi2,
                y=dff2,
                labels={"x": "Service", "y": "Charge"},
                title=option,
                text_auto=".3s",
            )
            st.write(fig)
        elif comparisonType == "Table":
            dff2 = (
                df.loc[df["User"] == f"{option}"]
                .groupby("Service")
                .sum()[["Charge", "Quantity", "Orders Count"]]
            )
            st.table(dff2)
    with comparison2:
        option = st.selectbox(
            label="Select the providers",
            options=userList,
        )
        if comparisonType == "Graph":
            dff2 = list(
                df[df["User"] == f"{option}"].groupby("Service").sum()["Charge"]
            )
            servis_listesi2 = list(df.loc[df["User"] == f"{option}"].Service.unique())
            fig = px.bar(
                x=servis_listesi2,
                y=dff2,
                labels={"x": "Service", "y": "Charge"},
                title=option,
                text_auto=".3s",
            )
            st.write(fig)
        elif comparisonType == "Table":
            dff2 = (
                df.loc[df["User"] == f"{option}"]
                .groupby("Service")
                .sum()[["Charge", "Quantity", "Orders Count"]]
            )
            st.table(dff2)
