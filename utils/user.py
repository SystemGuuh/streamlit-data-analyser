import streamlit as st
import requests

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
    st.cache_data.clear()
    st.session_state['loggedIn'] = False