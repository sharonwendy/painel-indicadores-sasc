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

# Cópia dos dados dentro do app: usada só se o CSV não estiver no repositório.
DADOS_EMBUTIDOS = {
    '01_bpc.csv': 'periodo,Pessoas com deficiência,Idosos,Total\n2019,54929,22365,78360\n2020,55501,22859,78360\n2021,56227,22993,79220\n2022,59592,24158,83750\n2023,67318,25996,93314\n2024,78104,27016,105120\n2025,83551,26593,110144\n2026/08,86346,27042,113388\n',
    '02_bolsa_familia.csv': 'periodo,Pessoas beneficiárias,População estimada,Proporção (%)\n2019,1335479,3273227,40.8\n2020,1374183,3281480,41.88\n2021,1381779,3289290,42.01\n2023,1557992,3302519,47.18\n2024,1528107,3302519,46.27\n2025,1425449,3302519,43.16\n2026,1381331,3302519,41.83\n',
    '03_desocupacao.csv': 'periodo,Taxa de desocupação (%)\n1º tri 2019,12.9\n2º tri 2019,13.0\n3º tri 2019,12.9\n4º tri 2019,13.3\n1º tri 2020,14.2\n2º tri 2022,9.4\n3º tri 2022,9.3\n4º tri 2022,9.5\n1º tri 2023,11.1\n2º tri 2023,9.7\n3º tri 2023,9.9\n4º tri 2023,10.6\n1º tri 2024,10.0\n2º tri 2024,7.6\n3º tri 2024,8.0\n4º tri 2024,7.5\n1º tri 2025,10.2\n2º tri 2025,8.5\n3º tri 2025,7.5\n4º tri 2025,8.0\n1º tri 2026,8.9\n2º tri 2026,8.3\n',
    '04_rendimento.csv': 'periodo,Rendimento médio mensal real (R$)\n1º tri 2019,2231\n2º tri 2019,2134\n3º tri 2019,2074\n4º tri 2019,1957\n1º tri 2020,2011\n2º tri 2022,2197\n3º tri 2022,2449\n4º tri 2022,2393\n1º tri 2023,2656\n2º tri 2023,2618\n3º tri 2023,2532\n4º tri 2023,2497\n1º tri 2024,2528\n2º tri 2024,2589\n3º tri 2024,2583\n4º tri 2024,2583\n1º tri 2025,2667\n2º tri 2025,2537\n3º tri 2025,2586\n4º tri 2025,2681\n1º tri 2026,2690\n2º tri 2026,2547\n',
    '05_informalidade.csv': 'periodo,Taxa de informalidade (%)\n1º tri 2019,58.8\n2º tri 2019,58.9\n3º tri 2019,60.2\n4º tri 2019,59.2\n1º tri 2020,58.7\n2º tri 2022,56.1\n3º tri 2022,54.4\n4º tri 2022,54.0\n1º tri 2023,52.4\n2º tri 2023,52.2\n3º tri 2023,55.0\n4º tri 2023,53.4\n1º tri 2024,54.8\n2º tri 2024,54.6\n3º tri 2024,54.4\n4º tri 2024,54.8\n1º tri 2025,54.5\n2º tri 2025,51.8\n3º tri 2025,52.7\n4º tri 2025,50.4\n1º tri 2026,50.2\n2º tri 2026,49.5\n',
    '06_familias_tradicionais.csv': 'periodo,Indígenas,Quilombolas,Ciganas,Comunidades de terreiro\n2019,112,5522,306,857\n2020,115,5580,305,730\n2021,180,6439,294,716\n2022,264,7902,301,862\n2023,488,8823,283,1612\n2024,1016,10330,265,1434\n2025,1483,11733,320,1261\n2026/09,1665,12952,362,1232\n',
    '07_injuria_racial.csv': 'periodo,Taxa por 100 mil habitantes\n2020,5.94\n2021,7.46\n2022,8.13\n2023,8.94\n2024,11.67\n2025,12.35\n',
    '08_racismo.csv': 'periodo,Taxa por 100 mil habitantes\n2020,0.24\n2021,0.76\n2022,1.32\n2023,2.3\n2024,15.94\n2025,16.63\n',
    '09_lgbtqia.csv': 'periodo,Lesão corporal dolosa,Homicídio doloso,Estupro,Homicídios dolosos – total Piauí\n2019,12,2,2,539\n2020,32,2,5,659\n2021,13,6,4,736\n2022,41,5,3,756\n2023,69,8,5,677\n2024,57,5,7,626\n2025,67,2,10,526\n',
    '10_idhm.csv': 'periodo,IDHM,IDHM Renda,IDHM Educação,IDHM Longevidade,Série\n1991,0.362,0.488,0.164,0.595,Censo\n2000,0.484,0.556,0.301,0.676,Censo\n2010,0.646,0.635,0.547,0.777,Censo\n2016,0.685,0.655,0.642,0.766,PNAD (série antiga)\n2017,0.694,0.653,0.665,0.769,PNAD (série antiga)\n2018,0.699,0.658,0.671,0.772,PNAD (série antiga)\n2019,0.706,0.657,0.692,0.775,PNAD (série antiga)\n2020,0.708,0.659,0.7,0.768,PNAD (série antiga)\n2021,0.69,0.649,0.698,0.726,PNAD (série antiga)\n2023,0.761,0.699,0.731,0.863,Radar IDHM 2026 (série nova)\n2024,0.764,0.695,0.742,0.866,Radar IDHM 2026 (série nova)\n',
    '11_gini.csv': 'periodo,Piauí,Brasil\n2019,0.538,0.543\n2020,0.474,0.523\n2021,0.515,0.543\n2022,0.518,0.517\n2023,0.549,0.517\n2024,0.493,0.504\n2025,0.508,0.511\n',
    '12_situacao_rua.csv': 'periodo,Total de famílias,Renda até meio salário-mínimo,Renda acima de meio salário-mínimo\n2019,601,582,19\n2020,629,604,25\n2021,663,638,25\n2022,903,883,20\n2023,1309,1242,67\n2024,1655,1535,120\n2025,1753,1624,129\n2026/09,1998,1832,166\n',
    '13_trabalho_infantil.csv': 'periodo,Crianças e adolescentes no CadÚnico em situação de trabalho infantil\n2023,770\n2024,443\n2025,218\n2026/08,134\n',
    '14_trabalho_infantil_resgatados.csv': 'periodo,Crianças e adolescentes afastados pela fiscalização\n2017,8\n2018,12\n2019,15\n2020,4\n2021,1\n2022,14\n2023,25\n2024,11\n2025,57\n',
    '15_idosos_denuncias.csv': 'periodo,Denúncias – Piauí\n2022,1157\n2023,1929\n2024,2434\n',
    '16_idge.csv': 'periodo,SASC,Piauí (média dos órgãos),Posição da SASC no ranking,Total de órgãos\n03/2024,0.62,0.58,9,28\n04/2024,0.62,0.58,10,28\n05/2024,0.74,0.68,9,28\n06/2024,0.74,0.72,14,28\n07/2024,0.58,0.73,26,28\n08/2024,0.68,0.76,21,28\n09/2024,0.78,0.78,18,32\n10/2024,0.79,0.65,28,32\n11/2024,0.48,0.79,28,32\n12/2024,0.48,0.76,30,32\n01/2025,0.4,0.72,30,31\n02/2025,0.45,0.76,29,32\n03/2025,0.4,0.79,29,32\n04/2025,0.4,0.79,29,32\n05/2025,0.4,0.77,28,32\n06/2025,0.4,0.78,28,32\n07/2025,0.4,0.77,27,32\n08/2025,0.4,0.78,27,32\n09/2025,0.56,0.77,,\n10/2025,0.56,0.78,,\n11/2025,0.56,0.8,,\n',
}

