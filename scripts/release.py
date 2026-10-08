#!/usr/bin/env python3
"""Create an immutable annotated version tag and publish release assets through gh."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import zipfile
ROOT=Path(__file__).resolve().parents[1]
def gh(*args):
    return subprocess.check_output(['gh',*args],text=True).strip()
def api(path,**fields):
    args=['api',path]
    for key,value in fields.items():
        args += ['-f',f'{key}={value}']
    return json.loads(gh(*args))
def main():
    repo=os.environ['GITHUB_REPOSITORY']
    commit=os.environ['GITHUB_SHA']
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo) or not re.fullmatch(r'[0-9a-f]{40}',commit):
        raise SystemExit('Invalid repository or commit identity')
    version=(ROOT/'VERSION').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+',version):
        raise SystemExit('Invalid version')
    tag='v'+version
    prefix=f'repos/{repo}'
    # List exact refs rather than treating every failed request as absence.
    refs=api(f'{prefix}/git/matching-refs/tags/{tag}')
    exact=[ref for ref in refs if ref['ref']==f'refs/tags/{tag}']
    if exact:
        obj=exact[0]['object']
        target=api(f'{prefix}/git/tags/{obj["sha"]}')['object']['sha'] if obj['type']=='tag' else obj['sha']
        releases=api(f'{prefix}/releases?per_page=100')
        if any(release['tag_name']==tag for release in releases):
            print(f'{tag} already published; leaving it unchanged')
            return
        if target!=commit:
            raise SystemExit(f'{tag} exists at another commit; refusing to move or publish it')
    else:
        obj=api(f'{prefix}/git/tags',tag=tag,message=f'Concepts directory {tag}',object=commit,type='commit')
        api(f'{prefix}/git/refs',ref=f'refs/tags/{tag}',sha=obj['sha'])
    changelog=(ROOT/'CHANGELOG.md').read_text()
    section=changelog.split(f'## [{version}]',1)[1].split('\n## [',1)[0]
    notes=ROOT/'_site/release-notes.md'
    notes.write_text(f'# {tag}\n\n'+section.split('\n',1)[1].strip()+'\n')
    archive=ROOT/f'_site/concepts-directory-{tag}.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as output:
        for path in sorted((ROOT/'_site').rglob('*')):
            if path.is_file() and path not in {archive,notes}:
                output.write(path,path.relative_to(ROOT/'_site'))
    catalog=ROOT/'catalog/directory.json'
    checksums=ROOT/'_site/SHA256SUMS'
    checksums.write_text(''.join(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n' for path in [archive,catalog]))
    gh('release','create',tag,str(archive),str(catalog),str(checksums),'--repo',repo,'--verify-tag','--title',f'{tag} — Concepts directory','--notes-file',str(notes))
    print(f'Published {tag} at {commit}')
if __name__=='__main__':
    main()
