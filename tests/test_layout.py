from pathlib import Path
import json,shutil,sys,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from validate_layout import validate

class SourceLayoutTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)/'layout'
        shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('.git','tmp','__pycache__'))
    def tearDown(self):self.temp.cleanup()
    def test_released_layout_is_complete(self):
        self.assertGreater(validate(self.root)['covered_files'],0)
    def test_changed_component_pin_is_rejected(self):
        p=self.root/'source-layout.json';data=json.loads(p.read_text());data['components'][0]['head']='0'*40;p.write_text(json.dumps(data))
        with self.assertRaises(AssertionError):validate(self.root)
    def test_changed_residual_recipe_is_rejected(self):
        p=self.root/'integration/recipe.json';data=json.loads(p.read_text());data['actions'].pop();p.write_text(json.dumps(data))
        with self.assertRaises(AssertionError):validate(self.root)
    def test_missing_coverage_is_rejected(self):
        p=self.root/'source-layout.json';data=json.loads(p.read_text());data['original_paths'].pop();p.write_text(json.dumps(data))
        with self.assertRaises(AssertionError):validate(self.root)
    def test_changed_imported_patch_is_rejected(self):
        recipe=json.loads((self.root/'integration/recipe.json').read_text());a=next(a for a in recipe['actions'] if a['type']=='patch');p=self.root/'integration'/a['file'];p.write_bytes(p.read_bytes()+b'\n')
        with self.assertRaises(AssertionError):validate(self.root)

if __name__=='__main__':unittest.main()