st.set_page_config(
    page_title="Indicadores SASC – Piauí",
    page_icon="📊",
    layout="wide",
)

# Paleta (mesma ordem de cores em todo o painel)
# Cores oficiais do Governo do Piauí (Manual de Identidade Visual 2023)
CORES = ["#034EA2", "#EF4123", "#007932", "#FDB913", "#231F20", "#5B8BD0"]

# --------------------------------------------------------------------------------------
# Catálogo de indicadores: arquivo, unidade, formato, fonte e notas
# --------------------------------------------------------------------------------------
INDICADORES = {
    "1 · Benefício de Prestação Continuada (BPC)": dict(
        tema="Assistência social", arquivo="01_bpc.csv", neutro=True, destaque="Total",
        unidade="pessoas", fmt=",.0f",
        descricao="Pessoas beneficiárias do BPC no Piauí, por tipo de benefício.",
        fonte="MDS – VIS Data 3 (Benefício de Prestação Continuada, por município pagador).",
        nota="2026: posição de agosto.",
    ),
    "2 · Programa Bolsa Família": dict(
        tema="Assistência social", arquivo="02_bolsa_familia.csv", neutro=True, destaque="Pessoas beneficiárias",
        series=["Pessoas beneficiárias"], unidade="pessoas", fmt=",.0f",
        extra="Proporção (%)", unidade_extra="% da população estimada do Piauí",
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
        tema="Povos e comunidades tradicionais", arquivo="06_familias_tradicionais.csv", neutro=True, destaque=None,
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
        extra="Homicídios dolosos – total Piauí", unidade_extra="vítimas de homicídio doloso (total do estado)",
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
    "11 · Índice de Gini": dict(
        tema="Trabalho e renda", arquivo="11_gini.csv", destaque="Piauí",
        series=["Piauí", "Brasil"], unidade="índice", fmt=",.3f", menor_melhor=True,
        descricao="Índice de Gini do rendimento domiciliar per capita – quanto maior, mais desigual.",
        fonte="IBGE – PNAD Contínua, Rendimento de todas as fontes (SIDRA tabela 7435).",
        nota="Valores pelo ano a que os dados se referem. No IBGE Cidades o 'ano' é o da publicação (um ano depois).",
    ),
    "12 · Famílias em situação de rua no CadÚnico": dict(
        tema="Assistência social", arquivo="12_situacao_rua.csv", neutro=True, destaque="Total de famílias",
        unidade="famílias", fmt=",.0f", padrao=["Total de famílias"],
        descricao="Famílias em situação de rua inscritas no Cadastro Único – Piauí, por faixa de renda per capita.",
        fonte="MDS – VIS Data 3 (Famílias em situação de rua cadastradas no Cadastro Único).",
        nota="Posição de dezembro de cada ano; 2026 = setembro. Total = até meio salário-mínimo + acima de meio salário-mínimo.",
    ),
    "13 · Trabalho infantil no CadÚnico": dict(
        tema="Assistência social", arquivo="13_trabalho_infantil.csv",
        destaque="Crianças e adolescentes no CadÚnico em situação de trabalho infantil",
        unidade="pessoas", fmt=",.0f", menor_melhor=True,
        descricao="Crianças e adolescentes (5 a 17 anos) com marcação de trabalho infantil no Cadastro Único – Piauí.",
        fonte="MDS – VIS Data 3 (Famílias e pessoas em situação de trabalho infantil inscritas no Cadastro Único).",
        nota="Posição de dezembro de cada ano; 2026 = agosto.",
    ),
    "14 · Trabalho infantil – afastamentos pela fiscalização": dict(
        tema="Assistência social", arquivo="14_trabalho_infantil_resgatados.csv", neutro=True,
        destaque="Crianças e adolescentes afastados pela fiscalização",
        unidade="pessoas", fmt=",.0f",
        descricao="Crianças e adolescentes afastados do trabalho infantil em ações da Auditoria-Fiscal do Trabalho – Piauí.",
        fonte="Ministério do Trabalho e Emprego – Radar SIT / Auditoria-Fiscal do Trabalho.",
        nota="2025: 57 afastamentos em 354 ações fiscais. Jan–abr/2026: 17.",
    ),
    "15 · Violações contra pessoas idosas": dict(
        tema="Direitos humanos e segurança", arquivo="15_idosos_denuncias.csv", destaque="Denúncias – Piauí",
        unidade="denúncias", fmt=",.0f", menor_melhor=True,
        descricao="Denúncias de violações de direitos humanos de pessoas idosas registradas na Ouvidoria Nacional (Disque 100) – Piauí.",
        fonte="MDHC – Ouvidoria Nacional de Direitos Humanos / ObservaDH.",
        nota="Uma denúncia pode conter várias violações. Brasil, 2024: 179.378 denúncias.",
    ),
    "16 · IDGE – Eficiência Governamental": dict(
        tema="Gestão", arquivo="16_idge.csv", destaque="SASC",
        series=["SASC", "Piauí (média dos órgãos)"], extra="Posição da SASC no ranking", unidade_extra="posição",
        unidade="índice", fmt=",.2f",
        descricao="Indicador de Desempenho de Eficiência Governamental (IDGE) da SASC comparado à média do Governo do Piauí.",
        fonte="Governo do Estado do Piauí – IDGE (dados internos informados pela SASC).",
        nota="Série mensal até nov/2025 (ranking até ago/2025) — ainda não atualizada. No ranking, quanto menor a posição, melhor.",
    ),
}


@st.cache_data
def carregar(arquivo: str) -> pd.DataFrame:
    # Procura o CSV na pasta data/ e, se não achar, ao lado do app.py (caso a pasta não tenha subido no GitHub)
    for pasta in (DATA, Path(__file__).parent):
        caminho = pasta / arquivo
        if caminho.exists():
            return pd.read_csv(caminho, dtype={"periodo": str})
    if arquivo in DADOS_EMBUTIDOS:
        import io
        return pd.read_csv(io.StringIO(DADOS_EMBUTIDOS[arquivo]), dtype={"periodo": str})
    st.error(f"Arquivo de dados não encontrado: {arquivo}.")
    st.stop()


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


def grafico(df, cfg, series, altura=460, rotulos=True, titulo=None):
    separadas = [s for s in cfg.get("painel_separado", []) if s in series]
    demais = [s for s in series if s not in separadas]
    multiplas = len(series) > 1
    if separadas and demais:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.12, row_heights=[0.4, 0.6],
                            subplot_titles=(" e ".join(separadas) + " (escala própria)", " · ".join(demais)))
        for t in _tracos(df, cfg, separadas, rotulos):
            fig.add_trace(t, row=1, col=1)
        for t in _tracos(df, cfg, demais, rotulos):
            fig.add_trace(t, row=2, col=1)
        _folga(fig, df[separadas].to_numpy().ravel(), row=1, col=1)
        _folga(fig, df[demais].to_numpy().ravel(), row=2, col=1)
        altura = 620
        fig.update_annotations(x=0.01, xanchor="left", font=dict(size=13, color="#4B5563"))
    else:
        fig = go.Figure(_tracos(df, cfg, series, rotulos))
        _folga(fig, df[series].to_numpy().ravel())
    if titulo is None:
        titulo = series[0] if not multiplas else cfg.get("titulo_grafico", "")
    unidade = cfg.get("unidade", "")
    texto_titulo = f"<b>{titulo}</b>" if titulo else ""
    texto_titulo = texto_titulo + (f"<br><span style='font-size:12px;color:#6B7280;font-weight:normal'>{unidade}</span>" if unidade else "")
    fig.update_layout(
        height=altura + 50, separators=",.", margin=dict(l=10, r=10, t=95 if multiplas else 75, b=10),
        title=dict(text=texto_titulo, x=0.01, xanchor="left", xref="paper", yref="container", y=1, yanchor="top",
                   pad=dict(t=14, l=0), font=dict(size=16, color="#1F2937")),
        legend=dict(orientation="h", y=1.02, yanchor="bottom", x=0.01, font=dict(size=12)), showlegend=multiplas,
        plot_bgcolor="white", paper_bgcolor="white", hovermode="x unified" if multiplas else "closest",
        template="plotly_white", font=dict(color="#374151", family="Montserrat, sans-serif"),
    )
    if separadas and demais:
        fig.update_layout(margin=dict(t=125), legend=dict(y=1.09))
    fig.update_xaxes(type="category", showgrid=False, tickangle=-45 if len(df) > 12 else 0)
    fig.update_yaxes(showgrid=True, gridcolor="#EEEEEE", tickformat=",", zeroline=True, zerolinecolor="#CCCCCC")
    return fig


