"""Testy pogrubiania pojęć ze słowniczka w tekście lekcji: pięć zasad dopasowania (każda osobnym przypadkiem), raz na lekcję, tylko zwykły tekst akapitów i list, podpowiedź dostępna dla czytnika ekranu i złożona lekcja."""

import html
import re

import pytest

from narzedzia import strona
from narzedzia.strona_slowniczek import Haslo, Slownik, pogrubione, wczytaj, PLIK_SLOWNICZKA


def slownik(*hasla: tuple[str, list[str]]) -> Slownik:
    """Słownik z krótkich opisów (pojęcie, odmiany); wyjaśnienie i fakt są próbne."""
    return Slownik(tuple(Haslo(p, tuple(o), f"Wyjaśnienie: {p}.", "f") for p, o in hasla))


def pogrub(tekst: str, *hasla: tuple[str, list[str]]) -> list[str]:
    """Pojęcia pogrubione w podanym HTML, w kolejności występowania."""
    return pogrubione(slownik(*hasla).pogrub(tekst))


# --- zasada 1: bez linii okruszków -------------------------------------------------------------------------------------


def test_okruszki_nie_sa_dopasowaniem():
    wejscie = "<p><em>Przewodnik po Claude Code · Moduł 1: Tryby pracy · Lekcja 1 z 4</em></p>\n<p>W lekcji o Claude Code jest tekst.</p>"
    wynik = slownik(("Claude Code", ["Claude Code"])).pogrub(wejscie)
    assert wynik.startswith("<p><em>Przewodnik po Claude Code · Moduł 1: Tryby pracy · Lekcja 1 z 4</em></p>")
    assert pogrubione(wynik) == ["Claude Code"] and wynik.count("pojecie-slowo") == 1


def test_okruszki_w_gotowej_lekcji_nie_trafiaja_do_pogrubienia(tmp_path):
    (tmp_path / "lekcja.md").write_text("*Przewodnik po Claude Code · Moduł 1: Tryby pracy · Lekcja 1 z 4*\n\n# Tytuł\n\nTu pada Claude Code po raz pierwszy w tekście.\n", encoding="utf-8")
    wynik = strona.zloz_strone(tmp_path)
    assert pogrubione(wynik) == ["Claude Code"]
    tresc = wynik.split('<div class="strona">', 1)[1]
    assert tresc.index("pojecie-slowo") > tresc.index("Tu pada")


# --- zasada 2: tylko zwykły tekst akapitów i list ------------------------------------------------------------------------

HASLO = ("Accept edits", ["Accept edits"])


@pytest.mark.parametrize(
    "wejscie",
    [
        "<h2>Tryb Accept edits</h2>",
        '<figure class="obraz"><img alt="Accept edits" src="x"><figcaption>Accept edits</figcaption></figure>',
        '<p>Zobacz <a href="https://example.pl">Accept edits</a>.</p>',
        "<p>Wpisz <code>Accept edits</code> i gotowe.</p>",
        "<pre><code>Accept edits</code></pre>",
        "<p>Naciśnij <kbd>Accept edits</kbd>.</p>",
        '<figure class="obraz"><img alt="a"><figcaption>b</figcaption><details><summary>Accept edits</summary><p>bez</p></details></figure>',
        "<div>Accept edits bez akapitu</div>",
    ],
    ids=["naglowek", "alt-i-podpis", "tekst-linku", "kod-w-linii", "blok-kodu", "klawisz", "naglowek-analogii", "poza-akapitem"],
)
def test_poza_zwyklym_tekstem_nic_sie_nie_pogrubia(wejscie):
    assert pogrub(wejscie, HASLO) == []


@pytest.mark.parametrize(
    "wejscie",
    ["<p>Tryb Accept edits działa.</p>", "<ul><li>Accept edits w liście</li></ul>", "<ol><li>Krok z <em>Accept edits</em></li></ol>", "<p>To <strong>Accept edits</strong> też.</p>"],
    ids=["akapit", "lista-punktowana", "lista-numerowana-i-kursywa", "pogrubienie-autora"],
)
def test_zwykly_tekst_akapitow_i_list_sie_pogrubia(wejscie):
    assert pogrub(wejscie, HASLO) == ["Accept edits"]


