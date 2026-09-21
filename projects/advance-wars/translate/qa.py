#!/usr/bin/env python3
"""Quality pass over a finished aw1_strings.json.

Reports things worth a human look rather than hard errors: strings that came
back unchanged, English left inside a Czech line, stray diacritics, and proper
names that vanished in translation. Czech declines names (Sonja -> Sonjo,
Eagle -> Eaglovi), so names are matched on their stem, not the full form.
"""
import json, re, sys

JS = sys.argv[1] if len(sys.argv) > 1 else 'translate/aw1_strings.json'
entries = json.load(open(JS, encoding='utf-8'))
tr = [e for e in entries if e.get('cz', '').strip()]
print('Translated entries: %d of %d' % (len(tr), len(entries)))

# 1) Came back unchanged. Map names and debug leftovers are meant to stay.
same = [e for e in tr if e['cz'] == e['en'] and len(e['en']) > 12 and ' ' in e['en']]
print('\nUnchanged strings longer than 12 chars: %d' % len(same))
for e in same:
    print('   0x%06X %r' % (e['str_off'], e['en'][:65]))

# 2) English function words surviving in a translated line.
EN_WORDS = re.compile(r'\b(the|and|you|your|are|with|this|that|have|will|from|'
                      r'they|them|what|when|there|here|about|would|should|could)\b',
                      re.I)
leftover = [(e, set(EN_WORDS.findall(e['cz'])))
            for e in tr if e['cz'] != e['en'] and EN_WORDS.search(e['cz'])]
print('\nEnglish function words left in a translation: %d' % len(leftover))
for e, words in leftover[:20]:
    print('   0x%06X %s -> %r' % (e['str_off'], sorted(words), e['cz'][:60]))

# 3) Diacritics. v0.1 is ASCII only; the injector folds them, but catching them
#    here keeps the JSON honest about how long a line really is.
dia = [e for e in tr if any(ord(c) > 127 for c in e['cz'])]
print('\nEntries containing non-ASCII characters: %d' % len(dia))
for e in dia[:20]:
    print('   0x%06X %r' % (e['str_off'], e['cz'][:60]))

# 4) Proper names dropped. Compare stems so Czech cases do not raise a flag.
NAMES = ['Andy', 'Max', 'Sami', 'Nell', 'Hachi', 'Olaf', 'Grit', 'Kanbei',
         'Sonja', 'Eagle', 'Drake', 'Sturm', 'Orange Star', 'Blue Moon',
         'Green Earth', 'Yellow Comet', 'Black Hole']
lost = []
for e in tr:
    for n in NAMES:
        stem = n[:4] if ' ' not in n else n
        if e['en'].count(n) > e['cz'].count(stem):
            lost.append((e, n))
            break
print('\nEntries where a proper name disappeared: %d' % len(lost))
for e, n in lost[:20]:
    print('   0x%06X lost %r' % (e['str_off'], n))
    print('      en: %r' % e['en'][:70])
    print('      cz: %r' % e['cz'][:70])

# 5) Two-word faction names broken over a line or box break read badly in a
#    text window ("armade Orange" / "Star novacci"). Move the break instead.
BS = chr(92)
TWO_WORD = [n for n in NAMES if ' ' in n]
split_names = []
for e in tr:
    for n in TWO_WORD:
        a, b = n.split(' ')
        for sep in (BS + 'r', BS + 'f', BS + 'e'):
            if a + sep + b in e['cz']:
                split_names.append((e, n))
                break
print('\nFaction names split across a break: %d' % len(split_names))
for e, n in split_names[:20]:
    print('   0x%06X %s' % (e['str_off'], n))
    print('      cz: %r' % e['cz'][:80])