TEMA_COR = {
    "Assistência social": "#034EA2",
    "Trabalho e renda": "#007932",
    "Povos e comunidades tradicionais": "#FDB913",
    "Direitos humanos e segurança": "#EF4123",
    "Desenvolvimento humano": "#034EA2",
    "Gestão": "#231F20",
}
TEMA_ICONE = {
    "Assistência social": "🤝",
    "Trabalho e renda": "💼",
    "Povos e comunidades tradicionais": "🌿",
    "Direitos humanos e segurança": "⚖️",
    "Desenvolvimento humano": "📈",
    "Gestão": "🏛️",
}

st.markdown("""
<style>
  @import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap");
  html, body, .stApp, .stApp *:not([class*="icon"]):not([data-testid*="Icon"]) {font-family: "Montserrat", sans-serif;}
  .faixa {height: 7px; border-radius: 0 0 8px 8px; margin: 0 0 12px 0;
          background: linear-gradient(90deg, #FDB913 0 33.3%, #EF4123 33.3% 66.6%, #007932 66.6% 100%);}
  .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1300px;}
  [data-testid="stSidebar"] {background: #FFFFFF; border-right: 1px solid #E5E7EB;}
  [data-testid="stSidebar"] .stRadio label p {font-size: 0.92rem;}
  .hero {background: linear-gradient(120deg, #034EA2 0%, #0A63C9 100%); color: #fff;
         border-radius: 16px 16px 0 0; padding: 28px 32px; margin-bottom: 0;}
  .hero h1 {color: #fff; font-size: 2rem; margin: 0 0 6px 0; padding: 0;}
  .hero p {color: #E6F4F8; margin: 0; font-size: 1rem;}
  .hero .chips {margin-top: 14px;}
  .hero .chip {display: inline-block; background: rgba(255,255,255,.18); border-radius: 999px;
               padding: 4px 12px; margin-right: 8px; font-size: .85rem;}
  .tema {display: flex; align-items: center; gap: 10px; margin: 28px 0 10px 0;}
  .tema .barra {width: 6px; height: 26px; border-radius: 4px;}
  .tema h3 {margin: 0; padding: 0; font-size: 1.25rem; color: #1F2937;}
  .kpi {border-top: 4px solid var(--cor); margin: -16px -16px 0 -16px; padding: 14px 16px 0 16px;
        border-radius: 14px 14px 0 0;}
  .kpi .titulo {font-size: .88rem; color: #4B5563; font-weight: 600; min-height: 2.4em; line-height: 1.2em;}
  .kpi .valor {font-size: 1.9rem; font-weight: 700; color: #111827; margin: 4px 0 2px 0;}
  .kpi .ref {font-size: .78rem; color: #6B7280;}
  .badge {display: inline-block; font-size: .78rem; font-weight: 600; border-radius: 999px;
          padding: 2px 10px; margin-top: 6px;}
  .bom {background: #E7F6EC; color: #1E7B3A;} .ruim {background: #FDECEC; color: #B42318;}
  .neutro {background: #F2F4F7; color: #475467;}
  div[data-testid="stVerticalBlockBorderWrapper"] {background: #fff; border-radius: 14px !important;
        box-shadow: 0 1px 3px rgba(16,24,40,.06);}
  .stButton button {border-radius: 999px; font-size: .8rem; padding: 2px 12px;}

  /* Força aparência clara mesmo se o tema do Streamlit estiver escuro */
  .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {background: #F5F7FA !important; color: #1F2937 !important;}
  [data-testid="stHeader"] {background: rgba(245,247,250,.9) !important;}
  .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp label, .stApp li,
  .stApp [data-testid="stMarkdownContainer"], .stApp [data-testid="stCaptionContainer"],
  .stApp [data-testid="stWidgetLabel"] * {color: #1F2937 !important;}
  .stApp [data-testid="stCaptionContainer"] * {color: #6B7280 !important;}
  [data-testid="stSidebar"], [data-testid="stSidebar"] > div {background: #FFFFFF !important;}
  [data-testid="stSidebar"] * {color: #1F2937 !important;}
  [data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {color: #6B7280 !important;}
  div[data-testid="stVerticalBlockBorderWrapper"] {background: #FFFFFF !important; border-color: #E5E7EB !important;}
  .kpi .titulo {color: #4B5563 !important;} .kpi .valor {color: #111827 !important;} .kpi .ref {color: #6B7280 !important;}
  .bom {color: #1E7B3A !important;} .ruim {color: #B42318 !important;} .neutro {color: #475467 !important;}
  .stButton button {background: #FFFFFF !important; color: #034EA2 !important; border: 1px solid #034EA2 !important;}
  .stButton button:hover {background: #034EA2 !important; color: #FFFFFF !important;}
  .stButton button p {color: inherit !important;}
  [data-baseweb="select"] > div, [data-baseweb="input"] > div {background: #FFFFFF !important; color: #1F2937 !important;}
  [data-testid="stExpander"] details {background: #FFFFFF !important; border-color: #E5E7EB !important;}
  [data-testid="stExpander"] summary * {color: #1F2937 !important;}
  .stAlert {background: #E8F1F8 !important;} .stAlert * {color: #1F4E79 !important;}
  .hero, .hero * {color: #FFFFFF !important;} .hero p {color: #E6F4F8 !important;}

  [data-testid="stRadioOption"] > div > div:first-child {background-color: #FFFFFF !important; border: 2px solid #9CA3AF !important;}
  [data-testid="stRadioOption"] > div > div:first-child > div {background-color: transparent !important;}
  [data-testid="stRadioOption"][data-selected="true"] > div > div:first-child {background-color: #034EA2 !important; border-color: #034EA2 !important;}
  [data-testid="stRadioOption"][data-selected="true"] > div > div:first-child > div {background-color: #FFFFFF !important;}
  [data-testid="stRadioOption"][data-selected="true"] p {font-weight: 700; color: #034EA2 !important;}
  table.tabela {width: 100%; border-collapse: collapse; background: #FFFFFF; font-size: .9rem;}
  table.tabela th {background: #034EA2; color: #FFFFFF !important; text-align: left; padding: 8px 10px;}
  table.tabela td {padding: 7px 10px; border-bottom: 1px solid #E5E7EB; color: #1F2937;}
  table.tabela tr:nth-child(even) td {background: #F8FAFC;}
  .stDownloadButton button {background: #FFFFFF !important; color: #034EA2 !important; border: 1px solid #034EA2 !important;}
  .stDownloadButton button p {color: inherit !important;}
  [data-baseweb="tag"] {background: #034EA2 !important;} [data-baseweb="tag"] * {color: #FFFFFF !important;}
</style>
""", unsafe_allow_html=True)


