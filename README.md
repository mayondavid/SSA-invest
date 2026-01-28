
​🏙️ SSA-Invest | Dashboard de FIIs em Tempo Real

​O SSA-Invest é um Web App interativo desenvolvido para o monitoramento estratégico de Fundos de Investimento Imobiliário (FIIs) listados na B3. O projeto utiliza dados em tempo real para fornecer métricas de rentabilidade, composição de carteira e tendências de mercado.

​🚀 Funcionalidades
​Gestão Dinâmica: Interface lateral que permite editar quantidades, preços médios e adicionar novos ativos sem mexer no código.
​Dados Real-Time: Integração com a API do Yahoo Finance para cotações atualizadas da B3.
​Análise Visual: * Sparklines: Mini-gráficos de tendência dos últimos 7 dias para cada ativo.

​Métricas de Performance: Cálculo automático de Lucro/Prejuízo e Dividend Yield on Cost.
​Diversificação: Gráficos interativos (Plotly) de setor e comparação de patrimônio.

​🛠️ Tecnologias Utilizadas
​Linguagem: Python 3.10+
​Framework Web: Streamlit
​Análise de Dados: Pandas
​Visualização: Plotly & Streamlit Charts
​Fonte de Dados: YFinance (Yahoo Finance API)
​Deploy: Streamlit Cloud

​📋 Como executar o projeto localmente:

Clone o repositório:
git clone https://github.com/seu-usuario/SSA-Invest.git
Instale as dependências:
pip install -r requirements.txt
Execute o app:
streamlit run app.py
