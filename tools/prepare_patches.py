"""Check pinned component contents and stage remaining source changes; input tree stays read-only."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'integration/tools/build'))
from reconstruct_candidate import reconstruct
from validate_layout import validate

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tree',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();validate(ROOT)
    layout=json.loads((ROOT/'source-layout.json').read_text())
    for c in layout['components']:
        repo=a.tree/c['project']
        head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
        if head!=c['head']:raise ValueError('component revision mismatch: '+c['project'])
        for r in c['expected_files']:
            if hashlib.sha256((repo/r['path']).read_bytes()).hexdigest()!=r['sha256']:
                raise ValueError('component content mismatch: '+c['project']+'/'+r['path'])
    result=reconstruct(a.tree,a.output,ROOT/'integration/recipe.json',scratch_root=a.output.resolve().parent)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
