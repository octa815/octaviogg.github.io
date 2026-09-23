#!/usr/bin/env python3
"""Generates the static pages of the portfolio into the repo root.

The HTML files are committed, so GitHub Pages needs no build step. Edit copy or
the shared header/footer here, then run:  python3 tools/build_pages.py
"""
import json, os, html, re

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://octa815.github.io/octaviogg.github.io/"
EMAIL = "octavio.ogg+pf@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/octagg"
GITHUB = "https://github.com/octa815"
ITCH = "https://pocketboy-games.itch.io/towerhero"
PHONE_WA = "34694455979"
V = "20260923d"  # cache-busting for css/js

from urllib.parse import quote
MSG_ES = "Hola Octavio, he visto tu portfolio y me encantaría contratarte ;)"
MSG_EN = "Hi Octavio, I've seen your portfolio and I'd love to hire you ;)"
MSG_ZH = "你好 Octavio，我看過你的作品集，很想聘請你 ;)"
WA_ES, WA_EN, WA_ZH = quote(MSG_ES), quote(MSG_EN), quote(MSG_ZH)
MAIL_ES = f"mailto:{EMAIL}?subject={quote('Te he visto en tu portfolio')}&amp;body={quote(MSG_ES)}"
MAIL_EN = f"mailto:{EMAIL}?subject={quote('Found you through your portfolio')}&amp;body={quote(MSG_EN)}"
MAIL_ZH = f"mailto:{EMAIL}?subject={quote('從你的作品集找到你')}&amp;body={quote(MSG_ZH)}"


# Traditional Chinese: tools/zh_hant.json maps the exact Spanish string to its
# translation. Missing keys fall back to English and are listed after a build.
ZH_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zh_hant.json")
ZH = json.load(open(ZH_PATH, encoding="utf-8")) if os.path.exists(ZH_PATH) else {}
ZH_MISSING = {}


def zh(es, en):
    if es in ZH:
        return ZH[es]
    ZH_MISSING[es] = en
    return en


def L(es, en, tag="span", cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<{tag}{c} lang="es">{es}</{tag}><{tag}{c} lang="en">{en}</{tag}>'
            f'<{tag}{c} lang="zh-Hant">{zh(es, en)}</{tag}>')


_TAG = re.compile(r"<[a-zA-Z][^<>]*\bdata-es-[^<>]*>")
_ATTR = re.compile(r'data-es-([a-z-]+)="([^"]*)"')


_EN_ONLY = re.compile(r"<[a-zA-Z][^<>]*\bdata-en-[^<>]*>")


def add_es_attrs(markup):
    """A tag with data-en-X but no data-es-X gets data-es-X from its current X."""
    def fix(m):
        tag = m.group(0)
        extra = []
        for attr in re.findall(r'data-en-([a-z-]+)="', tag):
            if f"data-es-{attr}=" in tag:
                continue
            cur = re.search(rf'(?<![\w-]){attr}="([^"]*)"', tag)
            if cur:
                extra.append(f'data-es-{attr}="{cur.group(1)}"')
        if not extra:
            return tag
        end = -2 if tag.endswith("/>") else -1
        return tag[:end] + " " + " ".join(extra) + tag[end:]
    return _EN_ONLY.sub(fix, markup)


def add_zh_attrs(markup):
    """Every data-es-X gets a data-zh-X sibling (translated or English fallback)."""
    markup = add_es_attrs(markup)
    def fix(m):
        tag = m.group(0)
        extra = []
        for attr, val in _ATTR.findall(tag):
            if f"data-zh-{attr}=" in tag:
                continue
            en = re.search(rf'data-en-{attr}="([^"]*)"', tag)
            en_val = html.unescape(en.group(1)) if en else html.unescape(val)
            extra.append(f'data-zh-{attr}="{html.escape(zh(html.unescape(val), en_val))}"')
        if not extra:
            return tag
        end = -2 if tag.endswith("/>") else -1
        return tag[:end] + " " + " ".join(extra) + tag[end:]
    return _TAG.sub(fix, markup)


# ---------- icons ----------
def icon(name, cls=""):
    p = {
        "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>',
        "moon": '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>',
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "arrow-left": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
        "arrow-up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
        "ext": '<path d="M7 17 17 7M8 7h9v9"/>',
        "download": '<path d="M12 3v12M7 10l5 5 5-5M5 21h14"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "check": '<path d="m5 12 5 5L20 7"/>',
        "alert": '<circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/>',
        "close": '<path d="M6 6l12 12M18 6 6 18"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
        "play": '<path d="M8 5v14l11-7z" fill="currentColor" stroke="none"/>',
    }
    brands = {
        "github": '<path fill="currentColor" d="M12 .5a11.5 11.5 0 0 0-3.64 22.41c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.69 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.81 1.19 1.84 1.19 3.1 0 4.42-2.7 5.4-5.26 5.68.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .5z"/>',
        "linkedin": '<path fill="currentColor" d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/>',
        "itch": '<path fill="currentColor" d="M3.13 1.34C2.08 1.96.02 4.33 0 4.95v1.03c0 1.3 1.22 2.45 2.33 2.45 1.33 0 2.44-1.1 2.44-2.4 0 1.3 1.07 2.4 2.4 2.4 1.33 0 2.36-1.1 2.36-2.4 0 1.3 1.14 2.4 2.47 2.4h.02c1.33 0 2.47-1.1 2.47-2.4 0 1.3 1.03 2.4 2.36 2.4 1.33 0 2.4-1.1 2.4-2.4 0 1.3 1.11 2.4 2.44 2.4C22.78 8.43 24 7.28 24 5.98V4.95c-.02-.62-2.08-2.99-3.13-3.61-3.27-.11-5.53-.13-8.87-.13-3.34 0-7.9.05-8.87.13zm6.35 6.45a2.78 2.78 0 0 1-4.74 0 2.8 2.8 0 0 1-2.4 1.3c-.3 0-.62-.08-.87-.17-.36 3.83-.26 6.55.3 7.8 1.64 1.9 9.04 1.83 10.23 1.83 1.2 0 8.6.07 10.23-1.83.56-1.25.66-3.97.3-7.8-.25.09-.57.17-.87.17-1 0-1.9-.5-2.4-1.3a2.78 2.78 0 0 1-4.74 0 2.8 2.8 0 0 1-2.43 1.3 2.8 2.8 0 0 1-2.43-1.3h-.01l-.17-.02zM8.3 10.26c.8 0 1.52 0 2.4.97a19.6 19.6 0 0 1 2.6 0c.88-.97 1.6-.97 2.4-.97 2.4 0 3 3.54 3.84 6.53.78 2.78-.25 2.85-1.53 2.85-1.9-.07-2.95-1.45-2.95-2.83-1.05.17-2.27.26-3.06.26s-2.01-.09-3.06-.26c0 1.38-1.05 2.76-2.95 2.83-1.28 0-2.31-.07-1.53-2.85.84-3 1.43-6.53 3.84-6.53zM12 12.78s-2.28 2.1-2.7 2.84l1.5-.06v1.3c0 .07.6.04 1.2.01.6.03 1.2.06 1.2-.01v-1.3l1.5.06c-.42-.75-2.7-2.84-2.7-2.84z"/>',
        "whatsapp": '<path fill="currentColor" d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.5h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.07-.13-.27-.2-.57-.35zM12.05 21.8h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.9-9.88a9.83 9.83 0 0 1 9.88 9.89c0 5.45-4.44 9.88-9.89 9.88zm8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.16-3.48-8.41z"/>',
    }
    if name in brands:
        return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{brands[name]}</svg>'
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p[name]}</svg>'


# ---------- structured data ----------
PERSON = {
    "@type": "Person",
    "@id": BASE + "#person",
    "name": "Octavio Gregorio Guerrero",
    "alternateName": "Octavio GG",
    "url": BASE,
    "image": BASE + "assets/img/octavio-800.jpg",
    "email": "mailto:" + EMAIL,
    "jobTitle": "Ingeniero Multimedia · Game Developer · Project Manager",
    "address": {"@type": "PostalAddress", "addressLocality": "Elda", "addressRegion": "Alicante", "addressCountry": "ES"},
    "homeLocation": {"@type": "Place", "name": "Elda, Alicante, España"},
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "Universidad de Alicante", "url": "https://www.ua.es"},
    "knowsLanguage": ["es", "en"],
    "knowsAbout": ["Desarrollo de videojuegos", "C++", "OpenGL", "Ensamblador Z80", "Gestión de proyectos", "React", "Node.js", "Blender", "Superresolución con IA"],
    "sameAs": [LINKEDIN, GITHUB, ITCH],
}


def crumbs_ld(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(items)],
    }


def ld(*nodes):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": list(nodes)}, ensure_ascii=False) + "</script>"


# ---------- chrome ----------
def head(*, path, title_es, title_en, desc_es, desc_en, ld_json="", robots="index,follow", og_type="website", base="", og_image="assets/img/og.jpg"):
    canonical = BASE + (path if path != "index.html" else "")
    base_tag = f'<base href="{base}">' if base else ""
    return f"""<!DOCTYPE html>
<html lang="es" data-es-title="{html.escape(title_es)}" data-en-title="{html.escape(title_en)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{base_tag}
<title>{html.escape(title_es)}</title>
<meta name="description" content="{html.escape(desc_es)}" data-es-content="{html.escape(desc_es)}" data-en-content="{html.escape(desc_en)}">
<meta name="robots" content="{robots}">
<meta name="author" content="Octavio Gregorio Guerrero">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#f4f1ea">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Octavio Gregorio">
<meta property="og:locale" content="es_ES">
<meta property="og:locale:alternate" content="en_GB">
<meta property="og:locale:alternate" content="zh_TW">
<meta property="og:title" content="{html.escape(title_es)}">
<meta property="og:description" content="{html.escape(desc_es)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<script>(function(){{var r=document.documentElement,s;try{{s=localStorage}}catch(e){{}}var t=s&&s.getItem('theme'),l=s&&s.getItem('lang');r.dataset.theme=t||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');if(l==='en')r.lang='en';if(l==='zh')r.lang='zh-Hant';r.classList.add('js')}})()</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..400&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@600&display=swap">
<link rel="stylesheet" href="assets/css/site.css?v={V}">
<script src="assets/js/site.js?v={V}" defer></script>
{ld_json}
</head>
<body>
<a class="skip-link" href="#main">{L("Saltar al contenido", "Skip to content")}</a>
"""


