import pandas as pd
import numpy as np
import streamlit as st
import scipy.stats as stats
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="PortFolio| Djalma Andrade", page_icon="🔐", layout="wide")

# Controles de desempenho na sidebar
st.sidebar.header("⚡ Desempenho")
MODO_LEVE = st.sidebar.toggle("Ativar Modo Leve (recomendado)", value=True)
USAR_AMOSTRA = st.sidebar.toggle("Usar amostra nos gráficos/testes", value=True)
TAM_AMOSTRA = st.sidebar.slider("Tamanho da amostra", 500, 20000, 3000, 500)
LIMITE_TABELA = st.sidebar.slider("Linhas para exibição de tabelas", 5, 200, 20, 5)

# Funções de suporte
@st.cache_data(show_spinner=False)
def carregar_csv():
    df = pd.read_csv("Global_Cybersecurity_Threats_2015-2024.csv")
    df = df.loc[:, ~df.columns.astype(str).str.contains(r"^Unnamed")]
    return df
def identificar_colunas(df):
    num = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    cat = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]
    return num, cat

def tabela_tipos(df):
    info = []
    n = len(df)
    for col in df.columns:
        nulls = df[col].isna().sum()
        null_pct = (nulls / n) * 100 if n else 0.0
        info.append({"coluna": col, "dtype": str(df[col].dtype), "%_nulos": round(null_pct, 2)})
    return pd.DataFrame(info)

def estatisticas_basicas(df, colunas_numericas):
    resumo = []
    for c in colunas_numericas:
        serie = pd.to_numeric(df[c], errors="coerce")
        resumo.append({
            "coluna": c,
            "count": int(serie.count()),
            "mean": float(serie.mean()) if serie.count() else np.nan,
            "median": float(serie.median()) if serie.count() else np.nan,
            "std": float(serie.std(ddof=1)) if serie.count() > 1 else np.nan,
            "var": float(serie.var(ddof=1)) if serie.count() > 1 else np.nan,
            "min": float(serie.min()) if serie.count() else np.nan,
            "max": float(serie.max()) if serie.count() else np.nan,
        })
    return pd.DataFrame(resumo)

def ic_media(amostra, alpha=0.05):
    amostra = pd.to_numeric(amostra, errors="coerce").dropna()
    n = len(amostra)
    media = amostra.mean() if n else np.nan
    s = amostra.std(ddof=1) if n > 1 else np.nan
    if n <= 1 or pd.isna(s) or s == 0:
        return float(media), (np.nan, np.nan)
    t_crit = stats.t.ppf(1 - alpha / 2, df=n - 1)
    erro = t_crit * s / np.sqrt(n)
    return float(media), (float(media - erro), float(media + erro))

@st.cache_data(show_spinner=False)
def amostrar_df(df, n, seed=42):
    if n >= len(df):
        return df
    return df.sample(n=n, random_state=seed)

# Carregamento dos dados
try:
    df = carregar_csv()
except Exception as e:
    st.error(f"Erro ao carregar o dataset: {e}")
    st.stop()

colunas_num, colunas_cat = identificar_colunas(df)
df_viz = amostrar_df(df, TAM_AMOSTRA) if USAR_AMOSTRA else df

# Abas principais
tabs = st.tabs(["🏠 Home", "🎓 Formação & Experiência", "🧠 Skills", "📊 Análise de Dados"])

with tabs[0]:
    st.header("Apresentação Pessoal")
    st.markdown("""
**Djalma Moreira de Andrade Filho**  
📧 djalmamoreirafilho@gmail.com  
🔗 LinkedIn - Djalma - LINK AQUI
💻 [GitHub - Djalma] - https://github.com/djxlma
                Carreira em desenvolvimento na área de Segurança Ofensiva, com foco em aprimorar habilidades
técnicas em testes de invasão e análise de vulnerabilidades. Experiência no suporte a rotinas do
setor, interação com clientes e fornecedores, organização do ambiente de trabalho e suporte às
atividades diárias da equipe, sempre comprometido com a qualidade e segurança dos serviços
prestados
""")

