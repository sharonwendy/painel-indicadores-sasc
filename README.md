# Painel de Indicadores Sociais – SASC / Piauí

Painel em [Streamlit](https://streamlit.io) com os indicadores 1 a 9 e o IDHM.

## Estrutura

```
app.py              ← o painel
requirements.txt    ← bibliotecas usadas
data/               ← um CSV por indicador (é aqui que os dados são atualizados)
```

## Publicar no Streamlit Community Cloud (gratuito)

1. Crie uma conta no **GitHub** (github.com) e um repositório novo, por exemplo `painel-indicadores-sasc`.
2. No repositório, clique em **Add file → Upload files** e envie `app.py`, `requirements.txt`, `README.md` e a pasta `data` inteira. Clique em **Commit changes**.
3. Acesse **share.streamlit.io**, entre com a conta do GitHub e clique em **Create app → Deploy a public app from GitHub**.
4. Escolha o repositório, a branch `main` e o arquivo `app.py`. Clique em **Deploy**.
5. Em alguns minutos o painel fica disponível num link `https://….streamlit.app` para compartilhar.

> No plano gratuito o repositório precisa ser público — os dados ficam visíveis para quem tiver o link do GitHub.
> Todos os dados deste painel já são públicos (IBGE, MDS, FBSP, PNUD).

## Atualizar os dados

1. Abra o CSV do indicador na pasta `data/` (pode ser no Excel, salvando como CSV UTF-8).
2. Acrescente uma linha no fim com o novo período.
3. No GitHub, envie o arquivo atualizado (Upload files → substitui o antigo). O painel atualiza sozinho.

Para mudar textos de fonte, notas ou descrição de um indicador, edite o bloco `INDICADORES` no início de `app.py`.

## Rodar no próprio computador (opcional)

```
pip install -r requirements.txt
streamlit run app.py
```
