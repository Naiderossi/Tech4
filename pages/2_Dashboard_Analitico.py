
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import math

st.set_page_config(page_title="Painel de Obesidade - Final", layout="wide")

# Carregar dados
df = pd.read_csv("Obesity_tratado.csv")

# Aplicar renomeações nas colunas para tornar nomes mais intuitivos
df["imc"] = df["weight"] / (df["height"] ** 2)
df["sedentario"] = df["faf"] == 0
bins = [0, 13, 18, 25, 35, 50, 100]
labels = ['Crianças', 'Adolescentes', '19-25', '26-35', '36-50', '51+']
df["faixa_personalizada"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)
df.columns = df.columns.str.lower()

# Sidebar
with st.sidebar:
    st.title("Painel de Controle")
    genero = st.multiselect("Gênero", df["gender"].unique(), default=list(df["gender"].unique()))
    transporte = st.multiselect("Transporte", df["mtrans"].unique(), default=list(df["mtrans"].unique()))
    idade = st.slider("Idade", int(df["age"].min()), int(df["age"].max()), (int(df["age"].min()), int(df["age"].max())))

df_filt = df[
    (df["gender"].isin(genero)) &
    (df["mtrans"].isin(transporte)) &
    (df["age"].between(idade[0], idade[1]))
]

# KPIs
st.markdown("## 🩺 Indicadores Gerais")
col1, col2, col3 = st.columns(3)
col1.metric("👥 Total de Entrevistados", len(df_filt))
col2.metric("🧔 Homens", int((df["gender"] == "Male").sum()))
col3.metric("👩 Mulheres", int((df["gender"] == "Female").sum()))

# Distribuição em cards traduzidos
translate_obesity = {
    "Insufficient_Weight": "Peso Insuficiente",
    "Normal_Weight": "Peso Normal",
    "Overweight_Level_I": "Sobrepeso I",
    "Overweight_Level_II": "Sobrepeso II",
    "Obesity_Type_I": "Obesidade I",
    "Obesity_Type_II": "Obesidade II",
    "Obesity_Type_III": "Obesidade III"
}
obesity_pct = df["obesity"].value_counts(normalize=True).mul(100).round(2).reset_index()
obesity_pct.columns = ["obesidade", "percentual"]
obesity_pct["obesidade_pt"] = obesity_pct["obesidade"].map(translate_obesity)

st.markdown("------")
st.markdown("## 🍩 Distribuição Percentual de Obesidade")

fig_donut = px.pie(
    df_pct,
    names="obesidade_pt",
    values="percentual",
    hole=0.5,
    color="obesidade_pt",
    color_discrete_sequence=px.colors.qualitative.Set2,
    title="Proporção de Níveis de Obesidade"
)

fig_donut.update_traces(
    textinfo='percent+label',
    textposition='outside',
    pull=[0.03 if i == df_pct["percentual"].idxmax() else 0 for i in range(len(df_pct))]
)

