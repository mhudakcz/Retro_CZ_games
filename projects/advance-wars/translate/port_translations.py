#!/usr/bin/env python3
"""Carry translations over to a freshly extracted aw1_strings.json.

Entries are matched on str_off, which is stable across extractor changes,
unlike the positional idx used inside the chunks.

    py -3 translate/extract.py baserom.gba translate/aw1_strings_new.json
    py -3 translate/port_translations.py
"""
import json, shutil

OLD = 'translate/aw1_strings.json'
NEW = 'translate/aw1_strings_new.json'

old = json.load(open(OLD, encoding='utf-8'))
new = json.load(open(NEW, encoding='utf-8'))

cz_by_off = {e['str_off']: e['cz'] for e in old if e.get('cz', '').strip()}
en_by_off = {e['str_off']: e['en'] for e in old}

carried = untranslated = changed = 0
for e in new:
    off = e['str_off']
    if off in cz_by_off:
        # Only carry a translation whose English source is unchanged.
        if en_by_off.get(off) == e['en']:
            e['cz'] = cz_by_off[off]
            carried += 1
        else:
            changed += 1
    else:
        untranslated += 1

shutil.copy(OLD, OLD + '.bak')
json.dump(new, open(OLD, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('Entries: %d (was %d)' % (len(new), len(old)))
print('Translations carried over: %d' % carried)
print('English text changed, dropped: %d' % changed)
print('Still untranslated: %d' % untranslated)
for e in new:
    if not e.get('cz', '').strip():
        print('  0x%06X [%3d] %r' % (e['str_off'], e['len'], e['en'][:70]))
