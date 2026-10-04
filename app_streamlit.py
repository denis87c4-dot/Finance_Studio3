import io
import json
import zipfile
import calendar
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm
import numpy_financial as npf
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Fluxo Financeiro Profissional", page_icon="💰", layout="wide"
)

# ==================== NAVEGAÇÃO LATERAL ====================
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

# ==================== ESTADOS DA SESSÃO ====================
COLUNAS_LANC = [
    "Tipo",
    "Conta",
    "Conta Destino",
    "Categoria",
    "Descrição",
    "Valor",
    "Data",
    "Parcelas",
    "Modo Valor",
    "Status",
    "Cenario",
]

if "lancamentos" not in st.session_state:
    st.session_state.lancamentos = pd.DataFrame(columns=COLUNAS_LANC)

if not st.session_state.lancamentos.empty and "Status" not in st.session_state.lancamentos.columns:
    st.session_state.lancamentos["Status"] = "Efetivado"

if not st.session_state.lancamentos.empty and "Cenario" not in st.session_state.lancamentos.columns:
    st.session_state.lancamentos["Cenario"] = "Efetivado"

if "categorias" not in st.session_state:
    st.session_state.categorias = [
        "Alimentação",
        "Transporte",
        "Moradia",
        "Salário",
        "Lazer",
    ]

if "contas" not in st.session_state:
    st.session_state.contas = [
        "Conta Corrente",
        "Carteira",
        "Cartão de Crédito",
        "Poupança",
    ]

if "cartoes" not in st.session_state:
    st.session_state.cartoes = [
        {
            "Nome": "Nubank",
            "Limite": 5000.0,
            "Fechamento": 5,
            "Vencimento": 12,
        },
        {
            "Nome": "Inter",
            "Limite": 3000.0,
            "Fechamento": 10,
            "Vencimento": 17,
        },
    ]

# ==================== FUNÇÕES AUXILIARES ====================
PREFIXO_AUTO = "[AUTO] Fatura "
CATEGORIA_FATURA = "Fatura Cartão"

def garantir_colunas(df):
    if "Status" not in df.columns:
        df["Status"] = "Efetivado"
    df["Status"] = df["Status"].fillna("Efetivado")
    if "Cenario" not in df.columns:
        df["Cenario"] = df["Status"].apply(lambda s: "Budget" if s == "Orçado" else "Efetivado")
    df["Cenario"] = df["Cenario"].fillna("Efetivado")
    return df

def _data_segura(ano, mes, dia):
    ultimo = calendar.monthrange(ano, mes)[1]
    return pd.Timestamp(year=ano, month=mes, day=min(dia, ultimo))

def vencimento_da_fatura(data_compra, fechamento, vencimento):
    d = pd.to_datetime(data_compra)
    ref = pd.Timestamp(d.year, d.month, 1)
    if d.day > fechamento:
        ref += pd.DateOffset(months=1)
    if vencimento <= fechamento:
        ref += pd.DateOffset(months=1)
    return _data_segura(ref.year, ref.month, int(vencimento)).date()

def sincronizar_budget_cartao(nome_cartao=None):
    df = st.session_state.lancamentos.copy()
    if df.empty:
        return
    df = garantir_colunas(df)
    if CATEGORIA_FATURA not in st.session_state.categorias:
        st.session_state.categorias.append(CATEGORIA_FATURA)

    cartoes = [c for c in st.session_state.cartoes if nome_cartao is None or c["Nome"] == nome_cartao]
    novos = []
    for c in cartoes:
        nome = c["Nome"]
        prefixo = f"{PREFIXO_AUTO}{nome} |"
        eh_auto = df["Descrição"].astype(str).str.startswith(prefixo)
        df = df[~eh_auto]

        gastos = df[(df["Conta"] == nome) & (df["Tipo"] == "Despesa") & (df["Status"] == "Efetivado")].copy()
        if gastos.empty:
            continue
        gastos["Valor"] = pd.to_numeric(gastos["Valor"], errors="coerce").fillna(0.0)
        gastos["Venc"] = gastos["Data"].apply(lambda x: vencimento_da_fatura(x, c["Fechamento"], c["Vencimento"]))
        pagos = pd.to_numeric(df[(df["Conta Destino"] == nome) & (df["Tipo"] == "Transferência") & (df["Status"] == "Efetivado")]["Valor"], errors="coerce").fillna(0.0).sum()
        restante = float(pagos)

        for venc, total in sorted(gastos.groupby("Venc")["Valor"].sum().items(), key=lambda x: x[0]):
            total = float(total)
            paga = restante >= total - 0.005
            if paga:
                restante -= total
            descricao_fatura = f"{prefixo} {pd.Timestamp(venc).strftime('%Y-%m')}"
            if paga:
                descricao_fatura += " ✅ Paga"
            novos.append(["Despesa", nome, "-", CATEGORIA_FATURA, descricao_fatura, total, venc, "Única", "Integral", "Efetivado" if paga else "Orçado", "Efetivado" if paga else "Budget"])

    if novos:
        df_novos = pd.DataFrame(novos, columns=COLUNAS_LANC)
        df = pd.concat([df, df_novos], ignore_index=True)
    st.session_state.lancamentos = df.reset_index(drop=True)

st.title(f"Aba: {aba}")
st.write("Aplicativo executando com sucesso.")
