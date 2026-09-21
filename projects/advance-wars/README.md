# Advance Wars 1 CZ

Český překlad hry **Advance Wars** (GBA, Intelligent Systems, 2001).

- **Cílová ROM:** `Advance Wars (USA) (Rev 1).gba`, 4 MB, kód `AWRE`,
  md5 `04775a93461d24cf1a7e3346d244e516`
- **Výstup:** `roms/Advance_Wars_CZ_v0.1.gba` (8 MB — ROM se rozšiřuje, viz níže)

## Proč ne přes disassembly

Ve složce `disassembly/` je [ketsuban/advancewars](https://github.com/ketsuban/advancewars),
ale je to raný IPS-based skelet (jediný `src/main.c`) a cílí navíc na **jinou
revizi ROM** (md5 `27f322f5…`). Pro překlad je nepoužitelný, takže text
reverzujeme přímo z binárky — stejnou cestou jako u Advance Wars 2.

## Formát textu

Stejný jako v AW2: null-terminovaný ASCII, na který ukazují 4bajtové LE
pointery ve tvaru `0x08000000 + offset`.

| kód | význam |
|---|---|
| `0x0D` (`\r`) | nový řádek uvnitř okna |
| `0x0E` (`\e`) | scénový / příkazový marker |
| `0x0F` (`\f`) | prompt, konec okna |

Text sedí v regionech `0x080000` (menu a UI), `0x110000`, `0x280000`–`0x300000`
(kampaň, tutoriály) a `0x3B0000`. Celkem **1839 stringů / 106,6 KB**.

## Pipeline

```bash
py -3 translate/extract.py            # ROM      -> translate/aw1_strings.json
py -3 translate/analyze_blocks.py     # kontrola bezpečnosti repackingu
py -3 translate/split_json.py 14      # JSON     -> translate/chunks/chunk_NN.json
#   ... překlad chunků ...
py -3 translate/check_progress.py     # stav + kontrola šířky řádků
py -3 translate/merge_json.py         # chunky   -> aw1_strings.json
py -3 translate/inject.py baserom.gba roms/Advance_Wars_CZ_v0.1.gba
```

`baserom.gba` je kopie originální ROM a **není v gitu**.

## Jak injektor řeší místo

AW1 má v ROM jen **33 KB** volného místa (`0x3F7D74`), zatímco AW2 měl 1,95 MB.
Přilepit češtinu na konec tedy nejde. `inject.py` proto:

1. **Repackuje každý souvislý blok textu na místě.** String zůstává na své
   původní adrese, dokud se před něj něco nerozroste; teprve pak se posune
   dopředu a přepíše se jeho pointer. Původní ROM má místy nepravidelný
   padding, takže přepočítávat layout natvrdo nejde.
2. **Přetečené stringy relokuje.** Nejdřív do původních 33 KB, pak do
   rozšíření ROM na 8 MB (standardní velikost GBA kartridge, adresní prostor
   sahá do 32 MB). Stringy, které se nevejdou, se tak nemusí krátit.
3. **Zapíchne 29 stringů**, na jejichž vnitřek ukazuje nějaký pointer — ty se
   nesmí hnout. Pokud se do svého slotu český překlad nevejde, zůstane
   anglicky.
4. Na závěr přepočítá komplementový checksum v hlavičce GBA.

### Ověření

`analyze_blocks.py` potvrdil dvě podmínky, bez kterých by repacking nebyl
bezpečný: uvnitř bloků **není žádný text, který by extraktor minul**, a
vnitřní pointery jsou ošetřené zapíchnutím.

Hlavní test je ale round-trip: `inject.py` s prázdnými překlady vyrobí ROM,
která je **bajt po bajtu shodná** s originálem. Simulace o 12 % delšího textu
spotřebuje 38 KB ze 4 MB dostupných.

```
ROUND-TRIP OK: original 4194304 bytes are byte-identical to the source ROM
```

## Kontrola překladu

`merge_json.py` zahodí každý překlad, ve kterém nesedí počet nebo pořadí
řídicích kódů proti originálu — radši anglický string než rozbité okno.
`check_progress.py` hlásí řádky delší než 40 znaků (šířka textového okna).
