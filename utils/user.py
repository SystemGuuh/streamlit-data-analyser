import streamlit as st
import requests
from streamlit import _CodeHasher

def login(userName: str, password: str) -> bool:
    if (userName is None):
        return False

    login_data = {
    "username": userName,
    "password": password,
    "loginSource": 1,
    }

    # trocar para nova api do epm
    login = requests.post('https://apps.eshows.com.br/eshows/Security/Login',json=login_data).json()
    
    if "error" in login:
        return False

    else:
        if login['data']['success'] == True:
            return login
        else:
            return False

def logout():
    st.session_state['loggedIn'] = False

def set_cookie(name, value, days=7):
    c = _CodeHasher()  # Cria um hash para o nome do cookie
    st.experimental_set_query_params(**{c._calculate_query_param(name): value}, **{c._calculate_query_param(name + "_expires"): days})

def get_cookie(name):
    c = _CodeHasher()
    return st.experimental_get_query_params().get(c._calculate_query_param(name), None)

def set_user_cookie(user, session):
    set_cookie("username", user)
    set_cookie("session", session)

def cookie_exists(name):
    c = _CodeHasher()
    return c._calculate_query_param(name) in st.experimental_get_query_params()
