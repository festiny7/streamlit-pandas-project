import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import streamlit as st
from streamlit_lottie import st_lottie
import mymodules


#  - - - - - LOGO AND ICON - - - - -
icon = mymodules.icon()
st.set_page_config(page_title="Perfect Analysis Web App", page_icon=icon, layout="wide")


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


#  - - - - - CONTAINERS - - - - -
header = st.container()
empty_first_look = st.container()  # Lottie animations here
first_look = st.container()  # All data shows, Header's first container

#  - - - - - CACHES - - - - -


@st.cache(suppress_st_warning=True)
def welcome():
    a = st.title("Welcome to Perfect Analysis!")
    # st.title("Welcome to Perfect Analysis!")
    # return a


@st.cache(suppress_st_warning=True)
def hcol_markdown():
    a = st.markdown("You can analysis your SMM Panel orders data.")


@st.cache(suppress_st_warning=True)
def hcol_markdown2():
    a = st.markdown("Get in touch with us at **perfectanalysis@gmail.com**")


@st.cache(suppress_st_warning=True)
def hcol_markdown3():
    a = header_markdown.markdown("""---""")


#  - - - - - LOGO AND ICON - - - - -
with header:
    header_empty_container = st.empty()
    header_empty = st.empty()
    with header_empty_container.container():
        welcome()
    h_col1, h_col2 = header_empty.columns(2)
    with h_col1:
        hcol_markdown()  # 🔎
    with h_col2:
        hcol_markdown2()  # 📮
    header_markdown = st.empty()
    hcol_markdown3()


#  - - - - - LOTTIE  - - - - -
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_data = load_lottieurl(
    "https://assets3.lottiefiles.com/packages/lf20_2UeWRZ.json"
)

#  - - - - - EMPTY FIRST LOOK CONTAINER - - - - -
with empty_first_look:
    empty_holder = st.empty()
    empty_holder.subheader("Your dataset will be here...")
    lottie_empty = st.empty()
    with lottie_empty.container():
        st_lottie(
            lottie_data,
            speed=1,
            loop=True,
            quality="low",
            height=500,
            width=500,
            key="data",
        )


#  - - - - - FIRST LOOK CONTAINER - - - - -

with first_look:
    if uploaded_file is not None:
        empty_holder.empty()
        lottie_empty.empty()
        header_empty_container.empty()
        header_empty.empty()
        header_markdown.empty()

        df = pd.read_csv(uploaded_file)

        df["Date"] = pd.to_datetime(df.Created, format="%Y-%m-%d")
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

        st.markdown(f"## Your {uploaded_file.name} data is here...")
        st.markdown("")

        fl_col1, fl_col2, fl_col3 = st.columns(3)

        fl_col1_total_charge = 0
        for i in df["Charge"]:
            fl_col1_total_charge += i

        with st.container():

            df_all_data = df

            if min(df_all_data["Date"]) != max(df_all_data["Date"]):
                first_date1, second_date1 = st.select_slider(
                    "Filter Date",
                    options=df_all_data["Date"].unique(),
                    value=(min(df_all_data["Date"]), max(df_all_data["Date"])),
                )
                dataQuery = "User == @provider & Charge >= @charge_number_input & @first_date1 <= Date <= @second_date1"  # & Link == @link_text_input"
            else:
                dataQuery = "User == @provider & Charge >= @charge_number_input"

            provider = st.multiselect(
                "Select the provider(s)",
                help="If you want, you can add/drop the providers.",
                options=df_all_data["User"].unique(),
                default=df_all_data["User"].unique(),
            )

            df_all_data_selection = df_all_data.query(dataQuery)

            if link_text_input:
                df_all_data_selection = df_all_data.query("Link == @link_text_input")

            fl_col4, fl_col5, fl_col6 = st.columns(3)

            # SESSION STATE FOR TOTAL CHARGE
            if "total_charge" not in st.session_state:
                st.session_state.total_charge = 0
            total_charge_session = 0
            for i in df_all_data_selection["Charge"]:
                total_charge_session += i

            # Custom CSS Hack for --> fl_col4.metric
            st.write(
                """
                <style>
                [data-testid="stMetricDelta"] svg {
                    display: none;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            ## EQUATE THE VARIABLE WITH THE TOTAL CHARGE
            st.session_state.total_charge = total_charge_session
            fl_col1.metric(
                label="💲 Total Charge",
                value=f"US $ {int(st.session_state.total_charge)}",
                delta=f"% {int((int(st.session_state.total_charge) / int(df.Charge.sum()))*100)}",
                help="The percentage is according to total charge.",
            )

            # SESSION STATE FOR NUMBER OF ORDERS
            if "number_of_orders" not in st.session_state:
                st.session_state.number_of_orders = 0
            numberOf_orders = df_all_data_selection.count()["ID"]
            st.session_state.number_of_orders = numberOf_orders

            fl_col2.metric(
                label="🎲 Number of Orders",
                value=f" {st.session_state.number_of_orders}",
                delta=f"% {int((int(st.session_state.number_of_orders) / int(df.count()['ID']))*100)}",
                help="The percentage is according to total orders count.",
            )
            try:
                averageOrder_charge = float(st.session_state.total_charge) / int(
                    st.session_state.number_of_orders
                )
                fl_col3.metric(
                    label="⭐ Average Order Charge",
                    value="US $ %.2f" % averageOrder_charge,
                )
                df_all_data_selection.index = np.arange(
                    1, len(df_all_data_selection) + 1
                )
                st.dataframe(df_all_data_selection)
                with st.expander("See the features of the table above."):
                    st.info(
                        "• You can resize the table at the right bottom of the table.\n\n• You can click the columns (Charge, Cost or Quantity) to sorting data."
                    )
            except Exception as e:
                st.info("Please control your filters.")

        st.markdown("---")

        # GROUP BY PROVIDERS AND SERVICES

        st.markdown("## Group by Providers and Services")
        df_gps = df
        df_gps_chart = df
        df_gps = df_gps.drop(
            ["ID", "External ID", "Start count", "Remains", "Service ID"], axis=1
        )
        df_gps = df_gps.groupby(["User", "Service"]).sum()
        st.dataframe(df_gps)
        st.bar_chart(df_gps_chart.groupby("Service").sum()["Charge"])

        st.markdown("---")

        # GROUP BY PROVIDERS
        st.markdown("## Group by Providers")
        gbp_tab1, gbp_tab2 = st.tabs(["Data Table", "Bar Chart Graphic"])
        df_gbp = df
        df_gbp = df_gbp.drop(
            ["ID", "External ID", "Start count", "Remains", "Service ID"], axis=1
        )
        df_gbp = df_gbp.groupby("User").sum().sort_values("Charge", ascending=False)
        with gbp_tab1:
            st.text(
                "You can click the columns (Charge, Cost or Quantity) to sorting data."
            )
            st.dataframe(df_gbp)
        with gbp_tab2:
            st.bar_chart(df_gbp.groupby("User").sum()["Charge"])
