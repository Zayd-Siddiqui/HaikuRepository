import streamlit as st
from MoodHaikuGenerator import MoodHaikuGenerator

haiku_generator = MoodHaikuGenerator()

st.set_page_config(page_title="Mood Haiku Generator", layout="centered")

st.markdown("""
<style>
body {
    margin-top: 5%;  # Percentage-based top margin
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box">Mood Haiku Generator</div>', unsafe_allow_html=True)
st.write("A glimpse into your mind")

user_input = st.text_area("How are you feeling today?", height=100)

if st.button("Generate Haiku"):
    if user_input.strip():
        try:
            haiku = haiku_generator.process(user_input)
            st.write("### Your Mood Haiku:")
            st.text(haiku)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter your mood description.")

st.markdown("<div style='margin-top:2rem;'>Created by Your Name</div>", unsafe_allow_html=True)
