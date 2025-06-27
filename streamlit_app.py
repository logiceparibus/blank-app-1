import streamlit as st
import yfinance as yf

# --- Login simples ---
st.sidebar.title("🔐 Login")
senha = st.sidebar.text_input("Digite a senha:", type="password")
senha_correta = "ouro2024"

if senha != senha_correta:
    st.warning("Acesso restrito. Digite a senha correta.")
    st.stop()

# --- Tela de preços ---
st.set_page_config(page_title="Tela de Preços", layout="wide")
st.title("📈 Tela de Preços: Ouro Spot, USD/BRL e Ouro em Reais por Grama")

@st.cache_data(ttl=60)
def get_preco(ticker):
    dados = yf.Ticker(ticker).history(period="1d", interval="1m")
    return dados['Close'].iloc[-1] if not dados.empty else None

preco_ouro_usd = get_preco("XAUUSD=X")
preco_usd_brl = get_preco("BRL=X")

if preco_ouro_usd and preco_usd_brl:
    gramas_por_onca = 31.1034768
    ouro_brl = (preco_ouro_usd / gramas_por_onca) * preco_usd_brl

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Ouro Spot (USD/oz)", f"${preco_ouro_usd:,.2f}")
    col2.metric("💵 USD/BRL", f"R${preco_usd_brl:,.4f}")
    col3.metric("📊 Ouro em Reais (R$/g)", f"R${ouro_brl:,.2f}")
else:
    st.warning("Não foi possível carregar os dados.")
