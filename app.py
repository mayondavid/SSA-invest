import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.title("🏙️ SSA-Invest | Dashboard de FIIs")

# 1. Configurações Iniciais
st.set_page_config(page_title="Minha Carteira FII", layout="wide")
st.title("🚀 Dashboard de Investimentos - B3")

# 2. Seus Dados (Edite aqui com seus valores reais)
# Criando um DataFrame para facilitar a gestão
meus_fiis = {
    "Ticker": ["MXRF11.SA", "XPML11.SA", "BTHF11.SA", "PVBI11.SA", "VGHF11.SA"],
    "Quantidade": [15, 1, 1, 1, 8],  # Exemplo de quantidades
    "Preco_Medio": [9.50, 110.00, 9.48, 81.00, 7.17], # Exemplo de preços médios
    "Setor": ["Papel", "Shopping", "Hedge Fund", "Lajes", "Hedge Fund"]
}
df_carteira = pd.DataFrame(meus_fiis)

# 3. Busca de Preços em Tempo Real
@st.cache_data(ttl=600) # Atualiza a cada 10 minutos
def pegar_precos(lista_tickers):
    data = yf.download(lista_tickers, period="1d")['Close']
    return data.iloc[-1]

precos_atuais = pegar_precos(df_carteira["Ticker"].tolist())

# 4. Cálculos Financeiros
df_carteira["Preco_Atual"] = df_carteira["Ticker"].map(precos_atuais)
df_carteira["Total_Investido"] = df_carteira["Quantidade"] * df_carteira["Preco_Medio"]
df_carteira["Valor_Atual"] = df_carteira["Quantidade"] * df_carteira["Preco_Atual"]
df_carteira["Lucro_Prejuizo"] = df_carteira["Valor_Atual"] - df_carteira["Total_Investido"]

# 5. Visualização (Cards)
total_patrimonio = df_carteira["Valor_Atual"].sum()
lucro_total = df_carteira["Lucro_Prejuizo"].sum()

c1, c2 = st.columns(2)
c1.metric("Patrimônio Total", f"R$ {total_patrimonio:,.2f}")
c2.metric("Lucro/Prejuízo Total", f"R$ {lucro_total:,.2f}", delta_color="normal")

st.write("---")

# 6. Gráficos Interativos
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Distribuição por Setor")
    fig_setor = px.pie(df_carteira, values='Valor_Atual', names='Setor', hole=.3)
    st.plotly_chart(fig_setor)

with col_graf2:
    st.subheader("Desempenho por Ativo (R$)")
    fig_barra = px.bar(df_carteira, x='Ticker', y='Lucro_Prejuizo', color='Lucro_Prejuizo',
                       color_continuous_scale='RdYlGn')
    st.plotly_chart(fig_barra)

# 7. Tabela Detalhada
st.subheader("Detalhamento da Carteira")
st.dataframe(df_carteira.style.format({
    "Preco_Medio": "R$ {:.2f}",
    "Preco_Atual": "R$ {:.2f}",
    "Total_Investido": "R$ {:.2f}",
    "Valor_Atual": "R$ {:.2f}",
    "Lucro_Prejuizo": "R$ {:.2f}"
}))
