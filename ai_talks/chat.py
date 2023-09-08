from pathlib import Path
from random import randrange
from typing import Optional

import streamlit as st
from src.styles.menu_styles import FOOTER_STYLES, HEADER_STYLES
from src.utils.conversation import get_user_input, show_chat_buttons, show_conversation
from src.utils.footer import show_info
from src.utils.helpers import get_files_in_dir, get_random_img, input_fields, get_search_data, get_chatgpt_pdf_syntes
from src.utils.lang import en, ru
from streamlit_option_menu import option_menu

import pandas as pd

# --- PATH SETTINGS ---
current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file: Path = current_dir / "src/styles/.css"
assets_dir: Path = current_dir / "assets"
icons_dir: Path = assets_dir / "icons"
img_dir: Path = assets_dir / "img"
tg_svg: Path = icons_dir / "tg.svg"

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "Nanozyme"
PAGE_ICON: str = "🤖"
LANG_EN: str = "En"
LANG_RU: str = "Ru"
AI_MODEL_OPTIONS: list[str] = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-32k",
]
# df.columns Index(['formula', 'activity', 'Syngony', 'length, nm', 'width, nm',
#    'depth, nm', 'surface', 'pol', 'surf', 'Mw(coat), g/mol', 'Km, mM',
#    'Vmax, mM/s', 'ReactionType', 'C min, mM', 'C max, mM', 'C(const), mM',
#    'Ccat(mg/mL)', 'ph', 'temp, °C', 'link'],
#   dtype='object')
COLUMNS = [
    "Km, mM",
    "Vmax, mM/s",
    "formula",
    "activity",
    "Syngony",
    "length, nm",
    "width, nm",
    "depth, nm",
    "surface",
    "ReactionType",
    "link",
]
ACTIVITI = [
    "peroxidase",
    "oxidase",
    "laccase",
    "catalase",
]
SYNGONY = {
    0: "amorphous",
    1: "triclinic",
    2: "monoclinic",
    3: "orthorhombic",
    4: "tetragonal",
    5: "trigonal",
    6: "hexagonal",
    7: "cubic",
}
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# --- LOAD CSS ---
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# selected_lang = option_menu(
#     menu_title=None,
#     options=[LANG_EN, LANG_RU, ],
#     icons=["globe2", "translate"],
#     menu_icon="cast",
#     default_index=0,
#     orientation="horizontal",
#     styles=HEADER_STYLES
# )

# Storing The Context
if "locale" not in st.session_state:
    st.session_state.locale = en
if "generated" not in st.session_state:
    st.session_state.generated = []
if "past" not in st.session_state:
    st.session_state.past = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "input_kind" not in st.session_state:
    st.session_state.input_kind = st.session_state.locale.input_kind_1
if "seed" not in st.session_state:
    st.session_state.seed = randrange(10**3)  # noqa: S311
if "costs" not in st.session_state:
    st.session_state.costs = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = []


def main() -> None:
    c1, c2 = st.columns(2)
    with c1, c2:
        c1.selectbox(label=st.session_state.locale.select_placeholder1, key="model", options=AI_MODEL_OPTIONS)
        st.session_state.input_kind = c2.radio(
            label=st.session_state.locale.input_kind,
            options=(st.session_state.locale.input_kind_1, st.session_state.locale.input_kind_2),
            horizontal=True,
        )
        role_kind = c1.radio(
            label=st.session_state.locale.radio_placeholder,
            options=(st.session_state.locale.radio_text1, st.session_state.locale.radio_text2),
            horizontal=True,
        )
        match role_kind:
            case st.session_state.locale.radio_text1:
                c2.selectbox(label=st.session_state.locale.select_placeholder2, key="role",
                             options=st.session_state.locale.ai_role_options)
            case st.session_state.locale.radio_text2:
                c2.text_input(label=st.session_state.locale.select_placeholder3, key="role")

    if st.session_state.user_text:
        show_conversation()
        st.session_state.user_text = ""
    get_user_input()
    show_chat_buttons()


