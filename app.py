import streamlit as st
import pandas as pd
import datetime
import calendar

st.set_page_config(page_title="Fluxo Financeiro Profissional", page_icon="💰", layout="wide")

# ==================== ESTADOS DA SESSÃO ====================
if "lancamentos" not in st.session_state:
    st.session_state.lancamentos = pd.DataFrame(columns=[
        "Tipo", "Conta", "Conta Destino", "Categoria", "Descrição", "Valor", "Data", "Parcelas", "Modo Valor", "Status", "Cenario"
    ])

if "categorias" not in st.session_state:
    st.session_state.categorias = ["Alimentação", "Transporte", "Moradia", "Salário", "Lazer", "Saúde", "Educação", "Fatura Cartão"]

if "contas" not in st.session_state:
    st.session_state.contas = ["Conta Corrente", "Carteira", "Cartão de Crédito", "Poupança", "Nubank", "Inter"]

if "cartoes" not in st.session_state:
    st.session_state.cartoes = [
        {"Nome": "Nubank", "Limite": 5000.0, "Fechamento": 5, "Vencimento": 12},
        {"Nome": "Inter", "Limite": 3000.0, "Fechamento": 10, "Vencimento": 17},
    ]

# ==================== NAVEGAÇÃO LATERAL ====================
st.sidebar.title("💰 Fluxo Financeiro")
aba = st.sidebar.radio(
    "Navegação",
    [
        "Sophisticated Graphics",
        "Graphics",
        "KPIs",
        "Dashboard",
        "Statistics",
        "Statistic 2",
        "Financial Analysis",
        "🤖 IA & Assistant",
        "Lançamentos",
        "Cadastro",
        "Cadastro de Categorias e Contas",
        "Cartões de Crédito",
        "Backup & Segurança",
    ],
)

st.title(f"Aba: {aba}")

df_atual = st.session_state.lancamentos

# ==================== Roteamento das 13 Abas ====================

if aba == "Sophisticated Graphics":
    st.subheader("Painel Gráfico Avançado & Tendências")
    if df_atual.empty:
        st.info("Cadastre dados na aba **Cadastro** para visualizar os gráficos analíticos.")
    else:
        st.bar_chart(df_atual, x="Data", y="Valor")

elif aba == "Graphics":
    st.subheader("Gráficos Executivos e Indicadores Reativos")
    if df_atual.empty:
        st.warning("Nenhum dado encontrado para gerar os gráficos.")
    else:
        st.line_chart(df_atual, x="Data", y="Valor")

elif aba == "KPIs":
    st.subheader("Central de KPIs e Resiliência Financeira")
    total_rec = df_atual[df_atual["Tipo"] == "Receita"]["Valor"].sum() if not df_atual.empty else 0
    total_desp = df_atual[df_atual["Tipo"] == "Despesa"]["Valor"].sum() if not df_atual.empty else 0
    saldo = total_rec - total_desp
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Receitas Totais", f"R$ {total_rec:,.2f}")
    col2.metric("Despesas Totais", f"R$ {total_desp:,.2f}")
    col3.metric("Saldo Líquido", f"R$ {saldo:,.2f}")

elif aba == "Dashboard":
    st.subheader("Dashboard Orçamentário e Budget vs. Realizado")
    if df_atual.empty:
        st.info("O dashboard está vazio. Insira transações para começar.")
    else:
        st.dataframe(df_atual, use_container_width=True)

elif aba == "Statistics":
    st.subheader("Estatísticas Descritivas e Curva de Probabilidade")
    st.write("Análise estatística baseada no histórico de lançamentos cadastrados.")
    if not df_atual.empty:
        st.write(df_atual.describe())

elif aba == "Statistic 2":
    st.subheader("Modelagem de Risco e Econometria Avançada")
    st.write("Ferramentas quantitativas, Value at Risk (VaR) e testes de estresse patrimonial.")

elif aba == "Financial Analysis":
    st.subheader("Financial Analysis (VPL, TIR e PMT)")
    st.write("Simuladores de engenharia financeira e modelagem corporativa.")

elif aba == "🤖 IA & Assistant":
    st.subheader("Central de Inteligência Artificial & Assistente Gemini")
    st.text_input("Faça uma pergunta sobre seus gastos ao assistente:")

elif aba == "Lançamentos":
    st.subheader("Auditoria e Consulta de Lançamentos")
    if df_atual.empty:
        st.warning("Nenhum lançamento registrado.")
    else:
        st.dataframe(df_atual, use_container_width=True)

elif aba == "Cadastro":
    st.subheader("Registrar Nova Movimentação")
    with st.form("form_cadastro_geral"):
        tipo = st.selectbox("Tipo", ["Despesa", "Receita", "Transferência"])
        conta = st.selectbox("Conta / Origem", st.session_state.contas)
        categoria = st.selectbox("Categoria", st.session_state.categorias)
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor (R$)", min_value=0.01, step=10.0)
        data = st.date_input("Data do Lançamento", datetime.date.today())
        status = st.selectbox("Status", ["Efetivado", "Orçado"])
        
        submitted = st.form_submit_button("Salvar no Sistema")
        
        if submitted:
            if not descricao.strip():
                st.error("Informe uma descrição válida.")
            else:
                novo_registro = pd.DataFrame([{
                    "Tipo": tipo,
                    "Conta": conta,
                    "Conta Destino": "-",
                    "Categoria": categoria,
                    "Descrição": descricao,
                    "Valor": valor,
                    "Data": str(data),
                    "Parcelas": "Única",
                    "Modo Valor": "Integral",
                    "Status": status,
                    "Cenário": "Budget" if status == "Orçado" else "Efetivado"
                }])
                st.session_state.lancamentos = pd.concat([st.session_state.lancamentos, novo_registro], ignore_index=True)
                st.success("Lançamento cadastrado com sucesso!")

elif aba == "Cadastro de Categorias e Contas":
    st.subheader("Gerenciar Centros de Custo e Contas")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Categorias Atuais:", st.session_state.categorias)
    with col2:
        st.write("Contas Atuais:", st.session_state.contas)

elif aba == "Cartões de Crédito":
    st.subheader("Gestão de Faturas e Limites de Cartão")
    for c in st.session_state.cartoes:
        st.write(f"**Cartão:** {c['Nome']} | **Limite:** R$ {c['Limite']:,.2f} | **Fechamento:** Dia {c['Fechamento']} | **Vencimento:** Dia {c['Vencimento']}")

elif aba == "Backup & Segurança":
    st.subheader("Backup, Exportação e Importação de Dados")
    st.write("Faça o download do seu histórico em formato JSON ou CSV ou limpe os registros locais.")
    if st.button("Restaurar Dados Padrão"):
        st.session_state.lancamentos = pd.DataFrame(columns=[
            "Tipo", "Conta", "Conta Destino", "Categoria", "Descrição", "Valor", "Data", "Parcelas", "Modo Valor", "Status", "Cenario"
        ])
        st.success("Dados redefinidos com sucesso!")
