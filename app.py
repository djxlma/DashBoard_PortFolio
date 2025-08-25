import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard Cibersegurança | Djalma Andrade', layout='wide')

# Carregar dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("Global_Cybersecurity_Threats_2015-2024.csv")
    df = df.loc[:, ~df.columns.astype(str).str.contains(r"^Unnamed")]
    return df

df = carregar_dados()

# Navegação
aba = st.sidebar.radio("Navegação", ["🏠 Home", "🎓 Formação & Experiências", "🧠 Skills", "📊 Análise de Dados"])

if aba == "🏠 Home":
    st.title("🏠 Apresentação Pessoal")
    st.markdown("""
**Djalma Moreira de Andrade Filho**  
📧 djalmamoreirafilho@gmail.com  
🔗 LinkedIn - Djalma  
💻 GitHub - Djalma

**Objetivo Profissional:**  
Carreira em desenvolvimento na área de Segurança Ofensiva, com foco em testes de invasão e análise de vulnerabilidades. Experiência com suporte técnico, interação com clientes e fornecedores, e organização do ambiente de trabalho.
""")

elif aba == "🎓 Formação & Experiências":
    st.title("🎓 Formação Acadêmica")
    st.markdown("""
- **Engenharia de Software — FIAP (Fev/2024 - Dez/2027)**  
  Participação em projetos práticos com Tech Mahindra e Oceans 20.
""")
    st.title("💼 Experiências Profissionais")
    st.markdown("""
- **Academia Point Fitness — Gestor de Atendimento (03/2020 a 08/2021)**  
  Responsável por cadastro de alunos, gestão de pagamentos e atendimento.

- **Banco Bradesco — Estagiário em Cash Management (04/2025 - Atual)**  
  Suporte aos processos de Cash Management, validação de dados e controle de informações.
""")

elif aba == "🧠 Skills":
    st.title("🧠 Hard Skills")
    st.markdown("""
- Python, Java, Java Swing, JavaScript, HTML, CSS, Cisco Packet Tracer  
- Redes de Computadores (básico)  
- Linux (básico)  
- Pacote Office (intermediário)
""")
    st.title("🤝 Soft Skills")
    st.markdown("""
- Organização e atenção aos detalhes  
- Gestão de tempo e liderança  
- Produtividade, adaptabilidade, proatividade  
- Comunicação eficaz
""")

elif aba == "📊 Análise de Dados":
    st.title("📊 Análise de Ameaças Cibernéticas")
    st.subheader("Amostra do Dataset")
    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("💸 Perdas Financeiras por Tipo de Ataque")
    fig1 = px.box(df, x="Attack Type", y="Financial Loss (in Million $)", color="Attack Type")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("👥 Distribuição de Usuários Afetados")
    fig2 = px.histogram(df, x="Number of Affected Users", nbins=50)
    st.plotly_chart(fig2, use_container_width=True)
