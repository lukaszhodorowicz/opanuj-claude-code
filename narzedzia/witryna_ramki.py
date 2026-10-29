"""Kawałki HTML wspólne dla strony startowej i stron lekcji: ramka zapisu na newsletter, nawigacja między lekcjami, odnośnik do Discorda."""

import html
from urllib.parse import urlencode

NAZWA_KURSU = "Opanuj Claude Code w godzinę"  # D-2026-10-24-06
# Teksty strony startowej: podyktowane przez Łukasza 28.10.2026, opis i ramka po filtrze jasnego pisania
PODTYTUL = "Darmowy kurs dla przedsiębiorców, marketerów i freelancerów"
HASLO = "Po polsku, czyli za darmo, konkretnie i z rozmachem"
OPIS_KURSU = (
    "<p>Samoaktualizujący się kurs Claude Code. "
    "Powstał na podstawie oficjalnej dokumentacji Anthropic.</p>"
    '<p class="start-wyroznienie">Naucz się pracy w aplikacji Claude Code w wersji okienkowej.</p>'
    "<p>W kursie znajdziesz jasne instrukcje, quiz, fiszki do nauki i ćwiczenia, "
    "w których klikasz na stronie jak w prawdziwej aplikacji Claude.</p>"
)
ZAPIS_NAGLOWEK = "Zapisz się, żeby otrzymywać informacje o aktualizacjach"  # Łukasz 29.10.2026
ZAPIS_OPIS = (
    "<p>Gdy Anthropic wypuści nowe funkcje lub zmiany w aplikacji, możesz dowiedzieć się o tym "
    "jako pierwszy. Zapisz się poniżej.</p>"
    "<p>Co poniedziałek rano wyślę Ci w newsletterze krótką informację o zmianach w kursie.</p>"
)
DISCORD = "https://discord.gg/GVyW87DEG3"  # serwer SmartLetter, zaproszenie bez wygasania (D-2026-10-28-03)
NEWSLETTER = "https://lukaszhodorowicz.pl/smartletter/"
GITHUB = "https://github.com/lukaszhodorowicz/opanuj-claude-code"  # publiczne repo kursu (D-2026-10-28-06), przycisk bez licznika gwiazdek
# Znak GitHuba (Octicon mark-github), siatka 16×16
GITHUB_ZNAK = "M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"
# Znak Discorda z plansz YouTube Łukasza (wiedza/YouTube/plansze-cta/discord.svg), siatka 24×24
DISCORD_ZNAK = "M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189Z"
ZRODLO_ZAPISU = "przewodnik-claude-code"  # pole zrodlo_zapisu w Mauticu: po nim widać zapisy z kursu

# Zapis idzie przez wtyczkę WordPressa z Turnstile, która przekazuje go do formularza 2 Mautica (D-2026-09-23-01, projekt amazon-ses).
# Bez Turnstile wtyczka odrzuca zgłoszenie, więc strona ładuje widżet z tym samym kluczem publicznym co strona SmartLettera.
ZAPIS_ADRES = "https://lukaszhodorowicz.pl/wp-admin/admin-post.php"
ZAPIS_FORMULARZ = "2"
ZAPIS_NAZWA_FORMULARZA = "ogarniam_a"
TURNSTILE_KLUCZ = "0x4AAAAAAFA1IoIW2fqGjzFE"
TURNSTILE_AKCJA = "smartletter"
_TS_UKRYTY = (
    "position:absolute;width:300px;height:0;overflow:hidden;pointer-events:none"
)


def adres_newslettera(kanal: str, kampania: str) -> str:
    """Strona zapisu SmartLettera z oznaczeniem źródła: jej skrypt przepisuje utm_* do pól zrodlo/kanal/kampania_zapisu."""
    return (
        NEWSLETTER
        + "?"
        + urlencode(
            {"utm_source": ZRODLO_ZAPISU, "utm_medium": kanal, "utm_campaign": kampania}
        )
    )


def _ukryte(nazwa: str, wartosc: str) -> str:
    return f'<input type="hidden" name="{html.escape(nazwa)}" value="{html.escape(wartosc)}">'


