# Překladový glosář Zelda: The Minish Cap CZ

Edituje se v JSON chunkech (`translate/chunks/chunk_NN.json`). Vyplň `"cz"` z `"en"`.

## Formát stringu

Každý string může obsahovat **escape sekvence a tokeny** — **zachovej je přesně**:
- `\n` = nový řádek uvnitř textboxu
- `{Var:1}`, `{Var:2}` atd. = runtime proměnné (jméno, číslo)
- `{Color:Green}`, `{Color:White}`, `{Color:Red}` atd. = barva textu
- Jiné `{...}` makra = herní příkazy (zachovat)

Příklad:
```
"en": "\nThe data in File {Var:1} is corrupted."
"cz": "\nData v souboru {Var:1} jsou poskozena."
```

## Tvrdá omezení

1. **Bez diakritiky** (v0.1) — mapuj á→a, é→e, í→i, ó→o, ú→u, ý→y, č→c, š→s, ž→z, ř→r, ě→e, ť→t, ď→d, ň→n, ů→u. Font GBA Zelda fontu může mít trochu accentů, ale pro jistotu jedeme ASCII.
2. **Šířka řádku ~28 znaků** mezi `\n`. Originál tak dělá, drž se.
3. **NESahej na**: `\n`, `{Var:N}`, `{Color:X}`, ostatní `{...}` tokeny, jména postav.
4. Délka celkem není omezena (tmc_strings + relocate zvládne).

## Klíčové postavy + místa (NEPŘEKLÁDAT vlastní jména)

| EN | CZ |
|----|----|
| Link | Link |
| Zelda | Zelda |
| Hyrule | Hyrule |
| Vaati | Vaati |
| Ezlo | Ezlo |
| Picori | Picori |
| Minish | Minish |
| Triforce | Triforce |
| Master Sword | Master Sword (nebo "Mistrovský meč") |
| Hyrule Castle | hrad Hyrule |
| Hyrule Town | mesto Hyrule |
| Picori Festival | Festival Piccoru |
| Picori Blade | Picori cepel |
| King Daltus | král Daltus → kral Daltus |
| Smith | Smith (Linkův dědeček) |
| Dampe | Dampe |
| Kinstone | Kámen osudu → Kamen osudu |
| Mt. Crenel | Mt. Crenel |
| Castor Wilds | Castor Wilds |
| Royal Valley | Královské údolí → Kralovske udoli |
| Wind Tribe | Kmen větru → Kmen vetru |
| Cloud Tops | Mraky |
| Veil Falls | Veil Falls |

## Herní termíny

| EN | CZ |
|----|----|
| Heart | srdce |
| Rupee / Rupees | rupie |
| Bomb | bomba |
| Bow | luk |
| Boomerang | bumerang |
| Lantern | lampa |
| Map | mapa |
| Compass | kompas |
| Big Key | velký klíč → velky klic |
| Small Key | malý klíč → maly klic |
| dungeon | dungeon |
| sword | meč → mec |
| shield | štít → stit |
| save / load | uložit / nahrát → ulozit / nahrat |
| copy | kopírovat → kopirovat |
| erase / delete | smazat |
| File | soubor |
| Yes / No | Ano / Ne |
| OK | OK |
| start / quit | start / konec |

## Styl

- **Tykání** — neformální, dětský/přátelský tón hry.
- Zelda dialogy bývají hravé, mírně archaické.
- Vykřičníky, otazníky zachovat.
- Když je v originálu `...` nebo `…`, zachovat.

## Příklad

```
"en": "Activate Sleep Mode?\n\n{Var:1} Yes      {Var:2} No"
"cz": "Aktivovat rezim spanku?\n\n{Var:1} Ano      {Var:2} Ne"
```