def test_tekst_po_linku_i_kodzie_w_tym_samym_akapicie_nadal_sie_liczy():
    wejscie = '<p><a href="#">Accept edits</a> i <code>Accept edits</code>, a potem Accept edits.</p>'
    wynik = slownik(HASLO).pogrub(wejscie)
    assert pogrubione(wynik) == ["Accept edits"]
    assert "a potem <span" in wynik and '<a href="#">Accept edits</a>' in wynik and "<code>Accept edits</code>" in wynik


def test_rozwijana_analogia_nie_jest_pogrubiana(tmp_path):
    (tmp_path / "obrazy").mkdir()
    # najmniejszy poprawny PNG
    png = bytes.fromhex("89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000d49444154789c6360f8cfc0f01f0005000201a5f645dc0000000049454e44ae426082")
    (tmp_path / "obrazy" / "a.png").write_bytes(png)
    (tmp_path / "lekcja.md").write_text("# T\n\n![Okno z napisem Accept edits](obrazy/a.png) <!-- analogia: To jak przełącznik Accept edits w aucie. -->\n", encoding="utf-8")
    wynik = strona.zloz_strone(tmp_path)
    figura = re.search(r"<figure.*?</figure>", wynik, re.S).group(0)
    assert pogrubione(figura) == [], "analogia pod obrazem nie zużywa pojęcia; pierwsze wystąpienie liczy się w tekście głównym"
    assert 'alt="Okno z napisem Accept edits"' in figura
    assert "<figcaption>Okno z napisem Accept edits</figcaption>" in figura, "opis obrazu zostaje bez pogrubienia"


def test_komentarz_html_w_tekscie_nie_jest_dopasowaniem(tmp_path):
    (tmp_path / "lekcja.md").write_text("# T\n\nTekst bez pojęcia. <!-- fakt: Accept edits -->\n\n<!-- Accept edits w osobnej linii -->\n", encoding="utf-8")
    assert pogrubione(strona.zloz_strone(tmp_path)) == []


def test_naglowek_i_kod_w_lekcji_oraz_quiz_i_fiszki_bez_pogrubienia(tmp_path):
    (tmp_path / "lekcja.md").write_text("# Tryb Accept edits\n\n## Accept edits w nagłówku\n\nWpisz `Accept edits`.\n\n```\nAccept edits\n```\n", encoding="utf-8")
    (tmp_path / "quiz.yaml").write_text("pytania:\n  - pytanie: Co robi Accept edits?\n    odpowiedzi: [a, b]\n    poprawna: 0\n    wyjasnienie: Accept edits zmienia pliki.\n    fakt: x\n", encoding="utf-8")
    (tmp_path / "fiszki.yaml").write_text("fiszki:\n  - przod: Accept edits\n    tyl: Tryb\n    fakt: x\n", encoding="utf-8")
    wynik = strona.zloz_strone(tmp_path)
    assert wynik.count('class="pojecie-slowo"') == 0, "ani w tekście lekcji, ani w quizie i fiszkach (JSON na stronie)"


# --- zasada 3: dłuższe dopasowanie -----------------------------------------------------------------------------------------

KATALOG = ("katalog wtyczek", ["katalogu wtyczek"])
WTYCZKA = ("wtyczka", ["wtyczek", "wtyczka"])


def test_dluzsza_forma_wygrywa_z_krotsza_w_srodku():
    assert pogrub("<p>Otwórz listę w katalogu wtyczek.</p>", WTYCZKA, KATALOG) == ["katalog wtyczek"]


def test_krotsza_forma_dziala_gdzie_dluzszej_nie_ma():
    assert pogrub("<p>Mamy katalogu wtyczek, a potem wtyczek osobno.</p>", WTYCZKA, KATALOG) == ["katalog wtyczek", "wtyczka"]


def test_dluzsza_forma_wygrywa_bez_wzgledu_na_kolejnosc_hasel():
    assert pogrub("<p>W katalogu wtyczek.</p>", KATALOG, WTYCZKA) == ["katalog wtyczek"]


def test_pierscien_zuzycia_przed_pierscieniem():
    wynik = pogrub("<p>Pierścień zużycia i Pierścień.</p>", ("pierścień zużycia", ["Pierścień zużycia"]), ("pierścień", ["Pierścień"]))
    assert wynik == ["pierścień zużycia", "pierścień"]


