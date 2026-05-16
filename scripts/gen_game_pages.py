#!/usr/bin/env python3
"""Generate per-game detail HTML pages from a manifest."""
import pathlib
import sys
import os

GAMES = [
    # slug, title, platform, platform_slug, year, genre, status, status_label, tagline, about_md, method_md, repo_note
    {
        "slug": "pokemon-ruby",
        "title": "Pokémon Ruby",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2002", "genre": "RPG",
        "status_class": "planned", "status_label": "PLANNED",
        "tagline": "Třetí generace Pokémonů — Hoenn region. První velký skok v sérii: nové schopnosti, dvojboje, příroda Hoennu.",
        "about": "Pokémon Ruby Version přinesla v roce 2002 zcela nový region Hoenn s 135 novými Pokémony, dvojboje (Double Battles), schopnosti (Abilities), přírodní typy útoků, a počasí (déšť, písečnou bouři, slunce). Hra je výrazně rozsáhlejší než Yellow.",
        "method": "Použijeme veřejný disassembly <a href='https://github.com/pret/pokeruby'>pret/pokeruby</a>. Workflow stejný jako u Yellow a FireRed. Pozor: Ruby má více než dvojnásobek textu Yellow.",
        "repo": "Pracovní repo dorazí, až se dostaneme k aktivnímu překladu této hry. V kalendáři za FireRed.",
    },
    {
        "slug": "zelda-link-to-the-past",
        "title": "Zelda: A Link to the Past",
        "platform": "SNES", "platform_slug": "snes",
        "year": "1991", "genre": "Action/Adventure",
        "status_class": "planned", "status_label": "PLANNED",
        "tagline": "Zlatá klasika z SNESu. Hyrule, Master Sword, Dark World — vše co vytvořilo identitu série Zelda.",
        "about": "The Legend of Zelda: A Link to the Past je top-down akční dobrodružství z roku 1991. Hráč coby Link prochází Hyrule i Dark World, řeší dungeony, sbírá Triforce. Dialogů spíš méně, ale ty co jsou, jsou kultovní.",
        "method": "Pro SNES Zeldu existuje silná hacking komunita. Texty jsou v relativně jednoduchém formátu, dají se extrahovat nástroji jako <strong>Hyrule Magic</strong> nebo <strong>ZScream</strong>. Žádný disassembly nepotřebujeme — text data jsou identifikovatelná a nahraditelná.",
        "repo": "Repo bude založen v okamžiku, kdy se k Zeldě dostaneme. Před zahájením prací na ní si chceme zafixovat workflow s Pokémon FireRed.",
    },
    {
        "slug": "zelda-minish-cap",
        "title": "Zelda: The Minish Cap",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2004", "genre": "Action/Adventure",
        "status_class": "planned", "status_label": "PLANNED",
        "tagline": "Capcomovo Zelda na GBA. Roztomilá grafika, miniaturní svět, klobouk Ezlo.",
        "about": "The Minish Cap je 2D Zelda hra od Capcomu (2004). Link se může zmenšovat na velikost lidí Minish a procházet svět z perspektivy myši. Hra má víc dialogů než LTTP a roztomilou prezentaci.",
        "method": "Komunita má nástroje pro úpravu textu (TMC editory). Není to čisté <em>disassembly</em>, ale ROM-hackerská cesta s extrakcí a injekcí textu je proveditelná.",
        "repo": "Stránka dostane repo, jakmile rozjedeme práci.",
    },
    {
        "slug": "super-mario-rpg",
        "title": "Super Mario RPG",
        "platform": "SNES", "platform_slug": "snes",
        "year": "1996", "genre": "JRPG",
        "status_class": "planned", "status_label": "PLANNED",
        "tagline": "Mario × Square = nečekaný hit z roku 1996. Plný humor, dialogy, party systém.",
        "about": "Super Mario RPG: Legend of the Seven Stars vzniklo jako spolupráce Nintenda a Square Soft. Je to plnotučné JRPG s pohledem z izometrie, party combat systémem, a překvapivě hlubokým humorem. Spousta textu.",
        "method": "SMRPG má aktivní hackerskou komunitu (smwcentral, romhacking.net) s nástroji pro editaci textu. Není disassembly, ale ROM-hacking cesta je dobře zmapovaná.",
        "repo": "Repo dorazí časem.",
    },
    {
        "slug": "fire-emblem",
        "title": "Fire Emblem (7)",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2003", "genre": "Tactical RPG",
        "status_class": "planned", "status_label": "PLANNED",
        "tagline": "První Fire Emblem co dorazil na západ. Plná taktická strategie + obrovský příběh.",
        "about": "Známý jen jako „Fire Emblem“ — sedmý díl série, prvni co vyšel mimo Japonsko. Hráč velí armádě, postavy umírají natrvalo, prokládáno desítkami dialogů a romancí. Stovky kapitol textu.",
        "method": "Aktivní FE komunita (feuniverse.us) má <strong>FEBuilderGBA</strong> — kompletní editor co dovede měnit texty bez disassembly. Pravděpodobně nejlepší tool napříč všemi GBA hrami.",
        "repo": "Repo dorazí časem.",
    },
    {
        "slug": "fire-emblem-sacred-stones",
        "title": "Fire Emblem: Sacred Stones",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2004", "genre": "Tactical RPG",
        "status_class": "planned", "status_label": "PLANNED",
        "tagline": "Osmý Fire Emblem, kratší a snazší než FE7. Ideální vstup do série.",
        "about": "Sacred Stones (FE8) je vstupní díl série — kratší, snazší, ale s vlastním kouzlem. Hráč si vybere mezi cestou Eirika a Ephraim. Dobré coby tutoriálová hra pro nováčky.",
        "method": "Stejný workflow jako FE7 — FEBuilderGBA.",
        "repo": "Repo dorazí časem.",
    },
    {
        "slug": "final-fantasy-6",
        "title": "Final Fantasy VI",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2006", "genre": "JRPG",
        "status_class": "planned", "status_label": "PLANNED",
        "tagline": "Mnozí to mají za <em>nejlepší</em> Final Fantasy. Hluboký příběh, 14 hratelných postav, Kefka.",
        "about": "FFVI Advance (2006) je port z SNESu z roku 1994. Steampunk svět, opera scene, Kefka jako jeden z nejlepších padouchů v dějinách JRPG. Obrovský objem textu — desítky hodin příběhu.",
        "method": "ff6hacking.com má robustní nástroje pro úpravu textu i v GBA verzi. Také existují slovesné slovníky a překladové projekty.",
        "repo": "Repo dorazí časem.",
    },
    {
        "slug": "final-fantasy-4",
        "title": "Final Fantasy IV",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2005", "genre": "JRPG",
        "status_class": "planned", "status_label": "PLANNED",
        "tagline": "Cecil, Kain, Rosa — temná fantasy s dramatickými zvraty.",
        "about": "FFIV Advance přidává nové bonus dungeony k originálu z 1991. Klasický příběh paladina hledajícího vykoupení. Slušná porce textu.",
        "method": "Square Enix GBA texty jsou ve standardizovaném formátu, lze je editovat pomocí FF Hacktools nebo podobných utilit.",
        "repo": "Repo dorazí časem.",
    },
    {
        "slug": "final-fantasy-5",
        "title": "Final Fantasy V",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2006", "genre": "JRPG",
        "status_class": "planned", "status_label": "PLANNED",
        "tagline": "Job system, který definoval žánr. Bartz, Faris, Lenna, Galuf.",
        "about": "FFV Advance přidává čtyři nové joby k slavnému jobsystému. Méně serióznější tón než FF4/6, ale herně možná nejhlubší. GBA verze přidává bonus content.",
        "method": "Stejně jako FF4 — Square GBA toolset.",
        "repo": "Repo dorazí časem.",
    },
    {
        "slug": "final-fantasy-1-2",
        "title": "Final Fantasy I+II: Dawn of Souls",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2004", "genre": "JRPG",
        "status_class": "planned", "status_label": "PLANNED",
        "tagline": "První dvě Final Fantasy v jedné kazetě. Vzpomínka na zrod žánru.",
        "about": "Dawn of Souls obsahuje remakey původních FF1 (1987) a FF2 (1988) s vylepšenou grafikou a bonus dungeony. Menší objem textu než pozdější díly.",
        "method": "Square GBA toolset funguje i tady.",
        "repo": "Repo dorazí časem.",
    },
    {
        "slug": "advance-wars",
        "title": "Advance Wars",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2001", "genre": "Turn-based Strategy",
        "status_class": "planned", "status_label": "PLANNED",
        "tagline": "Tahová válka v cartoon obalu. Andy, Max, Sami a Orange Star vs. Blue Moon.",
        "about": "Advance Wars je tahová strategie od Intelligent Systems (autoři Fire Emblem). 30+ misí, briefingy mezi misemi, charisma CO (Commanding Officers). Dialogy nejsou tak hluboké jako u FE, ale jsou kompaktní a memorable. Tom Clancy/Hot Dog/USA charm.",
        "method": "Pro Advance Wars nejsou veřejné disassembly. Komunita má ale text editory a obecně se hra dá hackovat (Romhacking.net má pár translation patches do jiných jazyků). Workflow: extrakce textu z ROM → překlad → injekce → ověření v emulátoru.",
        "repo": "Repo dorazí, jakmile se dostaneme k aktivnímu překladu.",
    },
    {
        "slug": "advance-wars-2",
        "title": "Advance Wars 2: Black Hole Rising",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2003", "genre": "Turn-based Strategy",
        "status_class": "planned", "status_label": "PLANNED",
        "tagline": "Pokračování AW. Black Hole armáda, Sturm, nové CO Sensei, Hawke, Lash, Adder, Flak.",
        "about": "Advance Wars 2 je pokračování s rozšířeným rosterem CO a delším příběhem. Stejný kreslený styl, stejné gameplay principy, víc obsahu. Dialogy nejdou do hloubky postav (žádná FE-styl romance), ale jsou character-defining.",
        "method": "Stejný workflow jako AW1 — ROM-hacking přístup s komunitními tools.",
        "repo": "Repo dorazí později.",
    },
    {
        "slug": "fft-advance",
        "title": "Final Fantasy Tactics Advance",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2003", "genre": "Tactical RPG",
        "status_class": "hard", "status_label": "HARD",
        "tagline": "Marche, Mewt a Ivalice. Tactics na GBA s job systémem a soudci.",
        "about": "FFTA má velmi specifický taktický systém s pravidly (\"laws\") a soudci, kteří trestají porušení. Příběh chytrý, dialogy plné dvojakosti. Texty jsou ale ve složitějším komprimovaném formátu.",
        "method": "Komunita tools má, ale ne tak hladce jako u jiných her. Reverse engineering text formátu by mohl zabrat nějaký čas.",
        "repo": "Repo dorazí, pokud se k té hře dostaneme.",
    },
    {
        "slug": "metroid-fusion",
        "title": "Metroid Fusion",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2002", "genre": "Action/Adventure",
        "status_class": "planned", "status_label": "PLANNED",
        "tagline": "SA-X, parazitická forma, klaustrofobický horor v Metroid stylu.",
        "about": "Metroid Fusion vrací sérii ke 2D kořenům po Super Metroid. Samus na BSL lodi, pronásledována SA-X formou. Hra má víc dialogů než předchozí Metroidy (předevsím cutscenes a briefingy).",
        "method": "Existují textové editory specifické pro Metroid Fusion. Workflow podobný jiným GBA hrám.",
        "repo": "Repo dorazí časem.",
    },
    {
        "slug": "metroid-zero-mission",
        "title": "Metroid: Zero Mission",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2004", "genre": "Action/Adventure",
        "status_class": "planned", "status_label": "PLANNED",
        "tagline": "Remake původního Metroid z 1986. Krásnější grafika, plnější příběh.",
        "about": "Zero Mission je remake originálního NES Metroid. Méně textu než Fusion, ale stále s úvodními briefingy a pár dialogy. Po porážce Mother Brain přichází bonus segment „Zero Suit Samus\".",
        "method": "Stejné nástroje a workflow jako Fusion.",
        "repo": "Repo dorazí časem.",
    },
    {
        "slug": "castlevania-aria",
        "title": "Castlevania: Aria of Sorrow",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2003", "genre": "Metroidvania",
        "status_class": "hard", "status_label": "HARD",
        "tagline": "Soma Cruz v zámku Drákuly v roce 2035. Mnozí to mají za nejlepší Castlevanii.",
        "about": "Aria of Sorrow je třetí GBA Castlevania. Soma Cruz objevuje, že může absorbovat duše nepřátel. Příběh sahá daleko za běžnou „rytíř zabije Drákulu\" linku.",
        "method": "Castlevania má custom text engine. Není <em>žádný</em> oficiální disassembly. Reverse engineering ROM bude potřeba — najít texty, pochopit kódování, identifikovat ukazatele.",
        "repo": "Repo bude jen pokud najdeme cestu k textům.",
    },
    {
        "slug": "castlevania-cotm",
        "title": "Castlevania: Circle of the Moon",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2001", "genre": "Metroidvania",
        "status_class": "hard", "status_label": "HARD",
        "tagline": "První GBA Castlevania. DSS karetní systém, Nathan Graves.",
        "about": "Circle of the Moon byla launch hra GBA. Tmavší grafika, ale neskutečně hluboký DSS systém kombinování karet. Méně dialogů než AoS.",
        "method": "Custom engine, podobně jako AoS — nutný reverse engineering. Méně textu = jednodušší než ostatní Castlevanie.",
        "repo": "Repo bude jen pokud najdeme cestu k textům.",
    },
    {
        "slug": "castlevania-hod",
        "title": "Castlevania: Harmony of Dissonance",
        "platform": "GBA", "platform_slug": "gba",
        "year": "2002", "genre": "Metroidvania",
        "status_class": "hard", "status_label": "HARD",
        "tagline": "Juste Belmont. Dva zámky, dvě dimenze, jeden Dracula.",
        "about": "HoD má dva paralelní zámky které se prozkoumávají. Hudba bohužel kontroverzní — méně oblíbená než AoS. Méně dialogů než AoS.",
        "method": "Custom engine, reverse engineering nutný.",
        "repo": "Repo bude jen pokud najdeme cestu k textům.",
    },
    {
        "slug": "super-mario-world",
        "title": "Super Mario World",
        "platform": "SNES", "platform_slug": "snes",
        "year": "1990", "genre": "Platformer",
        "status_class": "planned", "status_label": "PLANNED (málo textu)",
        "tagline": "Mario + Yoshi v Dinosaur Land. Launch hra SNESu.",
        "about": "Super Mario World je launch hra SNESu z roku 1990. Mario, Luigi, Yoshi, 96 východů, Bowserovi synové. Dialogů je v ní opravdu málo — pár intro/outro textů, pár cedulí.",
        "method": "Nejaktivnější SNES hacking komunita vůbec (smwcentral.net) má <strong>Lunar Magic</strong> a desítky text editorů. Tahle hra je technicky nejlepší vstupní bod do SNES romhackingu.",
        "repo": "Repo dorazí časem.",
    },
    {
        "slug": "yoshis-island",
        "title": "Super Mario World 2: Yoshi's Island",
        "platform": "SNES", "platform_slug": "snes",
        "year": "1995", "genre": "Platformer",
        "status_class": "hard", "status_label": "HARD",
        "tagline": "Pastelová grafika, Yoshi jako hrdina, baby Mario na zádech.",
        "about": "Yoshi's Island vypadá jako kreslená pohádka. Hodnocení 5/5 napříč recenzemi. Texty: spíš málo, hlavně menu a hub texty. Hra má custom enginy pro téměř všechno.",
        "method": "Yoshi's Island je technicky složitější než SMW — používá Super FX2 chip, speciální grafiku. Méně otevřených tools. Menší textový objem ale plus.",
        "repo": "Repo bude jen pokud najdeme cestu.",
    },
    {
        "slug": "super-metroid",
        "title": "Super Metroid",
        "platform": "SNES", "platform_slug": "snes",
        "year": "1994", "genre": "Action/Adventure",
        "status_class": "planned", "status_label": "PLANNED (málo textu)",
        "tagline": "Šablona pro celý metroidvania žánr. Planet Zebes, baby Metroid, finále tisíciletí.",
        "about": "Super Metroid je legendární. Téměř bez dialogů — appraisálné vyprávění prostředím. Pár textových briefingů, item descriptions, ending. Malý překlad-relevant text objem.",
        "method": "Aktivní SM hacking komunita. <strong>SMILE</strong> a další editory umí měnit text. Workflow zaběhnutý.",
        "repo": "Repo dorazí časem.",
    },
    {
        "slug": "super-r-type",
        "title": "Super R-Type",
        "platform": "SNES", "platform_slug": "snes",
        "year": "1991", "genre": "Shoot 'em up",
        "status_class": "hard", "status_label": "HARD (málo textu)",
        "tagline": "Klasický side-scrolling shooter z Irem stable.",
        "about": "Super R-Type je shooter — text v ní téměř není. Pár obrazovek mezi misemi, menu, game over. Překládat ho má smysl jen pokud chceš opravdu „kompletní katalog\".",
        "method": "Žádná silná komunita kolem této hry. Asi by se musel udělat ad-hoc text dump.",
        "repo": "Pravděpodobně to nestihneme.",
    },
    {
        "slug": "startrek-dsn9",
        "title": "Star Trek: Deep Space Nine",
        "platform": "SNES", "platform_slug": "snes",
        "year": "1995", "genre": "Adventure",
        "status_class": "hard", "status_label": "HARD",
        "tagline": "DS9 jako adventura. Sisko, Quark, Dax, prostor stanice na Bajoru.",
        "about": "Hra existuje, ale je značně neznámá. Adventura na téma seriálu. Bude obsahovat značný objem textu (dialogy postav).",
        "method": "Žádná hackerská komunita. Vlastní reverse engineering by trval.",
        "repo": "Nevhodný kandidát.",
    },
    {
        "slug": "startrek-tng",
        "title": "Star Trek TNG: Future's Past",
        "platform": "SNES", "platform_slug": "snes",
        "year": "1994", "genre": "Adventure",
        "status_class": "hard", "status_label": "HARD",
        "tagline": "Picard, Riker, Data, Worf — Enterprise-D ve vesmírné záhadě.",
        "about": "TNG adventura zahrnující komunikaci s posádkou, away mise, vesmírné souboje. Slušný textový objem.",
        "method": "Stejně neznámý ROM, stejně potřebný reverse engineering.",
        "repo": "Nevhodný kandidát.",
    },
    {
        "slug": "startrek-academy",
        "title": "Star Trek: Starfleet Academy",
        "platform": "SNES", "platform_slug": "snes",
        "year": "1994", "genre": "Simulator",
        "status_class": "hard", "status_label": "HARD",
        "tagline": "Bridge simulator. Vyzkoušej si Kobayashi Maru.",
        "about": "Bridge simulator — řídíš loď ze sedátka kapitána. Méně dialogů, spíš briefingy a velitelské příkazy.",
        "method": "Stejný problém jako ostatní Star Trek SNES hry.",
        "repo": "Nevhodný kandidát.",
    },
    {
        "slug": "re1",
        "title": "Resident Evil",
        "platform": "PS1", "platform_slug": "ps1",
        "year": "1996", "genre": "Survival Horror",
        "status_class": "skip", "status_label": "SKIP",
        "tagline": "Spencer Mansion, S.T.A.R.S., zombie. Začátek největší survival horror série.",
        "about": "Originální Resident Evil je legendární. PS1 disk obsahuje plně dabované filmečky, hluboké menu, file system uvnitř hry. Bohatý textový obsah.",
        "method": "<strong>PS1 je mimo scope tohoto projektu.</strong> Disc-based hry vyžadují úplně jiný workflow: extrakce ISO, dekomprese archivu, identifikace text data uvnitř (často hardcoded v binárce nebo v custom containerech), modifikace, opětovné sestavení ISO. Plus dabingu se nedotkneme. Realisticky by jedna hra zabrala týdny.",
        "repo": "Mimo scope.",
    },
    {
        "slug": "re3",
        "title": "Resident Evil 3: Nemesis",
        "platform": "PS1", "platform_slug": "ps1",
        "year": "1999", "genre": "Survival Horror",
        "status_class": "skip", "status_label": "SKIP",
        "tagline": "Jill Valentine vs. Nemesis v Raccoon City. Devadesátkový horror v top formě.",
        "about": "RE3 přidává Nemesis — bossa který tě pronásleduje po celé hře. Hodně cutscenes, hodně menu, files.",
        "method": "Stejné důvody jako u RE1 — PS1 je mimo scope.",
        "repo": "Mimo scope.",
    },
    {
        "slug": "silent-hill",
        "title": "Silent Hill",
        "platform": "PS1", "platform_slug": "ps1",
        "year": "1999", "genre": "Survival Horror",
        "status_class": "skip", "status_label": "SKIP",
        "tagline": "Mlha, sirény, Harry Mason, ztracená Cheryl. Psychologický horor nejvyšší ligy.",
        "about": "Silent Hill je hluboký, atmosférický, plný dialogů a multiple endings. PS1 disc, plně dabovaný.",
        "method": "Stejné důvody jako u Resident Evil — PS1 mimo scope.",
        "repo": "Mimo scope.",
    },
]

