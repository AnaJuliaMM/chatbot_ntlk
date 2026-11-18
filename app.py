import streamlit as st
from service import processar_mensagem

# Configurar metadados
st.set_page_config(page_title="GPSA - Assistente", page_icon="⚙️", layout="wide")

# Sidebar
with st.sidebar:
    st.image("logo.png", width=400)

# Tela principal
st.header("Assistente de agendamento")

MENSAGEM_BOAS_VINDAS = """Olá! 👋 Eu sou o **assistente de agendamento** e posso te ajudar com **compra de máquinas** e **manutenção**.

Você pode fazer algumas das perguntas abaixo:

- 🛒 *Quero comprar uma máquina*
- 📖 *Quero consultar as máquinas disponíveis*
- 📅 *Quero agendar uma manutenção*
- ❌ *Quero cancelar a manutenção*
"""

# Histórico da conversa (começa com a mensagem de boas-vindas)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": MENSAGEM_BOAS_VINDAS}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Nova mensagem
prompt = st.chat_input("Digite sua mensagem")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    resposta = processar_mensagem(prompt)
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.write(resposta)