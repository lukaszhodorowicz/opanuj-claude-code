"""Sekcja „Kto za tym stoi?” na stronie startowej: czterech agentów jako ośmiobitowy Clawd w SVG i zdjęcie Łukasza z okularami z memu."""

import html

# Paleta Clawda ze stylu piksel Claude Code (ogarniam-ai/style/piksel-claude-code, src/config.js)
KOLORY = {
    "c": "#D97757",  # koral
    "j": "#EE9E7B",  # jasny koral
    "d": "#B65B40",  # ciemny koral
    "k": "#12110F",  # tusz
    "b": "#FFFFFF",
}

# Clawd na siatce 40×26 kratek: (x, y, szerokość, wysokość, kolor); proporcje jak w clawd.js (korpus 10×6 jednostek, jednostka = 2 kratki)
CLAWD = {
    "rece": [(4, 11, 4, 2, "c"), (28, 11, 4, 2, "c")],
    "korpus": [
        (8, 6, 20, 12, "c"),
        (8, 6, 20, 1, "j"),  # jasna krawędź góry
        (9, 7, 3, 1, "j"),  # odblask na czole
        (8, 16, 20, 2, "d"),  # ciemny pas przy dole
    ],
    "nogi-a": [(10, 18, 2, 5, "d"), (20, 18, 2, 5, "d")],  # nogi idą parami na zmianę
    "nogi-b": [(14, 18, 2, 5, "d"), (24, 18, 2, 5, "d")],
    "oczy": [(12, 8, 2, 4, "k"), (22, 8, 2, 4, "k")],  # oczy-szparki
}

DODATKI = {
    "pisarz": [  # ołówek w prawej ręce i kartka w lewej
        (31, 12, 2, 2, "k"),
        *[(32 + i, 10 - 2 * i, 2, 2, "#F2C14E") for i in range(4)],
        (36, 2, 2, 2, "#E8A0A0"),
        (0, 9, 5, 8, "b"),
        (1, 11, 3, 1, "k"),
        (1, 13, 3, 1, "k"),
        (1, 15, 2, 1, "k"),
    ],
    "fakty": [  # lupa
        (32, 12, 2, 2, "#5A3B2A"),
        (34, 10, 2, 2, "#5A3B2A"),
        (35, 3, 4, 6, "#BFE3F5"),
        (35, 2, 4, 1, "k"),
        (35, 9, 4, 1, "k"),
        (34, 3, 1, 6, "k"),
        (39, 3, 1, 6, "k"),
        (36, 4, 1, 2, "b"),
    ],
    "cwiczenia": [  # młotek
        (32, 6, 2, 10, "#8B5A3C"),
        (28, 2, 10, 4, "#8A8F98"),
        (28, 5, 10, 1, "#5E636B"),
        (29, 3, 2, 1, "#C9CDD3"),
    ],
    "grafik": [  # beret, pędzel i paleta
        (10, 3, 16, 3, "#2B2B6E"),
        (17, 1, 2, 2, "#2B2B6E"),
        (32, 6, 2, 8, "#C49A6C"),
        (32, 4, 2, 2, "#9AA0A6"),
        (32, 1, 2, 3, "#3FA7F5"),
        (0, 12, 6, 5, "#E9D3A3"),
        (1, 13, 1, 1, "#E5484D"),
        (3, 13, 1, 1, "#3FA7F5"),
        (2, 15, 1, 1, "#46A758"),
        (4, 15, 1, 1, "#F2C14E"),
    ],
}

AGENCI = [
    ("pisarz", "Agent pisarz", "Pisze lekcje, quizy i fiszki."),
    ("fakty", "Agent od faktów", "Sprawdza każde zdanie z dokumentacją Anthropic."),
    (
        "cwiczenia",
        "Agent od ćwiczeń",
        "Buduje ekrany aplikacji, które klikasz w ćwiczeniach.",
    ),
    ("grafik", "Agent grafik", "Rysuje obrazki do lekcji."),
]