TEMPLATE = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} CZ — Retro hry česky</title>
<meta name="description" content="Český překlad hry {title} pro {platform}.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/game.css">
</head>
<body data-platform="{platform_slug}">

<header>
  <nav><a href="../index.html">← zpět na katalog</a></nav>
  <div class="platform-tag">{platform} · {year} · {genre}</div>
  <h1 class="crt">{title}<br><span class="accent">česky</span></h1>
  <p class="tagline">{tagline}</p>
  <span class="badge status-{status_class}">{status_label}</span>
</header>

<main>

<section>
  <h2>O hře</h2>
  <p>{about}</p>
</section>

<section>
  <h2>Jak na překlad</h2>
  <p>{method}</p>
</section>

<section>
  <h2>Stav</h2>
  <p>Zatím nezačato. Sleduj <a href="../index.html">katalog</a> nebo pilotní projekt <a href="https://mhudakcz.github.io/GBC_Pokemon_Yellow_AI_CZ/">Pokémon Yellow CZ</a>, který běží jako referenční implementace celého workflow.</p>
</section>

<section>
  <h2>Repo a kontakt</h2>
  <p>{repo}</p>
</section>

</main>

<footer>
  <p><a href="../index.html">← zpět na Retro hry česky</a></p>
  <p style="margin-top:8px; font-size:16px; opacity:0.7;">Fanouškovský projekt — všechny ochranné známky patří jejich vlastníkům.</p>
</footer>

</body>
</html>
"""

def main():
    out_dir = pathlib.Path(__file__).resolve().parent.parent / "docs" / "games"
    out_dir.mkdir(parents=True, exist_ok=True)

    for g in GAMES:
        path = out_dir / f"{g['slug']}.html"
        if g['slug'] == 'pokemon-firered':
            print(f"  skip (custom): {path.name}")
            continue
        path.write_text(TEMPLATE.format(**g), encoding='utf-8')
        print(f"  wrote: {path.name}")

    print(f"\nTotal: {len(GAMES)-1} placeholder pages + 1 custom (firered) = {len(GAMES)} games")

if __name__ == '__main__':
    main()
