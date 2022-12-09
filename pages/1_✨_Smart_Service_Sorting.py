import streamlit as st
import pandas as pd
import mymodules

#  - - - - - LOGO AND ICON - - - - -
icon = mymodules.icon()
st.set_page_config(page_title="Perfect Analysis Web App", page_icon=icon, layout="wide")

mymodules.hide_smt()


#  - - - - - SIDEBAR - - - - -
with st.sidebar:
    # st.markdown("""---""")
    st.text("Upload your file.")
    uploaded_file = st.file_uploader("Choose a CSV file.", type=["csv"])


st.title("Smart Service Analysing")
st.markdown("---")


def convert_csv(df):
    return df.to_csv().encode("utf-8")


if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    with st.container():
        st.subheader(f"Your '{uploaded_file.name}' Dataset")
        df = df[df["Status"].str.contains("Cancel") == False]
        df_smart_service = df
        df_smart_service["Service"] = (
            df_smart_service["Service"].str.slice(0, 50).apply(lambda x: x + "...")
        )
        df_smart_service["Orders Count"] = 1
        df_smart_service_groupby = df_smart_service.groupby(
            ["Service ID", "Service"]
        ).sum()[["Charge", "Quantity", "Orders Count"]]
        df_smart_service_groupby["Average Charge"] = (
            df_smart_service.groupby(["Service ID", "Service"]).sum()["Charge"]
            / df_smart_service.groupby(["Service ID", "Service"]).sum()["Orders Count"]
        )
        st.caption(
            f"ℹ️&nbsp;&nbsp;&nbsp;In this table, only **completed and partial orders** have been analysed. File name: <b>{uploaded_file.name}</b>\n\nℹ️&nbsp;&nbsp;&nbsp; This table sorted by charges from high to low. You can click if you want to sort by others like Quantity, Orders Count and Average ($ USD).\n\n",
            unsafe_allow_html=True,
        )  # ℹ️&nbsp;&nbsp;&nbsp; You can take notes at the right of the page.",unsafe_allow_html=True)
        ss_col1, ss_col2 = st.columns([3, 1.5])

        with ss_col1:
            download_button_data = convert_csv(
                df_smart_service_groupby.sort_values("Charge", ascending=False)
            )
            st.dataframe(
                df_smart_service_groupby.sort_values("Charge", ascending=False),
                width=1000,
                height=400,
            )
            st.download_button(
                label="Download Dataset",
                data=download_button_data,
                file_name="NewSortedData.csv",
                mime="text/csv",
                help="You can download your dataset above as a CSV file.",
            )

        with ss_col2:
            text = st.text_area(
                label="You can take notes here.",
                placeholder="For Example \n\n1) Instagram Likes - Service ID: 6\n\n2) Instagram Likes - Service ID: 8\n\n...\n\n...",
                height=375,
            )
            st.download_button(
                "Download Note",
                data=text,
                file_name="Perfect-Analysis-Notes.txt",
                mime="text/plain",
                help="You can download your notes as a txt file.",
            )

        st.markdown("---")

        with st.container():
            st.subheader("Graphs")
            grap_col1, grap_col2 = st.columns(2)
            grap_col3, grap_col4 = st.columns(2)
            df_graphService = df_smart_service
            with grap_col1:
                st.markdown("##### Charge Graph")
                st.bar_chart(df_graphService.groupby("Service").sum()["Charge"])
            with grap_col2:
                st.markdown("##### Quantity Graph")
                st.bar_chart(df_graphService.groupby("Service").sum()["Quantity"])
            with grap_col3:
                st.markdown("##### Orders Count Graph")
                st.bar_chart(
                    data=df_graphService.groupby("Service").sum()["Orders Count"]
                )
            with grap_col4:
                st.markdown("##### Average Charge Graph")
                df_graphService_2 = df_graphService.groupby(
                    ["Service ID", "Service"]
                ).sum()[["Charge", "Quantity", "Orders Count"]]
                df_graphService_2["Average Charge"] = (
                    df_graphService.groupby(["Service ID", "Service"]).sum()["Charge"]
                    / df_graphService.groupby(["Service ID", "Service"]).sum()[
                        "Orders Count"
                    ]
                )
                st.bar_chart(
                    df_graphService_2.groupby("Service").sum()["Average Charge"]
                )

        st.markdown("---")
        with st.container():
            st.header("Tips for sorting services to earn more")
            st.info(
                "Perfect Analysis can't see how fast are the services. So that, also you should look at the speed of the services."
            )
            st.markdown(
                """
            
            <h3 style="font-size:24px;color:#FFE7D3">Low-Priced Services Sorting</h3>
            <ul>
                <li style="font-size:16px"> For cheap services , you need to focus the "Average Charge".</li>         
                <li style="font-size:16px"> Because these services charges are very low. Don't forget that Perfect Panels hopes that you have more number of orders. </li>
            </ul>  
            
            <h3 style="font-size:24px;color:#FFE7D3">Mid-Priced Services</h3>
            <ul>
                <li style="font-size:16px"> In mid-priced services, the important thing is "Total Charge" for each service. You don't need to look Quantity or Orders Count.  </li>
            </ul>
            
            <h3 style="font-size:24px;color:#FFE7D3">High-Priced Services</h3>
            <ul>
                <li style="font-size:16px"> In high-priced services, the important thing is "Quantity". </li>
                <li style="font-size:16px">In generally the "Orders Count" is low. If the "Quantity" is high, it means that every customer who buys this service likes the service and has bought it again and again.</li>
                <li style="font-size:16px"> Any customer don't buy the high-priced service if the service is bad.  </li>
            </ul>          
            
            """,
                unsafe_allow_html=True,
            )

        with st.container():
            new_df = df
            new_df["Service"] = (
                new_df["Service"].str.slice(0, 40).apply(lambda x: x + "...")
            )
            new_df = new_df.groupby("Service").sum()["Charge"]
            st.dataframe(new_df)
            download_newDF = convert_csv(new_df)
            st.download_button(
                label="Download Dataset",
                data=download_newDF,
                file_name="NewSortedDataset.csv",
                mime="text/csv",
            )
