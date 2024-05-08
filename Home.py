import streamlit as st

#colocar para printar o horário e dia da ultima atualização do bd
def run():
    st.set_page_config(
        page_title="Eshows-Data Analytics",
        page_icon="🎤",
        layout="wide"
    )

    with st.sidebar:
        st.write("Dash Clientes")
        
    col1, col2 = st.columns([4,1])
    col2.image("./assets/imgs/eshows-logo.png", width=100)
    col1.write("# Dash Clientes -")


if __name__ == "__main__":
    run()