def test_dluzsza_forma_zuzytego_pojecia_nie_oddaje_krotszej():
    """Drugie „katalogu wtyczek” to to samo, już pogrubione pojęcie; „wtyczek” w jego środku nie dostaje własnego pogrubienia."""
    assert pogrub("<p>W katalogu wtyczek jest to samo, co w katalogu wtyczek.</p>", WTYCZKA, KATALOG) == ["katalog wtyczek"]


# --- zasada 4: wielkość liter ----------------------------------------------------------------------------------------------


def test_skill_nie_lapie_skill_md():
    wynik = slownik(("skill", ["skill"])).pogrub("<p>Plik SKILL.md opisuje skill.</p>")
    assert pogrubione(wynik) == ["skill"] and "SKILL.md opisuje" in wynik


def test_wielka_litera_to_osobna_forma():
    assert pogrub("<p>Skill w tytule.</p>", ("skill", ["skill"])) == []
    assert pogrub("<p>Skill w tytule.</p>", ("skill", ["skill", "Skill"])) == ["skill"]


# --- zasada 5: formy ze znakami całą frazą, zwykłe całym wyrazem ------------------------------------------------------------


@pytest.mark.parametrize(
    "tekst, forma",
    [
        ("Wpisz /goal i czekaj.", "/goal"),
        ("Wpisz /compact teraz.", "/compact"),
        ("Kliknij menu + obok pola.", "menu +"),
        ("Wybierz Manual (ręczny) z listy.", "Manual (ręczny)"),
        ("Otwórz Settings (ustawienia) aplikacji.", "Settings (ustawienia)"),
    ],
)
def test_forma_ze_znakami_pasuje_calej_fraza(tekst, forma):
    assert pogrub(f"<p>{tekst}</p>", ("pojęcie", [forma])) == ["pojęcie"]
    czesc = forma.split(" ")[0]
    if " " in forma:
        assert pogrub(f"<p>Tylko {czesc} bez reszty.</p>", ("pojęcie", [forma])) == [], "sama część frazy nie wystarcza"


def test_forma_z_ukosnikiem_nie_laczy_sie_z_poprzednim_wyrazem():
    assert pogrub("<p>Ścieżka a/goal nic nie znaczy.</p>", ("polecenie", ["/goal"])) == []


@pytest.mark.parametrize("tekst", ["To natura.", "Terminalowy.", "Nieterminal.", "Pre-hook działa.", "Hook-owy tekst, hook-owy."])
def test_zwykla_forma_tylko_calym_wyrazem(tekst):
    assert pogrub(f"<p>{tekst}</p>", ("tura", ["tura"]), ("terminal", ["terminal"]), ("hook", ["hook", "Hook"])) == []


def test_granice_slowa_z_polskimi_znakami():
    haslo = ("tura", ["tura", "turę"])
    assert pogrub("<p>Jedna tura, jedną turę.</p>", haslo) == ["tura"]
    assert pogrub("<p>Zażółć turą, pasturę, tura!</p>", ("tura", ["tura", "turę"])) == ["tura"], "„pasturę” i „turą” to inne wyrazy"
    assert pogrub("<p>Zturę ą.</p>", haslo) == []


def test_twarda_spacja_i_zlamanie_linii_w_formie_wieloczlonowej():
    html_tekstu = "<p>Otwórz karta zgody albo karta\nzgody.</p>"
    wynik = slownik(("karta zgody", ["karta zgody"])).pogrub(html_tekstu)
    assert pogrubione(wynik) == ["karta zgody"]


# --- raz na lekcję ---------------------------------------------------------------------------------------------------------


def test_haslo_raz_na_lekcje_mimo_wielu_odmian_i_akapitow():
    wejscie = "<p>Pierwsza sesja.</p><p>Druga sesja i sesji.</p><ul><li>Trzecia sesją</li></ul>"
    wynik = slownik(("sesja", ["sesja", "sesji", "sesją"])).pogrub(wejscie)
    assert pogrubione(wynik) == ["sesja"] and wynik.count("pojecie-slowo") == 1
    assert wynik.index("pojecie-slowo") < wynik.index("Druga"), "pogrubione jest pierwsze wystąpienie"
    assert "Druga sesja i sesji." in wynik and "Trzecia sesją" in wynik


