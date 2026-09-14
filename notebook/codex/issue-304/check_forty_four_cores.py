"""Fresh exact author audit of the complete explicit forty-four-core manifest."""
from pathlib import Path
import hashlib,json
from check_all_cores import check

ROOT=Path(__file__).parent

if __name__=='__main__':
    path=ROOT/'all-forty-four-cores.json'
    manifest=json.loads(path.read_text())
    assert len(manifest['cases'])==44
    assert len({tuple(c['pattern']) for c in manifest['cases']})==44
    result=[]
    for c in manifest['cases']:
        r=check(c);result.append(r)
        print(r['tag'],'mass',r['mass'],'max',r['maximum_load'],'atoms',r['atoms'],flush=True)
    (ROOT/'all-forty-four-author-audits.json').write_text(json.dumps({
        'manifest_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'status':'author exact arithmetic passed; independent review required',
        'cases':result},indent=2)+'\n')