def html_zapisu(miejsce: str, naglowek: str = ZAPIS_NAGLOWEK) -> str:
    """Ramka zapisu na newsletter; `miejsce` (np. „start-gora”, „koniec-modulu-1”) trafia do pola kanal_zapisu."""
    ukryte = "".join(
        _ukryte(n, w)
        for n, w in (
            ("action", "sl_zapis"),
            ("mauticform[formId]", ZAPIS_FORMULARZ),
            ("mauticform[formName]", ZAPIS_NAZWA_FORMULARZA),
            ("mauticform[return]", ""),
            ("mauticform[zrodlo_zapisu]", ZRODLO_ZAPISU),
            ("mauticform[kanal_zapisu]", miejsce),
            ("mauticform[kampania_zapisu]", ""),
        )
    )
    pole_id = f"zapis-email-{html.escape(miejsce)}"
    return (
        f'<section class="zapis" id="zapis-{html.escape(miejsce)}">'
        f'<h2 class="zapis-tytul">{html.escape(naglowek)}</h2>'
        f'<div class="zapis-opis">{ZAPIS_OPIS}</div>'
        f'<form class="zapis-formularz signup-form" action="{ZAPIS_ADRES}" method="POST">'
        f"{ukryte}"
        '<input type="text" name="sl_strona" value="" tabindex="-1" autocomplete="off" aria-hidden="true" class="zapis-pulapka">'
        f'<label class="zapis-etykieta" for="{pole_id}">Twój adres e-mail</label>'
        '<div class="zapis-rzad">'
        f'<input type="email" id="{pole_id}" name="mauticform[email]" required autocomplete="email" placeholder="Twój adres e-mail">'
        '<button type="submit" name="mauticform[zapisz]" value="1">Zapisz mnie</button>'
        "</div>"
        f'<div class="cf-turnstile" data-sitekey="{TURNSTILE_KLUCZ}" data-action="{TURNSTILE_AKCJA}" '
        'data-appearance="interaction-only" data-size="flexible" '
        'data-before-interactive-callback="zapisTsPokaz" data-after-interactive-callback="zapisTsSchowaj" '
        f'style="{_TS_UKRYTY}"></div>'
        '<p class="zapis-blad" hidden>Nie udało się zapisać. Odśwież stronę i spróbuj jeszcze raz.</p>'
        "</form></section>"
    )


def skrypt_zapisu() -> str:
    """Widżet Turnstile i czekanie na jego token przed wysyłką (ta sama logika co we wtyczce zapisu na lukaszhodorowicz.pl)."""
    return (
        "<script>window.zapisTsPokaz=function(){document.querySelectorAll('.cf-turnstile').forEach(function(c){c.style.cssText='';});};"
        f"window.zapisTsSchowaj=function(){{document.querySelectorAll('.cf-turnstile').forEach(function(c){{c.style.cssText='{_TS_UKRYTY}';}});}};"
        "(function(){if(/[?&]sl_zapis=blad/.test(location.search)){document.querySelectorAll('.zapis-blad').forEach(function(p){p.hidden=false;});}"
        "document.addEventListener('submit',function(e){var f=e.target;if(!f.querySelector||!f.querySelector('.cf-turnstile'))return;"
        "var t=f.querySelector('input[name=\"cf-turnstile-response\"]');if(t&&t.value)return;"
        "e.preventDefault();if(f.dataset.czeka)return;f.dataset.czeka='1';var n=0;"
        "var i=setInterval(function(){var t=f.querySelector('input[name=\"cf-turnstile-response\"]');n++;"
        "if((t&&t.value)||n>50){clearInterval(i);delete f.dataset.czeka;HTMLFormElement.prototype.submit.call(f);}},200);"
        "},true);})();</script>"
        '<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" defer></script>'
    )


def html_discord() -> str:
    """Zaproszenie na Discorda pod treścią strony, w kolorach Discorda i z jego znakiem."""
    return (
        '<section class="discord">'
        '<h2><svg class="discord-znak" viewBox="0 0 24 24" aria-hidden="true">'
        f'<path fill="currentColor" d="{DISCORD_ZNAK}"/></svg>Pytania i pomoc na Discordzie</h2>'
        "<p>Masz pytanie do lekcji albo chcesz pokazać swój efekt? Napisz na Discordzie.</p>"
        f'<p><a class="przycisk przycisk-discord" href="{DISCORD}">Wejdź na Discorda</a></p>'
        "</section>"
    )


def html_github() -> str:
    """Przycisk do publicznego repozytorium w górnym pasku strony startowej: sam znak i napis, bez licznika gwiazdek i bez zewnętrznych skryptów."""
    return (
        f'<a class="gora-github" href="{GITHUB}" aria-label="Kurs na GitHubie">'
        '<svg viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
        f'<path fill="currentColor" d="{GITHUB_ZNAK}"/></svg>'
        '<span class="gora-github-napis">GitHub</span></a>'
    )


def html_nawigacji(adres_lekcji: str, poprzednia, nastepna, do_startu: str) -> str:
    """Przyciski pod lekcją: oznaczenie przerobionej, poprzednia i następna lekcja, powrót do spisu."""

    def link(lekcja, klasa: str, etykieta: str) -> str:
        if lekcja is None:
            return f'<span class="{klasa} nawigacja-pusta"></span>'
        return (
            f'<a class="{klasa}" href="{do_startu}{lekcja.adres}">'
            f'<span class="nawigacja-etykieta">{etykieta}</span>'
            f'<span class="nawigacja-tytul">{html.escape(lekcja.tytul)}</span></a>'
        )

    return (
        f'<nav class="nawigacja" aria-label="Lekcje" data-lekcja="{html.escape(adres_lekcji)}">'
        '<div class="nawigacja-oznacz"><button type="button" class="przycisk oznacz-przerobiona" data-postep-przycisk>'
        "Oznacz lekcję jako przerobioną</button></div>"
        '<div class="nawigacja-rzad">'
        f"{link(poprzednia, 'nawigacja-poprzednia', 'Poprzednia lekcja')}"
        f"{link(nastepna, 'nawigacja-nastepna', 'Następna lekcja')}"
        "</div>"
        f'<p class="nawigacja-spis"><a href="{do_startu}">← Wszystkie lekcje</a></p>'
        "</nav>"
    )
