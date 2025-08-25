import pandas as pd
import numpy as np
import streamlit as st
import scipy.stats as stats
import plotly.express as px

st.set_page_config(page_title="PortFolio | Djalma Andrade", layout="wide")

st.sidebar.header("Navegação")
pagina = st.sidebar.radio(
    "Selecione a página:",
    [
        "Home",
        "Formação & Experiência",
        "Skills",
        "Análise de Dados"
    ]
)

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

try:
    df = carregar_csv()
except Exception as e:
    st.error(f"Erro ao carregar o dataset: {e}")
    st.stop()

colunas_num, colunas_cat = identificar_colunas(df)

if pagina == "Home":
    st.markdown("## Apresentação Pessoal")

    col1, col2 = st.columns([1, 4], vertical_alignment="center")

    with col1:
        st.image("sua_foto.jpg", width=270)

    with col2:
        st.markdown(
            """
            <div style="text-align: left;">
                <h3 style="margin-bottom:5px; font-size:28px; color:#ffffff;">
                    <b>Djalma Moreira de Andrade Filho</b>
                </h3>
                <p style="font-size:18px; line-height:1.6; color:#cccccc;">
                    Profissional em desenvolvimento na área de <b>Segurança Ofensiva</b>, com foco em aprimorar
                    habilidades técnicas em testes de invasão e análise de vulnerabilidades. Experiência em suporte às rotinas do setor,
                    interação com clientes e fornecedores, organização do ambiente de trabalho e suporte às atividades diárias da equipe,
                    sempre comprometido com a qualidade e segurança dos serviços prestados.
                </p>
                <p style="margin-top:15px;">
                    <a href="https://github.com/djxlma" target="_blank" style="text-decoration:none; margin-right:15px;">
                        <img src="https://cdn-icons-png.flaticon.com/512/733/733553.png" width="30"/>
                    </a>
                    <a href="https://www.linkedin.com/in/djalma-andrade-6211682b6/" target="_blank" style="text-decoration:none; margin-right:15px;">
                        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="30"/>
                    </a>
                    <a href="mailto:djalmamoreirafilho@gmail.com" target="_blank" style="text-decoration:none;">
                        <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" width="30"/>
                    </a>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

elif pagina == "Formação & Experiência":
    st.header("Formação & Experiência")
    st.subheader("Formação Acadêmica")
    st.markdown("""
- Engenharia de Software — FIAP (Fev/2024 - Dez/2027)  
    Participação dos projetos práticos proporcionados pela instituição, atuando em
    desafios da Tech Mahindra e da Oceans 20 com experiências práticas e alinhadas às
    demandas do mercado.      
- Formação: Python - RocketSeat.
- Formação em andamento: Java - RocketSeat.
- Formação em andamento: HackTheBox CyberSecurity Academy.
- Formação em andamento: Linux Fundamentos - FIAP.
- Formação em andamento: Redes de Computadores - FIAP.
""")
    st.subheader("Experiências Profissionais")
    st.markdown("""
- Academia Point Fitness — Gestor de Atendimento (03/2020 a 08/2021)  
  Fui responsável por operar o sistema voltado ao cadastro de novos alunos, atualização de
informações e gestão de pagamentos. Isso otimizou o acompanhamento das mensalidades e
a emissão de recibos. Executei um atendimento ágil e organizado, garantindo uma boa
experiência aos clientes.

- Banco Bradesco — Estagiário em Cash Management (04/2025 - Atual)  
  Atuo no suporte aos processos de Cash Management, garantindo a fluidez e padronização
das informações enviadas ao time de implementação. Minhas atividades envolvem validar
dados em solicitações, conferir controles internos, revisar planilhas em Excel e
apresentações em PowerPoint, além de monitorar a atualização dos sistemas para assegurar
a confiabilidade das informações e apoiar a tomada de decisão.
""")

elif pagina == "Skills":
    st.header("Skills")
    st.subheader("Hard Skills")
    st.markdown("""
- Conhecimento de Python, Java, Java Swing, JavaScript, HTML, CSS, Cisco Packet Tracer.
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

elif pagina == "Análise de Dados":
    st.header("Análise de Dados")

    st.markdown(
        f"""
        <div style="background-color:#1E1E2F; padding:15px; border-radius:8px; color:#ffffff;">
            <h4>Resumo do Dataset</h4>
            Este dataset possui informações sobre ameaças cibernéticas globais de 2015 a 2024, incluindo variáveis categóricas e numéricas, 
            como país, tipo de ameaça, ano, quantidade de incidentes e valor de impacto estimado.  
            A análise permite identificar padrões, tendências e correlações relevantes para decisões estratégicas de segurança.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="background-color:#0E1117; padding:15px; border-radius:8px; color:#ffffff; margin-top:10px;">
            <h4>Perguntas de análise sugeridas</h4>
            <ul style="margin-left:20px;">
                <li>Qual o valor médio dos pedidos por categoria/status?</li>
                <li>Existe diferença significativa entre pedidos B2B e não-B2B?</li>
                <li>Há correlação entre quantidade (Qty) e valor do pedido?</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    sub = st.tabs(["Bases & Tipos", "Estatísticas", "Teste t (Welch)", "Gráficos"])

    with sub[0]:
        st.subheader("Amostra do Dataset")
        st.write("**Dimensões (completas):** ", df.shape)
        st.dataframe(df.head(20), use_container_width=True)
        st.subheader("Tipos de Variáveis e % de Nulos")
        st.dataframe(tabela_tipos(df), use_container_width=True)

    with sub[1]:
        st.subheader("Resumo Descritivo")
        cols_sel = st.multiselect("Colunas numéricas", options=colunas_num, default=colunas_num[:3])
        if cols_sel:
            resumo = estatisticas_basicas(df, cols_sel)
            st.dataframe(resumo, use_container_width=True)

    with sub[2]:
        st.subheader("Teste t de Welch")
        metrica = st.selectbox("Métrica numérica", options=colunas_num)
        grupo = st.selectbox("Variável categórica", options=colunas_cat)
        if metrica and grupo:
            categorias = df[grupo].dropna().astype(str).unique().tolist()
            if len(categorias) >= 2:
                cat1 = st.selectbox("Grupo A", options=categorias)
                cat2 = st.selectbox("Grupo B", options=categorias, index=1)
                df_a = pd.to_numeric(df[df[grupo].astype(str) == cat1][metrica], errors="coerce").dropna()
                df_b = pd.to_numeric(df[df[grupo].astype(str) == cat2][metrica], errors="coerce").dropna()
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
            fig = px.histogram(df, x=num_sel, nbins=30)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            cat_sel = st.selectbox("Boxplot - variável categórica", options=colunas_cat)
            num_box = st.selectbox("Boxplot - métrica numérica", options=colunas_num)
            fig = px.box(df, x=cat_sel, y=num_box, points="outliers")
            st.plotly_chart(fig, use_container_width=True)
