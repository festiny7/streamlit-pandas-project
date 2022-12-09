import streamlit as st
from PIL import Image
from mymodules import hide_smt

st.set_page_config(page_title="About Us", page_icon="💻", layout="centered")
st.markdown("<p><center><h1>About Us</p></center></h1>", unsafe_allow_html=True)
st.markdown("---")

hide_smt()

st.markdown("<h2><center>Who we are?</center></h2>", unsafe_allow_html=True)
st.markdown(
    """<p><center>We are a team that previously had an SMM Panel. We have lots of problems about orders analysis. 
We can't see the details of the orders. Which service is the best seller? Which provider has the most of sales?
\nWhy the charge is so high today? And we can't compare the services or providers on Perfect Panel.</center></p>""",
    unsafe_allow_html=True,
)
st.markdown(
    """<p><center>Then we want to do something about that. Because SMM is a big business.
There are lots of service, providers and users. In business like this, you need to analysis your data to
true service sorting, to compare the providers/services, and much more...</center></p>""",
    unsafe_allow_html=True,
)
st.markdown("---")


au_col1, au_col2, au_col3 = st.columns(3)

with au_col1:
    image_1 = Image.open(
        rf"C:\Users\charl\Desktop\github\streamlit\images\frontend_dev.png"
    )
    st.image(image_1)
    au_col1.markdown(
        "<h4><center>Frontend Developer</center></h4>", unsafe_allow_html=True
    )
    au_col1.markdown(
        "<hp><center>I'm setting the design for you to better UX. </center></hp>",
        unsafe_allow_html=True,
    )

with au_col2:
    image_2 = Image.open(
        rf"C:\Users\charl\Desktop\github\streamlit\images\data_analyst.png"
    )
    st.image(image_2)
    au_col2.markdown("<h4><center>Data Analyst</center></h4>", unsafe_allow_html=True)
    au_col2.markdown(
        "<hp><center>I'm developing the algorithm to analysis the data.</center></hp>",
        unsafe_allow_html=True,
    )

with au_col3:
    image_3 = Image.open(
        rf"C:\Users\charl\Desktop\github\streamlit\images\sales_director.png"
    )
    st.image(image_3)
    au_col3.markdown(
        "<h4><center>Marketing Director</center></h4>", unsafe_allow_html=True
    )
    au_col3.markdown(
        "<hp><center>I'm responsible for marketing the Perfect Analysis.</center></hp>",
        unsafe_allow_html=True,
    )