def run_agi():
    # match selected_lang:
    #     case "En":
    #         st.session_state.locale = en
    #     case "Ru":
    #         st.session_state.locale = ru
    #     case _:
    #         st.session_state.locale = en
    st.session_state.locale = ru
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.locale.title}</h1>", unsafe_allow_html=True)
    # selected_footer = option_menu(
    #     menu_title=None,
    #     options=[
    #         st.session_state.locale.footer_option1,
    #         # st.session_state.locale.footer_option0,
    #         # st.session_state.locale.footer_option2,
    #     ],
    #     # icons=["info-circle", "chat-square-text", "piggy-bank"],  # https://icons.getbootstrap.com/
    #     icons=["info-circle"],  # https://icons.getbootstrap.com/
    #     menu_icon="cast",
    #     default_index=0,
    #     orientation="horizontal",
    #     styles=FOOTER_STYLES
    # )
    # match selected_footer:
    #     case st.session_state.locale.footer_option0:
    #         main()
    #     case st.session_state.locale.footer_option1:
    #         # st.image(f"{img_dir}/{get_random_img(get_files_in_dir(img_dir))}")
    #         show_info(tg_svg)
            
    #     case st.session_state.locale.footer_option2:
    #         show_donates()
    #     case _:
    #         show_info(tg_svg)
    
    selected_footer = option_menu(
        menu_title=None,
        options=[
            "Поиск по базе знаний",
        ],
        # icons=["info-circle", "chat-square-text", "piggy-bank"],  # https://icons.getbootstrap.com/
        icons=["search"],  # https://icons.getbootstrap.com/
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles=FOOTER_STYLES
    )
    
    df_data_filtered = pd.read_csv("data/nanozymes_extended.csv")
    input_option = st.radio("Выберите вариант ввода:", (r"Только $$K_m$$", r"Только $$V_{max}$$", r"$$K_m$$ и $$V_{max}$$"), index=0)
    activiti_option = st.radio("Выберите активность:", ("all", *ACTIVITI), index=0)

    # В зависимости от выбранного варианта, отображайте соответствующие поля ввода
    K_m, V_max = None, None
    
    match input_option:
        case r"Только $$K_m$$":
            # st.write("Вы выбрали вариант Только K_m")
            K_m, V_max = input_fields("K_m")
        case r"Только $$V_{max}$$":
            # st.write("Вы выбрали вариант Только V_max")
            K_m, V_max = input_fields("V_max")
        case r"$$K_m$$ и $$V_{max}$$":
            # st.write("Вы выбрали вариант K_m и V_max")
            K_m, V_max = input_fields("K_m", "V_max")
    st.markdown("")
    # see_data = st.expander('Вы можете нажать здесь, чтобы увидеть необработанные данные 👉')
    # df_data_filtered = pd.read_excel("data/nanozymes.xlsx")
    
    # with see_data:
    #     st.dataframe(data=df_data_filtered.reset_index(drop=True))
    st.text('')
    print("df_data_filtered", df_data_filtered)
    print("df.columns", df_data_filtered.columns)
    if st.button('Получить наиболее подходящие результаты') and (K_m or V_max):
        data = df_data_filtered
        if activiti_option != "all":
            data = data[data["activity"] == activiti_option]
            
        res = get_search_data(data, K_m, V_max)
        i = 1
        for distance, _data in res:
            # Нумерация с единицы
            try:
                st.write(f"{i}. {_data['formula']}")
                i += 1
                __data = pd.DataFrame(_data).T
                see_data = st.expander('Подробности')
                with see_data:
                    _prep_data = __data[COLUMNS]
                    try:
                        _prep_data["Syngony"] = _prep_data["Syngony"].apply(lambda x: SYNGONY.get(int(x), None))
                    except ValueError:
                        _prep_data["Syngony"] = None
                    st.dataframe(data=_prep_data.reset_index(drop=True))
                    # st.dataframe(data=__data[columns].reset_index(drop=True))
                    # st.dataframe(data=__data.reset_index(drop=True))
                syntes = st.expander('Синтез')
                with syntes:
                    # st.write(f"{__data.index[0]}) {__data['formula']}\n")
                    # st.write("Заглушка для синтеза, про который пока можно почитать тут: ", __data["link"])
                    st.write(get_chatgpt_pdf_syntes(__data))
            except BaseException:
                continue
                

            
    else:
        st.write('')
    
    


if __name__ == "__main__":
    run_agi()