# Okulary z memu „deal with it” na siatce 24×5 kratek
OKULARY = [
    (0, 0, 24, 1, "k"),
    (1, 1, 10, 2, "k"),
    (2, 3, 8, 1, "k"),
    (3, 4, 6, 1, "k"),
    (11, 1, 2, 1, "k"),
    (13, 1, 10, 2, "k"),
    (14, 3, 8, 1, "k"),
    (15, 4, 6, 1, "k"),
    (3, 1, 1, 1, "b"),
    (4, 2, 1, 1, "b"),
    (15, 1, 1, 1, "b"),
    (16, 2, 1, 1, "b"),
]

ZDJECIE = "zasoby/lukasz.webp"  # poza „szok” z ~/.claude/assets/reference-photos/wyciete-pozy/poza_szok_studio.png, przycięta do postaci, 560×785 px, tło przezroczyste
# Oczy na zdjęciu (rozpoznawanie twarzy macOS Vision, 28.10.2026): lewe 240×134, prawe 317×133 px.
# Okulary: środek między oczami, szerokość 2,6 rozstawu oczu; położenie w procentach, żeby skalowało się z obrazkiem.
OKULARY_STYL = "left:31.9%;top:14.6%;width:35.8%"


def _prostokaty(kratki: list) -> str:
    return "".join(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{KOLORY.get(k, k)}"/>'
        for x, y, w, h, k in kratki
    )


def svg_kratek(kratki, szerokosc: int, wysokosc: int, klasa: str, opis: str) -> str:
    """Rysunek z kratek jako SVG bez wygładzania krawędzi; słownik {nazwa: kratki} daje grupy <g class="nazwa"> do animacji."""
    if isinstance(kratki, dict):
        prostokaty = "".join(
            f'<g class="{nazwa}">{_prostokaty(k)}</g>' for nazwa, k in kratki.items()
        )
    else:
        prostokaty = _prostokaty(kratki)
    return (
        f'<svg class="{klasa}" viewBox="0 0 {szerokosc} {wysokosc}" shape-rendering="crispEdges" '
        f'role="img" aria-label="{html.escape(opis)}">{prostokaty}</svg>'
    )


def html_kto_za_tym_stoi() -> str:
    """Sekcja na dół strony startowej: czterech agentów i „Co za agent” z okularami, które zjeżdżają, gdy sekcja pojawi się na ekranie."""
    karty = "".join(
        f'<figure class="agent" style="--opoznienie:{-0.3 * i:.1f}s">'
        f"{svg_kratek({**CLAWD, 'rekwizyt': DODATKI[klucz]}, 40, 26, 'agent-rysunek', nazwa)}"
        f"<figcaption><b>{html.escape(nazwa)}</b><span>{html.escape(rola)}</span></figcaption></figure>"
        for i, (klucz, nazwa, rola) in enumerate(AGENCI)
    )
    prawdziwy = (
        '<figure class="agent agent-prawdziwy" tabindex="0" aria-label="Co za agent: Łukasz Hodorowicz">'
        f'<div class="agent-foto"><img src="{ZDJECIE}" alt="Łukasz Hodorowicz" width="560" height="785" loading="lazy">'
        f"{svg_kratek(OKULARY, 24, 5, 'agent-okulary', 'okulary przeciwsłoneczne')}</div>"
        "<figcaption><b>Co za agent</b></figcaption></figure>"
    ).replace(
        'class="agent-okulary"', f'class="agent-okulary" style="{OKULARY_STYL}"', 1
    )
    skrypt = (
        "<script>(function(){var k=document.querySelector('.agent-prawdziwy');if(!k)return;"
        "var zjedz=function(){k.classList.remove('okulary-na');void k.offsetWidth;k.classList.add('okulary-na');};"
        "if('IntersectionObserver' in window){new IntersectionObserver(function(w,o){if(w[0].isIntersecting){zjedz();o.disconnect();}},"
        "{threshold:.6}).observe(k);}else{zjedz();}"
        "k.addEventListener('click',zjedz);})();</script>"
    )
    return (
        '<section class="kto" id="kto-za-tym-stoi"><h2>Kto za tym stoi?</h2>'
        '<p class="kto-wstep">Za tym procederem stoją:</p>'
        f'<div class="kto-siatka">{karty}{prawdziwy}</div></section>{skrypt}'
    )
