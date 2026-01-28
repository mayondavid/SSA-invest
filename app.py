import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SSA-Invest | Dashboard FII", layout="wide", page_icon="🏙️")

st.title("🏙️ SSA-Invest | Dashboard de FIIs em Tempo Real")
st.caption("Desenvolvido para monitoramento estratégico de ativos na B3")

# 2. GESTÃO DE DADOS (TABELA EDITÁVEL)
st.sidebar.header("📝 Configuração da Carteira")
st.sidebar.write("Altere as quantidades e preços médios abaixo:")

# Dados iniciais para não começar vazio
dados_iniciais = {
    "Ticker": ["MXRF11.SA", "XPML11.SA", "BTHF11.SA", "PVBI11.SA", "VGHF11.SA"],
    "Quantidade": [100, 10, 50, 5, 120],
    "Preco_Medio": [10.20, 112.00, 9.80, 95.00, 9.10],
    "Setor": ["Papel", "Shopping", "Hedge Fund", "Lajes", "Hedge Fund"]
}
df_base = pd.DataFrame(dados_iniciais)

# Tabela editável na Sidebar
df_carteira = st.sidebar.data_editor(
    df_base,
    num_rows="dynamic",
    hide_index=True,
    use_container_width=True
)

# 3. BUSCA DE DADOS EM TEMPO REAL (YFINANCE)
@st.cache_data(ttl=600) # Cache de 10 minutos para performance
def buscar_dados_mercado(tickers):
    # Puxa histórico de 7 dias para os Sparklines e o preço atual
    try:
        hist = yf.download(tickers, period="7d", interval="1d")['Close']
        return hist
    except:
        st.error("Erro ao conectar com a API da B3. Verifique os tickers.")
        return pd.DataFrame()

if not df_carteira.empty:
    historico = buscar_dados_mercado(df_carteira["Ticker"].tolist())
    
    # 4. PROCESSAMENTO E CÁLCULOS
    # Pegando o último preço de fechamento
    precos_atuais = historico.iloc[-1]
    df_carteira["Preco_Atual"] = df_carteira["Ticker"].map(precos_atuais)
    
    df_carteira["Total_Investido"] = df_carteira["Quantidade"] * df_carteira["Preco_Medio"]
    df_carteira["Valor_Atual"] = df_carteira["Quantidade"] * df_carteira["Preco_Atual"]
    df_carteira["Lucro_Prejuizo"] = df_carteira["Valor_Atual"] - df_carteira["Total_Investido"]
    df_carteira["Rentabilidade_Pct"] = ((df_carteira["Preco_Atual"] / df_carteira["Preco_Medio"]) - 1) * 100

    # 5. DASHBOARD - VISUALIZAÇÃO PRINCIPAL
    # Cards de Resumo
    total_patrimonio = df_carteira["Valor_Atual"].sum()
    lucro_total = df_carteira["Lucro_Prejuizo"].sum()
    rent_total_pct = ((total_patrimonio / df_carteira["Total_Investido"].sum()) - 1) * 100

    c1, c2, c3 = st.columns(3)
    c1.metric("Patrimônio Total", f"R$ {total_patrimonio:,.2f}")
    c2.metric("Lucro/Prejuízo Total", f"R$ {lucro_total:,.2f}", f"{rent_total_pct:.2f}%")
    c3.metric("Nº de Ativos", len(df_carteira))

    st.write("---")

    # Sparklines e Métricas Individuais
    st.subheader("📈 Performance e Tendência (7 dias)")
    cols_ativos = st.columns(len(df_carteira))

    for i, (index, row) in enumerate(df_carteira.iterrows()):
        with cols_ativos[i]:
            ticker = row['Ticker']
            dados_fundo = historico[ticker].dropna()
            
            st.metric(
                label=ticker.replace(".SA", ""),
                value=f"R$ {row['Preco_Atual']:.2f}",
                delta=f"{row['Rentabilidade_Pct']:.2f}%"
            )
            st.line_chart(dados_fundo, height=80)

    st.write("---")

    # Gráficos de Análise
    col_g1, col_g2 = st.columns([1, 1])

    with col_g1:
        st.subheader("🍕 Divisão por Setor")
        fig_setor = px.pie(df_carteira, values='Valor_Atual', names='Setor', hole=.4,
                           color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_setor, use_container_width=True)

    with col_g2:
        st.subheader("📊 Valor Investido vs. Valor Atual")
        fig_comp = px.bar(df_carteira, x="Ticker", y=["Total_Investido", "Valor_Atual"],
                          barmode="group", color_discrete_map={"Total_Investido": "#CBD5E0", "Valor_Atual": "#2ECC71"})
        st.plotly_chart(fig_comp, use_container_width=True)

    # Tabela de Dados Final
    with st.expander("🔍 Ver Detalhes da Tabela"):
        st.dataframe(df_carteira.style.format({
            "Preco_Medio": "R$ {:.2f}", "Preco_Atual": "R$ {:.2f}",
            "Total_Investido": "R$ {:.2f}", "Valor_Atual": "R$ {:.2f}",
            "Lucro_Prejuizo": "R$ {:.2f}", "Rentabilidade_Pct": "{:.2f}%"
        }), use_container_width=True)

else:
    st.warning("Adicione ativos na barra lateral para visualizar o dashboard.")
