# Překladový glosář Advance Wars 1 CZ

Tahová válečná strategie (GBA, 2001, Intelligent Systems). Text se edituje
v JSON chunkech (`chunks/chunk_NN.json`), pole `"cz"` se vyplní překladem
pole `"en"`. Navazuje na glosář Advance Wars 2 — **termíny musí sedět mezi
oběma díly**.

## Formát stringu

Řídicí escape sekvence — **zachovej je přesně a ve stejném pořadí**:

| escape | význam |
|---|---|
| `\r` | nový řádek uvnitř textového okna |
| `\e` | scénový/příkazový marker — NIKDY nepřekládat, nech na místě |
| `\f` | prompt / konec okna (čeká na stisk hráče) |
| `\xNN` | syrový bajt — nech přesně tak |

## Tvrdá omezení

1. **Bez diakritiky.** Mapuj á→a, é→e, í→i, ó→o, ú→u, ý→y, č→c, š→s, ž→z,
   ř→r, ě→e, ť→t, ď→d, ň→n, ů→u. (Injektor to sice umí složit sám, ale piš
   rovnou bez háčků, ať je vidět skutečná délka řádku.)
2. **Šířka řádku max 40 znaků** mezi `\r` / `\f` / `\e`. Hra needituje
   zalomení sama — co se nevejde, zmizí za okrajem okna. Ideálně drž délku
   originálního řádku.
3. **Počet řádků zachovej.** Když má originál dva `\r`, měj taky dva.
   Když se ti čeština nevejde, radši zkrať formulaci, nepřidávej řádek.
4. Celková délka textu problém není (injektor stringy relokuje), **šířka
   řádku ano**.
5. Nesahej na `\e`, `\f`, `\xNN`, jména frakcí ani jména velitelů.

## Frakce (NEPŘEKLÁDAT — vlastní jména)

Orange Star, Blue Moon, Green Earth, Yellow Comet, Black Hole, Cosmo Land.

## Velitelé / COs (NEPŘEKLÁDAT jména)

| frakce | COs |
|---|---|
| Orange Star | Andy, Max, Sami, Nell, Hachi |
| Blue Moon | Olaf, Grit |
| Yellow Comet | Kanbei, Sonja |
| Green Earth | Eagle, Drake |
| Black Hole | Sturm |

## Jednotky

| EN | CZ |
|----|----|
| Infantry | pechota |
| Mech | mech |
| Recon | pruzkumnik |
| Tank | tank |
| Md. Tank | tezky tank |
| APC | APC |
| Artillery | delostrelectvo |
| Rocket | raketomet |
| Anti-Air | protiletadlo |
| Missile | rakety |
| Fighter | stihacka |
| Bomber | bombarder |
| B Copter | bojovy vrtulnik |
| T Copter | transportni vrtulnik |
| Battleship | bitevni lod |
| Cruiser | krizník → krizik (bez diakritiky: krizik) |
| Lander | vysadkova lod |
| Sub | ponorka |

## Terén a budovy

| EN | CZ |
|----|----|
| HQ | HQ |
| city | mesto |
| base | zakladna |
| airport | letiste |
| port | pristav |
| plain | plan |
| wood(s) | les |
| mountain | hory |
| road | silnice |
| bridge | most |
| river | reka |
| sea | more |
| shoal | melcina |
| reef | utes |

## Herní termíny

| EN | CZ |
|----|----|
| CO (Commanding Officer) | velitel (CO) |
| CO Power | CO sila |
| unit | jednotka |
| army | armada |
| turn | tah |
| capture | obsadit |
| funds | finance |
| fuel | palivo |
| ammo | munice |
| HP | HP |
| attack / defense | utok / obrana |
| movement | pohyb |
| Fog of War | Mlha valky |
| victory / defeat | vitezstvi / porazka |
| Field Training | Vycvik |
| War Room | Valecna mistnost |
| Design Maps | Tvorba map |
| Campaign | Tazeni |
| Battle Maps | Bojove mapy |

## Styl

- **Tykání u kamarádských postav** (Andy, Max, Sami, Grit), **vykání
  u formálních** (Nell vůči kadetovi vyká, Sturm, Kanbei, Eagle, Drake).
- Andy = mladý, nadšený, trochu naivní. Max = drsňák, přímý. Sami = ostrá,
  sebevědomá. Nell = instruktorka, klidná a věcná. Olaf = protivný, ironický.
  Grit = pomalý venkovský klid, mluví lidově. Kanbei = hrdý, formální.
  Sonja = chytrá, analytická. Eagle = pyšný, ostrý. Drake = dobrácký mořský
  vlk. Sturm = chladný, nadřazený záporák.
- Vojenský tón, ale ne archaický. Vykřičníky a otazníky zachovej.
- Tutoriálové texty (Field Training) piš jasně a instruktážně, druhá osoba.

## Příklad

```
"en": "Andy? Listen up, pal. I'm Max.\rThe best CO in the business.\f"
"cz": "Andy? Poslouchej, kamarade. Ja jsem Max.\rNejlepsi velitel siroko daleko.\f"
```
