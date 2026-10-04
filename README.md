# Fluxo Financeiro Profissional 💰

Sistema completo de gestão financeira pessoal e empresarial, fluxo de caixa, cartões de crédito com faturas automáticas, estatísticas paramétricas, projeções e modelagem de risco com a nova aba **Statistic 2**.

---

## 🚀 Como Executar Localmente (Versão Web React / TypeScript)

### Pré-requisitos
- Node.js (versão 18 ou superior)
- npm ou yarn ou pnpm

### Passos de Execução:
1. Instale as dependências:
   ```bash
   npm install
   ```

2. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```

3. Abra o navegador em:
   ```
   http://localhost:3000
   ```

---

## 🐍 Como Executar Localmente (Versão Python / Streamlit)

Caso deseje executar a versão em Python via Streamlit:

### Pré-requisitos
- Python 3.9+
- Bibliotecas necessárias:
  ```bash
  pip install streamlit pandas numpy plotly scipy numpy-financial
  ```

### Executar:
```bash
streamlit run app_streamlit.py
```

---

## 📑 Estrutura de Abas do Sistema:
1. **Sophisticated Graphics:** Painel 360° com 20 gráficos preditivos, regressão OLS e Média Móvel Ponderada (WMA).
2. **Graphics:** 20 KPIs executivos vinculados a filtros de data e cenário, além de visualizações de BI.
3. **KPIs:** Central com 25 métricas de solidez, fragilidade e score de estresse patrimonial.
4. **Dashboard:** Controle orçamentário Budget vs. Realizado, agrupamento temporal e rastreamento de descrições.
5. **Statistics:** Parâmetros estatísticos (curtose, assimetria, desvio padrão), curva de sino normal $P(X < x)$ e forecast.
6. **Statistic 2 (NOVA):** 16 KPIs econométricos (VaR 95%, CVaR, Índice de Gini, Entropia de Shannon, Sharpe, Sortino, Z-Solvência), 8 gráficos de dispersão/Bollinger/Lorenz e 4 relatórios aprofundados com teste de estresse e exportação CSV.
7. **Financial Analysis:** Modelagem corporativa em estilo Excel (`VPL`, `TIR`, `VF`) e simulador de empréstimos com amortização `PMT`.
8. **🤖 IA & Assistant:** Diagnóstico preditivo automático e chat assistente integrado com Google Gemini.
9. **Lançamentos:** Consulta detalhada, filtros globais, edição inline e exclusão seletiva ou em lote.
10. **Cadastro:** Lançamento de despesas, receitas e transferências com parcelamento (divisão ou replicação) e sincronização de fatura.
11. **Cadastro de Categorias e Contas:** Gestão de centros de custo e contas bancárias.
12. **Cartões de Crédito:** Gestão de faturas automáticas com base nas datas de fechamento e vencimento, limites e liquidação.
13. **Backup & Segurança:** Download do código-fonte completo (.zip), exportação JSON/CSV, importação de backups e persistência no navegador.
