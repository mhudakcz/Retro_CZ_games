#!/usr/bin/env python3
"""Patch GCC path->string errors in tmc tools.

Reads /tmp/b.log, finds lines like:
  .../file.cpp:14:18: error: no matching function for call to
      'std::vector<...string...>::push_back(std::filesystem::...path...)'
and for each, rewrites the push_back(...) argument on that line to append
.string() (wrapping the inner expression).

Also handles: 'could not convert ... path ... to ... string' on a return line.
"""
import re, sys
from pathlib import Path

log_path = sys.argv[1] if len(sys.argv) > 1 else 'build_errors.log'
log = Path(log_path).read_text(encoding='utf-8', errors='ignore')

# Collect (file, line) for path->string push_back errors and conversion errors
targets = {}  # (file, lineno) -> kind
for m in re.finditer(r'^(.*?\.cpp|.*?\.h):(\d+):\d+: error: (.*)$', log, re.M):
    f, ln, msg = m.group(1), int(m.group(2)), m.group(3)
    if 'path' not in msg:
        continue
    if 'push_back' in msg or 'could not convert' in msg or 'no known conversion' in msg or 'no match' in msg:
        targets.setdefault((f, ln), msg)

print(f'{len(targets)} path-related error lines to patch')

# Group by file
by_file = {}
for (f, ln), msg in targets.items():
    by_file.setdefault(f, []).append(ln)

def patch_pushback(line):
    # cmd.push_back(EXPR);  ->  cmd.push_back((EXPR).string());
    m = re.search(r'(\.push_back\()(.+)(\)\s*;)\s*$', line)
    if not m:
        return None
    inner = m.group(2)
    if inner.strip().endswith('.string()'):
        return None
    new = line[:m.start(2)] + f'({inner}).string()' + line[m.end(2):]
    return new

def patch_return(line):
    # return EXPR;  -> return (EXPR).string();
    m = re.search(r'(\breturn\s+)(.+)(;)\s*$', line)
    if not m:
        return None
    inner = m.group(2)
    if inner.strip().endswith('.string()'):
        return None
    new = line[:m.start(2)] + f'({inner}).string()' + line[m.end(2):]
    return new

changed_files = 0
changed_lines = 0
for f, lns in by_file.items():
    p = Path(f)
    if not p.exists():
        print(f'  MISSING: {f}')
        continue
    lines = p.read_text(encoding='utf-8').splitlines(keepends=True)
    file_changed = False
    for ln in lns:
        if ln-1 >= len(lines):
            continue
        orig = lines[ln-1]
        new = None
        if '.push_back(' in orig:
            new = patch_pushback(orig)
        elif 'return' in orig:
            new = patch_return(orig)
        if new and new != orig:
            lines[ln-1] = new
            file_changed = True
            changed_lines += 1
    if file_changed:
        p.write_text(''.join(lines), encoding='utf-8')
        changed_files += 1
        print(f'  patched {f}')

print(f'Patched {changed_lines} lines in {changed_files} files')
