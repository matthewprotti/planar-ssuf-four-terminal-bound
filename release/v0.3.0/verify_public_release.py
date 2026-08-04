#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys
root=Path(__file__).resolve().parents[2]
def req(c,m):
    if not c: raise AssertionError(m)
req((root/'README.md').is_file(),'README missing')
req((root/'release/v0.3.0/FINAL_SCOPE_LEDGER.md').is_file(),'scope ledger missing')
req((root/'review_evidence/v0.3.0/SECOND_REVIEW_INGEST.json').is_file(),'review ingest missing')
readme=(root/'README.md').read_text(encoding='utf-8')
scope=(root/'release/v0.3.0/FINAL_SCOPE_LEDGER.md').read_text(encoding='utf-8')
review=(root/'review_evidence/v0.3.0/README.md').read_text(encoding='utf-8')
for token in ['fixed gadget','not represented as conventional journal peer review']:
    req(token.lower() in readme.lower(),f'README token missing: {token}')
for token in ['bounded-', 'middle region', 'unrestricted planar sharpness']:
    req(token.lower() in scope.lower(),f'scope fence missing: {token}')
req('fixed finite atlas only' in review.lower(),'R3B scope fence missing')
for p in root.rglob('*'):
    req(not p.is_symlink(),f'symlink forbidden: {p}')
for p in [root/'README.md', *list((root/'release/v0.3.0').rglob('*'))]:
    if p.resolve() == Path(__file__).resolve():
        continue
    if p.is_file() and p.suffix.lower() in {'.md','.txt','.py','.json','.yml','.yaml','.toml','.cff'}:
        t=p.read_text(encoding='utf-8')
        req('/mnt/data/' not in t,f'local path leaked: {p}')
print('PASS: publication scope, review labels, paths, and symlinks')
