#!/usr/bin/env python3
"""Check catalog integrity, generated Markdown, local links, and site anchors."""
import json
from pathlib import Path
import re
import subprocess
import sys
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def fail(message):
    errors.append(message)
data=json.loads((ROOT/'catalog/directory.json').read_text())
paths=set()
for section in data:
    if section['track'] not in {'software','ai','principal'}:
        fail('Unknown track: '+section['track'])
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',section['slug']):
        fail('Invalid slug: '+section['slug'])
    key=(section['track'],section['slug'])
    if key in paths:
        fail('Duplicate category: '+str(key))
    paths.add(key)
    seen=set()
    for entry in section['entries']:
        if set(entry)!= {'terms'} or not entry['terms']:
            fail('Entries must contain only nonempty terms: '+str(key))
        for term in entry['terms']:
            if not isinstance(term,str) or not term.strip() or term!=term.strip() or '\n' in term:
                fail('Invalid concept name: '+repr(term))
            if term.casefold() in seen:
                fail('Repeated concept within category: '+term)
            seen.add(term.casefold())
    for label,url in section['references']:
        if not label or not url.startswith('https://'):
            fail('Invalid category reference: '+str(key))
version=(ROOT/'VERSION').read_text().strip()
if not re.fullmatch(r'0|[1-9]\d*',version.split('.')[0]) or not re.fullmatch(r'\d+\.\d+\.\d+',version):
    fail('VERSION must be a stable semantic version')
if f'## [{version}]' not in (ROOT/'CHANGELOG.md').read_text():
    fail('VERSION must have a matching changelog section')
for file in ROOT.rglob('*.md'):
    if '.git' in file.parts or '_site' in file.parts:
        continue
    text=file.read_text()
    if not text.endswith('\n'):
        fail(str(file.relative_to(ROOT))+': missing final newline')
    if len(re.findall(r'^# ',text,re.M))!=1:
        fail(str(file.relative_to(ROOT))+': require exactly one H1')
    if re.search(r'[ \t]+$',text,re.M):
        fail(str(file.relative_to(ROOT))+': trailing whitespace')
    for link in re.findall(r'\[[^\]\n]+\]\(([^)\s]+)\)',text):
        if re.match(r'(https?://|mailto:|#)',link):
            continue
        target=(file.parent/link.split('#')[0]).resolve()
        if not target.is_relative_to(ROOT) or not target.exists():
            fail(str(file.relative_to(ROOT))+': broken local link '+link)
subprocess.run([sys.executable,str(ROOT/'scripts/build.py'),'--check','--site'],check=True)
class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.hrefs=[]; self.assets=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if 'href' in attrs: self.hrefs.append(attrs['href'])
        if 'src' in attrs: self.assets.append(attrs['src'])
parser=SiteParser(); parser.feed((ROOT/'_site/index.html').read_text())
if len(parser.ids)!=len(set(parser.ids)):
    fail('Duplicate site IDs')
for href in parser.hrefs+parser.assets:
    if href.startswith('#'):
        if href[1:] not in parser.ids: fail('Broken site anchor: '+href)
    elif not href.startswith('https://') and not (ROOT/'_site'/href).exists():
        fail('Broken site asset: '+href)
if errors:
    raise SystemExit('\n'.join(errors))
unique=len({t.casefold() for s in data for e in s['entries'] for t in e['terms']})
print(f'PASS: {len(data)} categories; {unique} unique display names; catalog, Markdown, links, and site anchors')
