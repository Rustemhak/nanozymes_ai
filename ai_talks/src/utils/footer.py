from pathlib import Path

import streamlit as st

from .constants import BUG_REPORT_URL, REPO_URL
from .helpers import render_svg


def show_info(icon: Path) -> None:
    st.divider()
    st.markdown(f"<div style='text-align: justify;'>{st.session_state.locale.responsibility_denial}</div>",
                unsafe_allow_html=True)
    st.divider()
    # st.markdown(f"""
    #     ### :page_with_curl: {st.session_state.locale.footer_title}
    #     - {render_svg(icon)} [{st.session_state.locale.footer_chat}](https://t.me/talks_ai)
    #     - {render_svg(icon)} [{st.session_state.locale.footer_channel}](https://t.me/talks_aii)
    # """, unsafe_allow_html=True)
    # st.divider()
    # st.markdown(f"project [repo on github]({REPO_URL}) waiting for your :star: | [report]({BUG_REPORT_URL}) a bug")