def header(active=""):
    def nav(href, es, en, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<li><a href="{href}"{cur}>{L(es, en)}</a></li>'

    items = [
        ("index.html#trabajo", "Proyectos", "Work", "work"),
        ("index.html#sobre-mi", "Sobre mí", "About", "about"),
        ("index.html#faq", "FAQ", "FAQ", "faq"),
        ("elements.html", "Archivo", "Archive", "archive"),
        ("index.html#contacto", "Contacto", "Contact", "contact"),
    ]
    nav_html = "\n".join(nav(*i) for i in items)
    mob = "\n".join(f'<li><a href="{h}">{L(es, en)}{icon("arrow")}</a></li>'.replace("<svg ", '<svg width="18" ') for h, es, en, _ in items)
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Octavio Gregorio — inicio" data-es-aria-label="Octavio Gregorio — inicio" data-en-aria-label="Octavio Gregorio — home">
      <img src="assets/img/logo-96.webp" alt="" width="34" height="34">
      <span>Octavio GG <small>/ multimedia</small></span>
    </a>
    <nav class="site-nav" aria-label="{'Principal'}" data-en-aria-label="Main" data-es-aria-label="Principal">
      <ul>
{nav_html}
      </ul>
    </nav>
    <div class="tools">
      <div class="lang-switch" role="group" aria-label="Idioma" data-es-aria-label="Idioma" data-en-aria-label="Language"><button type="button" data-set-lang="es" lang="es" aria-label="Español">ES</button><button type="button" data-set-lang="en" lang="en" aria-label="English">EN</button><button type="button" data-set-lang="zh" lang="zh-Hant" aria-label="繁體中文">中</button></div>
      <button class="icon-btn theme-toggle" type="button" aria-label="Activar modo oscuro" aria-pressed="false">{icon("moon", "i-moon")}{icon("sun", "i-sun")}</button>
      <a class="btn btn--sm btn--ink header-cv" href="cv_octavio_gregorio.pdf" download>{L("Descargar CV", "Download CV")}</a>
      <button class="icon-btn menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Abrir menú"><span class="bars"><span class="bar"></span><span class="bar"></span></span></button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu">
  <ul>
{mob}
  </ul>
  <a class="btn btn--primary" href="cv_octavio_gregorio.pdf" download>{icon("download")}{L("Descargar CV (PDF)", "Download CV (PDF)")}</a>
</div>
"""


def footer(mobile_cta=True):
    cta = ""
    if mobile_cta:
        cta = f"""<div class="mobile-cta" aria-label="{'Acciones rápidas'}" data-en-aria-label="Quick actions" data-es-aria-label="Acciones rápidas" role="region">
  <a class="btn btn--primary" href="index.html#contacto">{L("Escríbeme", "Get in touch")}</a>
  <a class="btn" href="cv_octavio_gregorio.pdf" download>{icon("download")}CV</a>
</div>"""
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="index.html"><img src="assets/img/logo-96.webp" alt="" width="34" height="34" loading="lazy"><span>Octavio GG</span></a>
        <p>{L("Ingeniero Multimedia en Elda, Alicante. Videojuegos, desarrollo y coordinación de proyectos.", "Multimedia engineer based in Elda, Alicante. Games, development and project coordination.")}</p>
      </div>
      <nav aria-label="Proyectos" data-en-aria-label="Projects" data-es-aria-label="Proyectos">
        <h2>{L("Proyectos", "Work")}</h2>
        <ul>
          <li><a href="tfg-superresolucion.html">{L("TFG: superresolución con IA", "Thesis: AI super-resolution")}</a></li>
          <li><a href="castle-of-shadows.html">Castle of Shadows</a></li>
          <li><a href="tower-hero.html">Tower Hero</a></li>
          <li><a href="elements.html">{L("Archivo de ficheros", "File archive")}</a></li>
        </ul>
      </nav>
      <nav aria-label="Contacto" data-en-aria-label="Contact" data-es-aria-label="Contacto">
        <h2>{L("Contacto", "Contact")}</h2>
        <ul>
          <li><a href="{MAIL_ES}" data-es-href="{MAIL_ES}" data-en-href="{MAIL_EN}" data-zh-href="{MAIL_ZH}">Email</a></li>
          <li><a href="{LINKEDIN}" rel="me noopener" target="_blank">LinkedIn</a></li>
          <li><a href="{GITHUB}" rel="me noopener" target="_blank">GitHub</a></li>
          <li><a href="https://pocketboy-games.itch.io" rel="noopener" target="_blank">itch.io</a></li>
        </ul>
      </nav>
      <nav aria-label="Legal">
        <h2>{L("Sitio", "Site")}</h2>
        <ul>
          <li><a href="privacidad.html">{L("Privacidad", "Privacy")}</a></li>
          <li><a href="cv_octavio_gregorio.pdf" download>{L("CV en PDF", "CV (PDF)")}</a></li>
        </ul>
      </nav>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Octavio Gregorio Guerrero</span>
      <span>Elda, Alicante · {L("España", "Spain")}</span>
    </div>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Volver arriba" data-es-aria-label="Volver arriba" data-en-aria-label="Back to top">{icon("arrow-up")}</button>
{cta}
</body>
</html>
"""


def breadcrumbs(items):
    lis = []
    for i, (es, en, href) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li><span aria-current="page">{L(es, en) if es != en else es}</span></li>')
        else:
            lis.append(f'<li><a href="{href}">{L(es, en) if es != en else es}</a></li>')
    return f'<nav class="crumbs wrap" aria-label="Migas de pan" data-es-aria-label="Migas de pan" data-en-aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'


def img(src, alt, w, h, cls="", eager=False, sizes=None, srcset=None):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    ss = f' srcset="{srcset}"' if srcset else ""
    sz = f' sizes="{sizes}"' if sizes else ""
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{src}"{ss}{sz} alt="{html.escape(alt)}" width="{w}" height="{h}" {load} decoding="async">'


def work(name):
    return f"assets/img/work/{name}-800.webp 800w, assets/img/work/{name}-1600.webp 1600w"


def gallery_item(name, alt, w=800, h=450, full_cls=""):
    return f"""<figure class="{full_cls}"><button type="button" data-full="assets/img/work/{name}-1600.webp" aria-label="{html.escape(alt)} — ampliar"><span class="skel" style="display:block">{img(f"assets/img/work/{name}-800.webp", alt, w, h)}</span></button></figure>"""


def lightbox():
    return f"""<dialog class="lightbox" id="lightbox" aria-label="Imagen ampliada">
  <button class="close" type="button" aria-label="Cerrar" data-en-aria-label="Close" data-es-aria-label="Cerrar">{icon("close")}</button>
  <img src="data:," alt="">
  <p></p>
</dialog>"""


def yt(vid, title_es, title_en, label_es="Ver vídeo", label_en="Watch video"):
    return f"""<div class="yt" data-id="{vid}" data-title="{html.escape(title_es)}">
  <button type="button" aria-label="{html.escape(label_es)}: {html.escape(title_es)}" data-es-aria-label="{html.escape(label_es)}: {html.escape(title_es)}" data-en-aria-label="{html.escape(label_en)}: {html.escape(title_en)}">
    <img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" width="480" height="360" loading="lazy" decoding="async">
    <span class="play">{icon("play")}{L(label_es, label_en)}</span>
  </button>
</div>"""


def cta_band():
    return f"""<section class="wrap" aria-label="Contacto" data-es-aria-label="Contacto" data-en-aria-label="Contact">
  <div class="cta-band" data-reveal>
    <div>
      <h2>{L("¿Buscas a alguien para un equipo así?", "Looking for someone for a team like this?")}</h2>
      <p>{L("Disponible para incorporación inmediata. Suelo responder en menos de 24 h.", "Available to start now. I usually reply within 24 h.")}</p>
    </div>
    <a class="btn" href="index.html#contacto">{L("Escríbeme", "Get in touch")}{icon("arrow", "arrow")}</a>
  </div>
</section>"""


def next_case(prev, nxt):
    return f"""<nav class="wrap next-case" aria-label="Más proyectos" data-es-aria-label="Más proyectos" data-en-aria-label="More work">
  <a href="{prev[0]}"><small>← {L("Anterior", "Previous")}</small><b>{prev[1]}</b></a>
  <a href="{nxt[0]}"><small>{L("Siguiente", "Next")} →</small><b>{nxt[1]}</b></a>
</nav>"""


def write(name, content):
    content = add_zh_attrs(content)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name, len(content))


# =====================================================================
# INDEX
# =====================================================================
FAQ = [
    ("¿Cuándo podrías empezar?", "When could you start?",
     "YA. Acabo de terminar el grado en 2026 y estoy disponible para incorporarme de inmediato.",
     "NOW. I just finished my degree in 2026 and I'm available to start immediately."),
    ("¿Qué tipo de puesto buscas?", "What kind of role are you after?",
     "Gestión de proyectos tecnológicos (project manager, producer, coordinación técnica) o desarrollo en cualquier entorno tecnológico. Donde mejor encajo es en un sitio en el que pueda organizar el trabajo del equipo sin perder el contacto con el código ni con las personas.",
     "Tech project management (project manager, producer, technical coordination) or development in any tech environment. I fit best where I can organise a team's work without losing touch with the code — or with the people."),
    ("¿Has coordinado equipos de verdad?", "Have you actually led teams?",
     "En la carrera, sí, y de forma continuada: en Castle of Shadows (Zero Studios) y en Tower Hero (PocketBoy) coordiné al equipo durante todo el curso: reparto de tareas, prioridades y seguimiento de entregas. En casi todos los proyectos en grupo acabé haciendo ese papel. Aún no lo he hecho en una empresa, y es justo lo que busco.",
     "At university, yes, consistently: on Castle of Shadows (Zero Studios) and Tower Hero (PocketBoy) I coordinated the team for the whole year — task split, priorities and delivery tracking. I ended up in that role in almost every group project. I haven't done it inside a company yet, and that's exactly what I'm looking for."),
    ("¿De qué va tu TFG?", "What was your thesis about?",
     'Casi todos los ordenadores modernos tienen una GPU dedicada y otra integrada que no se usa. Construí un sistema que le pasa cada frame a la integrada para reescalarlo con IA en tiempo real, sin tocar el juego. Obtuve una nota de 10 con mención a Matrícula de Honor. <a class="link" href="tfg-superresolucion.html">Aquí lo cuento entero</a>.',
     'Almost every modern computer has a dedicated GPU plus an integrated one that sits idle. I built a system that hands every frame to the integrated GPU to upscale it with AI in real time, without touching the game. It got a 10/10 with honours. <a class="link" href="tfg-superresolucion.html">Full write-up here</a>.'),
    ("¿Qué idiomas hablas?", "Which languages do you speak?",
     "Español nativo desde el lanzamiento del Grand Theft Auto: Vice City e inglés avanzado: tengo el B2 oficial de la EOI y completé el curso de C1. Puedo trabajar, documentar y hacer reuniones en inglés.",
     "Native Spanish since Grand Theft Auto: Vice City came out, and advanced English: I hold the official B2 (EOI) and completed the C1 course. I can work, write docs and run meetings in English."),
]