with tabs[1]:
    st.header("Formação & Experiência")
    st.subheader("Formação Acadêmica")
    st.markdown("""
- Engenharia de Software — FIAP (Fev/2024 - Dez/2027)  
  Projetos práticos com Tech Mahindra e Oceans 20
""")
    st.subheader("Experiências Profissionais")
    st.markdown("""
- Academia Point Fitness — Gestor de Atendimento (03/2020 a 08/2021)  
  Cadastro de alunos, gestão de pagamentos, atendimento ao cliente.

- Banco Bradesco — Estagiário em Cash Management (04/2025 - Atual)  
  Suporte aos processos, validação de dados, controle de informações.
""")

with tabs[2]:
    st.header("Skills")
    st.subheader("Hard Skills")
    st.markdown("""
- Python, Java, Java Swing, JavaScript, HTML, CSS, Cisco Packet Tracer  
- Redes de Computadores (básico)  
- Linux (básico)  
- Pacote Office (intermediário)
""")
    st.subheader("Soft Skills")
    st.markdown("""
- Organização e atenção aos detalhes  
- Gestão de tempo e liderança  
- Produtividade, adaptabilidade, proatividade  
- Comunicação eficaz
""")

with tabs[3]:
    st.header("📊 Análise de Dados")
    sub = st.tabs(["📦 Bases & Tipos", "🧮 Estatísticas", "🧪 Teste t (Welch)", "📈 Gráficos"])

    with sub[0]:
        st.subheader("Amostra do Dataset")
        st.write("**Dimensões (completas):** ", df.shape)
        st.dataframe(df.head(LIMITE_TABELA), use_container_width=True)
        st.subheader("Tipos de Variáveis e % de Nulos")
        st.dataframe(tabela_tipos(df), use_container_width=True)

    with sub[1]:
        st.subheader("Resumo Descritivo")
        if st.toggle("Calcular estatísticas", value=not MODO_LEVE):
            cols_sel = st.multiselect("Colunas numéricas", options=colunas_num, default=colunas_num[:3])
            if cols_sel:
                resumo = estatisticas_basicas(df, cols_sel)
                st.dataframe(resumo, use_container_width=True)

    with sub[2]:
        st.subheader("Teste t de Welch")
        metrica = st.selectbox("Métrica numérica", options=colunas_num)
        grupo = st.selectbox("Variável categórica", options=colunas_cat)
        if metrica and grupo:
            categorias = df_viz[grupo].dropna().astype(str).unique().tolist()
            if len(categorias) >= 2:
                cat1 = st.selectbox("Grupo A", options=categorias)
                cat2 = st.selectbox("Grupo B", options=categorias, index=1)
                df_a = pd.to_numeric(df_viz[df_viz[grupo].astype(str) == cat1][metrica], errors="coerce").dropna()
                df_b = pd.to_numeric(df_viz[df_viz[grupo].astype(str) == cat2][metrica], errors="coerce").dropna()
                if len(df_a) > 5 and len(df_b) > 5:
                    media_a, ic_a = ic_media(df_a)
                    media_b, ic_b = ic_media(df_b)
                    t_stat, p_val = stats.ttest_ind(df_a, df_b, equal_var=False)
                    st.metric(f"Média {cat1}", f"{media_a:.2f}")
                    st.metric(f"Média {cat2}", f"{media_b:.2f}")
                    st.write(f"**Teste t (Welch)** → t = {t_stat:.3f}, p-valor = {p_val:.4f}")

    with sub[3]:
        st.subheader("Gráficos Interativos")
        col1, col2 = st.columns(2)
        with col1:
            num_sel = st.selectbox("Histograma - coluna numérica", options=colunas_num)
            fig = px.histogram(df_viz, x=num_sel, nbins=30)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            cat_sel = st.selectbox("Boxplot - variável categórica", options=colunas_cat)
            num_box = st.selectbox("Boxplot - métrica numérica", options=colunas_num)
            fig = px.box(df_viz, x=cat_sel, y=num_box, points="outliers")
            st.plotly_chart(fig, use_container_width=True)
