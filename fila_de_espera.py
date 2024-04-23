import streamlit as st
import psycopg2
import re  # Importe o módulo de expressões regulares
import pyodbc

def conectar_db():
    server = 'streamlit.database.windows.net'  # Atualize com seu nome de servidor
    database = 'analise_vendas'  # Atualize com o nome do seu banco de dados
    username = 'streamlit'  # Atualize com seu nome de usuário
    password = 'Maumau157@'  # Atualize com sua senha
    driver= '{ODBC Driver 17 for SQL Server}'  # Este driver pode variar dependendo da sua instalação
    conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    return conn

# Função para inserir dados na fila de espera
def inserir_na_fila_espera(nome, email, telefone, interesse):
    conn = conectar_db()
    cur = conn.cursor()
    # Ajuste nos placeholders para usar com pyodbc
    cur.execute(
        "INSERT INTO fila_espera (nome, email, telefone, interesse) VALUES (?, ?, ?, ?)",
        nome, email, telefone, interesse
    )
    conn.commit()
    cur.close()
    conn.close()

def formulario_fila_espera():
    st.title("🌟 Transforme Seu Aprendizado!")
    st.header("Garanta Sua Vaga Agora na Ferramenta de Estudos Mais Inovadora e ganhe 50% de desconto!")

    # CSS para personalizar o layout
    st.markdown("""
    <style>
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
    .stSelectbox>div>div>select {
        border-radius: 20px;
    }
    .stButton>button {
        border-radius: 20px;
        border: 2px solid #4CAF50;
        color: white;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
    


    with st.form("fila_espera_form", clear_on_submit=True):
        nome = st.text_input("Nome", placeholder="Seu nome completo", help="Campo obrigatório.")
        email = st.text_input("E-mail", placeholder="Seu melhor e-mail", help="Campo obrigatório.")
        telefone = st.text_input("Telefone", placeholder="Seu número de telefone com DDD", help="Somente números.")
        interesse = st.selectbox("Interesse na Ferramenta", ["Compra", "Teste Gratuito", "Mais Informações"], help="Campo obrigatório.")
        
        submitted = st.form_submit_button("Enviar 🚀")
        if submitted:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Por favor, insira um endereço de e-mail válido.")
            elif not telefone.isdigit():
                st.error("O telefone deve conter apenas números.")
            elif nome and email and telefone and interesse:
                inserir_na_fila_espera(nome, email, telefone, interesse)
                st.success("Obrigado por se juntar à fila de espera! Entraremos em contato em breve.")
                st.success('Parabéns, você ganhou 50% de desconto!')
                st.balloons()  # Adiciona uma animação de balões como feedback visual
            else:
                st.error("Por favor, preencha todos os campos.")

    # Botão de contato estilizado
    contato_link = "https://wa.me/5511911218952"
    st.markdown(f'<a href="{contato_link}" target="_blank"><button style="background-color: #4CAF50; color: white; padding: 10px 20px; margin: 10px 0; border: none; cursor: pointer;">Entre em Contato 💬</button></a>', unsafe_allow_html=True)

formulario_fila_espera()