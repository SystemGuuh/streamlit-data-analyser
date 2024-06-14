import streamlit as st
from utils.user import login


def handle_login(userName, password):
    #user data deve conter o usuario
    if user_data := login(userName, password):
        st.session_state['loggedIn'] = True
        st.session_state['user_data'] = user_data
    else:
        st.session_state['loggedIn'] = False
        st.error("Email ou senha inválidos!!")

def show_login_page():
    col1, col2 = st.columns([4,1])
    col2.image("./assets/imgs/eshows-logo.png", width=100)
    col1.write("## Dashboard de dados")
    userName = st.text_input(label="", value="", placeholder="Email")
    password = st.text_input(label="", value="", placeholder="Senha", type="password")
    st.button("Login", on_click=handle_login, args=(userName, password))

def main():
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        st.session_state['user_data'] = None
    
    if not st.session_state['loggedIn']:
        show_login_page()
        st.stop()
    else:
        st.switch_page("pages/Home.py")
    
if __name__ == '__main__':
    st.set_page_config(
    page_title="Relatórios Eshows",
    page_icon="./assets/imgs/eshows-logo100x100.png",
    layout="centered",
    )
    main()