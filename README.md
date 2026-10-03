# brandao.design

Site da Brandão Consultoria em Dados. Toda mudança salva neste repositório é publicada automaticamente pela Netlify em cerca de 1 minuto.

## Onde mexer

| Quero… | Onde |
|---|---|
| Publicar, editar ou apagar um post | pasta `posts/` |
| Trocar imagens, cores ou fontes | pasta `static/assets/` |
| Mudar textos da página inicial | `build.py` (função `home`) |

A pasta `_site/` é gerada automaticamente. Não edite e não envie para o GitHub.

## Publicar um post novo

1. Abra a pasta `posts/` e clique em `_modelo.md`.
2. Copie todo o conteúdo do arquivo.
3. Volte para `posts/` e clique em **Add file → Create new file**.
4. Dê um nome ao arquivo, por exemplo `governanca-de-indicadores.md`. Use só letras minúsculas, números e hífens. O nome vira o endereço do post: `brandao.design/blog/governanca-de-indicadores.html`.
5. Cole o conteúdo, preencha o cabeçalho e escreva o texto.
6. Apague a linha `rascunho: true`, ou troque por `rascunho: false`.
7. Clique em **Commit changes**.

Em cerca de 1 minuto, o post aparece no site, na página Insights e entre os dois mais recentes da página inicial.

## O cabeçalho do post

```yaml
---
titulo: Título do post
data: 2026-10-03          # AAAA-MM-DD
serie: Insight            # etiqueta acima do título: Case, Insight, Pesquisa…
resumo: Uma ou duas frases para o card e para o Google.
imagem: robo              # robo, computador, tv, bule, grupo, interacao ou olhar
rascunho: true            # opcional; true = não publica
---
```

O tempo de leitura é calculado automaticamente.

## Editar ou apagar

- **Editar:** abra o arquivo, clique no lápis ✏️, altere e clique em **Commit changes**.
- **Apagar:** abra o arquivo, clique em **⋯ → Delete file** e depois em **Commit changes**.
- **Esconder sem apagar:** coloque `rascunho: true` no cabeçalho.

## Escrevendo o texto (Markdown)

```markdown
## Intertítulo
**negrito**, *itálico*, [link](https://exemplo.com)

- item de lista
1. lista numerada

> citação em destaque
```

## Se algo der errado

Se o post tiver um erro no cabeçalho, a Netlify não publica, e **o site anterior continua no ar**. O motivo aparece em **Netlify → Deploys**, na linha do deploy com falha. A mensagem começa com `[erro]` e diz qual arquivo e qual campo corrigir.

## Testar no computador (opcional)

```bash
pip install -r requirements.txt
python build.py
# abra _site/index.html no navegador
```