fig_donut.update_layout(
    showlegend=True,
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("------")
# IMC por idade com insight
st.markdown("## ⚖️ IMC Médio por Idade")
col4, col5 = st.columns([2, 1])
with col4:

    imc_idade = df.groupby("age")["imc"].mean().reset_index()
    fig_imc = px.line(imc_idade, x="age", y="imc", title="IMC Médio por Idade")
    pico_imc = imc_idade.loc[imc_idade["imc"].idxmax()]
    fig_imc.add_annotation(
        x=pico_imc["age"], y=pico_imc["imc"],
        text="📌 Pico de IMC médio",
        showarrow=True, arrowhead=2, ay=-40,
        font=dict(size=11, color="red"), bgcolor="white", bordercolor="red"
    )
   
    st.plotly_chart(fig_imc, use_container_width=True)
    with st.expander("💡 Ver insight"):
        st.markdown("O IMC médio aumenta até cerca de 25 anos.Após os 30, tende a estabilizar.")

# Alimentação
st.markdown("## 🍽️ Alimentação e Hidratação por Obesidade")
col6, col7 = st.columns([2, 1])
with col6:
    alim = df.groupby("obesity")[["ncp", "ch2o"]].mean().reset_index()
    fig_alim = px.bar(alim, x="obesity", y=["ncp", "ch2o"], barmode="group")
    st.plotly_chart(fig_alim, use_container_width=True)
    with st.expander("💡 Ver insight"):
        st.markdown("Pessoas com peso normal fazem mais refeições e bebem mais água.Reflete hábitos saudáveis.")

# Atividade física por obesidade
st.markdown("## 🏃 Atividade Física por Obesidade")
col8, col9 = st.columns([2, 1])
with col8:
    atividade = df_filt.groupby("obesity")["faf"].mean().reset_index()
    fig_faf = px.bar(atividade, x="obesity", y="faf", color="obesity")
    st.plotly_chart(fig_faf, use_container_width=True)
    with st.expander("💡 Ver insight"):
        st.markdown("Pessoas obesas são menos ativas fisicamente.Reflete relação inversa entre exercício e obesidade.")

# Sedentarismo
st.markdown("## 🛋️ Sedentarismo por Obesidade")
col10, col11 = st.columns([2, 1])
with col10:
    sedentarismo = df_filt.groupby(["obesity", "sedentario"]).size().reset_index(name="quantidade")
    fig_sed = px.bar(sedentarismo, x="obesity", y="quantidade", color="sedentario", barmode="group")
    st.plotly_chart(fig_sed, use_container_width=True)
    with st.expander("💡 Ver insight"):
        st.markdown("Obesidade tipo I e II concentram maior sedentarismo.")

# Fumantes
st.markdown("## 🚬 Fumantes por Obesidade")
col12, col13 = st.columns([2, 1])
with col12:
    fumantes = df_filt.groupby(["obesity", "smoke"]).size().reset_index(name="quantidade")
    fig_smoke = px.bar(fumantes, x="obesity", y="quantidade", color="smoke", barmode="group")
    st.plotly_chart(fig_smoke, use_container_width=True)
    with st.expander("💡 Ver insight"):
        st.markdown("Tabagismo aparece em todos os níveis.Mais comum em obesidade avançada.")


# Obesidade por faixa etária com anotação
st.markdown("## 📊 Obesidade por Faixa Etária")
col14, col15 = st.columns([2.5, 1])
with col14:
    faixa_ob = df.groupby(["faixa_personalizada", "obesity"]).size().reset_index(name="quantidade")

    # identificar faixa com mais registros totais
    total_faixa = faixa_ob.groupby("faixa_personalizada")["quantidade"].sum().reset_index()
    faixa_pico = total_faixa.loc[total_faixa["quantidade"].idxmax()]

    fig_ob_faixa = px.bar(faixa_ob, x="faixa_personalizada", y="quantidade", color="obesity", barmode="stack",
                          title="Obesidade por Faixa Etária com Anotação de Pico")

    fig_ob_faixa.add_annotation(
        x=faixa_pico["faixa_personalizada"],
        y=faixa_pico["quantidade"],
        text="📌 Faixa com mais casos",
        showarrow=True,
        arrowhead=2,
        ay=-40,
        font=dict(size=11, color="red"),
        bgcolor="white",
        bordercolor="red"
    )
    st.plotly_chart(fig_ob_faixa, use_container_width=True)
    with st.expander("💡 Ver insight"):
        st.markdown("Faixas de 19 a 50 anos concentram a maior parte dos casos.")


# Histórico Familiar vs Obesidade
st.markdown("## 🧬 Obesidade por Histórico Familiar")
col_fam1, col_fam2 = st.columns([2.2, 1])

with col_fam1:
    hist_fam = df.groupby(["family_history", "obesity"]).size().reset_index(name="quantidade")
    hist_fam["family_history_pt"] = hist_fam["family_history"].map({"yes": "Sim", "no": "Não"})
    hist_fam["obesidade_pt"] = hist_fam["obesity"].map({
        "Insufficient_Weight": "Peso Insuficiente",
        "Normal_Weight": "Peso Normal",
        "Overweight_Level_I": "Sobrepeso I",
        "Overweight_Level_II": "Sobrepeso II",
        "Obesity_Type_I": "Obesidade I",
        "Obesity_Type_II": "Obesidade II",
        "Obesity_Type_III": "Obesidade III"
    })

    fig_fam = px.bar(
        hist_fam,
        x="family_history_pt",
        y="quantidade",
        color="obesidade_pt",
        barmode="group",
        color_discrete_map={
            "Peso Insuficiente": "#4C78A8",
            "Peso Normal": "#A1CDEC",
            "Obesidade I": "#E45756",
            "Obesidade II": "#FFB5B8",
            "Obesidade III": "#FFA500",
            "Sobrepeso I": "#72B7B2",
            "Sobrepeso II": "#C2E7E5"
        },
        text="quantidade",
        title="Distribuição de Obesidade por Histórico Familiar"
    )

    fig_fam.update_layout(
        xaxis_title="Histórico Familiar",
        yaxis_title="Quantidade",
        legend_title="Nível de Obesidade",
        font=dict(size=14),
        plot_bgcolor="#fafafa"
    )
    fig_fam.update_traces(textposition="outside")

    grupo_pico = hist_fam.loc[hist_fam["quantidade"].idxmax()]
    fig_fam.add_annotation(
        x=grupo_pico["family_history_pt"],
        y=grupo_pico["quantidade"],
        text="📌 Maior ocorrência",
        showarrow=True,
        arrowhead=2,
        ay=-40,
        font=dict(size=11, color="red"),
        bgcolor="white",
        bordercolor="red"
    )

    st.plotly_chart(fig_fam, use_container_width=True)

with col_fam2:
    with st.expander("💡 Ver insight"):
        st.markdown("Indivíduos com histórico familiar têm maior incidência de obesidade grave.")


# 🔗 Correlação entre Fatores de Saúde e Comportamento
st.markdown("## 🧪 Correlação entre Fatores")

col_corr1, col_corr2 = st.columns([2, 1])
with col_corr1:
  rename_cols = {
    "age": "Idade",
    "height": "Altura (m)",
    "weight": "Peso (kg)",
    "ncp": "Refeições/dia",
    "ch2o": "Água/dia",
    "faf": "Atividade Física",
    "tue": "Tempo em Tela"
}

df_corr = df.rename(columns=rename_cols)
correlacao_pt = df_corr[list(rename_cols.values())].corr().round(2)

fig_corr = px.imshow(
    correlacao_pt,
    text_auto=True,
    color_continuous_scale='RdBu',
    title="Relação Entre Fatores de Saúde e Comportamento",
    aspect="auto"
)
fig_corr.update_layout(
    margin=dict(l=0, r=0, t=50, b=0),
    coloraxis_colorbar=dict(title="Correlação")
)
st.plotly_chart(fig_corr, use_container_width=True)

with st.expander("💡 Ver insight"):
      st.markdown("Pessoas mais altas tendem a pesar mais | Exercício físico se relaciona com maior consumo de água.|Idade está ligada à redução do tempo em tecnologia. |Obesidade é multifatorial:combinação de hábitos importa mais que um único fator.")


# Tabela final
st.markdown("## 📋 Tabela de Dados Filtrados")
st.dataframe(df_filt)



