# Překladový glosář Advance Wars 2 CZ

Překládáme tahovou válečnou strategii. Text se edituje v JSON chunkech
(`chunk_NN.json`), pole `"cz"` se vyplní překladem pole `"en"`.

## Formát stringu

Každý string má řídicí escape sekvence — **zachovej je přesně**:
- `\r` = nový řádek uvnitř textového okna
- `\e` = scénový/příkazový marker (NIKDY nepřekládat, nech na místě)
- `\f` = prompt / konec okna (čeká na hráče)
- `\xNN` = syrový bajt (nech přesně tak)

Příklad:
```
"en": "How goes the Macro Land invasion?\\f"
"cz": "Jak pokracuje invaze do Macro Landu?\\f"
```

## Tvrdá omezení

1. **Bez diakritiky** (v0.1) — mapuj á→a, é→e, í→i, ó→o, ú→u, ý→y, č→c, š→s,
   ž→z, ř→r, ě→e, ť→t, ď→d, ň→n, ů→u. (Font AW2 sice má pár accentů přes
   prefix `'` a `~`, ale pro jistotu jedeme ASCII.)
2. **Šířka řádku ~33 znaků** mezi `\r`. Delší řádek se v okně ořízne.
   Drž se délky originálu — když originál má 2 řádky (`\r`), měj taky ~2.
3. **NESahej na**: `\e`, `\f`, `\xNN`, jména frakcí, jména CO.
4. Délka celkem není problém (text se relokuje), ale šířka řádku ano.

## Slovník — frakce (NEPŘEKLÁDAT, vlastní jména)

| EN | CZ |
|----|----|
| Orange Star | Orange Star |
| Blue Moon | Blue Moon |
| Green Earth | Green Earth |
| Yellow Comet | Yellow Comet |
| Black Hole | Black Hole |
| Wars World | Wars World |
| Macro Land / Cosmo Land | Macro Land / Cosmo Land |

## Slovník — COs (velitelé, NEPŘEKLÁDAT jména)

Andy, Max, Sami, Nell, Hachi, Olaf, Grit, Colin, Kanbei, Sonja, Sensei,
Eagle, Drake, Jess, Sturm, Hawke, Lash, Adder, Flak, Jugger, Koal.

## Slovník — herní termíny

| EN | CZ |
|----|----|
| CO (Commanding Officer) | velitel (CO) |
| HQ | základna / HQ |
| capture | obsadit |
| unit | jednotka |
| Infantry | pěchota |
| Mech | mech |
| Tank | tank |
| Recon | průzkumník → pruzkumnik |
| Artillery | dělostřelectvo → delostrelectvo |
| Rockets | rakety |
| Anti-Air | protiletadlo |
| Missiles | střely → strely |
| Fighter | stíhačka → stihacka |
| Bomber | bombardér → bombarder |
| B-Copter / T-Copter | bojový/transportní vrtulník (zkrať dle šířky) |
| Lander | výsadková loď → vysadkova lod |
| Cruiser | křižník → krizik/krizník |
| Battleship | bitevní loď → bitevni lod |
| Sub | ponorka |
| APC | APC (transportér) |
| base / airport / port | základna / letiště → letiste / přístav → pristav |
| city | město → mesto |
| funds / money | finance / peníze → penize |
| turn | tah |
| Power / CO Power | CO síla → CO sila |
| Super CO Power | Super CO síla |
| Fog of War | Mlha války → Mlha valky |
| Commander | velitel |
| army | armáda → armada |
| victory / defeat | vítězství → vitezstvi / porážka → porazka |
| attack | útok → utok |
| defense | obrana |
| move | pohyb |
| HP | HP |

## Styl

- **Vykání mezi vojáky/veliteli? Spíš vykání u formálních (Sturm, Hawke),
  tykání u kamarádských (Andy, Max, Sami).** Drž charakter postavy.
- Sturm = chladný záporák. Hawke = formální, oddaný. Andy = mladý, energický.
- Vojenský, ale ne přehnaně archaický tón.
- Vykřičníky a otazníky zachovat.

## Příklad

```
"en": "Excellent, my lord. The other COs\\rhave just completed their operations.\\f"
"cz": "Vyborne, pane. Ostatni velitele\\rprave dokoncili sve operace.\\f"
```
