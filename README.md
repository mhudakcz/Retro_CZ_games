# Retro hry česky

Komunitní české překlady retro herních klasik. Open-source meta-projekt zaměřený na hry pro Game Boy / GBA / SNES.

## Co je v tomto repu

- **`docs/`** — GitHub Pages: landing page + detail stránky pro každou hru
- **`projects/`** — pracovní adresáře pro jednotlivé hry (typicky odkazují na vlastní samostatné repo)
- **`scripts/`** — pomocné nástroje (generátor HTML stránek, atd.)
- **`IN/`** — vstupní ROM-ky (NENÍ v gitu — pouze lokálně)

## Hotové projekty

| Hra | Platforma | Stav | Detail |
|---|---|---|---|
| [Pokémon Yellow](https://mhudakcz.github.io/GBC_Pokemon_Yellow_AI_CZ/) | GBC | v0.4 DONE | samostatný repo |

## Pilot

[Pokémon Yellow CZ](https://github.com/mhudakcz/GBC_Pokemon_Yellow_AI_CZ) — první projekt, slouží jako referenční implementace celého workflow (disassembly → překlad → build → ROM).

## Aktuálně rozjíždíme

- Pokémon FireRed (GBA) — viz `docs/games/pokemon-firered.html`

## Filozofie

1. **Jen text měníme** — žádné gameplay změny, žádné nové funkce.
2. **Open-source** — každý projekt má vlastní repo, čistý git history.
3. **Reprodukovatelné buildy** — kde to jde, byte-perfektní disassembly, ROM se buildí ze zdroje.
4. **Bez diakritiky v prvním kole** — háčky a čárky řeší později rozšířením fontu.
5. **Honest about feasibility** — některé hry jsou mimo scope (PS1 disc-based), a říkáme to nahlas.

## Spuštění Pages lokálně

Stačí kterýkoli statický server:
```bash
cd docs
py -3 -m http.server 8000
# pak http://localhost:8000
```

## Atribuce

Tento projekt je **fanouškovský**. Všechny ochranné známky patří jejich vlastníkům (Nintendo, Game Freak, Capcom, Konami, Square Enix, atd.). Tady poskytujeme pouze diff (textové změny) nad otevřenými disassembly nebo komunitními ROM-hacking tools.
