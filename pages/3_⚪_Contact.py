import streamlit as st
import mymodules


st.set_page_config(page_title="Contact", page_icon=mymodules.icon(), layout="centered")
st.markdown("<p><center><h1>Contact</p></center></h1>", unsafe_allow_html=True)
st.markdown("---")

mymodules.hide_smt()

#  - - - - - SIDEBAR - - - - -
with st.sidebar:
    st.text("Upload your file.")
    uploaded_file = st.file_uploader("Choose a CSV file.", type=["csv"])

    charge_number_input = st.number_input(
        "Charge",
        help="For example if you type 1, the orders with more than $1 will appear.",
    )

    logo = st.image(mymodules.logo())


st.markdown(
    "<p><center>Do you have any issue or request? You can get in touch with the form.</center></p>",
    unsafe_allow_html=True,
)

contact_form = """
<form action="https://formsubmit.co/perfectanalysis@gmail.com" method="POST">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_template" value="table">
     <input type="text" name="name" placeholder="Name" required>
     <input type="email" name="email" placeholder="Email" required>
     <textarea name="message" placeholder="Your Message"></textarea>
     <button type="submit">Send</button>
     <input type="hidden" name="_next" value="http://localhost:8501/Contact">
</form>
"""
st.markdown(contact_form, unsafe_allow_html=True)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css(r"C:\Users\charl\Desktop\github\streamlit\style\style.css")

st.markdown("---")

contact_col1, contact_col2, contact_col3 = st.columns(3)

with contact_col1:
    st.markdown("<p><center><h2>Mail</h2></center></p>", unsafe_allow_html=True)
    st.markdown(
        "<p><center>perfectanalysis@gmail.com</center></p>", unsafe_allow_html=True
    )

# <p><center> </center></p>
with contact_col2:
    st.markdown("<p><center><h2>Telegram</h2></center></p>", unsafe_allow_html=True)
    st.markdown("<p><center>@perfectAnalysis</center></p>", unsafe_allow_html=True)

with contact_col3:
    st.markdown("<p><center><h2>Skype</h2></center></p>", unsafe_allow_html=True)
    st.markdown(
        "<p><center>perfectanalysis@outlook.com</center></p>", unsafe_allow_html=True
    )
