import os

import streamlit as st
from dotenv import load_dotenv

from tabs import chat, doctor, home, track
from utils import style
from utils.db import get_db_client

load_dotenv()

st.set_page_config(page_title="KAKI Care", page_icon="💙", layout="centered")
style.inject_css()

client = get_db_client()
user_id = int(os.getenv("USER_ID", 1))

tab_home, tab_chat, tab_track, tab_doctor = st.tabs(
    ["🏠 Home", "💬 KAKI", "📋 Track", "👨‍⚕️ Doctor"]
)

with tab_home:
    home.render(client, user_id)

with tab_chat:
    chat.render(user_id)

with tab_track:
    track.render(client, user_id)

with tab_doctor:
    doctor.render(client, user_id)
