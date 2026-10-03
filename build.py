#!/usr/bin/env python3
"""Gera o site estático de brandao.design a partir de parciais simples."""
import datetime
import re
import shutil
from pathlib import Path

BASE = Path(__file__).parent
ROOT = BASE / "_site"          # pasta gerada (não editar)
STATIC = BASE / "static"       # css, fontes e imagens
POSTS_DIR = BASE / "posts"     # posts em Markdown

EMAIL = "paulo@brandao.design"
EMPRESA = "Brandão Consultoria em Dados LTDA"

SYMBOL_PATH = ("M 582.046875 678.363281 L 489.277344 678.363281 L 397.296875 566.714844 L 397.296875 562.550781 "
    "L 447.203125 562.550781 C 451.570312 583.632812 463.75 598.8125 478.101562 598.8125 C 496.121094 598.8125 "
    "510.726562 574.90625 510.726562 545.410156 C 510.726562 515.917969 496.121094 492.007812 478.101562 492.007812 "
    "C 465.945312 492.007812 455.351562 500.804688 449.738281 516.9375 L 397.296875 516.9375 L 397.296875 513.285156 "
    "L 489.277344 401.636719 L 512.636719 401.636719 L 512.636719 470.417969 L 558.722656 470.417969 L 558.722656 "
    "401.636719 L 582.046875 401.636719 L 674.027344 513.285156 L 674.027344 516.9375 L 620.527344 516.9375 C "
    "614.914062 500.804688 604.320312 492.007812 592.164062 492.007812 C 574.148438 492.007812 559.542969 515.917969 "
    "559.542969 545.410156 C 559.542969 574.90625 574.148438 598.8125 592.164062 598.8125 C 606.519531 598.8125 "
    "618.699219 583.632812 623.0625 562.550781 L 674.027344 562.550781 L 674.027344 566.714844 Z M 602.28125 "
    "355.511719 L 469.039062 355.511719 L 351.175781 497.765625 L 351.175781 582.234375 L 469.039062 724.488281 "
    "L 602.28125 724.488281 L 720.148438 582.234375 L 720.148438 497.765625 Z")
SYMBOL_VB = "351 355 369.5 369.5"


def symbol(cls="", size=None):
    s = f' width="{size}" height="{size}"' if size else ""
    return (f'<svg class="{cls}" viewBox="{SYMBOL_VB}"{s} aria-hidden="true" focusable="false">'
            f'<path fill="currentColor" fill-rule="evenodd" d="{SYMBOL_PATH}"/></svg>')


_seal_n = [0]


def seal(cls="seal"):
    _seal_n[0] += 1
    sid = f"sealArc{_seal_n[0]}"
    return f'''<svg class="{cls}" viewBox="0 0 200 200" role="img" aria-label="Selo Research. Resist. Rebuild.">
  <defs><path id="{sid}" d="M100,100 m-72,0 a72,72 0 1,1 144,0 a72,72 0 1,1 -144,0"/></defs>
  <circle cx="100" cy="100" r="95" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text fill="currentColor" font-family="Newsreader, Georgia, serif" font-size="17" letter-spacing="5.2">
    <textPath href="#{sid}">RESEARCH · RESIST · REBUILD ·</textPath>
  </text>
  <svg x="62" y="62" width="76" height="76" viewBox="{SYMBOL_VB}"><path fill="currentColor" fill-rule="evenodd" d="{SYMBOL_PATH}"/></svg>
</svg>'''


