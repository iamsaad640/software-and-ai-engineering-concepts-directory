#!/usr/bin/env python3
"""Delete unchanged heads of merged PRs; preserve default, protected, and active branches."""
import argparse
import json
import os
import subprocess
from urllib.parse import quote

def candidates(branches, pull_requests, default):
    active={p['head']['ref'] for p in pull_requests if p['state']=='open'}
    merged={(p['head']['ref'],p['head']['sha']) for p in pull_requests if p.get('merged_at')}
    return [b for b in branches if b['name']!=default and not b['protected'] and b['name'] not in active and (b['name'],b['commit']['sha']) in merged]

def gh_api(path,method=None):
    args=['gh','api',path]
    if method:
        args += ['--method',method]
        subprocess.run(args,check=True)
        return None
    return json.loads(subprocess.check_output(args,text=True))

def pages(path):
    output=subprocess.check_output(['gh','api','--paginate','--slurp',path],text=True)
    return [item for page in json.loads(output) for item in page]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    prefix='repos/'+os.environ['GITHUB_REPOSITORY']
    default=gh_api(prefix)['default_branch']
    branches=pages(prefix+'/branches?per_page=100')
    prs=pages(prefix+'/pulls?state=all&per_page=100')
    for branch in candidates(branches,prs,default):
        # Recheck current ref and open PRs immediately before deletion.
        name=quote(branch['name'],safe='')
        current=gh_api(prefix+'/branches/'+name)
        open_prs=pages(prefix+'/pulls?state=open&per_page=100')
        if current['protected'] or current['commit']['sha']!=branch['commit']['sha'] or any(p['head']['ref']==branch['name'] for p in open_prs):
            print('Preserved changed or active branch: '+branch['name'])
            continue
        print(('Would delete: ' if args.dry_run else 'Deleting: ')+branch['name'])
        if not args.dry_run:
            gh_api(prefix+'/git/refs/heads/'+name,method='DELETE')
if __name__=='__main__':
    main()
