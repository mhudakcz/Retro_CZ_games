# Překladový glosář Pokémon FireRed CZ

Závazná pravidla a slovník pro konzistenci napříč všemi soubory.

## Tvrdá omezení

1. **Max 36 znaků na vizuální řádek** (mezi `\n`, `\l`, `\p`).
   FireRed text box má variable-width font, ale ~36 znaků = bezpečný horní strop.
2. **Diakritika částečně nativní**:
   - **POUŽÍVEJ NATIVNĚ:** á é í ó ú Á É Í Ó Ú (jsou v originálním fontu!)
   - **MAPUJ NA ASCII:** ý→y, č→c, š→s, ž→z, ř→r, ě→e, ť→t, ď→d, ň→n, ů→u
     (a velké analogicky: Ý→Y, Č→C, Š→S, Ž→Z, Ř→R, Ě→E, Ť→T, Ď→D, Ň→N, Ů→U)
3. **Nikdy nesahej na:**
   - Návěští (`Foo_Text_Bar::`)
   - `.string` macro samotné
   - Speciální tokeny v {curly braces}: `{PLAYER}`, `{RIVAL}`, `{STR_VAR_1}`, `{NAME}` …
   - Escape sekvence: `\n` (nový řádek), `\l` (scroll-down nový řádek), `\p` (nový odstavec, čeká na hráče), `$` (konec)
   - Literál `POKéMON` — zachovat přesně tak (originální font má `é`)
4. **Po každém souboru:** `py -3 -X utf8 ../translate/width_check.py data/maps/Foo/text.inc` musí být OK.

## Diakritika v praxi

**Příklady správného použití:**

```
"Vítej, mladíku!" — VÍ má í (nativní), takže napiš jak je
"Šťastnou cestu" — Šť nemá nativní, mapuj na "Stastnou cestu"
"Žádný problém" — Ž nemá nativní, mapuj na "Zadny problem"
"Děkuji!" — ě nemá nativní, ale é nativní, takže "Dekuji!" je OK
"Pokémon" — keep as POKéMON (originální font)
"Příliš" — ř a í: ř→r, í je nativní: "Príliš" ne, "Priliš" ne. Mapuj VŠECHNY:
  ř→r, í→i. Hmm, ale í je nativní... mapuj jen ty co nejsou.
  Správně: "Příliš" → "Príliš" (řemapuj r), pak í zůstává jako í = "Príliš"

Wait — pokud chceme konzistenci: pouze á é í ó ú jdou nativně.
ý → y, č → c, š → s, ž → z, ř → r, ě → e, ť → t, ď → d, ň → n, ů → u

Příklad jednoho slova:
"Příliš" obsahuje ř (→r) a í (nativní) a š (→s):
  P r í l i š  →  P r í l i s  →  "Prílis"
```

## Standardní překlady

| EN | CZ | Pozn. |
|----|----|----|
| POKéMON | POKéMON | nikdy nepřepisuj (originální token v charmap) |
| OAK | OAK | vlastní jméno |
| MOM | MAMA | máma → mama |
| TRAINER | trénér | é nativní |
| LEADER | vúdce | ú nativní |
| GYM | GYM | beze změny |
| BADGE | ODZNAK | |
| LEAGUE | LIGA | |
| CHAMPION | šampión → SAMPIÓN | š→S, ó nativní |
| ROCKET / TEAM ROCKET | TEAM ROCKET | vlastní jméno týmu |
| ELITE FOUR | ELITNÍ ČTYŘKA → ELITNÍ CTYRKA | č→c, ř→r |
| WILD | divoký → divoký (ý→y: divoky) | |
| TRADE | výměna → výmena (ě→e: vymena) | |
| EVOLVE | vyvinout | |
| EVOLUTION | vývoj → vývoj (no diac change) | |
| ATTACK | útok | ú nativní |
| FAINTED | omdlel | |
| HEAL | uzdravit | |
| Hello! | Ahoj! | |
| Hi! | Čau! → Cau! | č→c |
| Thanks! | Díky! | í nativní |
| Bye! | Měj se! → Mej se! | ě→e |
| Wait! | Počkej! → Pockej! | č→c |
| Sorry | Promiň → Prominn? Ne — ň→n: Promin | |
| Yes / No | Ano / Ne | |
| Okay! | Dobře! → Dobre! | ř→r |
| Please | Prosím | í nativní |
| Excellent! | Výborně! → Výborne! | ě→e, ý→y: Vyborne! |
| Great! | Skvělé! → Skvélé? Ne — ě→e: Skvele! |  é nativní by bylo… ne, é≠ě. Mapuj. |
| Strong | silný → silny | ý→y |
| Battle | boj / souboj | |
| Items | předměty → predmety | ř,ě→r,e |
| Money | peníze | í nativní |
| Buy / Sell | koupit / prodat | |
| Shop / MART | OBCHOD | možno krátit |
| POKéMON CENTER | POKéMON CENTRUM | |
| POKé BALL | POKé BALL | |
| POKéDEX | POKéDEX | |
| TM / HM | TM / HM | |
| EXP / LEVEL | EXP / ÚROVEŇ → EXP / UROVEN | ň→n |
| HP / PP | HP / PP | |
| STATS | STATY | |
| SPEED | RYCHLOST | |
| ATTACK (stat) | ÚTOK | ú nativní |
| DEFENSE | OBRANA | |
| SPECIAL | SPECIÁL | á nativní |
| POTION | LEKTVAR | |
| ANTIDOTE | PROTIJED | |
| KEY | KLÍČ → KLIC | č→c, í nativní by bylo KLÍC, ne dělej KLIC |
| MAP | MAPA | |
| TOWN | MĚSTO → MESTO | ě→e |
| CITY | MĚSTO → MESTO | |
| ROUTE | CESTA | |

## Speciální jména (ponechat anglicky / původně)

- Jména Pokémonů (PIKACHU, CHARIZARD, …) — beze změny
- Jména útoků (THUNDERBOLT, …) — beze změny (řeší se zvlášť)
- Jména předmětů (POTION, …) — beze změny (řeší se zvlášť)
- Jména měst (CELADON CITY, PEWTER CITY, atd.) na cedulích — beze změny
- Jména postav (BROCK, MISTY, BILL, LANCE, …) — beze změny
- Profesor OAK — beze změny

## Stylistické pokyny

- **Tykání**. FireRed má neformální/přátelský tón.
- **Krátké věty**. Dialogy mají dynamiku — neprodlužuj.
- **NPC mluví jako kamarádi** — žádné formální obraty.
- Vykřičníky a otazníky zachovat z originálu.
- Trojtečka `…` v originálu je jediný znak v charmap — zachovat.
- Když uvažuješ o překladu, **myš za sebe stejně používá diakritiku** (správnou českou), pak ji ručně transformuj podle pravidel výše.

## Jak ověřit šířku

```bash
cd disassembly
py -3 -X utf8 ../translate/width_check.py data/maps/PalletTown/text.inc
```

Linter sleduje 36 znaků na řádek (mezi `\n`, `\l`, `\p`). Tokenům v {curly braces} přiřazuje max šířku (PLAYER=7, STR_VAR=10).