def head(title, desc, prefix, path=""):
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#f3f4f8">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://brandao.design/{path}">
<meta property="og:image" content="https://brandao.design/assets/img/og.png">
<meta property="og:locale" content="pt_BR">
<meta name="format-detection" content="telephone=no">
<link rel="canonical" href="https://brandao.design/{path}">
<link rel="icon" type="image/svg+xml" href="{prefix}assets/img/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400;1,6..72,500&display=swap">
<link rel="preload" href="{prefix}assets/fonts/NewAstro-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{prefix}assets/css/site.css">
</head>'''



import math

MENU_JS = '''<script>
(function () {
  var btn = document.getElementById("menu-btn"), nav = document.getElementById("nav");
  if (!btn || !nav) return;
  function setOpen(open) {
    btn.setAttribute("aria-expanded", String(open));
    btn.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
    nav.classList.toggle("open", open);
    document.body.classList.toggle("menu-open", open);
  }
  btn.addEventListener("click", function () { setOpen(btn.getAttribute("aria-expanded") !== "true"); });
  nav.addEventListener("click", function (e) { if (e.target.closest("a")) setOpen(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
  window.addEventListener("resize", function () { if (window.innerWidth >= 1024) setOpen(false); });
})();
</script>'''


def header(prefix, current):
    home = f"{prefix}index.html"

    def cur(k):
        return ' aria-current="page"' if k == current else ""
    return f'''<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="{home}" aria-label="Brandão — página inicial">{symbol()}<span class="wordmark">Brandão</span></a>
    <nav class="nav" id="nav" aria-label="Principal">
      <a href="{home}#solucoes">Soluções</a>
      <a href="{home}#para-quem">Para quem decide</a>
      <a href="{home}#metodologia">Metodologia</a>
      <a href="{prefix}blog/index.html"{cur("blog")}>Insights</a>
      <a href="{home}#quem-somos">Quem somos</a>
      <a href="{home}#contato">Contato</a>
    </nav>
    <div class="header-actions">
      <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Abrir menu"><span></span></button>
    </div>
  </div>
</header>'''


def footer(prefix):
    return f'''<footer class="site-footer">
  <div class="wrap footer-grid">
    <div style="display:grid;gap:12px">
      <a class="brand" href="{prefix}index.html">{symbol()}<span class="wordmark">Brandão</span></a>
      <p class="motto">Research. Resist. Rebuild.</p>
    </div>
    <div class="legal">
      <span>{EMPRESA}</span>
      <span>Belo Horizonte · Minas Gerais · Brasil</span>
      <span>© 2026 · brandao.design</span>
    </div>
  </div>
</footer>
<div class="stripe" aria-hidden="true"></div>
{MENU_JS}'''


# --------------------------------------------------------------------------
# Diagrama do ciclo PDCA (SVG gerado)
# --------------------------------------------------------------------------
def ring_svg():
    C, R, W = 170, 120, 46

    def pt(deg, r):
        a = math.radians(deg)
        return C + r * math.sin(a), C - r * math.cos(a)

    quads = [
        ("P", 0, "var(--magenta)", "#fafafa"),
        ("D", 90, "var(--orange)", "#030e2b"),
        ("C", 180, "var(--teal)", "#030e2b"),
        ("A", 270, "var(--violet)", "#030e2b"),
    ]
    parts = []
    for letter, a, fill, ink in quads:
        a1, a2, tip = a + 4, a + 78, a + 88
        x1, y1 = pt(a1, R)
        x2, y2 = pt(a2, R)
        parts.append(f'<path d="M{x1:.1f},{y1:.1f} A{R},{R} 0 0 1 {x2:.1f},{y2:.1f}" fill="none" stroke="{fill}" stroke-width="{W}"/>')
        o = pt(a2, R + W / 2 + 4)
        i = pt(a2, R - W / 2 - 4)
        t = pt(tip, R)
        parts.append(f'<path d="M{o[0]:.1f},{o[1]:.1f} L{t[0]:.1f},{t[1]:.1f} L{i[0]:.1f},{i[1]:.1f} Z" fill="{fill}"/>')
        lx, ly = pt(a + 41, R)
        parts.append(f'<text x="{lx:.1f}" y="{ly + 11:.1f}" text-anchor="middle" font-size="32" fill="{ink}">{letter}</text>')
    center = f'''<svg x="{C-22}" y="{C-66}" width="44" height="44" viewBox="{SYMBOL_VB}"><path fill="#fafafa" fill-rule="evenodd" d="{SYMBOL_PATH}"/></svg>
  <text x="{C}" y="{C+2}" text-anchor="middle" font-size="19" fill="#fafafa">Discovery</text>
  <text x="{C}" y="{C+22}" text-anchor="middle" font-size="15" fill="#8a93ae" font-family="Manrope, sans-serif" font-weight="800">+</text>
  <text x="{C}" y="{C+44}" text-anchor="middle" font-size="19" fill="#fafafa">Delivery</text>'''
    return f'''<svg class="ring" viewBox="0 0 340 340" role="img" aria-labelledby="ringTitle">
  <title id="ringTitle">Ciclo contínuo PDCA: Planejar, Executar, Checar e Agir, girando entre discovery e delivery</title>
  {''.join(parts)}
  {center}
</svg>'''


# --------------------------------------------------------------------------
# Posts
# --------------------------------------------------------------------------
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def load_posts():
    """Lê os arquivos .md da pasta posts/ e devolve a lista de posts, do mais novo para o mais antigo.
    Arquivos que começam com _ são ignorados, assim como posts com rascunho: true."""
    import markdown
    import yaml
    posts = []
    for f in sorted(POSTS_DIR.glob("*.md")):
        if f.name.startswith("_"):
            continue
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
        if not m:
            raise SystemExit(f"[erro] {f.name}: faltou o cabeçalho entre --- no topo do arquivo.")
        meta = yaml.safe_load(m.group(1)) or {}
        if meta.get("rascunho"):
            continue
        for campo in ("titulo", "data", "resumo"):
            if not meta.get(campo):
                raise SystemExit(f"[erro] {f.name}: o campo '{campo}' é obrigatório.")
        d = meta["data"]
        if isinstance(d, str):
            d = datetime.date.fromisoformat(d)
        corpo = m.group(2)
        palavras = len(re.sub(r"<[^>]+>", " ", corpo).split())
        posts.append({
            "slug": f.stem,
            "title": str(meta["titulo"]),
            "serie": str(meta.get("serie", "Insight")),
            "summary": str(meta["resumo"]),
            "img": str(meta.get("imagem", "robo")),
            "iso": d.isoformat(),
            "date": f"{d.day} {MESES[d.month - 1]} {d.year}",
            "read": f"{max(1, round(palavras / 200))} min",
            "body": markdown.markdown(corpo, extensions=["extra", "sane_lists"]),
        })
    posts.sort(key=lambda p: p["iso"], reverse=True)
    return posts


POSTS = load_posts()


def post_card(p, prefix):
    return f'''<a class="post-card" href="{prefix}blog/{p["slug"]}.html">
  <div class="thumb"><img src="{prefix}assets/img/{p["img"]}.webp" alt=""></div>
  <div>
    <div class="meta">{p.get("serie","Nota")} · {p["date"]} · {p["read"]} de leitura</div>
    <h3>{p["title"]}</h3>
    <p>{p["summary"]}</p>
  </div>
</a>'''


# --------------------------------------------------------------------------
# Home
# --------------------------------------------------------------------------
def home():
    P = ""
    cards = "\n".join(post_card(p, P) for p in POSTS[:2])
    return f'''{head("Brandão Consultoria em Dados", "A inteligência por trás das decisões de empresas e governos locais. Pesquisa própria, estrutura de dados e orientação especializada.", P)}
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
{header(P, "home")}
<main id="conteudo">

<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">Pesquisa · Estrutura de dados · Consultoria</p>
      <h1 class="display">A inteligência por trás das decisões de <span class="hl">empresas e governos locais.</span></h1>
      <p class="lede">Pesquisa própria, estrutura de dados e orientação especializada em um só parceiro, para que líderes decidam <em>com evidência, rapidez e menos risco</em>.</p>
      <div class="hero-actions">
        <a class="btn solid" href="#insights">Leia os insights <span class="arrow" aria-hidden="true">→</span></a>
        <a class="link" href="#metodologia">Conheça a metodologia ↓</a>
      </div>
    </div>
    <div class="hero-visual">
      <canvas class="dither" aria-hidden="true"></canvas>
      <figure class="gridcard">
        <div class="photo"><img src="assets/img/olhar.webp" alt="Retrato em bitmap de um rosto dividido em dois tons, turquesa e laranja" width="933" height="1400"></div>
        <figcaption class="caption">
          <span class="display">Feito por humanos</span>
          <small>Dados com<br>rigor científico</small>
        </figcaption>
      </figure>
      {seal("seal")}
    </div>
  </div>
</section>
<div class="trust" aria-label="Como trabalhamos">
  <div class="wrap">
    <ul>
      <li>Metodologia documentada</li>
      <li>Fontes verificáveis</li>
      <li>LGPD desde o projeto</li>
      <li>Atuação em todo o Brasil</li>
    </ul>
  </div>
</div>

<section id="solucoes">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow o">Como apoiamos decisões</p>
      <h2 class="display">Pesquisa, estrutura e orientação em um só lugar</h2>
      <p class="lede">Nossas pesquisas, metodologias e especialistas ajudam líderes a transformar dados dispersos em decisões que se sustentam.</p>
    </div>
    <div class="services">
      <article class="svc" style="--c: var(--magenta)">
        <span class="tag">01 · Pesquisa</span>
        <h3 class="display">Insights e pesquisas exclusivas</h3>
        <p class="muted">Análises objetivas, construídas com metodologia documentada e fontes verificáveis.</p>
        <ul>
          <li>Relatórios e análises de cenário</li>
          <li>Estudos de caso nacionais e internacionais</li>
          <li>Diagnósticos de maturidade de dados</li>
          <li>Pesquisa de uso e comportamento</li>
        </ul>
      </article>
      <article class="svc" style="--c: var(--teal)">
        <span class="tag">02 · Estrutura de dados</span>
        <h3 class="display">Governança, coleta e tratamento</h3>
        <p class="muted">A base que garante que cada número tenha origem, dono e qualidade medida.</p>
        <ul>
          <li>Governança de dados e de produtos digitais</li>
          <li>Coleta minimizada, com finalidade declarada</li>
          <li>Pipelines rastreáveis e reprodutíveis</li>
          <li>Indicadores com ficha, dono e meta</li>
        </ul>
      </article>
      <article class="svc" style="--c: var(--orange)">
        <span class="tag">03 · Orientação especializada</span>
        <h3 class="display">Assessoria em dados</h3>
        <p class="muted">Acompanhamento contínuo, no mesmo modelo de uma assessoria contábil ou jurídica.</p>
        <ul>
          <li>Apoio recorrente à tomada de decisão</li>
          <li>Leitura e interpretação de dados</li>
          <li>Capacitação de equipes técnicas</li>
          <li>Pesquisas sob demanda</li>
        </ul>
      </article>
    </div>
  </div>
</section>

<section id="para-quem">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow m">Para quem decide</p>
      <h2 class="display">Soluções por área de atuação</h2>
      <p class="lede">Cada organização decide de um jeito. Adaptamos pesquisa, dados e orientação à realidade de quem lidera.</p>
    </div>
    <div class="roles">
      <article class="role" style="--c: var(--magenta)">
        <h3>Governos e secretarias</h3>
        <p>Qualidade dos dados publicados, transparência ativa e indicadores de políticas públicas.</p>
      </article>
      <article class="role" style="--c: var(--orange)">
        <h3>Câmaras e gabinetes</h3>
        <p>Assessoria em dados para fiscalizar o orçamento e fundamentar decisões legislativas.</p>
      </article>
      <article class="role" style="--c: var(--teal)">
        <h3>Federações e entidades setoriais</h3>
        <p>Plataformas de métricas e indicadores para programas, redes de atendimento e associados.</p>
      </article>
      <article class="role" style="--c: var(--violet)">
        <h3>Empresas com agenda ESG e ODS</h3>
        <p>Dados verificáveis para medir impacto e reportar avanços com credibilidade.</p>
      </article>
      <article class="role" style="--c: var(--silicon)">
        <h3>Times de produtos digitais</h3>
        <p>Governança e métricas que mostram o que o produto entrega a quem o utiliza.</p>
      </article>
    </div>
  </div>
</section>

<section id="metodologia">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow m">Metodologia própria · Indicadores</p>
      <h2 class="display">Todo produto digital mede alguma coisa. Poucos medem o que importa.</h2>
      <p class="lede">O maior ganho da governança são bons indicadores. Nossa metodologia define métricas que refletem o produto e apoiam decisões reais.</p>
    </div>
    <div class="ind-grid">
      <div class="layers">
        <article class="layer" style="--c: var(--orange)">
          <span class="dot" aria-hidden="true"></span>
          <h3>Uso</h3>
          <p><span class="q">As pessoas usam?</span> Acesso, conclusão de tarefas, retorno e abandono.</p>
        </article>
        <article class="layer" style="--c: var(--teal)">
          <span class="dot" aria-hidden="true"></span>
          <h3>Qualidade do dado</h3>
          <p><span class="q">O número é confiável?</span> Completude, atualidade, consistência e rastreabilidade.</p>
        </article>
        <article class="layer" style="--c: var(--magenta)">
          <span class="dot" aria-hidden="true"></span>
          <h3>Resultado</h3>
          <p><span class="q">O que mudou?</span> O efeito do produto na vida de quem ele atende.</p>
        </article>
      </div>
      <div>
        <article class="ficha" aria-label="Exemplo de ficha de indicador">
          <div class="ficha-head">
            <span class="eyebrow">Ficha de indicador</span>
            <span class="chip">Exemplo</span>
          </div>
          <div class="ficha-body">
            <h3>Índice de Qualidade da Base (IQB)</h3>
            <dl>
              <div><dt>Camada</dt><dd><strong>Qualidade do dado</strong></dd></div>
              <div><dt>Definição</dt><dd>Mede se cada base chega no prazo, no layout e na sintaxe combinados, e quanto ela precisou ser corrigida antes de ser usada.</dd></div>
              <div><dt>Componentes</dt><dd>
                <table class="comp">
                  <tr><th scope="row">Prazo</th><td>chegou na data combinada? (sim = 1, não = 0)</td><td class="v">1</td></tr>
                  <tr><th scope="row">Layout</th><td>mesmas colunas, nomes e ordem do dicionário? (1 ou 0)</td><td class="v">1</td></tr>
                  <tr><th scope="row">Sintaxe</th><td>% de registros com tipos e formatos válidos (datas, CNPJ, valores)</td><td class="v">98%</td></tr>
                  <tr><th scope="row">Inferência</th><td>% de valores corrigidos, imputados ou deduzidos antes do uso</td><td class="v">6%</td></tr>
                </table>
              </dd></div>
              <div><dt>Fórmula</dt><dd class="formula">IQB = Prazo × Layout × Sintaxe × (1 − Inferência) × 100<br><span class="calc">1 × 1 × 0,98 × 0,94 × 100 = <strong>92</strong></span></dd></div>
              <div><dt>Fonte</dt><dd>Dicionário de dados, log de cargas e registro de correções do pipeline</dd></div>
              <div><dt>Dono</dt><dd>Área responsável pela base, com apoio do time de dados</dd></div>
              <div><dt>Periodicidade</dt><dd>A cada carga, consolidado por mês</dd></div>
              <div><dt>Meta</dt><dd><strong>≥ 90 pontos</strong> · resultado do exemplo: 92<div class="meta-bar" aria-hidden="true"><i></i></div></dd></div>
              <div><dt>Decisão que apoia</dt><dd>Quais fornecedores precisam de acordo de layout e onde automatizar a validação antes de publicar.</dd></div>
            </dl>
          </div>
        </article>
        <p class="ficha-note">Atraso ou layout quebrado zeram o índice: uma base fora do combinado não pode ser usada como se estivesse certa. Todo indicador que entregamos tem uma ficha assim, com definição, fórmula, fonte, dono, periodicidade, meta e a decisão que ele apoia.</p>
      </div>
    </div>
  </div>
</section>

<section class="manifesto" aria-label="Manifesto">
  <div class="wrap">
    <p class="eyebrow">Manifesto</p>
    <p class="manifesto-line">Dado sem governança é <em>opinião com gráfico.</em></p>
    <p class="manifesto-sub">Por isso começamos pela governança: quem responde por cada dado, o que ele significa e como ele é tratado. Só então o gráfico merece confiança.</p>
  </div>
</section>

<section id="metodo" class="dark">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Metodologia própria · Ciclo contínuo</p>
      <h2 class="display">Produto não termina. Evolui em ciclos.</h2>
      <p class="lede">Um discovery inicial para entender o terreno. Depois, discovery e delivery em ciclo contínuo, girando um PDCA.</p>
    </div>
    <div class="cycle">
        <article class="kickoff">
          <span class="tag">Ponto de partida · Discovery inicial</span>
          <h3 class="display">Entender antes de medir</h3>
          <ul>
            <li>Produto, cliente e cenário</li>
            <li>Problemas e dores de quem usa e de quem decide</li>
            <li>Fontes de dados disponíveis</li>
            <li>Planejamento e arquitetura de coleta e tratamento</li>
            <li>Proposta de solução e primeiros indicadores</li>
          </ul>
          <p class="into">↓ Entra no ciclo contínuo</p>
        </article>
      <div class="ring-col">
        {ring_svg()}
        <p class="cycle-note" style="text-align:center">Cada volta deixa o produto e seus indicadores um pouco melhores.</p>
      </div>
        <ol class="pdca">
          <li style="--c: var(--magenta)"><span class="letter" aria-hidden="true">P</span><h3>Planejar <small>· Discovery</small></h3><p>Priorizar hipóteses e revisar indicadores e metas.</p></li>
          <li style="--c: var(--orange)"><span class="letter" aria-hidden="true">D</span><h3>Executar <small>· Delivery</small></h3><p>Coletar, tratar e entregar melhorias no produto.</p></li>
          <li style="--c: var(--teal)"><span class="letter" aria-hidden="true">C</span><h3>Checar <small>· Indicadores</small></h3><p>Medir uso, qualidade do dado e resultado.</p></li>
          <li style="--c: var(--violet)"><span class="letter" aria-hidden="true">A</span><h3>Agir <small>· Melhoria</small></h3><p>Padronizar o que funcionou. Corrigir o que não funcionou. Recomeçar.</p></li>
        </ol>
    </div>
  </div>
</section>

<section id="insights" class="alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow o">Insights</p>
      <h2 class="display">Pesquisas para decidir melhor</h2>
      <p class="lede">Publicamos análises abertas e, em breve, pesquisas exclusivas para membros.</p>
    </div>
    <div class="posts">
{cards}
    </div>
    <div class="lines">
      <p class="eyebrow">Linhas de pesquisa</p>
      <ul>
        <li>IA no setor público: o que funciona e o que falha</li>
        <li>Maturidade de dados em organizações</li>
        <li>Indicadores de produtos e serviços digitais</li>
        <li>Transparência e qualidade de dados públicos</li>
      </ul>
    </div>
    <div class="blog-more"><a class="btn" href="blog/index.html">Todos os insights <span class="arrow" aria-hidden="true">→</span></a></div>
  </div>
</section>

<section id="quem-somos">
  <div class="wrap about-grid">
    <figure class="gridcard">
      <div class="photo"><img src="assets/img/interacao.webp" alt="Ilustração em bitmap de duas mãos se aproximando" width="1400" height="935"></div>
      <figcaption class="caption"><span class="display">Humano + máquina</span><small>IHC aplicada<br>a dados</small></figcaption>
    </figure>
    <div>
      <div class="section-head" style="margin-bottom:20px">
        <p class="eyebrow">Quem somos</p>
        <h2 class="display">Dados com rigor e com gente</h2>
      </div>
      <div class="prose muted">
        <p>Somos uma consultoria de dados que une engenharia de dados, gestão de produto e Interação Humano-Computador.</p>
        <p>Nossa experiência vem de produtos de dados públicos no Governo Federal: transparência ativa, acesso à informação e maturidade de dados.</p>
        <p>Levamos esse rigor a governos e empresas que querem decidir melhor sem abrir mão da ética.</p>
      </div>
      <dl class="creds">
        <div><dt>Sede</dt><dd>Belo Horizonte · MG</dd></div>
        <div><dt>Atuação</dt><dd>Todo o Brasil, presencial e remoto</dd></div>
      </dl>

      <article class="founder" aria-labelledby="fundador-nome">
        <div class="founder-head">
          <img class="founder-photo" src="assets/img/paulo-brandao.webp" alt="Foto de Paulo Brandão" width="460" height="460">
          <div>
            <p class="eyebrow o">Fundador</p>
            <h3 class="display" id="fundador-nome">Paulo Brandão</h3>
          </div>
        </div>
        <p class="muted">Data Product Manager e especialista em Interação Humano-Computador. Atua com produtos de dados públicos e pesquisa como a tecnologia influencia o comportamento e a sociedade.</p>
        <dl class="creds">
          <div><dt>Atuação</dt><dd>Data Product Manager</dd></div>
          <div><dt>Especialização</dt><dd>Interação Humano-Computador (PUC-Rio)</dd></div>
          <div><dt>Especialização em andamento</dt><dd>Deep Learning (UFPE)</dd></div>
          <div><dt>Graduação</dt><dd>Gestão de TI (FIAP)</dd></div>
        </dl>
      </article>
    </div>
  </div>
</section>

<section id="principios">
  <div class="wrap principles-grid">
    <div class="principles-art">
      <div class="frame"><img src="assets/img/grupo.webp" alt="Fotografia em bitmap de três pessoas lado a lado, em tons de roxo, laranja e turquesa" width="1400" height="935"></div>
      {seal("seal")}
    </div>
    <div>
      <div class="section-head" style="margin-bottom:20px">
        <p class="eyebrow">Princípios</p>
        <h2 class="display">O que não negociamos</h2>
      </div>
      <ul class="plist">
        <li><span class="k">i.</span><div><h3>Ética acima de tudo</h3><p>Nenhum projeto justifica manipulação ou dado sem finalidade.</p></div></li>
        <li><span class="k">ii.</span><div><h3>Pessoas em primeiro lugar</h3><p>Cada dado representa alguém. Decidimos pensando em quem está do outro lado.</p></div></li>
        <li><span class="k">iii.</span><div><h3>Transparência e democracia</h3><p>Métodos documentados e resultados que qualquer cidadão pode auditar.</p></div></li>
        <li><span class="k">iv.</span><div><h3>Direitos humanos para a IA</h3><p>Em vez de humanizar a IA, ensinamos a ela a respeitar quem ela atende.</p></div></li>
      </ul>
    </div>
  </div>
</section>

<section id="contato" class="contact">
  <div class="wrap contact-grid">
    <div style="display:grid;gap:18px;align-content:start">
      <p class="eyebrow m">Contato</p>
      <h2 class="display">Vamos conversar?</h2>
      <p class="lede">Tem uma pergunta, uma ideia de pesquisa ou um desafio com dados? Escreva para nós. Lemos e respondemos todas as mensagens.</p>
      <div class="mail"><code id="email">{EMAIL}</code><button type="button" id="copy">Copiar</button></div>
    </div>
    <form id="form" novalidate>
      <label for="nome">Nome<input id="nome" name="nome" autocomplete="name" required></label>
      <label for="org">Organização<input id="org" name="org" autocomplete="organization"></label>
      <label for="tipo">Tipo de organização
        <select id="tipo" name="tipo">
          <option>Prefeitura, câmara ou governo</option>
          <option>Federação ou entidade setorial</option>
          <option>Empresa</option>
          <option>Terceiro setor</option>
          <option>Outro</option>
        </select>
      </label>
      <label for="msg">Mensagem<textarea id="msg" name="msg" required placeholder="Qual decisão sua organização precisa tomar com mais segurança?"></textarea></label>
      <button class="btn solid block" type="submit">Enviar mensagem <span class="arrow" aria-hidden="true">→</span></button>
      <p class="form-note" id="note" role="status"></p>
    </form>
  </div>
</section>

</main>
{footer(P)}
<script>
(function () {{
  var email = "{EMAIL}";
  var copy = document.getElementById("copy");
  function selectEmail() {{
    var r = document.createRange(); r.selectNodeContents(document.getElementById("email"));
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  }}
  copy.addEventListener("click", function () {{
    var done = function () {{ copy.textContent = "Copiado"; setTimeout(function () {{ copy.textContent = "Copiar"; }}, 1800); }};
    try {{ navigator.clipboard.writeText(email).then(done, selectEmail); }} catch (e) {{ selectEmail(); }}
  }});
  var form = document.getElementById("form"), note = document.getElementById("note");
  form.addEventListener("submit", function (ev) {{
    ev.preventDefault();
    var nome = form.nome.value.trim(), msg = form.msg.value.trim();
    if (!nome || !msg) {{ note.textContent = "Preencha nome e mensagem para enviar."; return; }}
    var assunto = "Contato pelo site: " + nome + (form.org.value ? " (" + form.org.value + ")" : "");
    var corpo = msg + "\\n\\n" + nome + "\\n" + form.org.value + "\\n" + form.tipo.value;
    note.textContent = "Abrindo seu aplicativo de e-mail. Se nada abrir, escreva para " + email + ".";
    window.location.href = "mailto:" + email + "?subject=" + encodeURIComponent(assunto) + "&body=" + encodeURIComponent(corpo);
  }});
}})();
</script>
<script>
(function () {{
  var c = document.querySelector(".hero .dither");
  if (!c || !c.getContext) return;
  var ctx = c.getContext("2d"), cell = 9, W, H, cols, rows, t = 0, last = 0, visible = true;
  var pal = ["#25156b", "#e82d55", "#ff8539", "#1fe3cb"];
  var bayer = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function size() {{
    var r = c.getBoundingClientRect();
    cols = Math.ceil(r.width / cell); rows = Math.ceil(r.height / cell);
    c.width = cols; c.height = rows; W = cols; H = rows;
  }}
  function draw() {{
    ctx.clearRect(0, 0, W, H);
    for (var y = 0; y < rows; y++) {{
      for (var x = 0; x < cols; x++) {{
        var v = Math.sin(x * 0.16 + t) * Math.cos(y * 0.12 - t * 0.7) + Math.sin((x + y) * 0.07 + t * 0.4);
        v = (v + 2) / 4; // 0..1
        var th = bayer[(y % 4) * 4 + (x % 4)] / 16;
        if (v * 0.9 > th + 0.25) {{
          var k = Math.min(3, Math.floor(v * 4.2));
          ctx.fillStyle = pal[k];
          ctx.fillRect(x, y, 1, 1);
        }}
      }}
    }}
  }}
  function loop(ts) {{
    if (visible && ts - last > 90) {{ t += 0.035; draw(); last = ts; }}
    requestAnimationFrame(loop);
  }}
  size(); draw();
  window.addEventListener("resize", function () {{ size(); draw(); }});
  if ("IntersectionObserver" in window) {{
    new IntersectionObserver(function (e) {{ visible = e[0].isIntersecting; }}).observe(c);
  }}
  if (!reduce) requestAnimationFrame(loop);
}})();
</script>
</body>
</html>
'''


def blog_index():
    P = "../"
    cards = "\n".join(post_card(p, P) for p in POSTS)
    return f'''{head("Insights · Brandão", "Pesquisas e análises sobre dados, IA, governança e indicadores para decisões mais seguras.", P, "blog/")}
<body class="page-light">
{header(P, "blog")}
<main>
  <section class="blog-hero">
    <div class="wrap">
      <p class="eyebrow">Insights</p>
      <h1 class="display">Pesquisas para decidir melhor</h1>
      <p class="lede">Análises objetivas sobre dados, IA, governança e indicadores. Em breve, pesquisas exclusivas para membros.</p>
    </div>
  </section>
  <section style="padding-top:0">
    <div class="wrap"><div class="posts">
{cards}
    </div></div>
  </section>
</main>
{footer(P)}
</body>
</html>
'''


def post_page(p):
    P = "../"
    return f'''{head(p["title"] + " · Brandão", p["summary"], P, "blog/" + p["slug"] + ".html")}
<body class="page-light">
{header(P, "blog")}
<main class="article">
  <div class="wrap">
    <header>
      <p class="eyebrow">{p.get("serie","Notas de laboratório")}</p>
      <h1 class="display" style="font-size:clamp(2rem,8.5vw,3.6rem)">{p["title"]}</h1>
      <p class="lede">{p["summary"]}</p>
      <p class="meta">Paulo Brandão · {p["date"]} · {p["read"]} de leitura</p>
    </header>
    <div class="cover"><img src="../assets/img/{p["img"]}.webp" alt=""></div>
    <div class="body">
{p["body"]}
    </div>
    <a class="back" href="index.html">← Todos os insights</a>
  </div>
</main>
{footer(P)}
</body>
</html>
'''


def page_404():
    P = "/"
    return f'''{head("418 · Sou um bule", "Página não encontrada.", P, "404.html")}
<body>
{header(P, "")}
<main class="teapot">
  <div class="wrap">
    <img src="/assets/img/bule.webp" alt="Bule de chá em bitmap">
    <p class="eyebrow m">Erro 404 · ou quase 418</p>
    <h1 class="display">Somos um bule.</h1>
    <p class="lede" style="margin-inline:auto">Esta página não existe. Mas o chá está servido.</p>
    <a class="btn solid" href="/">Voltar ao início <span class="arrow" aria-hidden="true">→</span></a>
  </div>
</main>
{footer(P)}
</body>
</html>
'''

def favicon():
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{SYMBOL_VB}">'
            f'<style>path{{fill:#030e2b}}@media (prefers-color-scheme:dark){{path{{fill:#fafafa}}}}</style>'
            f'<path fill-rule="evenodd" d="{SYMBOL_PATH}"/></svg>')


if __name__ == "__main__":
    if ROOT.exists():
        shutil.rmtree(ROOT)
    shutil.copytree(STATIC, ROOT)
    (ROOT / "blog").mkdir(parents=True, exist_ok=True)
    (ROOT / "index.html").write_text(home(), encoding="utf-8")
    (ROOT / "blog" / "index.html").write_text(blog_index(), encoding="utf-8")
    for p in POSTS:
        (ROOT / "blog" / f'{p["slug"]}.html').write_text(post_page(p), encoding="utf-8")
    (ROOT / "404.html").write_text(page_404(), encoding="utf-8")
    (ROOT / "assets" / "img" / "favicon.svg").write_text(favicon(), encoding="utf-8")
    (ROOT / "CNAME").write_text("brandao.design\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://brandao.design/sitemap.xml\n", encoding="utf-8")
    urls = ["", "blog/"] + [f'blog/{p["slug"]}.html' for p in POSTS]
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>https://brandao.design/{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    print(f"ok: site gerado em _site/ com {len(POSTS)} post(s)")
