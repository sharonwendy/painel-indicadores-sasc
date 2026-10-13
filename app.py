"""Painel de Indicadores Sociais – SASC / Piauí.

Para rodar localmente:  streamlit run app.py
Para atualizar os dados: edite os arquivos CSV da pasta data/ (uma linha por período).
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

DATA = Path(__file__).parent / "data"

st.set_page_config(
    page_title="Indicadores SASC – Piauí",
    page_icon="📊",
    layout="wide",
)

# Paleta (mesma ordem de cores em todo o painel)
CORES = ["#2E75B6", "#C55A11", "#7F7F7F", "#D9A400", "#548235", "#7030A0"]

# --------------------------------------------------------------------------------------
# Catálogo de indicadores: arquivo, unidade, formato, fonte e notas
# --------------------------------------------------------------------------------------
INDICADORES = {
    "1 · Benefício de Prestação Continuada (BPC)": dict(
        tema="Assistência social", arquivo="01_bpc.csv", destaque="Total",
        unidade="pessoas", fmt=",.0f",
        descricao="Pessoas beneficiárias do BPC no Piauí, por tipo de benefício.",
        fonte="MDS – VIS Data 3 (Benefício de Prestação Continuada, por município pagador).",
        nota="2026: posição de agosto.",
    ),
    "2 · Programa Bolsa Família": dict(
        tema="Assistência social", arquivo="02_bolsa_familia.csv", destaque="Pessoas beneficiárias",
        series=["Pessoas beneficiárias"], unidade="pessoas", fmt=",.0f",
        extra="Proporção (%)",
        descricao="Pessoas beneficiárias do Programa Bolsa Família e proporção em relação à população estimada.",
        fonte="MDS – VIS Data 3 (Programa Bolsa Família; Estimativa/Contagem da População).",
        nota="2022 não disponível na base. População projetada de 2023 usada para 2023 a 2026.",
    ),
    "3 · Taxa de desocupação": dict(
        tema="Trabalho e renda", arquivo="03_desocupacao.csv", destaque="Taxa de desocupação (%)",
        unidade="%", fmt=",.1f", sufixo="%", menor_melhor=True,
        descricao="Taxa de desocupação das pessoas de 14 anos ou mais, na semana de referência – Piauí.",
        fonte="IBGE – PNAD Contínua, SIDRA tabela 4093.",
        nota="Do 2º tri/2020 ao 1º tri/2022 os dados estaduais não estão disponíveis.",
    ),
    "4 · Rendimento médio mensal real": dict(
        tema="Trabalho e renda", arquivo="04_rendimento.csv", destaque="Rendimento médio mensal real (R$)",
        unidade="R$", fmt=",.0f", prefixo="R$ ",
        descricao="Rendimento médio mensal real habitualmente recebido em todos os trabalhos – Piauí.",
        fonte="IBGE – PNAD Contínua, SIDRA tabela 5436.",
        nota="Valores a preços do 2º trimestre de 2026. 2º tri/2020 a 1º tri/2022 não disponíveis.",
    ),
    "5 · Taxa de informalidade": dict(
        tema="Trabalho e renda", arquivo="05_informalidade.csv", destaque="Taxa de informalidade (%)",
        unidade="%", fmt=",.1f", sufixo="%", menor_melhor=True,
        descricao="Taxa de informalidade das pessoas de 14 anos ou mais ocupadas – Piauí.",
        fonte="IBGE – PNAD Contínua, SIDRA tabela 8529.",
        nota="Mantido o mesmo recorte de períodos dos indicadores 3 e 4.",
    ),
    "6 · Famílias tradicionais no CadÚnico": dict(
        tema="Povos e comunidades tradicionais", arquivo="06_familias_tradicionais.csv", destaque=None,
        unidade="famílias", fmt=",.0f", painel_separado=["Quilombolas"],
        descricao="Famílias indígenas, quilombolas, ciganas e de comunidades de terreiro cadastradas no CadÚnico – Piauí.",
        fonte="MDS – VIS Data 3 (aplicacoes.cidadania.gov.br/vis/data3).",
        nota="2026: posição de setembro. As famílias quilombolas aparecem no painel de cima, com escala própria, "
             "para que os demais grupos fiquem legíveis.",
    ),
    "7 · Registros de injúria racial": dict(
        tema="Direitos humanos e segurança", arquivo="07_injuria_racial.csv", destaque="Taxa por 100 mil habitantes",
        unidade="por 100 mil hab.", fmt=",.2f", menor_melhor=True,
        descricao="Taxa de registros de injúria racial por 100 mil habitantes – Piauí.",
        fonte="Fórum Brasileiro de Segurança Pública – Anuário Brasileiro de Segurança Pública (edições 2022 a 2026).",
        nota="2024 atualizado conforme o Anuário 2026.",
    ),
    "8 · Registros de racismo": dict(
        tema="Direitos humanos e segurança", arquivo="08_racismo.csv", destaque="Taxa por 100 mil habitantes",
        unidade="por 100 mil hab.", fmt=",.2f", menor_melhor=True,
        descricao="Taxa de registros de racismo por 100 mil habitantes – Piauí.",
        fonte="Fórum Brasileiro de Segurança Pública – Anuário Brasileiro de Segurança Pública (edições 2022, 2023 e 2026).",
        nota="O salto a partir de 2024 pode refletir mudança na forma de registro (equiparação da injúria racial ao racismo, Lei 14.532/2023).",
    ),
    "9 · Violência contra a população LGBTQIA+": dict(
        tema="Direitos humanos e segurança", arquivo="09_lgbtqia.csv", destaque=None,
        series=["Lesão corporal dolosa", "Homicídio doloso", "Estupro"],
        extra="Homicídios dolosos – total Piauí",
        unidade="registros", fmt=",.0f", menor_melhor=True,
        descricao="Registros de crimes contra pessoas LGBTQIA+ no Piauí, por tipo.",
        fonte="Fórum Brasileiro de Segurança Pública – Anuário Brasileiro de Segurança Pública (edições 2021 a 2026).",
        nota="2024 atualizado conforme o Anuário 2026. Dados de 2026 serão divulgados em julho de 2027.",
    ),
    "10 · Índice de Desenvolvimento Humano (IDHM)": dict(
        tema="Desenvolvimento humano", arquivo="10_idhm.csv", destaque="IDHM",
        series=["IDHM", "IDHM Renda", "IDHM Educação", "IDHM Longevidade"], padrao=["IDHM"],
        unidade="índice", fmt=",.3f",
        descricao="IDHM do Piauí e suas dimensões (renda, educação e longevidade).",
        fonte="PNUD, Ipea e FJP – Atlas do Desenvolvimento Humano no Brasil / Radar IDHM 2026.",
        nota="2023 e 2024 seguem a nova série do Radar IDHM e não são diretamente comparáveis com 2016–2021. "
             "Posição do Piauí no ranking das UFs em 2024: 19º.",
    ),
}


@st.cache_data
def carregar(arquivo: str) -> pd.DataFrame:
    df = pd.read_csv(DATA / arquivo, dtype={"periodo": str})
    return df


def br(valor, fmt=",.0f", prefixo="", sufixo=""):
    """Formata número no padrão brasileiro (1.234,5)."""
    if pd.isna(valor):
        return "–"
    s = format(valor, fmt).replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{prefixo}{s}{sufixo}"


def series_do(cfg, df):
    if cfg.get("series"):
        return cfg["series"]
    return [c for c in df.columns if c not in ("periodo", "Série", cfg.get("extra"))]


def _posicoes(df, series):
    """Posição dos rótulos ponto a ponto: a série mais alta em cima, a mais baixa embaixo."""
    pos = {s: [] for s in series}
    for _, linha in df[series].iterrows():
        ordem = linha.dropna().sort_values()
        for k, (nome, v) in enumerate(ordem.items()):
            if k == len(ordem) - 1:
                pos[nome].append("top center")
            elif k == 0:
                pos[nome].append("bottom center")
            else:
                acima, abaixo = ordem.iloc[k + 1] - v, v - ordem.iloc[k - 1]
                pos[nome].append("top center" if acima > abaixo else "bottom center")
        for nome in series:
            if nome not in ordem.index:
                pos[nome].append("top center")
    return pos


def _tracos(df, cfg, series, rotulos, cor_inicial=0):
    pos = _posicoes(df, series)
    nomes = list(df.columns.drop("periodo"))
    tracos = []
    for s in series:
        cor = CORES[nomes.index(s) % len(CORES)] if s in nomes else CORES[cor_inicial]
        texto = [br(v, cfg["fmt"], cfg.get("prefixo", ""), cfg.get("sufixo", "")) for v in df[s]]
        tracos.append(go.Scatter(
            x=df["periodo"], y=df[s], name=s, mode="lines+markers+text" if rotulos else "lines+markers",
            text=texto, textposition=pos[s], textfont=dict(size=12, color=cor),
            line=dict(color=cor, width=3), marker=dict(size=8, line=dict(color="white", width=1.5)),
            hovertemplate="%{x}<br>" + s + ": %{text}<extra></extra>", cliponaxis=False,
        ))
    return tracos


def _folga(fig, valores, **kw):
    mx = max(valores) if len(valores) else 1
    fig.update_yaxes(range=[-mx * 0.12, mx * 1.15], **kw)


def grafico(df, cfg, series, altura=460, rotulos=True):
    separadas = [s for s in cfg.get("painel_separado", []) if s in series]
    demais = [s for s in series if s not in separadas]
    multiplas = len(series) > 1
    if separadas and demais:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_heights=[0.4, 0.6])
        for t in _tracos(df, cfg, separadas, rotulos):
            fig.add_trace(t, row=1, col=1)
        for t in _tracos(df, cfg, demais, rotulos):
            fig.add_trace(t, row=2, col=1)
        _folga(fig, df[separadas].to_numpy().ravel(), row=1, col=1)
        _folga(fig, df[demais].to_numpy().ravel(), row=2, col=1)
        altura = 620
    else:
        fig = go.Figure(_tracos(df, cfg, series, rotulos))
        _folga(fig, df[series].to_numpy().ravel())
    fig.update_layout(
        height=altura, separators=",.", margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", y=1.08, x=0), showlegend=multiplas,
        plot_bgcolor="white", hovermode="x unified" if multiplas else "closest",
    )
    fig.update_xaxes(type="category", showgrid=False, tickangle=-45 if len(df) > 12 else 0)
    fig.update_yaxes(showgrid=True, gridcolor="#EEEEEE", tickformat=",", zeroline=True, zerolinecolor="#CCCCCC")
    return fig


def card(nome, cfg):
    df = carregar(cfg["arquivo"])
    col = cfg["destaque"]
    if col is None:  # indicadores com várias séries: usa a soma
        col = "_total"
        df = df.assign(_total=df[series_do(cfg, df)].sum(axis=1))
    atual, ant = df[col].iloc[-1], df[col].iloc[-2]
    delta = atual - ant
    st.metric(
        label=f"{nome.split(' · ')[1]} ({df['periodo'].iloc[-1]})",
        value=br(atual, cfg["fmt"], cfg.get("prefixo", ""), cfg.get("sufixo", "")),
        delta=f"{br(delta, cfg['fmt'])} vs. {df['periodo'].iloc[-2]}",
        delta_color="inverse" if cfg.get("menor_melhor") else "normal",
    )


# --------------------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------------------
st.sidebar.title("📊 Indicadores SASC")
st.sidebar.caption("Secretaria da Assistência Social e Cidadania – Piauí")
paginas = ["Visão geral"] + list(INDICADORES)
escolha = st.sidebar.radio("Escolha o indicador", paginas, label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.caption("Dados atualizados em outubro de 2026.")

if escolha == "Visão geral":
    st.title("Painel de Indicadores Sociais – Piauí")
    st.caption("Último valor disponível de cada indicador e variação em relação ao período anterior. "
               "Escolha um indicador no menu ao lado para ver a série completa.")
    temas = {}
    for nome, cfg in INDICADORES.items():
        temas.setdefault(cfg["tema"], []).append((nome, cfg))
    for tema, itens in temas.items():
        st.subheader(tema)
        cols = st.columns(3)
        for i, (nome, cfg) in enumerate(itens):
            with cols[i % 3]:
                with st.container(border=True):
                    card(nome, cfg)
else:
    cfg = INDICADORES[escolha]
    df = carregar(cfg["arquivo"])
    st.title(escolha.split(" · ")[1])
    st.caption(f"{cfg['tema']} · {cfg['descricao']}")

    series = series_do(cfg, df)
    if len(series) > 1:
        series = st.multiselect("Séries exibidas", series, default=cfg.get("padrao", series))
    if not series:
        st.info("Selecione ao menos uma série.")
        st.stop()

    rotulos = st.toggle("Mostrar valores nos pontos", value=True)
    st.plotly_chart(grafico(df, cfg, series, rotulos=rotulos), width="stretch")

    if cfg.get("extra") and cfg["extra"] in df.columns:
        st.plotly_chart(grafico(df, {**cfg, "fmt": ",.1f" if "%" in cfg["extra"] else ",.0f",
                                     "sufixo": "%" if "%" in cfg["extra"] else "", "prefixo": ""},
                                [cfg["extra"]], altura=320, rotulos=rotulos),
                        width="stretch")

    if cfg.get("nota"):
        st.info(cfg["nota"], icon="ℹ️")
    st.markdown(f"**Fonte:** {cfg['fonte']}")

    with st.expander("Ver tabela de dados"):
        tabela = df.copy()
        for c in tabela.columns:
            if c not in ("periodo", "Série") and pd.api.types.is_numeric_dtype(tabela[c]):
                f = ",.1f" if "%" in c else cfg["fmt"]
                tabela[c] = tabela[c].map(lambda v, f=f: br(v, f))
        st.dataframe(tabela.rename(columns={"periodo": "Período"}), hide_index=True, width="stretch")
        st.download_button("Baixar CSV", df.to_csv(index=False).encode("utf-8"),
                           file_name=cfg["arquivo"], mime="text/csv")