def test_kazde_haslo_dostaje_swoje_pogrubienie_w_kolejnosci_tekstu():
    wynik = pogrub("<p>Najpierw terminal, potem sesja, znów terminal.</p>", ("sesja", ["sesja"]), ("terminal", ["terminal"]))
    assert wynik == ["terminal", "sesja"]


def test_pierwsze_wystapienie_moze_byc_w_liscie_przed_akapitem():
    wynik = slownik(("sesja", ["sesja"])).pogrub("<ul><li>sesja w liście</li></ul><p>sesja w akapicie</p>")
    assert wynik.index("pojecie-slowo") < wynik.index("w akapicie")


# --- podpowiedź dla czytnika ekranu i wygląd znacznika ---------------------------------------------------------------------


def test_znacznik_ma_podpowiedz_powiazana_z_pogrubionym_slowem():
    wynik = Slownik((Haslo('Tryb <"A">', ("tryb A",), "Opis z <b> i & znakami.", "f"),)).pogrub("<p>To tryb A.</p>")
    slowo = re.search(r'<strong class="pojecie-slowo" role="button" tabindex="0" aria-expanded="false" aria-describedby="([\w-]+)" data-pojecie="([^"]*)">tryb A</strong>', wynik)
    assert slowo, wynik
    opis = re.search(rf'<span class="pojecie-opis" id="{slowo.group(1)}">(.*?)</span>', wynik)
    assert opis and html.unescape(opis.group(1)) == "Opis z <b> i & znakami." and "<b>" not in wynik
    assert 'role="tooltip"' in wynik and html.unescape(slowo.group(2)) == 'Tryb <"A">'
    assert re.search(r'<span class="pojecie-nazwa" aria-hidden="true">', wynik), "nazwa w podpowiedzi jest tylko do oglądania, czytnik czyta samo wyjaśnienie"


def test_identyfikatory_podpowiedzi_sa_unikalne():
    wynik = slownik(("a", ["aaa"]), ("b", ["bbb"]), ("c", ["ccc"])).pogrub("<p>aaa bbb ccc</p>")
    ids = re.findall(r'id="(pojecie-\d+)"', wynik)
    assert len(ids) == 3 == len(set(ids))


def test_pusty_slownik_i_brak_pliku_nic_nie_zmieniaja(tmp_path):
    assert Slownik(()).pogrub("<p>tekst</p>") == "<p>tekst</p>"
    assert wczytaj(tmp_path / "brak.yaml") == ()


def test_zly_ksztalt_hasla_to_blad_ze_sciezka(tmp_path):
    plik = tmp_path / "s.yaml"
    plik.write_text("pojecia:\n  - {pojecie: A, wyjasnienie: x}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="s.yaml"):
        wczytaj(plik)


# --- prawdziwy słowniczek i prawdziwa lekcja -------------------------------------------------------------------------------


def test_prawdziwy_slowniczek_ma_63_hasla_z_odmianami():
    hasla = wczytaj(PLIK_SLOWNICZKA)
    assert len(hasla) == 63 and all(h.odmiany and h.wyjasnienie for h in hasla)


def test_lekcja_okno_zgody_pogrubia_kazde_haslo_najwyzej_raz():
    from pathlib import Path

    katalog = Path(__file__).resolve().parent.parent / "moduly" / "tryby-pracy" / "okno-zgody"
    wynik = strona.zloz_strone(katalog)
    pogrubione_pojecia = pogrubione(wynik)
    assert pogrubione_pojecia and len(pogrubione_pojecia) == len(set(pogrubione_pojecia))
    assert "Manual" in pogrubione_pojecia and "Claude Code" in pogrubione_pojecia
    tresc = wynik.split('<div class="strona">', 1)[1]
    assert "Przewodnik po Claude Code" not in tresc.split("pojecie-slowo", 1)[0], "okruszki nie są w tekście, przed pierwszym pogrubieniem"
    for fraza in re.findall(r"<h[1-4]>(.*?)</h[1-4]>", tresc):
        assert "pojecie-slowo" not in fraza