def index():
    faq_ld = {
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a.split("<a")[0]).strip()}} for q, _, a, _ in FAQ],
    }
    site_ld = {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": "Octavio Gregorio — Portfolio", "inLanguage": ["es", "en"], "publisher": {"@id": BASE + "#person"}}
    out = head(
        path="index.html",
        title_es="Octavio Gregorio · Ingeniero Multimedia, Game Dev y Project Manager",
        title_en="Octavio Gregorio · Multimedia Engineer, Game Dev & Project Manager",
        desc_es="Portfolio de Octavio Gregorio Guerrero, ingeniero multimedia en Elda (Alicante). Videojuegos en C++ y Z80, TFG de superresolución con IA (10, MH) y coordinación de equipos.",
        desc_en="Portfolio of Octavio Gregorio Guerrero, multimedia engineer in Elda (Alicante, Spain). Games in C++ and Z80, AI super-resolution thesis (10/10) and team coordination.",
        ld_json=ld(PERSON, site_ld, faq_ld),
        og_type="profile",
    )
    out += header()
    faq_html = "\n".join(
        f"""<details data-reveal style="--i:{i}"><summary>{L(qe, qn)}<span class="plus" aria-hidden="true"></span></summary><div class="answer">{L(ae, an, "p")}</div></details>"""
        for i, (qe, qn, ae, an) in enumerate(FAQ)
    )
    out += f"""<main id="main" tabindex="-1">

<!-- HERO -->
<section class="hero wrap" aria-labelledby="hero-title">
  <div class="hero-grid">
    <div>
      <p class="status" data-enter style="--i:0"><span class="dot" aria-hidden="true"></span>{L("Disponible ahora · Elda, Alicante", "Available now · Elda, Alicante")}</p>
      <h1 id="hero-title" class="display" data-enter style="--i:1">Octavio<br>Gregorio <span class="light">Guerrero</span></h1>
      <p class="lede" data-enter style="--i:2">{L("Ingeniero multimedia. Programo, coordino equipos, organizo el trabajo y <em>me preocupo por el producto</em>.", "Multimedia engineer. I code, lead teams, organise the work and <em>care about the product</em>.")}</p>
      <div class="hero-actions" data-enter style="--i:3" data-cta-trigger>
        <a class="btn btn--primary" href="#contacto">{L("Escríbeme", "Get in touch")}{icon("arrow", "arrow")}<small class="tiny">{L("porfa :)", "please :)")}</small></a>
        <a class="btn" href="cv_octavio_gregorio.pdf" download>{icon("download", "arrow-down")}{L("Descargar CV", "Download CV")}</a>
      </div>
      <p class="hero-note" data-enter style="--i:4">{icon("clock")}{L("Suelo responder en menos de 24 h", "I usually reply within 24 h")}</p>
    </div>
    <figure class="portrait" data-enter>
      <div class="frame">
        <picture>
          <source type="image/webp" srcset="assets/img/octavio-480.webp 480w, assets/img/octavio-800.webp 800w" sizes="(max-width: 860px) 300px, 400px">
          <img src="assets/img/octavio-800.jpg" alt="Retrato de Octavio Gregorio sonriendo, con gafas y camisa blanca" data-es-alt="Retrato de Octavio Gregorio sonriendo, con gafas y camisa blanca" data-en-alt="Portrait of Octavio Gregorio smiling, wearing glasses and a white shirt" width="800" height="1000" fetchpriority="high" decoding="async">
        </picture>
      </div>
      <img class="sticker" src="assets/img/icon-192.png" alt="" width="84" height="84">
      <figcaption>{L("¡Hola! Soy yo, el pulpo es mi logo. Porque de Octavio… Octa… Oct… que sale 8… ¿lo pillas?… ¿no?… Bueno, pues soy yo :)", "Hi! That's me, and the octopus is my logo. Because Octavio… Octa… Oct… that's 8… get it?… no?… Well, anyway, that's me :)")}</figcaption>
    </figure>
  </div>

  <ul class="proof" aria-label="Datos destacados" data-es-aria-label="Datos destacados" data-en-aria-label="Highlights">
    <li data-enter style="--i:5"><strong>10 · MH</strong><span>{L("Nota del TFG, con mención a Matrícula de Honor", "Thesis grade, with a distinction (Matrícula de Honor)")}</span></li>
    <li data-enter style="--i:6"><strong>GBRetroDev'25</strong><span>{L("Participante oficial con un juego de Game Boy en Z80", "Official entry with a Game Boy game in Z80")}</span></li>
    <li data-enter style="--i:7"><strong>{L("Motor propio", "Own engine")}</strong><span>{L("Castle of Shadows: C++ y OpenGL, coordinando al equipo", "Castle of Shadows: C++ and OpenGL, leading the team")}</span></li>
    <li data-enter style="--i:8"><strong>2026</strong><span>{L("Graduado en Ingeniería Multimedia (UA)", "BSc Multimedia Engineering (Univ. of Alicante)")}</span></li>
  </ul>
</section>

<!-- WORK -->
<section class="section" id="trabajo" aria-labelledby="work-title">
  <div class="wrap">
    <div class="section-head" data-reveal>
      <span class="num">01</span>
      <h2 id="work-title">{L("Proyectos elegidos", "Selected work")}</h2>
      <p>{L("Tres proyectos de los que me siento orgulloso.", "Three projects I'm proud of.")}</p>
    </div>

    <div class="cases">
      <a class="case-card case-card--wide" href="tfg-superresolucion.html" data-reveal>
        <div class="case-media skel">{img("assets/img/work/tfg-fsrcnn-1280.webp", "Minecraft con shaders reconstruido a 1080p por IA en la GPU integrada", 1280, 720, sizes="(max-width: 760px) 100vw, 620px").replace("<img ", "<img data-en-alt=\"Minecraft with shaders rebuilt to 1080p by AI on the integrated GPU\" ")}</div>
        <div class="case-body">
          <p class="case-kicker"><span>2025–26</span><span>TFG · {L("Investigación", "Research")}</span><span>10 · MH</span></p>
          <h3 class="case-title">{L("Reescalar juegos con IA usando la GPU que nadie usa", "Upscaling games with AI on the GPU nobody uses")}</h3>
          <p class="case-desc">{L("Un sistema que captura cada frame del juego y se lo pasa a la GPU integrada para reconstruirlo a resolución completa en tiempo real.", "A system that grabs every game frame and hands it to the integrated GPU to rebuild it at full resolution in real time.")}</p>
          <span class="case-more">{L("Leer el caso", "Read the case study")}{icon("arrow", "arrow")}</span>
        </div>
      </a>

      <a class="case-card" href="castle-of-shadows.html" data-reveal style="--i:1">
        <div class="case-media skel">{img("assets/img/work/cos-cover-800.webp", "Arte de Castle of Shadows: caballero con armadura low-poly sobre fondo rojo", 800, 450, srcset=work("cos-cover"), sizes="(max-width: 760px) 100vw, 540px").replace("<img ", "<img data-en-alt=\"Castle of Shadows key art: low-poly armoured knight on a red background\" ")}</div>
        <div class="case-body">
          <p class="case-kicker"><span>2025–26</span><span>Zero Studios</span><span>{L("Coordinador y programador", "Lead & programmer")}</span></p>
          <h3 class="case-title">Castle of Shadows</h3>
          <p class="case-desc">{L("Juego 3D de acción sobre un motor propio. Coordiné al equipo, programé el motor y sacamos el producto adelante.", "3D action game on an in-house engine. I led the team, programmed the engine and we shipped the product.")}</p>
          <span class="case-more">{L("Leer el caso", "Read the case study")}{icon("arrow", "arrow")}</span>
        </div>
      </a>

      <a class="case-card" href="tower-hero.html" data-reveal style="--i:2">
        <div class="case-media skel" style="background:#95a297">{img("assets/img/work/towerhero-cover.webp", "Portada de Tower Hero: un héroe en lo alto de una torre rodeado de esqueletos y murciélagos, en pixel art", 900, 900, eager=False).replace('<img ', '<img style="object-fit:contain;image-rendering:pixelated" ')}</div>
        <div class="case-body">
          <p class="case-kicker"><span>2025</span><span>PocketBoy</span><span>{L("PM y programador", "PM & programmer")}</span></p>
          <h3 class="case-title">Tower Hero</h3>
          <p class="case-desc">{L("Un tower defense para Game Boy escrito en ensamblador. Entrada oficial de GBRetroDev'25.", "A Game Boy tower defense written in assembly. Official GBRetroDev'25 entry.")}</p>
          <span class="case-more">{L("Leer el caso", "Read the case study")}{icon("arrow", "arrow")}</span>
        </div>
      </a>
    </div>

    <h3 class="more-head" data-reveal>{L("Más proyectos", "More projects")}</h3>
    <ul class="more-list">
      <li data-reveal><div class="more-row">
        <span class="year">2026</span>
        <div><h3>3DOCNA <span class="badge">{L("En construcción", "Work in progress")}</span></h3><p>{L("Mi pequeño negocio de impresión 3D: pedidos personalizados y catálogo propio en PLA, PETG y TPU. Diseño, producción y clientes.", "My small 3D-printing business: custom orders and an own catalogue in PLA, PETG and TPU. Design, production and customers.")}</p></div>
        <span class="stack">Blender · OpenSCAD · Bambu Lab A1</span><span class="go" aria-hidden="true"></span></div></li>
      <li data-reveal><a class="more-row" href="https://github.com/octa815/UA_PixelDepot" target="_blank" rel="noopener">
        <span class="year">2025</span>
        <div><h3>PixelDepot</h3><p>{L("Gestor de assets para estudios de videojuegos, accesible (WCAG 2.1).", "Asset manager for game studios, built to WCAG 2.1.")}</p></div>
        <span class="stack">React · Node · MongoDB</span>{icon("ext", "go")}</a></li>
      <li data-reveal><a class="more-row" href="https://youtu.be/JT4wM71QWTo" target="_blank" rel="noopener">
        <span class="year">2024</span>
        <div><h3>2Dymiros</h3><p>{L("Juego de cartas en C++ sin motor: turnos, IA básica y estados de partida.", "Card game in C++ with no engine: turns, basic AI and game states.")}</p></div>
        <span class="stack">C++</span>{icon("ext", "go")}</a></li>
      <li data-reveal><a class="more-row" href="https://youtu.be/HxZO4kSogeQ" target="_blank" rel="noopener">
        <span class="year">2025</span>
        <div><h3>{L("Cortometraje", "Short film")}</h3><p>{L("Rodaje con cámaras profesionales y postproducción completa: montaje y color.", "Shot on professional cameras, fully post-produced: edit and grade.")}</p></div>
        <span class="stack">DaVinci Resolve</span>{icon("ext", "go")}</a></li>
      <li data-reveal><a class="more-row" href="interiorismo.html">
        <span class="year">2023</span>
        <div><h3>{L("Un interior dentro del Taj Mahal", "An interior inside the Taj Mahal")}</h3><p>{L("Modelado e iluminación de día y de noche.", "Modelling and day/night lighting.")}</p></div>
        <span class="stack">Blender</span>{icon("arrow", "go")}</a></li>
      <li data-reveal><a class="more-row" href="animation.html">
        <span class="year">2023</span>
        <div><h3>{L("O.V.O., un robot en la Luna", "O.V.O., a robot on the Moon")}</h3><p>{L("Modelado, rigging y animación de un robot cuadrúpedo.", "Modelling, rigging and animating a four-legged robot.")}</p></div>
        <span class="stack">Blender</span>{icon("arrow", "go")}</a></li>
      <li data-reveal><a class="more-row" href="scripting.html">
        <span class="year">2023</span>
        <div><h3>{L("Lluvia procedural", "Procedural rain")}</h3><p>{L("Script en Python que genera una escena de lluvia editable.", "Python script that builds an editable rain scene.")}</p></div>
        <span class="stack">Python · Blender</span>{icon("arrow", "go")}</a></li>
    </ul>
  </div>
</section>

<!-- ABOUT -->
<section class="section" id="sobre-mi" aria-labelledby="about-title">
  <div class="wrap">
    <div class="section-head" data-reveal>
      <span class="num">02</span>
      <h2 id="about-title">{L("Sobre mí", "About")}</h2>
    </div>
    <div class="about-grid">
      <div class="about-text" data-reveal>
        {L("Me gradué en Ingeniería Multimedia en la Universidad de Alicante en 2026. Vengo de los videojuegos, pero lo que más disfruto es que un proyecto con mucha gente salga bien.", "I graduated in Multimedia Engineering from the University of Alicante in 2026. I come from games, but what I enjoy most is a project with lots of people going well.", "p")}
        {L("En casi todos los trabajos en grupo de la carrera acabé coordinando: repartir tareas, marcar un ritmo y decidir qué se recorta cuando no llega el tiempo. Por eso busco puestos de <strong>gestión de proyectos tecnológicos</strong> sin dejar de tocar código.", "In almost every group project at university I ended up coordinating: splitting tasks, setting a pace and deciding what gets cut when time runs out. That's why I'm looking for <strong>tech project management</strong> roles where I still touch code.", "p")}
        <ul class="ways">
          <li><span class="n">01</span><div><b>{L("Organizo antes de programar", "I plan before I code")}</b>{L("Tareas repartidas, ritmos claros y todo el mundo sabiendo qué toca esta semana.", "Tasks split, a clear pace, and everyone knowing what this week is for.")}</div></li>
          <li><span class="n">02</span><div><b>{L("Que salga adelante", "Ship it first")}</b>{L("Lo importante es entregar; el detalle se pule sobre algo que ya funciona.", "Delivering comes first; polish happens on something that already works.")}</div></li>
          <li><span class="n">03</span><div><b>{L("Aprendo lo que haga falta", "I learn what the project needs")}</b>{L("De ensamblador Z80 a OpenCL: si el proyecto lo pide, me pongo.", "From Z80 assembly to OpenCL: if the project needs it, I pick it up.")}</div></li>
        </ul>
      </div>
      <div data-reveal style="--i:1">
        <h3 class="sub-h">{L("Herramientas", "Toolbox")}</h3>
        <dl class="stack-list">
          <div><dt>{L("Lenguajes", "Languages")}</dt><dd>C, C++, JavaScript, Python, Java, PHP, ASM Z80, HTML/CSS</dd></div>
          <div><dt>Game dev</dt><dd>OpenGL, raylib, Game Boy ASM, Unreal Engine 5, Unity</dd></div>
          <div><dt>Web</dt><dd>React, Node.js, Express, MongoDB, Angular, Ionic, WordPress</dd></div>
          <div><dt>{L("Datos", "Data")}</dt><dd>MySQL, MongoDB, Oracle DB</dd></div>
          <div><dt>{L("Entorno", "Tooling")}</dt><dd>Git, GitHub, Docker, CI/CD, VS Code, Visual Studio, Android Studio</dd></div>
          <div><dt>{L("3D y vídeo", "3D & video")}</dt><dd>Blender, OpenSCAD, {L("impresión FDM (Bambu Lab A1)", "FDM printing (Bambu Lab A1)")}, DaVinci Resolve</dd></div>
          <div><dt>{L("Idiomas", "Languages")}</dt><dd>{L("Español nativo · Inglés avanzado (B2, curso C1)", "Spanish (native) · English (advanced, B2 + C1 course)")}</dd></div>
        </dl>
        <ol class="timeline" aria-label="Formación" data-es-aria-label="Formación" data-en-aria-label="Education">
          <li><span class="when">2026</span><div><b>{L("Grado en Ingeniería Multimedia", "BSc Multimedia Engineering")}</b>{L("Universidad de Alicante · Escuela Politécnica Superior", "University of Alicante · Polytechnic School")}</div></li>
          <li><span class="when">2025–26</span><div><b>{L("Prácticas y TFG en la EPS", "Internship & thesis at the EPS")}</b>{L("Superresolución con IA en GPU híbrida · 10, Matrícula de Honor", "AI super-resolution on hybrid GPUs · 10/10 with honours")}</div></li>
          <li><span class="when">2020</span><div><b>{L("B2 de inglés", "English B2")}</b>{L("EOI Elda · curso de C1 completado", "EOI Elda · C1 course completed")}</div></li>
          <li><span class="when">2018–20</span><div><b>{L("Bachillerato Tecnológico", "High school, technology track")}</b><span>Colegio Sagrada Familia, Elda</span></div></li>
        </ol>
      </div>
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="section" id="faq" aria-labelledby="faq-title">
  <div class="wrap">
    <div class="section-head" data-reveal>
      <span class="num">03</span>
      <h2 id="faq-title">{L("Lo que me preguntan los entrevistadores en la primera llamada", "What interviewers ask me on the first call")}</h2>
      <p>{L("(Por favor, llamadme.)", "(Please call me.)")}</p>
    </div>
    <div class="faq">
{faq_html}
    </div>
  </div>
</section>

<!-- CONTACT -->
<section class="section" id="contacto" aria-labelledby="contact-title" data-cta-hide>
  <div class="wrap">
    <div class="section-head" data-reveal>
      <span class="num">04</span>
      <h2 id="contact-title">{L("Hablemos", "Let's talk")}</h2>
      <p>{L("Cuéntame qué buscas: un puesto, un proyecto o una duda sobre algo de aquí.", "Tell me what you're after: a role, a project, or a question about something here.")}</p>
    </div>
    <div class="contact-grid">
      <div class="direct" data-reveal>
        <div class="quick">
          <h3>{L("Escríbeme por email", "Email me")}</h3>
          <p>{L("Es la forma más rápida. Suelo contestar en menos de 24 h.", "It's the fastest way. I usually reply within 24 h.")}</p>
          <button class="copy-email" type="button" data-copy="{EMAIL}">
            <span class="addr">{EMAIL}</span>
            <span class="state"><span class="idle">{L("Copiar", "Copy")}</span><span class="done" role="status">{icon("check").replace('<svg ', '<svg width="14" height="14" style="display:inline;vertical-align:-2px" ')} {L("Copiado", "Copied")}</span></span>
          </button>
          <div class="row" style="margin-top:12px">
            <a class="btn btn--primary" href="{MAIL_ES}" data-es-href="{MAIL_ES}" data-en-href="{MAIL_EN}" data-zh-href="{MAIL_ZH}">{icon("mail")}{L("Abrir email", "Open email")}</a>
            <a class="btn" href="https://wa.me/{PHONE_WA}?text={WA_ES}" data-es-href="https://wa.me/{PHONE_WA}?text={WA_ES}" data-en-href="https://wa.me/{PHONE_WA}?text={WA_EN}" data-zh-href="https://wa.me/{PHONE_WA}?text={WA_ZH}" target="_blank" rel="noopener">{icon("whatsapp")}WhatsApp</a>
          </div>
        </div>
      </div>

      <aside class="direct" data-reveal style="--i:1" aria-label="Redes" data-es-aria-label="Redes" data-en-aria-label="Profiles">
        <ul class="socials">
          <li><a href="{LINKEDIN}" target="_blank" rel="me noopener">{icon("linkedin")}<span>LinkedIn <small>/in/octagg</small></span>{icon("ext", "go").replace('<svg ', '<svg width="16" height="16" ')}</a></li>
          <li><a href="{GITHUB}" target="_blank" rel="me noopener">{icon("github")}<span>GitHub <small>@octa815</small></span>{icon("ext", "go").replace('<svg ', '<svg width="16" height="16" ')}</a></li>
          <li><a href="https://pocketboy-games.itch.io" target="_blank" rel="noopener">{icon("itch")}<span>itch.io <small>PocketBoy</small></span>{icon("ext", "go").replace('<svg ', '<svg width="16" height="16" ')}</a></li>
          <li><a href="cv_octavio_gregorio.pdf" download>{icon("download")}<span>{L("CV en PDF", "CV (PDF)")} <small>2026</small></span>{icon("arrow", "go").replace('<svg ', '<svg width="16" height="16" ')}</a></li>
        </ul>
      </aside>
    </div>
  </div>
</section>
</main>
"""
    out += footer()
    write("index.html", out)


# =====================================================================
# CASE STUDY helper
# =====================================================================
def case_page(*, scripts=(), file, title, h1, lede, eyebrow, facts, cover, toc, body, prev, nxt, desc_es, desc_en, title_en, extra_ld=None, lightbox_on=False, crumb_parent=("Proyectos", "Work", "index.html#trabajo")):
    crumbs = [("Inicio", "Home", "index.html"), crumb_parent, (title, title, file)]
    art = {
        "@type": "CreativeWork",
        "name": title,
        "url": BASE + file,
        "author": {"@id": BASE + "#person"},
        "description": desc_es,
        "inLanguage": "es",
    }
    if extra_ld:
        art.update(extra_ld)
    out = head(
        path=file,
        title_es=f"{title} · Caso de estudio · Octavio Gregorio",
        title_en=f"{title_en} · Case study · Octavio Gregorio",
        desc_es=desc_es,
        desc_en=desc_en,
        ld_json=ld(PERSON, crumbs_ld([("Inicio", "index.html"), (crumb_parent[0], crumb_parent[2]), (title, file)]), art),
        og_type="article",
    )
    out += header("work")
    facts_html = "".join(f"<div><dt>{L(a, b)}</dt><dd>{c}</dd></div>" for a, b, c in facts)
    toc_html = "".join(f'<li><a href="#{i}">{L(es, en)}</a></li>' for i, es, en in toc)
    out += f"""<main id="main" tabindex="-1">
{breadcrumbs(crumbs)}
<header class="case-hero wrap">
  <p class="eyebrow" data-enter style="--i:0">{eyebrow}</p>
  <h1 class="display" data-enter style="--i:1">{h1}</h1>
  <p class="lede" data-enter style="--i:2">{lede}</p>
  <dl class="facts" data-enter style="--i:3">{facts_html}</dl>
</header>
<div class="wrap" data-enter style="--i:4">
{cover}
</div>
<div class="wrap prose-grid">
  <aside class="toc" aria-label="En esta página" data-es-aria-label="En esta página" data-en-aria-label="On this page">
    <p class="sub-h">{L("En esta página", "On this page")}</p>
    <ol>{toc_html}</ol>
  </aside>
  <article class="prose">
{body}
  </article>
</div>
{cta_band()}
{next_case(prev, nxt)}
</main>
{lightbox() if lightbox_on else ""}
{"".join(scripts)}
"""
    out += footer()
    write(file, out)


# =====================================================================
# TFG
# =====================================================================
def fig(src, w, h, alt_es, alt_en, cap_es, cap_en, zoom=None, cls=""):
    inner = f'<img src="{src}" alt="{html.escape(alt_es)}" data-es-alt="{html.escape(alt_es)}" data-en-alt="{html.escape(alt_en)}" width="{w}" height="{h}" loading="lazy" decoding="async">'
    if zoom:
        inner = f'<div class="gallery"><button type="button" data-full="{zoom}" aria-label="{html.escape(alt_es)}" data-es-aria-label="{html.escape(alt_es)}" data-en-aria-label="{html.escape(alt_en)}"><span class="skel" style="display:block">{inner}</span></button></div>'
    else:
        inner = f'<div class="skel figbox">{inner}</div>'
    return f'<figure class="{cls}">{inner}<figcaption>{L(cap_es, cap_en)}</figcaption></figure>'


def tfg():
    modes = [("Rendimiento", "Performance", "480×270 · x4", "60", "29.3 dB"),
             ("Equilibrado", "Balanced", "640×360 · x3", "48", "31.0 dB"),
             ("Calidad", "Quality", "960×540 · x2", "25", "35.0 dB")]
    mode_rows = "".join(f"<tr><td>{L(a, b)}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in modes)
    body = f"""
<section id="problema" data-reveal>
  <h2>{L("El problema", "The problem")}</h2>
  {L("La mayoría de equipos de juego tienen dos GPUs: la dedicada (dGPU), que renderiza el juego, y una integrada (iGPU) dentro del procesador. Durante una partida, la dedicada va al límite y la integrada está prácticamente parada. Es potencia de cálculo que ya has pagado y no usas.", "Most gaming machines have two GPUs: the dedicated one (dGPU) that renders the game, and an integrated one (iGPU) inside the CPU. During a session the dGPU is maxed out while the iGPU sits almost idle — compute you've paid for and never use.", "p")}
  {L("DLSS, FSR y XeSS hacen el reescalado en la misma GPU que renderiza, así que compiten por ella. La pregunta del trabajo: ¿se puede pasar esa carga a la iGPU, en tiempo real y sin tocar el juego?", "DLSS, FSR and XeSS upscale on the same GPU that renders, so they compete for it. The question: can that load move to the iGPU, in real time, without touching the game?", "p")}
</section>

<section id="arquitectura" data-reveal>
  <h2>{L("La arquitectura", "The architecture")}</h2>
  {L("La dGPU renderiza el juego en pequeño; el frame viaja una sola vez por el bus PCIe hasta la memoria principal y la iGPU, que comparte esa memoria con la CPU, lo reconstruye a resolución completa. El jugador solo ve la reconstrucción.", "The dGPU renders the game small; the frame crosses the PCIe bus once into main memory, and the iGPU — which shares that memory with the CPU — rebuilds it at full resolution. The player only sees the reconstruction.", "p")}
  {fig("assets/img/work/tfg-arquitectura.webp", 1400, 842, "Diagrama de la arquitectura híbrida: la dGPU renderiza en pequeño, el frame pasa a la memoria compartida y la iGPU lo reconstruye con IA", "Hybrid architecture diagram: the dGPU renders small, the frame goes to shared memory and the iGPU rebuilds it with AI", "Figura 3.1 de la memoria: reparto de tareas entre CPU, iGPU y dGPU.", "Figure 3.1 from the thesis: how work is split between CPU, iGPU and dGPU.", zoom="assets/img/work/tfg-arquitectura.webp")}
</section>

<section id="sistema" data-reveal>
  <h2>{L("Cómo funciona por dentro", "How it works inside")}</h2>
  {L("Es un sistema completo que funciona con cualquier aplicación OpenGL en Linux, sin modificarla. Todo el código es abierto.", "It's an end-to-end system that works with any OpenGL application on Linux, unmodified. All the code is open source.", "p")}
  <ol class="pipeline">
    <li><b>{L("Render", "Render")}</b>{L("El juego corre oculto en una pantalla virtual (Xvfb) y la dGPU lo renderiza a baja resolución vía PRIME.", "The game runs hidden on a virtual display (Xvfb) and the dGPU renders it at low resolution via PRIME.")}</li>
    <li><b>{L("Captura", "Capture")}</b>{L("Una librería en C inyectada con <code>LD_PRELOAD</code> intercepta <code>glXSwapBuffers</code> y copia el frame.", "A C library injected with <code>LD_PRELOAD</code> intercepts <code>glXSwapBuffers</code> and copies the frame.")}</li>
    <li><b>{L("Transferencia", "Transfer")}</b>{L("El frame se publica en memoria compartida POSIX, sin copias extra.", "The frame is published to POSIX shared memory, with no extra copies.")}</li>
    <li><b>{L("Reconstrucción", "Rebuild")}</b>{L("La iGPU lo reescala con FSRCNN (OpenVINO) y se muestra en una sola ventana.", "The iGPU upscales it with FSRCNN (OpenVINO) and it's shown in a single window.")}</li>
  </ol>
  <h3>{L("Los detalles que costaron", "The details that took work")}</h3>
  <ul>
    <li>{L("<strong>Motores modernos:</strong> Minecraft (LWJGL3/GLFW) no llama a <code>glXSwapBuffers</code> directamente, sino que pide el puntero en tiempo de ejecución. El wrapper intercepta también <code>dlsym</code> y <code>glXGetProcAddressARB</code>.", "<strong>Modern engines:</strong> Minecraft (LWJGL3/GLFW) doesn't call <code>glXSwapBuffers</code> directly; it asks for the pointer at runtime. The wrapper also intercepts <code>dlsym</code> and <code>glXGetProcAddressARB</code>.")}</li>
    <li>{L("<strong>Shaders que esconden el frame:</strong> Iris/Photon dejan un framebuffer intermedio enlazado y la captura se paraba en silencio. Se fuerza la lectura del framebuffer de la ventana y se restaura después.", "<strong>Shaders hiding the frame:</strong> Iris/Photon leave an intermediate framebuffer bound and capture silently stopped. The wrapper forces a read from the window framebuffer and restores it afterwards.")}</li>
    <li>{L("<strong>Captura sin presentación:</strong> en la pantalla virtual, presentar cada frame por software era el cuello de botella. Como nadie ve esa pantalla, el wrapper captura y no presenta: el render pasó de ~13 a 44,6 FPS.", "<strong>Capture without presenting:</strong> on the virtual display, presenting each frame in software was the bottleneck. Since nobody sees that display, the wrapper captures and skips presenting: render went from ~13 to 44.6 FPS.")}</li>
    <li>{L("<strong>Jugar de verdad:</strong> teclado y ratón se reenvían al juego oculto con XTEST, en modo relativo durante la partida y absoluto en los menús.", "<strong>Actually playable:</strong> keyboard and mouse are forwarded to the hidden game via XTEST — relative during gameplay, absolute in menus.")}</li>
  </ul>
</section>

<section id="resultados" data-reveal>
  <h2>{L("Qué salió", "Results")}</h2>
  {L("Ocho experimentos en un sobremesa con Intel Core Ultra 7 265K (con iGPU) y NVIDIA RTX 5060, usando glxgears, SuperTuxKart y Minecraft con el paquete de shaders Photon para saturar la dGPU.", "Eight experiments on a desktop with an Intel Core Ultra 7 265K (with iGPU) and an NVIDIA RTX 5060, using glxgears, SuperTuxKart and Minecraft with the Photon shader pack to saturate the dGPU.", "p")}
  <ul class="numbers">
    <li><b>+33&nbsp;%</b>{L("de fluidez frente a renderizar nativo a 1080p (57,6 frente a 43,4 FPS).", "smoother than native rendering at 1080p (57.6 vs 43.4 FPS).")}</li>
    <li><b>×2</b>{L("casi, frente al nativo en 4K (54,9 frente a 25,7 FPS).", "almost, versus native at 4K (54.9 vs 25.7 FPS).")}</li>
    <li><b>15/15</b>{L("combinaciones en las que la iGPU gana a hacer la IA en la propia dGPU, hasta +26,6 FPS.", "combinations where the iGPU beats running the AI on the dGPU itself, up to +26.6 FPS.")}</li>
    <li><b>&lt;1&nbsp;ms</b>{L("para capturar y mover cada frame: menos del 3&nbsp;% del retardo.", "to capture and move each frame: under 3% of the latency.")}</li>
  </ul>
  {fig("assets/img/work/tfg-fps-x3.webp", 1040, 650, "Gráfica de FPS del juego según la resolución de entrada con escala x3: la híbrida se mantiene arriba mientras la dedicada y la nativa caen", "Game FPS by input resolution at x3: hybrid stays on top while dedicated and native drop", "FPS del juego con escala x3: híbrida (IA en iGPU), dedicada (IA en dGPU) y render nativo.", "Game FPS at x3 scale: hybrid (AI on iGPU), dedicated (AI on dGPU) and native render.", zoom="assets/img/work/tfg-fps-x3.webp")}
  {L("La clave está en un experimento de carga: con la dGPU libre, la inferencia allí es 2,5 veces más rápida que en la iGPU. Pero cuando la dGPU está ocupada renderizando, su tiempo se triplica (de 4,1 a 11,1 ms) mientras la iGPU sigue estable. La ventaja no es que la iGPU sea más rápida: es que libera a la dGPU justo cuando más falta hace.", "The key is a load experiment: with the dGPU free, inference there is 2.5× faster than on the iGPU. But once the dGPU is busy rendering, its time triples (4.1 → 11.1 ms) while the iGPU stays flat. The win isn't that the iGPU is faster — it's that it frees the dGPU exactly when it's needed.", "p")}
  <h3>{L("Modos de calidad", "Quality modes")}</h3>
  {L("Como en DLSS, el sistema ofrece tres preajustes (salida 1080p):", "Like DLSS, the system offers three presets (1080p output):", "p")}
  <table class="modes">
    <thead><tr><th>{L("Modo", "Mode")}</th><th>{L("Render", "Render")}</th><th>FPS</th><th>PSNR</th></tr></thead>
    <tbody>{mode_rows}</tbody>
  </table>
  {fig("assets/img/work/tfg-zoom.webp", 480, 830, "Ampliación de la misma zona: render nativo, reescalado bicúbico y reconstrucción FSRCNN", "Zoomed crop of the same area: native render, bicubic upscale and FSRCNN reconstruction", "De arriba abajo: nativo, bicúbico y FSRCNN en la iGPU (modo Equilibrado).", "Top to bottom: native, bicubic and FSRCNN on the iGPU (Balanced mode).", zoom="assets/img/work/tfg-zoom.webp", cls="narrow")}
  {L("Y una conclusión honesta: la calidad la manda la resolución a la que renderizas (+11 dB de 144p a 720p), no el modelo. FSRCNN se eligió por ligero, no por listo, y apenas mejora al bicúbico. El margen de calidad está en usar un modelo mejor; la arquitectura ya funciona.", "And an honest takeaway: quality is driven by the render resolution (+11 dB from 144p to 720p), not the model. FSRCNN was picked for being light, not clever, and barely beats bicubic. The quality headroom is in a better model; the architecture already works.", "p")}
</section>

<section id="aprendido" data-reveal>
  <h2>{L("Lo que me llevo", "What I took away")}</h2>
  {L("Empezó en unas prácticas en la EPS en marzo de 2025 y acabó siendo el TFG en julio de 2026. Me obligó a bajar a capas que en la carrera solo había visto de pasada: interceptar llamadas de OpenGL, pelearme con drivers, compositores y servidores gráficos.", "It started as an internship at the EPS in March 2025 and became my thesis in July 2026. It pushed me into layers I'd only glimpsed at university: intercepting OpenGL calls, wrestling with drivers, compositors and display servers.", "p")}
  {L("Lo que más me enseñó fueron los errores: medidas que tuve que repetir por dejar el juego abierto de fondo, o una pantalla virtual que durante semanas parecía hacer inviable la arquitectura y acabó siendo su mejor escenario. Lo siguiente sería pasar el postprocesado a la GPU, montar un pipeline asíncrono y probar la NPU del procesador.", "What taught me most were the mistakes: measurements I had to redo because the game was left running in the background, or a virtual display that for weeks seemed to kill the idea and ended up being its best setup. Next steps would be moving post-processing to the GPU, an asynchronous pipeline and trying the CPU's NPU.", "p")}
  <div class="callout"><b>{L("Nota: 10 · Matrícula de Honor", "Grade: 10/10 · with distinction")}</b>{L("Tutores: Antonio Macía Lillo e Higinio Mora Mora (Dpto. de Tecnología Informática y Computación, Universidad de Alicante).", "Supervisors: Antonio Macía Lillo and Higinio Mora Mora (Dept. of Computer Technology, University of Alicante).")}</div>
  <p style="display:flex;flex-wrap:wrap;gap:10px"><a class="btn btn--ink" href="https://hdl.handle.net/10045/170538" target="_blank" rel="noopener">{L("Leer la memoria en RUA", "Read the thesis (RUA, Spanish)")}{icon("ext", "arrow")}</a><a class="btn" href="https://github.com/cloudlab-aia/game_external_proc" target="_blank" rel="noopener">{icon("github")}{L("Código en GitHub", "Code on GitHub")}</a></p>
</section>
"""
    cover = f"""<figure class="case-cover-fig"><div class="case-cover skel">{img("assets/img/work/tfg-fsrcnn-1280.webp", "Minecraft con shaders Photon: un río entre bambú, reconstruido a 1080p por FSRCNN en la iGPU desde 640×360", 1280, 720, eager=True).replace('<img ', '<img data-en-alt="Minecraft with Photon shaders: a river among bamboo, rebuilt to 1080p by FSRCNN on the iGPU from 640×360" ')}</div><figcaption>{L("Frame reconstruido por la iGPU: el juego renderizó a 640×360 y lo que ves sale a 1080p.", "Frame rebuilt by the iGPU: the game rendered at 640×360 and what you see comes out at 1080p.")}</figcaption></figure>"""
    case_page(
        file="tfg-superresolucion.html",
        title="TFG: superresolución con IA",
        title_en="Thesis: AI super-resolution",
        h1=L("Reescalar juegos con IA usando la GPU que nadie usa", "Upscaling games with AI on the GPU nobody uses"),
        lede=L("Trabajo de Fin de Grado: un sistema híbrido dGPU + iGPU que reconstruye cada frame a resolución completa en tiempo real, sin modificar el juego. Nota: 10 con mención a Matrícula de Honor.", "Bachelor's thesis: a hybrid dGPU + iGPU system that rebuilds every frame at full resolution in real time, without modifying the game. Graded 10/10 with distinction."),
        eyebrow=L("Caso de estudio · Investigación", "Case study · Research"),
        facts=[("Periodo", "Period", L("Mar 2025 – Jul 2026", "Mar 2025 – Jul 2026")), ("Tipo", "Type", L("TFG · Universidad de Alicante", "Thesis · Univ. of Alicante")), ("Resultado", "Result", L("10 · Matrícula de Honor", "10/10 · distinction")), ("Stack", "Stack", "C · Python · OpenGL/GLX · OpenVINO · ONNX Runtime · Linux")],
        cover=cover,
        toc=[("problema", "El problema", "The problem"), ("arquitectura", "La arquitectura", "The architecture"), ("sistema", "Cómo funciona", "How it works"), ("resultados", "Qué salió", "Results"), ("aprendido", "Lo que me llevo", "Takeaways")],
        body=body,
        prev=("tower-hero.html", "Tower Hero"),
        nxt=("castle-of-shadows.html", "Castle of Shadows"),
        desc_es="TFG de Octavio Gregorio (10, Matrícula de Honor): sistema híbrido dGPU + iGPU para superresolución con IA en videojuegos. +33 % de FPS frente al render nativo a 1080p.",
        desc_en="Octavio Gregorio's thesis (10/10, distinction): a hybrid dGPU + iGPU system for real-time AI super-resolution in games. +33% FPS over native rendering at 1080p.",
        extra_ld={"@type": "Thesis", "inSupportOf": "Grado en Ingeniería Multimedia", "sameAs": ["https://hdl.handle.net/10045/170538", "https://github.com/cloudlab-aia/game_external_proc"], "datePublished": "2026-09-10", "image": BASE + "assets/img/work/tfg-fsrcnn-1280.webp", "sourceOrganization": {"@type": "CollegeOrUniversity", "name": "Universidad de Alicante"}, "keywords": "superresolución, upscaling, GPU integrada, GPU dedicada, arquitectura híbrida, videojuegos, FSRCNN, RealESRGAN, OpenCL, OpenVINO"},
        lightbox_on=True,
    )


# =====================================================================
# CASTLE OF SHADOWS
# =====================================================================
def castle():
    body = f"""
<section id="proyecto" data-reveal>
  <h2>{L("El proyecto", "The project")}</h2>
  {L("Castle of Shadows es un videojuego 3D de acción y mazmorras hecho en equipo, dentro de Zero Studios, para la asignatura de Videojuegos de la carrera. La condición: nada de Unity ni Unreal. El motor lo construye el propio equipo en C++ sobre OpenGL y raylib.", "Castle of Shadows is a 3D action/dungeon game made as a team, under Zero Studios, for the Games course of my degree. The rule: no Unity, no Unreal. The team builds its own engine in C++ on top of OpenGL and raylib.", "p")}
  {L("Eso significa que cosas que un motor comercial da hechas (render, cámara, escena, entrada, colisiones) hay que diseñarlas, repartirlas y mantenerlas entre todos mientras el juego avanza.", "That means everything a commercial engine gives you for free (rendering, camera, scene, input, collisions) has to be designed, split up and maintained by the team while the game moves forward.", "p")}
  {yt("oQshnOxXmU0", "Castle of Shadows — tráiler", "Castle of Shadows — trailer", "Ver vídeo", "Watch video")}
</section>

<section id="rol" data-reveal>
  <h2>{L("Mi papel", "My role")}</h2>
  {L("Coordiné al equipo, programé el motor y me encargué de que el producto saliera adelante.", "I led the team, programmed the engine and made sure the product shipped.", "p")}
  <ul>
    <li>{L("<strong>Planificación:</strong> reparto de tareas y ritmo de trabajo del equipo durante todo el curso.", "<strong>Planning:</strong> splitting tasks and setting the team's pace for the whole year.")}</li>
    <li>{L("<strong>Prioridades:</strong> decidir qué funcionalidades entraban en cada entrega y cuáles esperaban.", "<strong>Priorities:</strong> deciding which features made each milestone and which waited.")}</li>
    <li>{L("<strong>Motor:</strong> programación del motor propio y participación en sus decisiones técnicas.", "<strong>Engine:</strong> programming the in-house engine and taking part in its technical decisions.")}</li>
    <li>{L("<strong>Seguimiento:</strong> controlar entregables para llegar a cada hito con algo jugable.", "<strong>Tracking:</strong> keeping an eye on deliverables so every milestone had something playable.")}</li>
  </ul>
</section>

<section id="leccion" data-reveal>
  <h2>{L("Por qué lo cuento", "Why it matters")}</h2>
  {L("Es el proyecto donde más se juntan las dos cosas que quiero hacer: entender la parte técnica lo bastante como para tomar decisiones con criterio, y organizar a la gente para que esas decisiones se conviertan en un juego terminado.", "It's the project where the two things I want to do meet: understanding the tech well enough to make sound calls, and organising people so those calls turn into a finished game.", "p")}
  <div class="callout"><b>{L("Capturas y vídeo, en camino", "More screenshots and video coming")}</b>{L('Se trabajará en la mejora del producto para pulirlo. Mientras, el equipo publica avances en <a class="link" href="https://www.instagram.com/realzerostudios/" target="_blank" rel="noopener">Instagram @realzerostudios</a>.', 'We\'ll keep improving and polishing the game. Meanwhile the team posts progress on <a class="link" href="https://www.instagram.com/realzerostudios/" target="_blank" rel="noopener">Instagram @realzerostudios</a>.')}</div>
</section>
"""
    cover = f"""<div class="case-cover skel">{img("assets/img/work/cos-cover-1600.webp", "Arte de Castle of Shadows: un caballero con armadura low-poly apoyado en su espada sobre fondo rojo, junto al logo del juego", 1600, 900, eager=True, srcset=work("cos-cover"), sizes="(max-width: 1200px) 100vw, 1120px").replace('<img ', '<img data-en-alt="Castle of Shadows key art: a low-poly armoured knight leaning on his sword over a red background, next to the game logo" ')}</div>"""
    case_page(
        file="castle-of-shadows.html",
        title="Castle of Shadows",
        title_en="Castle of Shadows",
        h1="Castle of Shadows",
        lede=L("Un juego 3D de acción y mazmorras sobre un motor propio en C++. Coordiné al equipo, programé el motor y sacamos el producto adelante.", "A 3D action/dungeon game on an in-house C++ engine. I led the team, programmed the engine and we shipped the product."),
        eyebrow=L("Caso de estudio · Videojuego en equipo", "Case study · Team game"),
        facts=[("Año", "Year", "2025–2026"), ("Equipo", "Team", "Zero Studios"), ("Rol", "Role", L("Coordinación · programación del motor", "Team lead · engine programming")), ("Stack", "Stack", "C++ · OpenGL · raylib")],
        cover=cover,
        toc=[("proyecto", "El proyecto", "The project"), ("rol", "Mi papel", "My role"), ("leccion", "Por qué lo cuento", "Why it matters")],
        body=body,
        prev=("tfg-superresolucion.html", L("TFG: superresolución", "Thesis: super-resolution")),
        nxt=("tower-hero.html", "Tower Hero"),
        desc_es="Castle of Shadows: videojuego 3D de acción con motor propio en C++, OpenGL y raylib. Octavio Gregorio coordinó al equipo de Zero Studios y programó el motor.",
        desc_en="Castle of Shadows: 3D action game on an in-house C++/OpenGL/raylib engine. Octavio Gregorio led the Zero Studios team and programmed the engine.",
        extra_ld={"@type": "VideoGame", "gamePlatform": "PC", "genre": "Action", "image": BASE + "assets/img/work/cos-cover-1600.webp", "author": {"@type": "Organization", "name": "Zero Studios"}, "contributor": {"@id": BASE + "#person"}},
    )


# =====================================================================
# TOWER HERO
# =====================================================================
def tower():
    shots = [
        ("towerhero-1", "Nivel 1: la torre en el centro del mapa y los primeros enemigos acercándose", "Level 1: the tower in the middle of the map with the first enemies closing in"),
        ("towerhero-2", "Nivel 2: la torre recibe el ataque de enemigos por varios flancos", "Level 2: the tower under attack from several sides"),
        ("towerhero-3", "Nivel 2 con la paleta oscura, justo al activar la energía de la torre", "Level 2 with the dark palette, right as the tower's energy fires"),
        ("towerhero-4", "Nivel 3: una oleada numerosa rodeando la torre", "Level 3: a large wave surrounding the tower"),
    ]
    gal = "".join(
        f"""<figure><button type="button" data-full="assets/img/work/{n}.webp" aria-label="{html.escape(es)}" data-en-aria-label="{html.escape(en)}" data-es-aria-label="{html.escape(es)}"><span class="skel" style="display:block"><img src="assets/img/work/{n}.webp" alt="{html.escape(es)}" data-es-alt="{html.escape(es)}" data-en-alt="{html.escape(en)}" width="800" height="724" loading="lazy" decoding="async"></span></button></figure>"""
        for n, es, en in shots
    )
    body = f"""
<section id="juego" data-reveal>
  <h2>{L("El juego", "The game")}</h2>
  {L("Las fuerzas oscuras avanzan hacia la torre de tu reino y hay que aguantar. Tocas a los enemigos para eliminarlos (algunos necesitan varios golpes). Cada seis derrotados se carga la energía de la torre, y con <kbd>A</kbd> la descargas contra todos. Si un solo enemigo llega a la torre, se acaba la partida.", "Dark forces march on your kingdom's tower and you have to hold. You tap enemies to take them out (some need several hits). Every six kills charge the tower's energy, and <kbd>A</kbd> unleashes it on everyone. If a single enemy reaches the tower, it's game over.", "p")}
  {L("Cinco niveles con dificultad creciente, pensado para partidas cortas.", "Five levels of rising difficulty, built for short sessions.", "p")}
  {yt("ULPoZf-G2Yo", "Tower Hero — gameplay", "Tower Hero — gameplay", "Ver gameplay", "Watch gameplay")}
</section>

<section id="jugar" data-reveal>
  <h2>{L("Juégalo aquí", "Play it here")}</h2>
  {L("Es la misma ROM que presentamos al concurso, corriendo en un emulador de Game Boy dentro de la página. No se descarga nada hasta que pulses encender.", "It's the same ROM we entered in the jam, running in a Game Boy emulator right in the page. Nothing downloads until you press power.", "p")}
  <div class="gb" id="gb" data-rom="assets/games/towerhero.gb" data-cta-hide>
    <div class="gb-body">
      <div class="gb-bezel">
        <span class="gb-led" aria-hidden="true"></span>
        <div class="gb-lcd">
          <canvas id="gb-canvas" width="160" height="144" tabindex="-1" aria-label="Pantalla de la Game Boy" data-es-aria-label="Pantalla de la Game Boy" data-en-aria-label="Game Boy screen"></canvas>
          <button class="gb-power" type="button" id="gb-power">{icon("play")}{L("Encender", "Power on")}</button>
          <p class="gb-msg" id="gb-msg" role="status" hidden></p>
        </div>
        <p class="gb-brand">PocketBoy <i>TOWER HERO</i></p>
      </div>
      <div class="gb-controls" aria-label="Controles" data-es-aria-label="Controles" data-en-aria-label="Controls">
        <div class="gb-dpad">
          <button type="button" data-btn="up" aria-label="Arriba" data-es-aria-label="Arriba" data-en-aria-label="Up"></button>
          <button type="button" data-btn="left" aria-label="Izquierda" data-es-aria-label="Izquierda" data-en-aria-label="Left"></button>
          <span aria-hidden="true"></span>
          <button type="button" data-btn="right" aria-label="Derecha" data-es-aria-label="Derecha" data-en-aria-label="Right"></button>
          <button type="button" data-btn="down" aria-label="Abajo" data-es-aria-label="Abajo" data-en-aria-label="Down"></button>
        </div>
        <div class="gb-ab">
          <button type="button" data-btn="b">B</button>
          <button type="button" data-btn="a">A</button>
        </div>
        <div class="gb-ss">
          <button type="button" data-btn="select">SELECT</button>
          <button type="button" data-btn="start">START</button>
        </div>
      </div>
    </div>
    <div class="gb-side">
      <p class="sub-h">{L("Controles con teclado", "Keyboard controls")}</p>
      <dl class="gb-keys">
        <div><dt><kbd>←</kbd><kbd>↑</kbd><kbd>→</kbd><kbd>↓</kbd></dt><dd>{L("Cruceta", "D-pad")}</dd></div>
        <div><dt><kbd>X</kbd></dt><dd>A</dd></div>
        <div><dt><kbd>Z</kbd></dt><dd>B</dd></div>
        <div><dt><kbd>Enter</kbd></dt><dd>Start</dd></div>
        <div><dt><kbd>Shift</kbd></dt><dd>Select</dd></div>
      </dl>
      <p class="muted" style="font-size:.92rem">{L("En móvil, usa los botones de la consola. También funciona con mando.", "On mobile, use the console's buttons. Gamepads work too.")}</p>
      <div class="gb-tools">
        <button class="btn btn--sm" type="button" id="gb-pause" disabled>{L("Pausa", "Pause")}</button>
        <button class="btn btn--sm" type="button" id="gb-reset" disabled>{L("Reiniciar", "Reset")}</button>
        <button class="btn btn--sm" type="button" id="gb-full" disabled>{L("Pantalla completa", "Fullscreen")}</button>
        <button class="btn btn--sm" type="button" id="gb-sound" aria-pressed="true" disabled>{L("Sonido: sí", "Sound: on")}</button>
      </div>
    </div>
  </div>
</section>

<section id="restricciones" data-reveal>
  <h2>{L("Programar para una Game Boy", "Programming for a Game Boy")}</h2>
  {L("No hay motor ni lenguaje de alto nivel: todo está escrito en ensamblador Z80 (el dialecto de la CPU de la Game Boy). La consola tiene una pantalla de 160×144 píxeles, cuatro tonos y unos pocos KB de RAM de trabajo, así que cada sprite, cada byte de memoria y cada ciclo cuentan.", "No engine, no high-level language: everything is written in Z80-style assembly for the Game Boy's CPU. The console has a 160×144 screen, four shades and a few KB of working RAM, so every sprite, byte and cycle counts.", "p")}
  {L("Lo hicimos entre tres personas del equipo PocketBoy: Javier Sainz-Pardo Tenza, Ángela Cabrera Ruiz y yo. El resultado es un <code>.gb</code> que corre en hardware real y en emulador.", "Three of us built it as PocketBoy: Javier Sainz-Pardo Tenza, Ángela Cabrera Ruiz and me. The result is a <code>.gb</code> ROM that runs on real hardware and emulators.", "p")}
  <h3>{L("Mi papel", "My role")}</h3>
  {L("Hice de project manager del equipo y de programador en las dos capas del juego: el <strong>gameplay</strong> (enemigos, oleadas, energía de la torre, niveles) y el <strong>funcionamiento interno</strong> que lo sostiene en la Game Boy.", "I was the team's project manager and a programmer on both layers of the game: the <strong>gameplay</strong> (enemies, waves, tower energy, levels) and the <strong>internal systems</strong> that make it run on the Game Boy.", "p")}
  <div class="gallery gallery--2 pixel">{gal}</div>
</section>

<section id="concurso" data-reveal>
  <h2>GBRetroDev'25</h2>
  {L("Tower Hero fue entrada oficial de <strong>GBRetroDev'25: Heroes of ASM 2</strong>, el concurso de desarrollo para Game Boy en ensamblador. Presentarlo implicaba cumplir las bases, cerrar una versión estable y publicarla.", "Tower Hero was an official entry to <strong>GBRetroDev'25: Heroes of ASM 2</strong>, the Game Boy assembly game jam. Entering meant meeting the rules, locking a stable build and publishing it.", "p")}
  <p><a class="btn btn--ink" href="{ITCH}" target="_blank" rel="noopener">{icon("itch")}{L("Jugar en itch.io", "Play on itch.io")}{icon("ext", "arrow")}</a></p>
</section>
"""
    cover = f"""<div class="case-cover case-cover--contain skel" style="background:#95a297"><img src="assets/img/work/towerhero-cover.webp" alt="Portada de Tower Hero: un héroe en lo alto de una torre de piedra rodeado de esqueletos, murciélagos y una serpiente, en pixel art" data-es-alt="Portada de Tower Hero: un héroe en lo alto de una torre de piedra rodeado de esqueletos, murciélagos y una serpiente, en pixel art" data-en-alt="Tower Hero cover art: a hero on top of a stone tower surrounded by skeletons, bats and a snake, in pixel art" width="900" height="900" fetchpriority="high" decoding="async" style="image-rendering:pixelated"></div>"""
    case_page(
        file="tower-hero.html",
        title="Tower Hero",
        title_en="Tower Hero",
        h1="Tower Hero",
        lede=L("Un tower defense para Game Boy escrito en ensamblador Z80 por un equipo de tres. Entrada oficial de GBRetroDev'25: Heroes of ASM 2.", "A Game Boy tower defense written in Z80 assembly by a team of three. Official entry to GBRetroDev'25: Heroes of ASM 2."),
        eyebrow=L("Caso de estudio · Game Boy", "Case study · Game Boy"),
        facts=[("Año", "Year", "2025"), ("Rol", "Role", L("PM · programación", "PM · programming")), ("Equipo", "Team", "PocketBoy (3) · Game Boy"), ("Stack", "Stack", L("Ensamblador Z80", "Z80 assembly"))],
        cover=cover,
        toc=[("juego", "El juego", "The game"), ("jugar", "Juégalo aquí", "Play it here"), ("restricciones", "Programar para Game Boy", "Game Boy constraints"), ("concurso", "GBRetroDev'25", "GBRetroDev'25")],
        body=body,
        prev=("castle-of-shadows.html", "Castle of Shadows"),
        nxt=("tfg-superresolucion.html", L("TFG: superresolución", "Thesis: super-resolution")),
        desc_es="Tower Hero: tower defense para Game Boy en ensamblador Z80, entrada oficial de GBRetroDev'25. Caso de estudio de Octavio Gregorio con capturas y gameplay.",
        desc_en="Tower Hero: a Game Boy tower defense in Z80 assembly, official GBRetroDev'25 entry. Case study by Octavio Gregorio with screenshots and gameplay.",
        extra_ld={"@type": "VideoGame", "gamePlatform": "Game Boy", "genre": "Tower defense", "url": BASE + "tower-hero.html", "sameAs": ITCH, "image": BASE + "assets/img/work/towerhero-cover.webp"},
        lightbox_on=True,
        scripts=['<script src="assets/js/gb-player.js?v=' + V + '" defer></script>'],
    )


# =====================================================================
# 3D projects (old URLs kept)
# =====================================================================
ARCH = ("Archivo", "Archive", "elements.html")


def interiorismo():
    day = [("taj-dia", "Vista general de día: estanques, braseros encendidos y el templete al fondo"),
           ("taj-dia1", "Pirámide escalonada en el centro del estanque, con luz cenital"),
           ("taj-dia2", "Vista aérea de los estanques y las plataformas de mármol"),
           ("taj-dia4", "Zona de descanso con alfombra roja, cojines y mesa baja con velas"),
           ("taj-dia5", "Templete de madera tallada con celosía y luz cálida interior"),
           ("taj-dia6", "Pasillo de entrada enmarcado por paneles de celosía"),
           ("taj-dia7", "Perspectiva del pasillo central entre dos estanques"),
           ("taj-dia8", "Estanques y pirámides desde un lateral"),
           ("taj-dia9", "Estanque en primer plano con el templete al fondo"),
           ("taj-dia10", "Detalle del estanque con braseros y pirámide oscura")]
    night = [("taj-noche1", "La sala de noche, iluminada solo por braseros y velas"),
             ("taj-noche2", "Zona de descanso de noche con velas sobre la mesa baja"),
             ("taj-noche2_luz", "La misma zona con una luz adicional sobre la alfombra"),
             ("taj-noche3", "Templete de noche con el interior iluminado en rojo"),
             ("taj-noche4", "Pasillo de entrada de noche"),
             ("taj-noche5", "Estanques de noche con braseros encendidos"),
             ("taj-noche6", "Vista frontal del templete desde el estanque, de noche"),
             ("taj-noche7", "Círculo de luz sobre la zona de descanso vista desde arriba")]
    g_day = "".join(gallery_item(n, a) for n, a in day)
    g_night = "".join(gallery_item(n, a) for n, a in night)
    body = f"""
<section id="idea" data-reveal>
  <h2>{L("La idea", "The idea")}</h2>
  {L("Un espacio inventado que podría estar escondido dentro del Taj Mahal: estanques, braseros, celosías talladas y una zona de descanso. Lo hice en Blender para Modelado y Animación por Computador, trabajando modelado, materiales e iluminación.", "An invented space that could be hidden inside the Taj Mahal: pools, braziers, carved lattices and a lounge area. I made it in Blender for the Computer Modelling & Animation course, covering modelling, materials and lighting.", "p")}
  <div class="gallery">{gallery_item("taj-zona", "Vista de la sala con estanques, pirámides escalonadas y braseros", full_cls="full")}</div>
</section>
<section id="dia" data-reveal>
  <h2>{L("De día", "Daytime")}</h2>
  {L("Luz natural entrando por el techo y rebotando en el mármol y el agua.", "Natural light coming through the ceiling and bouncing off marble and water.", "p")}
  <div class="gallery">{g_day}</div>
</section>
<section id="noche" data-reveal>
  <h2>{L("De noche", "Night")}</h2>
  {L("La misma escena sin luz exterior: solo braseros, velas y el interior del templete. Sirvió para practicar cómo cambia una escena entera con la iluminación.", "The same scene without daylight: just braziers, candles and the temple's interior. Good practice in how lighting alone changes a whole scene.", "p")}
  <div class="gallery">{g_night}</div>
</section>
"""
    cover = f"""<div class="case-cover skel">{img("assets/img/work/taj-dia-pano-1600.webp", "Panorámica de día del interior: estanques, braseros y el templete de madera al fondo", 1600, 667, eager=True, srcset=work("taj-dia-pano"), sizes="(max-width: 1200px) 100vw, 1120px")}</div>"""
    case_page(
        file="interiorismo.html", title="Un interior dentro del Taj Mahal", title_en="An interior inside the Taj Mahal",
        h1=L("Un interior dentro del Taj Mahal", "An interior inside the Taj Mahal"),
        lede=L("Modelado e iluminación de un escenario ficticio, de día y de noche.", "Modelling and lighting a fictional set, by day and by night."),
        eyebrow=L("Proyecto 3D · Blender", "3D project · Blender"),
        facts=[("Año", "Year", "2023"), ("Tipo", "Type", L("Individual · asignatura", "Solo · coursework")), ("Trabajo", "Work", L("Modelado, materiales, luz", "Modelling, materials, lighting")), ("Stack", "Stack", "Blender")],
        cover=cover, toc=[("idea", "La idea", "The idea"), ("dia", "De día", "Daytime"), ("noche", "De noche", "Night")], body=body,
        prev=("scripting.html", L("Lluvia procedural", "Procedural rain")), nxt=("animation.html", "O.V.O."),
        desc_es="Proyecto 3D en Blender de Octavio Gregorio: modelado e iluminación de un interior ficticio dentro del Taj Mahal, con versiones de día y de noche.",
        desc_en="Blender 3D project by Octavio Gregorio: modelling and lighting a fictional interior inside the Taj Mahal, with day and night versions.",
        lightbox_on=True, crumb_parent=ARCH,
    )


def animation():
    renders = [("ovo-selfie", "O.V.O. sujetando la cámara para hacerse una foto, con la Tierra al fondo"),
               ("ovo-epica", "Plano contrapicado de O.V.O. sobre la superficie lunar"),
               ("ovo-frente", "O.V.O. de frente, con sus ojos verdes brillantes"),
               ("ovo-hola", "O.V.O. levantando una pata para saludar"),
               ("ovo-obsrevando", "O.V.O. observando algo fuera de cuadro"),
               ("ovo-pensando", "O.V.O. inclinado, como pensando"),
               ("ovo-saludos", "O.V.O. de pie sobre dos patas, saludando a lo lejos")]
    g = "".join(gallery_item(n, a) for n, a in renders)
    body = f"""
<section id="video" data-reveal>
  <h2>{L("El vídeo", "The video")}</h2>
  {L("O.V.O. es un robot de cuatro patas que modelé, rigueé y animé en Blender. La historia: está en misión cerca de la Tierra, le mandan una cámara para comprobar que todo va bien… y decide usarla para hacerse fotos.", "O.V.O. is a four-legged robot I modelled, rigged and animated in Blender. The story: it's on a mission near Earth, gets sent a camera to check everything's fine… and decides to take selfies with it.", "p")}
  {yt("xsF1OzIbQyA", "O.V.O. — animación en Blender", "O.V.O. — Blender animation")}
</section>
<section id="informe" data-reveal>
  <h2>{L("Informe de misión", "Mission report")}</h2>
  <blockquote>{L("Robot: O.V.O. · Ubicación: espacio exterior, cerca de la Tierra · Estado: buscando otras formas de vida inteligente. Al final del vídeo gira los ojos de una forma extraña. Puede que viera algo detrás de la cámara. Solicitamos una nave de búsqueda a Met-247828.", "Robot: O.V.O. · Location: outer space, near Earth · Status: searching for other intelligent life. At the end of the video it rolls its eyes oddly. It may have seen something behind the camera. Requesting a search ship to Met-247828.", "p")}</blockquote>
</section>
<section id="renders" data-reveal>
  <h2>Renders</h2>
  <div class="gallery">{g}</div>
</section>
"""
    cover = f"""<div class="case-cover skel">{img("assets/img/work/ovo-selfie-1600.webp", "O.V.O., un robot negro con luces verdes, sujetando una cámara con la Tierra de fondo", 1600, 900, eager=True, srcset=work("ovo-selfie"), sizes="(max-width: 1200px) 100vw, 1120px")}</div>"""
    case_page(
        file="animation.html", title="O.V.O., un robot en la Luna", title_en="O.V.O., a robot on the Moon",
        h1=L("O.V.O., un robot en la Luna", "O.V.O., a robot on the Moon"),
        lede=L("Modelado, rigging y animación de un robot cuadrúpedo con un poco de historia detrás.", "Modelling, rigging and animating a four-legged robot, with a bit of a story."),
        eyebrow=L("Proyecto 3D · Animación", "3D project · Animation"),
        facts=[("Año", "Year", "2023"), ("Tipo", "Type", L("Individual · asignatura", "Solo · coursework")), ("Trabajo", "Work", L("Modelado, rigging, animación", "Modelling, rigging, animation")), ("Stack", "Stack", "Blender")],
        cover=cover, toc=[("video", "El vídeo", "The video"), ("informe", "Informe de misión", "Mission report"), ("renders", "Renders", "Renders")], body=body,
        prev=("interiorismo.html", L("Taj Mahal", "Taj Mahal")), nxt=("scripting.html", L("Lluvia procedural", "Procedural rain")),
        desc_es="O.V.O.: robot cuadrúpedo modelado, rigueado y animado en Blender por Octavio Gregorio. Vídeo de la animación y renders.",
        desc_en="O.V.O.: a four-legged robot modelled, rigged and animated in Blender by Octavio Gregorio. Animation video and renders.",
        lightbox_on=True, crumb_parent=ARCH,
    )


def scripting():
    def clip(n, es, en):
        return f"""<figure><div class="clip"><video autoplay loop muted playsinline preload="none" poster="assets/img/work/lluvia-{n}.webp" width="1280" height="720" aria-label="{html.escape(es)}" data-es-aria-label="{html.escape(es)}" data-en-aria-label="{html.escape(en)}"><source src="assets/media/lluvia-{n}.mp4" type="video/mp4"></video></div><figcaption>{L(es, en)}</figcaption></figure>"""

    body = f"""
<section id="script" data-reveal>
  <h2>{L("Qué hace", "What it does")}</h2>
  {L("Un script en Python para Blender que monta una escena de lluvia y deja al usuario ajustarla: cantidad de gotas, movimiento y luz. La idea era no tener que colocar nada a mano.", "A Python script for Blender that builds a rain scene and lets the user tweak it: drop count, motion and lighting. The point was never placing anything by hand.", "p")}
  {clip("0002", "El script generando la lluvia en la escena", "The script generating rain in the scene")}
</section>
<section id="control" data-reveal>
  <h2>{L("Movimiento y luz", "Motion and light")}</h2>
  {clip("0003", "Cambios de movimiento de la lluvia", "Changing how the rain moves")}
  {clip("0004", "Variaciones de iluminación sobre la misma escena", "Lighting variations on the same scene")}
</section>
<section id="descargas" data-reveal>
  <h2>{L("Descargas", "Downloads")}</h2>
  {L("El código, la escena y la memoria del proyecto:", "The code, the scene and the project report:", "p")}
  <p style="display:flex;flex-wrap:wrap;gap:10px">
    <a class="btn btn--sm" href="proyectos/script_blend/Simulador_Lluvia.py" download>{icon("download")}Simulador_Lluvia.py</a>
    <a class="btn btn--sm" href="proyectos/script_blend/Escena.blend" download>{icon("download")}Escena.blend</a>
    <a class="btn btn--sm" href="proyectos/script_blend/Memoria%20MAC.pdf" target="_blank" rel="noopener">{icon("download")}{L("Memoria (PDF)", "Report (PDF)")}</a>
  </p>
</section>
"""
    cover = f"""<div class="case-cover skel">{img("assets/img/work/lluvia-0002.webp", "Fotograma de la escena de lluvia generada por el script en Blender", 1280, 720, eager=True)}</div>"""
    case_page(
        file="scripting.html", title="Lluvia procedural en Blender", title_en="Procedural rain in Blender",
        h1=L("Lluvia procedural en Blender", "Procedural rain in Blender"),
        lede=L("Un script en Python que genera una escena de lluvia editable.", "A Python script that generates an editable rain scene."),
        eyebrow=L("Proyecto 3D · Scripting", "3D project · Scripting"),
        facts=[("Año", "Year", "2023"), ("Tipo", "Type", L("Individual · asignatura", "Solo · coursework")), ("Trabajo", "Work", L("Scripting, escena", "Scripting, scene")), ("Stack", "Stack", "Python · Blender")],
        cover=cover, toc=[("script", "Qué hace", "What it does"), ("control", "Movimiento y luz", "Motion and light"), ("descargas", "Descargas", "Downloads")], body=body,
        prev=("animation.html", "O.V.O."), nxt=("interiorismo.html", L("Taj Mahal", "Taj Mahal")),
        desc_es="Script en Python para Blender de Octavio Gregorio que genera una escena de lluvia editable: vídeos de demostración, código y escena descargables.",
        desc_en="Python script for Blender by Octavio Gregorio that generates an editable rain scene: demo videos, downloadable code and scene.",
        crumb_parent=ARCH,
    )


# =====================================================================
# Archive
# =====================================================================
def archive():
    files = [
        ("doc", "PDF", "CV — Octavio Gregorio", "Currículum actualizado (2026).", "Updated CV (2026).", [("cv_octavio_gregorio.pdf", "Descargar", "Download", True)]),
        ("doc", "PDF", "TFG — Sistema híbrido GPU", "Memoria completa en el repositorio de la UA.", "Full thesis on the University of Alicante repository.", [("https://hdl.handle.net/10045/170538", "Abrir", "Open", False)]),
        ("page", "WEB", "Tower Hero", "Caso de estudio con capturas y gameplay.", "Case study with screenshots and gameplay.", [("tower-hero.html", "Ver", "View", False)]),
        ("page", "WEB", "Castle of Shadows", "Caso de estudio del juego con motor propio.", "Case study of the in-house engine game.", [("castle-of-shadows.html", "Ver", "View", False)]),
        ("page", "WEB", "Taj Mahal — interiorismo", "Renders de día y de noche.", "Day and night renders.", [("interiorismo.html", "Ver", "View", False)]),
        ("page", "WEB", "O.V.O. — animación", "Vídeo y renders del robot.", "Robot video and renders.", [("animation.html", "Ver", "View", False)]),
        ("page", "WEB", "Lluvia procedural", "Vídeos del script en acción.", "Videos of the script in action.", [("scripting.html", "Ver", "View", False)]),
        ("code", "PY", "Simulador_Lluvia.py", "Script de Python que genera la lluvia en Blender.", "Python script that generates the rain in Blender.", [("proyectos/script_blend/Simulador_Lluvia.py", "Descargar", "Download", True)]),
        ("code", "BLEND", "Escena.blend", "Escena de Blender lista para abrir.", "Blender scene ready to open.", [("proyectos/script_blend/Escena.blend", "Descargar", "Download", True)]),
        ("doc", "PDF", "Memoria MAC", "Documento técnico del proyecto de scripting.", "Technical report for the scripting project.", [("proyectos/script_blend/Memoria%20MAC.pdf", "Abrir", "Open", False)]),
        ("media", "MP4", "Demo lluvia · generación", "Clip del script generando la escena.", "Clip of the script building the scene.", [("assets/media/lluvia-0002.mp4", "Ver", "Watch", False)]),
        ("media", "MP4", "Demo lluvia · movimiento", "Ajustes de movimiento.", "Motion tweaks.", [("assets/media/lluvia-0003.mp4", "Ver", "Watch", False)]),
        ("media", "MP4", "Demo lluvia · iluminación", "Variaciones de luz.", "Lighting variations.", [("assets/media/lluvia-0004.mp4", "Ver", "Watch", False)]),
        ("code", "RBXL", "Robot.rbxl", "Archivo del robot para Roblox Studio.", "Robot file for Roblox Studio.", [("proyectos/anim_blend/Robot.rbxl", "Descargar", "Download", True)]),
        ("doc", "TXT", "Video.txt", "Notas del bloque de animación.", "Notes for the animation block.", [("proyectos/anim_blend/Video.txt", "Abrir", "Open", False)]),
        ("code", "ZIP", "Sunegami — WEB.zip", "Proyecto web de Sunegami, comprimido.", "Sunegami web project, zipped.", [("proyectos/WEB.zip", "Descargar", "Download", True)]),
        ("media", "YT", "2Dymiros — gameplay", "Juego de cartas en C++.", "Card game in C++.", [("https://youtu.be/JT4wM71QWTo", "Ver", "Watch", False)]),
        ("media", "YT", "Cortometraje", "Postproducción digital en DaVinci Resolve.", "Post-production in DaVinci Resolve.", [("https://youtu.be/HxZO4kSogeQ", "Ver", "Watch", False)]),
    ]
    rows = []
    for cat, typ, name, des, den, acts in files:
        a_html = ""
        for href, les, len_, dl in acts:
            ext = href.startswith("http")
            attrs = ' download' if dl else (' target="_blank" rel="noopener"' if ext else "")
            a_html += f'<a class="btn btn--sm" href="{href}"{attrs}>{L(les, len_)}{icon("download" if dl else ("ext" if ext else "arrow"), "arrow")}</a>'
        search = f"{name} {des} {den} {typ}".lower()
        rows.append(f'<li data-cat="{cat}" data-search="{html.escape(search)}"><div class="file"><span class="type">{typ}</span><div><b>{name}</b>{L(des, den)}</div><div class="acts">{a_html}</div></div></li>')
    chips = [("all", "Todo", "All"), ("page", "Proyectos", "Projects"), ("doc", "Documentos", "Documents"), ("code", "Código", "Code"), ("media", "Vídeo", "Video")]
    chip_html = "".join(f'<button class="chip" type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{L(e, n)}</button>' for k, e, n in chips)
    out = head(
        path="elements.html",
        title_es="Archivo de proyectos y descargas · Octavio Gregorio",
        title_en="Project archive & downloads · Octavio Gregorio",
        desc_es="Archivo de Octavio Gregorio: CV, memoria del TFG, escenas de Blender, scripts de Python, vídeos y proyectos antiguos, todo descargable.",
        desc_en="Octavio Gregorio's archive: CV, thesis, Blender scenes, Python scripts, videos and older projects, all downloadable.",
        ld_json=ld(PERSON, crumbs_ld([("Inicio", "index.html"), ("Archivo", "elements.html")])),
    )
    out += header("archive")
    out += f"""<main id="main" tabindex="-1">
{breadcrumbs([("Inicio", "Home", "index.html"), ("Archivo", "Archive", "elements.html")])}
<section class="simple wrap" style="padding-top:32px">
  <p class="eyebrow" data-enter style="--i:0">{L("Archivo", "Archive")}</p>
  <h1 class="display" data-enter style="--i:1">{L("Todo lo demás", "Everything else")}</h1>
  <p class="lede" data-enter style="--i:2">{L("Ficheros, entregas y proyectos antiguos en un solo sitio. Busca o filtra por tipo.", "Files, coursework and older projects in one place. Search or filter by type.")}</p>
  <div data-enter style="--i:3;margin-top:40px">
    <div class="toolbar" role="search">
      <label class="sr-only" for="q">{L("Buscar en el archivo", "Search the archive")}</label>
      <input id="q" type="search" placeholder="Buscar por nombre o tipo…" data-es-placeholder="Buscar por nombre o tipo…" data-en-placeholder="Search by name or type…" autocomplete="off">
      <div class="chips" aria-label="Filtrar" data-es-aria-label="Filtrar" data-en-aria-label="Filter">{chip_html}</div>
    </div>
    <p class="sr-only" id="count" aria-live="polite"></p>
    <ul class="files" id="files">
{chr(10).join(rows)}
    </ul>
    <p class="empty-state" id="empty" hidden>{L("Nada con ese nombre. Prueba otra palabra.", "Nothing by that name. Try another word.")}</p>
  </div>
</section>
</main>
<script>
(() => {{
  const q = document.getElementById('q'), items = [...document.querySelectorAll('#files li')], chips = [...document.querySelectorAll('.chip')], empty = document.getElementById('empty'), count = document.getElementById('count');
  let cat = 'all';
  const run = () => {{
    const term = q.value.trim().toLowerCase();
    let n = 0;
    items.forEach(li => {{ const ok = (cat === 'all' || li.dataset.cat === cat) && (!term || li.dataset.search.includes(term)); li.hidden = !ok; if (ok) n++; }});
    empty.hidden = n > 0;
    const lg = document.documentElement.lang; count.textContent = lg === 'en' ? n + ' files' : lg === 'zh-Hant' ? n + ' 個檔案' : n + ' archivos';
  }};
  q.addEventListener('input', run);
  chips.forEach(c => c.addEventListener('click', () => {{ cat = c.dataset.filter; chips.forEach(x => x.setAttribute('aria-pressed', String(x === c))); run(); }}));
}})();
</script>
"""
    out += footer()
    write("elements.html", out)


# =====================================================================
# Thanks, privacy, 404
# =====================================================================
def privacidad():
    es = f"""<div lang="es">
  <p><strong>Última actualización:</strong> 23 de septiembre de 2026.</p>
  <h2>Quién es el responsable</h2>
  <p>Octavio Gregorio Guerrero, Elda (Alicante, España). Contacto: <a class="link" href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  <h2>Qué datos recojo</h2>
  <p>Ninguno. Esta web no tiene formulario, ni analítica, ni publicidad, ni cookies. Si me escribes por email o WhatsApp, uso tu mensaje solo para responderte y lo borro si me lo pides.</p>
  <h2>Servicios de terceros</h2>
  <ul>
    <li><strong>GitHub Pages</strong> (GitHub Inc.) aloja la web y puede registrar tu IP en sus logs técnicos.</li>
    <li><strong>Google Fonts</strong> sirve las tipografías.</li>
    <li><strong>YouTube</strong> (modo sin cookies) solo se carga si pulsas en un vídeo.</li>
  </ul>
  <h2>Almacenamiento local</h2>
  <p>El navegador guarda <code>theme</code> y <code>lang</code> en almacenamiento local para recordar el modo claro/oscuro y el idioma. Es técnico, no identifica a nadie y no sale de tu dispositivo.</p>
  <h2>Tus derechos</h2>
  <p>Puedes pedir acceso, rectificación o supresión de cualquier dato que me hayas enviado escribiendo a <a class="link" href="mailto:{EMAIL}">{EMAIL}</a>. También puedes reclamar ante la <a class="link" href="https://www.aepd.es" target="_blank" rel="noopener">Agencia Española de Protección de Datos</a>.</p>
</div>"""
    en = f"""<div lang="en">
  <p><strong>Last updated:</strong> 23 September 2026.</p>
  <h2>Who is responsible</h2>
  <p>Octavio Gregorio Guerrero, Elda (Alicante, Spain). Contact: <a class="link" href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  <h2>What I collect</h2>
  <p>Nothing. This site has no form, no analytics, no ads and no cookies. If you email or WhatsApp me, I use your message only to reply and delete it if you ask.</p>
  <h2>Third-party services</h2>
  <ul>
    <li><strong>GitHub Pages</strong> (GitHub Inc.) hosts the site and may log your IP technically.</li>
    <li><strong>Google Fonts</strong> serves the typefaces.</li>
    <li><strong>YouTube</strong> (privacy-enhanced mode) loads only if you click a video.</li>
  </ul>
  <h2>Local storage</h2>
  <p>Your browser stores <code>theme</code> and <code>lang</code> in local storage to remember light/dark mode and language. It's technical, identifies no one and never leaves your device.</p>
  <h2>Your rights</h2>
  <p>You can ask for access, correction or deletion of anything you've sent me by emailing <a class="link" href="mailto:{EMAIL}">{EMAIL}</a>. You can also complain to the Spanish data protection authority, the <a class="link" href="https://www.aepd.es" target="_blank" rel="noopener">AEPD</a>.</p>
</div>"""
    zhb = f"""<div lang="zh-Hant">
  <p><strong>最後更新：</strong>2026 年 9 月 23 日。</p>
  <h2>負責人</h2>
  <p>Octavio Gregorio Guerrero，西班牙阿利坎特省埃爾達（Elda）。聯絡方式：<a class="link" href="mailto:{EMAIL}">{EMAIL}</a>。</p>
  <h2>我收集哪些資料</h2>
  <p>完全不收集。本網站沒有表單、沒有分析工具、沒有廣告，也沒有 Cookie。如果你透過電子郵件或 WhatsApp 聯絡我，我只會用你的訊息來回覆你；只要你提出要求，我就會刪除它。</p>
  <h2>第三方服務</h2>
  <ul>
    <li><strong>GitHub Pages</strong>（GitHub Inc.）託管本網站，可能在技術日誌中記錄你的 IP。</li>
    <li><strong>Google Fonts</strong> 提供網站字型。</li>
    <li><strong>YouTube</strong>（隱私強化模式）只會在你點擊影片時載入。</li>
  </ul>
  <h2>本機儲存</h2>
  <p>瀏覽器會在本機儲存 <code>theme</code> 與 <code>lang</code>，用來記住淺色／深色模式與語言。這是技術性資料，無法識別任何人，也不會離開你的裝置。</p>
  <h2>你的權利</h2>
  <p>你可以寫信到 <a class="link" href="mailto:{EMAIL}">{EMAIL}</a>，要求查閱、更正或刪除你寄給我的任何資料。你也可以向西班牙資料保護局 <a class="link" href="https://www.aepd.es" target="_blank" rel="noopener">AEPD</a> 提出申訴。</p>
</div>"""
    out = head(
        path="privacidad.html",
        title_es="Política de privacidad · Octavio Gregorio",
        title_en="Privacy policy · Octavio Gregorio",
        desc_es="Política de privacidad del portfolio de Octavio Gregorio: sin formulario, sin analítica y sin cookies.",
        desc_en="Privacy policy for Octavio Gregorio's portfolio: no form, no analytics, no cookies.",
        ld_json=ld(crumbs_ld([("Inicio", "index.html"), ("Privacidad", "privacidad.html")])),
    )
    out += header()
    out += f"""<main id="main" tabindex="-1">
{breadcrumbs([("Inicio", "Home", "index.html"), ("Privacidad", "Privacy", "privacidad.html")])}
<section class="simple wrap" style="padding-top:32px">
  <p class="eyebrow">{L("Legal", "Legal")}</p>
  <h1 class="display">{L("Privacidad", "Privacy")}</h1>
  <p class="lede">{L("Versión corta: esta web no recoge datos.", "Short version: this site collects no data.")}</p>
  <div class="prose legal" style="margin-top:40px">
{es}
{en}
{zhb}
  </div>
</section>
</main>
"""
    out += footer(mobile_cta=False)
    write("privacidad.html", out)


def notfound():
    out = head(
        path="404.html",
        title_es="Página no encontrada (404) · Octavio Gregorio",
        title_en="Page not found (404) · Octavio Gregorio",
        desc_es="Esta página no existe. Vuelve al portfolio de Octavio Gregorio.",
        desc_en="This page doesn't exist. Head back to Octavio Gregorio's portfolio.",
        robots="noindex,follow",
        base="/octaviogg.github.io/",
    )
    out += header()
    out += f"""<main id="main" tabindex="-1">
<section class="simple wrap">
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:48px;align-items:center">
    <div>
      <p class="eyebrow" data-enter style="--i:0">Error 404</p>
      <h1 class="display" data-enter style="--i:1">{L("Esta sala del castillo no existe.", "This room of the castle doesn't exist.")}</h1>
      <p class="lede" data-enter style="--i:2">{L("Puede que el enlace esté roto o que la página se haya movido con el rediseño. Estos caminos sí llevan a algún sitio:", "The link may be broken or the page moved during the redesign. These paths do lead somewhere:")}</p>
      <div class="actions" data-enter style="--i:3">
        <a class="btn btn--primary" href="index.html">{L("Ir al inicio", "Go home")}{icon("arrow", "arrow")}</a>
        <a class="btn" href="index.html#trabajo">{L("Ver proyectos", "See work")}</a>
        <a class="btn" href="index.html#contacto">{L("Contactar", "Contact")}</a>
      </div>
    </div>
    <div class="gb-screen" data-enter style="--i:2" aria-hidden="true">
      <div><b>GAME OVER</b><p style="margin-top:14px">404 · ROOM NOT FOUND</p><p style="margin-top:22px"><span class="blink">&#9654;&#xFE0E;</span> CONTINUE?</p></div>
    </div>
  </div>
</section>
</main>
"""
    out += footer(mobile_cta=False)
    write("404.html", out)


if __name__ == "__main__":
    index(); tfg(); castle(); tower(); interiorismo(); animation(); scripting(); archive(); privacidad(); notfound()
    if ZH_MISSING:
        miss = os.path.join(os.path.dirname(ZH_PATH), "zh_missing.json")
        json.dump(ZH_MISSING, open(miss, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"[zh] {len(ZH_MISSING)} strings without Traditional Chinese (English used) -> {miss}")