def resumo(cfg):
    df = carregar(cfg["arquivo"])
    col = cfg["destaque"]
    if col is None:  # indicadores com várias séries: usa a soma
        col = "_total"
        df = df.assign(_total=df[series_do(cfg, df)].sum(axis=1))
    serie = df[["periodo", col]].dropna()
    return serie["periodo"].tolist(), serie[col].tolist()


def sparkline(periodos, valores, cor):
    fig = go.Figure(go.Scatter(x=periodos, y=valores, mode="lines", line=dict(color=cor, width=2.5),
                               fill="tozeroy", fillcolor=cor + "1A", hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[periodos[-1]], y=[valores[-1]], mode="markers",
                             marker=dict(color=cor, size=7), hoverinfo="skip"))
    mn, mx = min(valores), max(valores)
    pad = (mx - mn) * 0.15 or abs(mx) * 0.1 or 1
    fig.update_layout(height=60, margin=dict(l=0, r=0, t=4, b=0), showlegend=False,
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    fig.update_xaxes(visible=False, type="category")
    fig.update_yaxes(visible=False, range=[mn - pad, mx + pad])
    return fig


def ir_para(nome):
    st.session_state["nav"] = nome


def card(nome, cfg):
    periodos, valores = resumo(cfg)
    cor = TEMA_COR.get(cfg["tema"], CORES[0])
    atual, ant = valores[-1], valores[-2]
    delta = atual - ant
    pct = (delta / ant * 100) if ant else 0
    if abs(delta) < 1e-12:
        classe, seta = "neutro", "→"
    elif cfg.get("neutro"):
        classe, seta = "neutro", ("▲" if delta > 0 else "▼")
    else:
        melhora = (delta < 0) if cfg.get("menor_melhor") else (delta > 0)
        classe, seta = ("bom" if melhora else "ruim"), ("▲" if delta > 0 else "▼")
    valor = br(atual, cfg["fmt"], cfg.get("prefixo", ""), cfg.get("sufixo", ""))
    var = br(delta, cfg["fmt"]) + (f" ({br(pct, ',.1f')}%)" if "%" not in cfg.get("sufixo", "") else " p.p.")
    st.markdown(
        f"""<div class="kpi" style="--cor:{cor}">
              <div class="titulo">{nome.split(' · ')[1]}</div>
              <div class="valor">{valor}</div>
              <div class="ref">{cfg['unidade']} · {periodos[-1]}</div>
              <span class="badge {classe}">{seta} {var} vs. {periodos[-2]}</span>
            </div>""",
        unsafe_allow_html=True,
    )
    st.plotly_chart(sparkline(periodos, valores, cor), width="stretch", theme=None,
                    config={"displayModeBar": False, "staticPlot": True}, key=f"spark_{nome}")
    st.button("Ver série completa →", key=f"btn_{nome}", on_click=ir_para, args=(nome,))


# --------------------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------------------
st.sidebar.markdown("## 📊 Indicadores SASC")
st.sidebar.caption("Secretaria da Assistência Social e Cidadania – Piauí")
paginas = ["Visão geral"] + list(INDICADORES)
if "nav" not in st.session_state:
    st.session_state["nav"] = "Visão geral"
escolha = st.sidebar.radio("Escolha o indicador", paginas, key="nav", label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.caption("Dados atualizados em outubro de 2026.")

if escolha == "Visão geral":
    temas = {}
    for nome, cfg in INDICADORES.items():
        temas.setdefault(cfg["tema"], []).append((nome, cfg))
    chips = "".join(f'<span class="chip">{TEMA_ICONE.get(t, "")} {t} · {len(v)}</span>' for t, v in temas.items())
    st.markdown(
        f"""<div class="hero">
              <h1>Painel de Indicadores Sociais – Piauí</h1>
              <p>Último valor disponível de cada indicador, variação em relação ao período anterior e tendência da série.
                 Clique em <b>Ver série completa</b> para detalhes, fonte e tabela.</p>
              <div class="chips">{chips}</div>
            </div><div class="faixa"></div>""",
        unsafe_allow_html=True,
    )
    st.caption("🟢 verde = melhora · 🔴 vermelho = piora · ⚪ cinza = variação sem leitura de melhora/piora (ex.: número de beneficiários). Para desemprego, informalidade, desigualdade e violências, queda é melhora.")
    for tema, itens in temas.items():
        cor = TEMA_COR.get(tema, CORES[0])
        st.markdown(f'<div class="tema"><div class="barra" style="background:{cor}"></div>'
                    f'<h3>{TEMA_ICONE.get(tema, "")} {tema}</h3></div>', unsafe_allow_html=True)
        cols = st.columns(3, gap="medium")
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
    titulo_principal = series[0] if len(series) == 1 else escolha.split(" · ")[1]
    st.plotly_chart(grafico(df, cfg, series, rotulos=rotulos, titulo=titulo_principal), width="stretch", theme=None)

    if cfg.get("extra") and cfg["extra"] in df.columns:
        fig_extra = grafico(df, {**cfg, "unidade": cfg.get("unidade_extra", ""), "fmt": ",.1f" if "%" in cfg["extra"] else ",.0f",
                                 "sufixo": "%" if "%" in cfg["extra"] else "", "prefixo": ""},
                            [cfg["extra"]], altura=320, rotulos=rotulos, titulo=cfg["extra"])
        if "Posição" in cfg["extra"]:
            fig_extra.update_yaxes(autorange="reversed", rangemode="normal", range=None)
            fig_extra.update_layout(title=dict(text="<b>Posição da SASC no ranking</b><br><span style='font-size:12px;color:#6B7280'>1º = melhor posição</span>"))
        st.plotly_chart(fig_extra, width="stretch", theme=None)

    if cfg.get("nota"):
        st.info(cfg["nota"], icon="ℹ️")
    st.markdown(f"**Fonte:** {cfg['fonte']}")

    with st.expander("Ver tabela de dados"):
        tabela = df.copy()
        for c in tabela.columns:
            if c not in ("periodo", "Série") and pd.api.types.is_numeric_dtype(tabela[c]):
                f = ",.1f" if "%" in c else (",.0f" if ("Posição" in c or "Total de" in c) else cfg["fmt"])
                tabela[c] = tabela[c].map(lambda v, f=f: br(v, f))
        st.markdown(tabela.rename(columns={"periodo": "Período"}).to_html(index=False, classes="tabela", na_rep="–", escape=True),
                    unsafe_allow_html=True)
        st.download_button("Baixar CSV", df.to_csv(index=False).encode("utf-8"),
                           file_name=cfg["arquivo"], mime="text/csv")
