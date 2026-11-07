"""Validate pinned source ownership and ensure each released change is represented once."""
from pathlib import Path
import hashlib,json,re,sys,xml.etree.ElementTree as ET

def validate(root):
    root=Path(root)
    layout=json.loads((root/'source-layout.json').read_text())
    recipe=json.loads((root/'integration/recipe.json').read_text())
    assert hashlib.sha256((root/'integration/recipe.json').read_bytes()).hexdigest()==layout['residual_recipe_sha256']
    raw=(root/'default.xml').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==layout['default_manifest_sha256']
    assert raw==(root/'integration/manifests/pinned.xml').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==recipe['manifest_sha256']
    assert hashlib.sha256((root/'upstream.xml').read_bytes()).hexdigest()==layout['upstream_manifest_sha256']
    pins={}
    for p in ET.fromstring(raw).findall('project'):
        path=p.get('path',p.get('name'))
        assert path not in pins and re.fullmatch('[0-9a-f]{40}',p.get('revision','')),path
        pins[path]=p
    represented=[]
    owned=set()
    for c in layout['components']:
        p=c['project'];owned.add(p)
        assert pins[p].get('name')=='wjdob/'+c['repo'] and pins[p].get('revision')==c['head']
        represented.extend(p+'/'+r['path'] for r in c['expected_files'])
    for r in recipe['files']+recipe.get('new_files',[]):
        assert r['project'] not in owned and pins[r['project']].get('revision')==r['revision'],r['path']
        represented.append(r['path'])
    assert len(represented)==len(set(represented))
    assert sorted(represented)==layout['original_paths'],'missing/duplicate recipe coverage'
    for a in recipe['actions']:
        assert a.get('project') not in owned
        assert not any(a.get('path','').startswith(p+'/') for p in owned)
        if a['type']=='patch':
            assert hashlib.sha256((root/'integration'/a['file']).read_bytes()).hexdigest()==a['sha256']
    external={r['source']:r['sha256'] for r in layout.get('external_inputs',[])}
    for r in recipe.get('new_files',[]):
        if r['source'] in external:
            assert external[r['source']]==r['canonical_sha256']
            assert r['source'].startswith('.local/')
        else:
            assert hashlib.sha256((root/'integration'/r['source']).read_bytes()).hexdigest()==r['canonical_sha256']
    for r in layout['imported_files']:
        assert hashlib.sha256((root/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
    return {'projects':len(pins),'covered_files':len(represented),'residual_actions':len(recipe['actions'])}

if __name__=='__main__':
    print('PASS:',validate(Path(__file__).resolve().parents[1]))
