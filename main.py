import streamlit as st
from utils.user import login, set_user_cookie, cookie_exists
from utils.components import hide_sidebar


def handle_login(userName, password):
    #user data deve conter o usuario
    if user_data := login(userName, password):
        st.session_state['loggedIn'] = True
        set_user_cookie(userName, st.session_state['loggedIn'])
    else:
        # mudar pra falso depois
        set_user_cookie(userName, st.session_state['loggedIn'])
        st.session_state['loggedIn'] = True
        st.error("Email ou senha inválidos!!")

def show_login_page():
    col1, col2 = st.columns([4,1])
    col2.image("./assets/imgs/eshows-logo.png", width=100)
    col1.write("## Dashboard de dados")
    userName = st.text_input(label="", value="", placeholder="Email")
    password = st.text_input(label="", value="", placeholder="Senha", type="password")
    st.button("Login", on_click=handle_login, args=(userName, password))

def main():
    if cookie_exists("session") and st.experimental_get_query_params()["session"][0] == "true":
        st.session_state['loggedIn'] = True

    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
    
    if not st.session_state['loggedIn']:
        show_login_page()
        st.stop()
    else:
        st.switch_page("pages/Home.py")
    
if __name__ == '__main__':
    st.set_page_config(
    page_title="Eshows: Dashboard",
    page_icon="🎤",
    layout="centered",
    )
    hide_sidebar()
    main()

    # quando carrega a página tá deslogando
    # adicionar querys de relatórios